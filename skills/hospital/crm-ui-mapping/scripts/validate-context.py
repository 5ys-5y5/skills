#!/usr/bin/env python3
"""Check caller-owned CRM mapping and evidence from stdin; never access a CRM."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print(json.dumps({'status': 'blocked', 'errors': ['Install scripts/requirements.txt in the execution environment']}))
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = {'patient-lookup', 'appointment-manage', 'visit-check-in', 'billing-lookup', 'contact-record'}


def check(data, phase, now=None):
    errors = []
    schema = json.loads((ROOT / 'references/context.schema.json').read_text())
    for error in Draft202012Validator(schema).iter_errors(data):
        # Report paths and constraints, not private input values.
        errors.append('schema: ' + '.'.join(map(str, error.absolute_path)) + ' (' + str(error.validator) + ')')
    if errors:
        return 'mapping_required' if phase == 'mapping' else 'blocked', errors
    profile, request = data['profile'], data['request']
    fields = profile['fields']
    workflow = request['workflow']
    if workflow not in WORKFLOWS:
        return 'blocked', ['Unknown workflow']
    contract = json.loads((ROOT / 'references/workflows' / workflow / 'contract.json').read_text())
    operation = contract['operations'].get(request['operation'])
    if operation is None:
        return 'blocked', ['Unknown operation for workflow']
    if profile['context'] != request['context']:
        errors.append('context: hospital, CRM or revision does not match')

    required = set(operation['fields']) | {key for key, value in fields.items() if value['required']}
    bindings = {**contract.get('result_bindings', {}), **operation.get('result_bindings', {})}
    for key, field in fields.items():
        result_key = field.get('result_key')
        if result_key:
            if result_key in bindings and bindings[result_key] != key:
                errors.append('Conflicting result binding: ' + result_key)
            else:
                bindings[result_key] = key
    for result_key in request.get('result_fields', []):
        if result_key not in bindings:
            errors.append('Missing result binding: ' + result_key)
        else:
            required.add(bindings[result_key])
    selected = required | set(request.get('targets', []))
    visited, active = set(), set()

    def visit(key):
        if key in active:
            errors.append('dependency cycle: ' + key)
            return
        if key in visited:
            return
        field = fields.get(key)
        if field is None:
            errors.append('Missing mapping: ' + key)
            return
        visited.add(key)
        active.add(key)
        if not field['xpath'].strip():
            errors.append('Missing xpath: ' + key)
        expected_role = operation['fields'].get(key, operation.get('optional_fields', {}).get(key))
        roles = ('read', 'input') if expected_role == 'read' else (expected_role,)
        if expected_role and ((key in operation['fields'] and not field['required']) or field['role'] not in roles):
            errors.append('Contract required/role mismatch: ' + key)
        for dependency in field.get('depends_on', []):
            visit(dependency)
        if 'scope_field' in field:
            scope = fields.get(field['scope_field'])
            if scope is not None and scope['role'] != 'container':
                errors.append('scope_field must identify a container: ' + key)
            visit(field['scope_field'])
        active.remove(key)

    for key in sorted(selected):
        visit(key)
    if errors:
        return 'mapping_required', errors
    if phase == 'mapping':
        return 'mapping_valid', []
    if phase == 'result':
        result = data.get('result')
        result_fields = request.get('result_fields')
        if not isinstance(result, dict) or not result_fields:
            return 'blocked', ['Missing result or requested result_fields']
        result_schema = json.loads((ROOT / 'references/workflows' / workflow / 'result.schema.json').read_text())
        for error in Draft202012Validator(result_schema).iter_errors(result):
            errors.append('result schema: ' + '.'.join(map(str, error.absolute_path)) + ' (' + str(error.validator) + ')')
        for key in set(result_fields) | set(operation.get('result_required', [])):
            value = result.get(key)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append('Missing requested result: ' + key)
        return ('blocked', errors) if errors else ('result_valid', [])

    evidence = data.get('evidence')
    if not evidence:
        return 'blocked', ['Missing evidence for this action']
    if evidence['request_id'] != request['id'] or evidence['context'] != request['context']:
        errors.append('evidence: request or context does not match')
    try:
        observed = datetime.fromisoformat(evidence['observed_at'].replace('Z', '+00:00'))
        if observed.tzinfo is None:
            raise ValueError('timezone required')
        age = ((now or datetime.now(timezone.utc)) - observed).total_seconds()
        if age < -5 or age > 300:
            errors.append('evidence: expired or future observation')
    except (ValueError, TypeError):
        errors.append('evidence: invalid observation timestamp')
    targets, action = request.get('targets', []), request.get('action')
    if not targets or not action:
        errors.append('Missing action or targets')
    satisfied = set(evidence['satisfied'])

    def require_dependencies(key, seen):
        if key in seen:
            return
        seen.add(key)
        for dependency in fields[key].get('depends_on', []):
            if dependency not in satisfied:
                errors.append('Unsatisfied prerequisite: ' + dependency)
            require_dependencies(dependency, seen)

    def verify(key, seen):
        if key in seen:
            return
        seen.add(key)
        field = fields[key]
        observation = evidence['fields'].get(key, {})
        if observation.get('matches') != 1 or not all(observation.get(flag) is True for flag in (
                'visible', 'semantic_confirmed', 'owner_confirmed')):
            errors.append('Unverified target: ' + key)
        require_dependencies(key, set())
        if 'scope_field' in field:
            verify(field['scope_field'], seen)

    for key in targets:
        field = fields[key]
        verify(key, set())
        if action in ('fill', 'select') and field['role'] != 'input':
            errors.append('action: target is not an input: ' + key)
        if action == 'click' and field['role'] not in ('input', 'action'):
            errors.append('action: target is not clickable: ' + key)
        if action != 'read' and not operation['writes'] and field.get('effect', 'record') == 'record':
            errors.append('action: record mutation forbidden for lookup: ' + key)
        if action in ('fill', 'select') or field.get('value_required', False):
            value = request.get('values', {}).get(key)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.append('Missing input value: ' + key)
            input_schema = operation.get('input_schemas', {}).get(key)
            if input_schema and not Draft202012Validator(input_schema).is_valid(value):
                errors.append('input schema: ' + key)
    return ('blocked', errors) if errors else ('ready', [])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', choices=('mapping', 'action', 'result'), required=True)
    args = parser.parse_args()
    try:
        data = json.load(sys.stdin)
        status, errors = check(data, args.phase)
    except (ValueError, TypeError, KeyError, RecursionError):
        status, errors = 'blocked', ['Invalid input or dependency structure']
    print(json.dumps({'status': status, 'errors': errors}, ensure_ascii=False))
    return 0 if status in ('mapping_valid', 'ready', 'result_valid') else 1


if __name__ == '__main__':
    sys.exit(main())
