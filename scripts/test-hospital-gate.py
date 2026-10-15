#!/usr/bin/env python3
"""Exercise the hospital prerequisite gate with synthetic in-memory payloads."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/hospital/crm-ui-mapping/scripts/validate-context.py'


def payload():
    context = {'hospital': 'fixture', 'crm': 'fixture-crm', 'revision': 'r1'}
    fields = {}
    for name in ('patient.identity', 'billing.identity', 'billing.total', 'billing.paid', 'billing.balance', 'billing.status'):
        fields[name] = {'xpath': "//*[@data-field='" + name + "']", 'required': True,
                        'role': 'read', 'description': name, 'scope': 'current patient bill'}
    return {'profile': {'context': context, 'fields': fields},
            'request': {'id': 'request-1', 'workflow': 'billing-lookup', 'operation': 'lookup',
                        'context': deepcopy(context), 'targets': ['billing.balance'], 'action': 'read', 'values': {}},
            'evidence': {'request_id': 'request-1', 'context': deepcopy(context),
                         'observed_at': datetime.now(timezone.utc).isoformat(),
                         'fields': {'billing.balance': {'matches': 1, 'visible': True,
                                   'semantic_confirmed': True, 'owner_confirmed': True}},
                         'satisfied': []}}


class GateTests(unittest.TestCase):
    def run_gate(self, data, phase='action'):
        result = subprocess.run([sys.executable, str(SCRIPT), '--phase', phase],
                                input=json.dumps(data), capture_output=True, text=True)
        self.assertTrue(result.stdout.strip(), result.stderr)
        return result.returncode, json.loads(result.stdout)

    def assert_blocked(self, data, reason, phase='action'):
        code, result = self.run_gate(data, phase)
        self.assertNotEqual(code, 0)
        self.assertIn(reason, ' '.join(result['errors']))

    def test_verified_target_is_ready(self):
        code, result = self.run_gate(payload())
        self.assertEqual(code, 0, result)
        self.assertEqual(result['status'], 'ready')

    def test_missing_mapping_routes_to_mapping(self):
        data = payload()
        del data['profile']['fields']['billing.balance']
        code, result = self.run_gate(data, 'mapping')
        self.assertNotEqual(code, 0)
        self.assertEqual(result['status'], 'mapping_required')

    def test_required_false_cannot_weaken_contract(self):
        data = payload()
        data['profile']['fields']['billing.identity']['required'] = False
        self.assert_blocked(data, 'billing.identity', 'mapping')

    def test_different_hospital_is_rejected(self):
        data = payload()
        data['request']['context']['hospital'] = 'other'
        self.assert_blocked(data, 'context')

    def test_stale_or_other_request_evidence_is_rejected(self):
        for key, value in [('request_id', 'old-request'), ('observed_at', '2000-01-01T00:00:00+00:00')]:
            data = payload()
            data['evidence'][key] = value
            self.assert_blocked(data, 'evidence')

    def test_unique_xpath_is_not_enough(self):
        data = payload()
        data['evidence']['fields']['billing.balance']['semantic_confirmed'] = False
        self.assert_blocked(data, 'billing.balance')

    def test_multiple_matches_are_rejected(self):
        data = payload()
        data['evidence']['fields']['billing.balance']['matches'] = 2
        self.assert_blocked(data, 'billing.balance')

    def test_extra_reveal_dependency_must_be_satisfied(self):
        data = payload()
        data['profile']['fields']['billing.reveal'] = {'xpath': "//*[@id='show-bill']", 'required': False,
            'role': 'action', 'description': 'Open the bill details', 'scope': 'current patient bill'}
        data['profile']['fields']['billing.balance']['depends_on'] = ['billing.reveal']
        self.assert_blocked(data, 'billing.reveal')
        data['evidence']['satisfied'] = ['billing.reveal']
        code, result = self.run_gate(data)
        self.assertEqual(code, 0, result)

    def test_lookup_cannot_write(self):
        data = payload()
        data['request']['action'] = 'fill'
        data['request']['values'] = {'billing.balance': 123}
        self.assert_blocked(data, 'action')

    def test_dependency_cycle_is_rejected(self):
        data = payload()
        fields = data['profile']['fields']
        fields['billing.balance']['depends_on'] = ['billing.total']
        fields['billing.total']['depends_on'] = ['billing.balance']
        self.assert_blocked(data, 'cycle', 'mapping')

    def test_mapping_phase_does_not_require_live_evidence(self):
        data = payload()
        del data['evidence']
        code, result = self.run_gate(data, 'mapping')
        self.assertEqual(code, 0, result)
        self.assertEqual(result['status'], 'mapping_valid')

    def test_required_custom_field_is_checked(self):
        data = payload()
        data['profile']['fields']['custom.booking-toggle'] = {'xpath': '', 'required': True,
            'role': 'action', 'description': 'Show the booking date', 'scope': 'patient detail'}
        self.assert_blocked(data, 'xpath', 'mapping')

    def test_nested_dependencies_cannot_be_skipped(self):
        data = payload()
        fields = data['profile']['fields']
        fields['billing.reveal'] = {'xpath': "//*[@id='reveal']", 'required': False,
            'role': 'action', 'description': 'Show bill', 'scope': 'patient', 'depends_on': ['patient.open']}
        fields['patient.open'] = {'xpath': "//*[@id='open']", 'required': False,
            'role': 'action', 'description': 'Open patient', 'scope': 'patient'}
        fields['billing.balance']['depends_on'] = ['billing.reveal']
        data['evidence']['satisfied'] = ['billing.reveal']
        self.assert_blocked(data, 'patient.open')

    def test_scope_must_be_container(self):
        data = payload()
        data['profile']['fields']['billing.balance']['scope_field'] = 'billing.total'
        self.assert_blocked(data, 'scope_field', 'mapping')

    def test_input_value_is_required_before_fill(self):
        data = payload()
        data['request'].update(workflow='contact-record', operation='create', action='fill', targets=['contact.body'])
        data['profile']['fields'] = {
            key: {'xpath': "//*[@data-field='" + key + "']", 'required': True, 'role': role,
                  'description': key, 'scope': 'current contact'}
            for key, role in [('contact.body', 'input'), ('contact.submit', 'action'), ('contact.identity', 'read')]}
        data['evidence']['fields'] = {'contact.body': {'matches': 1, 'visible': True,
                                                     'semantic_confirmed': True, 'owner_confirmed': True}}
        self.assert_blocked(data, 'Missing input value')
        data['request']['values'] = {'contact.body': 'Requested contact note'}
        code, result = self.run_gate(data)
        self.assertEqual(code, 0, result)

    def test_input_value_type_follows_task_schema(self):
        data = payload()
        data['request'].update(workflow='contact-record', operation='create', action='fill', targets=['contact.body'])
        data['profile']['fields'] = {
            key: {'xpath': "//*[@data-field='" + key + "']", 'required': True, 'role': role,
                  'description': key, 'scope': 'current contact'}
            for key, role in [('contact.body', 'input'), ('contact.submit', 'action'), ('contact.identity', 'read')]}
        data['evidence']['fields'] = {'contact.body': {'matches': 1, 'visible': True,
                                                     'semantic_confirmed': True, 'owner_confirmed': True}}
        data['request']['values'] = {'contact.body': {'unexpected': 'object'}}
        self.assert_blocked(data, 'input schema')

    def test_result_requires_requested_information(self):
        data = payload()
        data['request']['result_fields'] = ['balance']
        data['result'] = {'patient_id': 'p', 'bill_id': 'b'}
        self.assert_blocked(data, 'balance', 'result')
        data['result']['balance'] = 0
        code, result = self.run_gate(data, 'result')
        self.assertEqual(code, 0, result)
        self.assertEqual(result['status'], 'result_valid')

    def test_narrow_balance_query_needs_no_unrequested_amounts(self):
        data = payload()
        for name in ('billing.total', 'billing.paid', 'billing.status'):
            del data['profile']['fields'][name]
        code, result = self.run_gate(data)
        self.assertEqual(code, 0, result)

    def test_requested_result_mapping_is_required_before_workflow(self):
        data = payload()
        data['request']['targets'] = ['billing.identity']
        data['request']['result_fields'] = ['balance']
        del data['profile']['fields']['billing.balance']
        self.assert_blocked(data, 'billing.balance', 'mapping')

    def test_custom_result_binding_is_supported(self):
        data = payload()
        data['request']['result_fields'] = ['booking_date']
        self.assert_blocked(data, 'result binding', 'mapping')
        data['profile']['fields']['custom.date'] = {'xpath': "//*[@id='booking-date']", 'required': False,
            'role': 'read', 'description': 'Booking date', 'scope': 'patient detail', 'result_key': 'booking_date'}
        code, result = self.run_gate(data, 'mapping')
        self.assertEqual(code, 0, result)


if __name__ == '__main__':
    unittest.main()
