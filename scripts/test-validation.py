#!/usr/bin/env python3
"""Exercise the validator against disposable copies, without external services."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import sys

ROOT = Path(__file__).resolve().parents[1]


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / 'repo'
        shutil.copytree(ROOT, self.repo, ignore=shutil.ignore_patterns(
            '.git', 'graft', '__pycache__', '.DS_Store'))

    def validate(self, *options):
        return subprocess.run(
            [sys.executable, str(self.repo / 'scripts/validate-skills.py'), *options],
            capture_output=True, text=True)

    def assert_rejected(self, reason):
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(reason, result.stderr)

    def test_repository_passes(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_product_configuration_is_optional(self):
        shutil.rmtree(self.repo / '.claude-plugin', ignore_errors=True)
        for path in (self.repo / 'skills').rglob('agents'):
            shutil.rmtree(path)
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_wrong_bucket_is_rejected(self):
        source = self.repo / 'skills/hospital/crm-ui-mapping'
        source.rename(self.repo / 'skills/crm-ui-mapping')
        self.assert_rejected('Expected skills/<bucket>/<name>/SKILL.md:')

    def test_standard_yaml_forms_are_accepted(self):
        path = self.repo / 'skills/hospital/crm-ui-mapping/SKILL.md'
        path.write_text('---\nname: "crm-ui-mapping"\ndescription: >-\n'
                        '  Find patients when a user requests\n  patient information.\n'
                        'compatibility: Requires an authorized CRM session.\n'
                        'metadata:\n  author: "Personal"\n---\n# Lookup\n')
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_standard_metadata_is_rejected(self):
        path = self.repo / 'skills/hospital/crm-ui-mapping/SKILL.md'
        cases = [
            ('name: crm-ui-mapping\ndescription: true', 'description'),
            ('name: crm-ui-mapping\ndescription: ' + 'x' * 1025, 'description'),
            ('name: crm-ui-mapping\ndescription: Lookup\nmetadata:\n  version: 1', 'metadata'),
            ('name: other-name\ndescription: Lookup', 'Folder/name mismatch'),
            ('name: crm-ui-mapping\ndescription: Lookup\ncompatibility: ' + 'x' * 501, 'compatibility'),
        ]
        for header, reason in cases:
            with self.subTest(reason=reason):
                path.write_text('---\n' + header + '\n---\n# Lookup\n')
                self.assert_rejected(reason)

    def test_missing_skill_in_plugin_is_rejected(self):
        path = self.repo / '.claude-plugin/plugin.json'
        if path.exists():
            data = json.loads(path.read_text())
            data['skills'].pop()
            path.write_text(json.dumps(data))
        result = self.validate('--packaging')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Plugin skill paths must match', result.stderr)

    def test_catalog_cannot_be_packaged_as_task(self):
        path = self.repo / '.claude-plugin/plugin.json'
        data = json.loads(path.read_text())
        data['skills'].append('./skills')
        path.write_text(json.dumps(data))
        result = self.validate('--packaging')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Plugin skill paths must match', result.stderr)

    def test_wrong_marketplace_target_is_rejected(self):
        path = self.repo / '.claude-plugin/marketplace.json'
        data = json.loads(path.read_text())
        data['plugins'][0]['source'] = './missing'
        path.write_text(json.dumps(data))
        result = self.validate('--packaging')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Marketplace must reference the local plugin', result.stderr)

    def test_malformed_metadata_is_rejected(self):
        path = self.repo / 'skills/hospital/crm-ui-mapping/agents/openai.yaml'
        path.write_text('interface:\n  display_nam: "Wrong key"\n')
        result = self.validate('--packaging')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Invalid UI metadata', result.stderr)

    def test_skill_references_cannot_escape_owner(self):
        path = self.repo / 'skills/hospital/crm-ui-mapping/SKILL.md'
        path.write_text(path.read_text() + '\n[other skill](../billing-lookup/SKILL.md)\n')
        self.assert_rejected('Missing or escaping file:')

    def test_source_tampering_is_rejected(self):
        path = self.repo / 'skills/engineering/chrome-devtools/SKILL.md'
        path.write_text(path.read_text() + '\nUndeclared adaptation.\n')
        self.assert_rejected('Source digest mismatch:')

    def test_broken_local_link_is_rejected(self):
        path = self.repo / 'README.md'
        path.write_text(path.read_text() + '\n[missing](missing.md)\n')
        self.assert_rejected('Missing or escaping file:')


if __name__ == '__main__':
    unittest.main()
