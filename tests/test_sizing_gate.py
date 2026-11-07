import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/sizing_gate.py'


class GateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / '.specify').mkdir()
        self.feature = self.root / 'specs/001-test'
        self.feature.mkdir(parents=True)
        for name in ('spec.md', 'plan.md'):
            (self.feature / name).write_text('Planning content\n')
        self.tasks = self.feature / 'tasks.md'
        self.tasks.write_text('- [ ] T001 First task\n- [ ] T002 Second task\n')
        self.review = self.feature / 'size-review.md'
        self.review.write_text('T-Shirt Size: M\nStatus: PENDING\nConfidence: MEDIUM\n')

    def run_gate(self, action, succeeds=True):
        result = subprocess.run([sys.executable, str(SCRIPT), action, str(self.feature)],
                                cwd=self.root, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0 if succeeds else 1, result.stdout + result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        return result

    def approve(self):
        self.run_gate('stage')
        self.run_gate('approve')
        self.run_gate('check')

    def test_completion_and_reopening_preserve_approval(self):
        self.approve()
        for checkbox in ('x', 'X', ' '):
            self.tasks.write_text(f'- [{checkbox}] T001 First task\n- [ ] T002 Second task\n')
            self.run_gate('check')

    def test_completion_between_stage_and_approval(self):
        self.run_gate('stage')
        self.tasks.write_text(self.tasks.read_text().replace('[ ]', '[x]'))
        self.run_gate('approve')
        self.run_gate('check')

    def test_scope_changes_invalidate_approval(self):
        self.approve()
        original = self.tasks.read_text()
        changes = [original.replace('First', 'Changed'), original.replace('T001', 'T003'),
                   ''.join(reversed(original.splitlines(keepends=True))), original + '- [ ] T003 New\n']
        for content in changes:
            with self.subTest(content=content):
                self.tasks.write_text(content)
                self.run_gate('check', False)
        self.tasks.write_text(original)
        for name in ('spec.md', 'plan.md', 'size-review.md'):
            path = self.feature / name
            before = path.read_text()
            path.write_text(before + 'Changed\n')
            self.run_gate('check', False)
            path.write_text(before)

    def test_checkboxes_in_code_remain_significant(self):
        self.tasks.write_text('```markdown\n- [ ] Example\n```\n')
        self.approve()
        self.tasks.write_text(self.tasks.read_text().replace('[ ]', '[x]'))
        self.run_gate('check', False)

    def test_invalid_or_duplicate_metadata_is_rejected(self):
        for content in ('T-Shirt Size: M\nStatus:\nPENDING\n',
                        'T-Shirt Size: M\nStatus: PENDING\nStatus: APPROVED\n',
                        'T-Shirt Size: M\nT-Shirt Size: XL\nStatus: PENDING\n'):
            with self.subTest(content=content):
                self.review.write_text(content)
                self.run_gate('stage', False)

    def test_invalid_json_records_are_denied(self):
        self.run_gate('stage')
        for content in ('[]', 'null', '42', '"text"', '{broken'):
            (self.feature / '.size-review-stage.json').write_text(content)
            self.run_gate('approve', False)
        self.approve()
        for content in ('[]', 'null', '{broken'):
            (self.feature / '.size-approval.json').write_text(content)
            self.run_gate('check', False)

    def test_missing_and_stale_approval_and_restage(self):
        self.run_gate('check', False)
        self.approve()
        self.review.write_text(self.review.read_text().replace('APPROVED', 'PENDING'))
        self.run_gate('stage')
        self.assertFalse((self.feature / '.size-approval.json').exists())
        self.tasks.write_text('Changed scope\n')
        self.run_gate('approve', False)

    def test_crlf_review(self):
        self.review.write_bytes(b'T-Shirt Size: M\r\nStatus: PENDING\r\nConfidence: MEDIUM\r\n')
        self.approve()


if __name__ == '__main__':
    unittest.main()
