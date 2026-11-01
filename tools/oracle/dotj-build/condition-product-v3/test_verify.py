"""Negative controls for the packaged condition qualification, using retained evidence."""
import copy
import importlib.util
import unittest
from pathlib import Path


class QualificationControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).with_name('verify.py')
        if not path.is_file():
            raise AssertionError('successor qualification implementation is missing')
        spec = importlib.util.spec_from_file_location('condition_product_v3', path)
        cls.v = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.v)
        cls.payload = cls.v.read(cls.v.LOGIC_LOCK)['normalizedPayload']

    def reject_payload(self, change, message):
        payload = copy.deepcopy(self.payload)
        change(payload)
        with self.assertRaisesRegex(ValueError, message):
            self.v.validate_logic_payload(payload)

    def test_real_payload(self):
        self.assertEqual(4, self.v.validate_logic_payload(self.payload))

    def test_duplicate_missing_and_reordered_ids(self):
        for mutation in [lambda p: p['rows'].pop(),
                         lambda p: p['rows'].append(copy.deepcopy(p['rows'][0])),
                         lambda p: p['rows'].reverse()]:
            self.reject_payload(mutation, 'coverage')

    def test_integer_is_not_boolean(self):
        self.reject_payload(lambda p: p['rows'][0]['evaluation'].update(success=1), 'typed field')

    def test_boolean_is_not_location(self):
        self.reject_payload(lambda p: next(r for r in p['rows'] if r['diagnostics'])['diagnostics'][0].update(line=True), 'typed field')

    def test_globals_and_marker_evidence(self):
        self.reject_payload(lambda p: p['rows'][0].update(globals={'P': False}), 'globals')
        self.reject_payload(lambda p: p['rows'][0].update(taskMarkerAbsent=1), 'task marker')

    def test_changed_warning_fields_and_omission(self):
        for field, value in [('code','MSB0000'),('file','wrong.proj'),('line',999),('column',999),('message','The condition "wrong" changed')]:
            def mutate(p, field=field, value=value):
                next(r for r in p['rows'] if any(d['kind']=='warning' for d in r['diagnostics']))['diagnostics'][0][field] = value
            self.reject_payload(mutate, 'warning')
        self.reject_payload(lambda p: next(r for r in p['rows'] if any(d['kind']=='warning' for d in r['diagnostics'])).update(diagnostics=[]), 'warning')

    def test_missing_or_forged_raw_descriptor(self):
        lock = self.v.read(self.v.LOGIC_LOCK)
        capture = self.v.read(lock['captures'][0]['path'])
        actual = capture['commands'][0]['stdout']
        for fake in [dict(actual, sha256='0'*64), dict(actual, path=str(self.v.B/'missing-2510.stdout')), {'sha256': actual['sha256']}]:
            with self.assertRaisesRegex(ValueError, 'descriptor|missing|hash'):
                self.v.validate_descriptor(fake)

    def test_forged_receipt_counts_and_module(self):
        record = self.v.receipt_fields()
        self.v.validate_receipt_fields(record)
        for field, value in [('conditionEvaluations',True),('conditionWarningFields',0),('moduleName','wrong.module'),('moduleExports',['x']),('taskMarkersAbsent',1),('acceptedTasksAdded',True)]:
            fake = copy.deepcopy(record); fake[field] = value
            with self.assertRaisesRegex(ValueError, 'receipt'):
                self.v.validate_receipt_fields(fake)

    def test_wrong_jar_and_valid_looking_forged_receipt(self):
        record = dict(self.v.receipt_fields(), status='PASS_PACKAGED_CONDITION_PRODUCT_V3')
        with self.assertRaisesRegex(ValueError, 'provenance'):
            self.v.validate_receipt_provenance(record)
        with self.assertRaisesRegex(ValueError, 'JAR'):
            self.v.verify_jar(self.v.LOGIC_LOCK, self.v.BASE/'src')

    def test_first_meaningful_rejection_evidence(self):
        payload = copy.deepcopy(self.payload)
        warning = next(r for r in payload['rows'] if any(d['kind']=='warning' for d in r['diagnostics']))
        warning['diagnostics'] = []
        baseline = self.v.B/'validation/Batch-2506-build2'
        command = copy.deepcopy(next(c for c in self.v.read(baseline/'verification.json')['commands'] if c['label']=='packaged-contract'))
        wrong_jar = self.v.B/'wrong-candidate-2510.jar'
        controls = [
            ('forged-receipt', lambda: self.v.validate_receipt_provenance(dict(self.v.receipt_fields(),status='PASS_PACKAGED_CONDITION_PRODUCT_V3'))),
            ('wrong-real-jar-provenance', lambda: self.v.verify_command(command,baseline,wrong_jar,baseline/'evaluation-contract-tests.jar')),
            ('omitted-warning', lambda: self.v.validate_logic_payload(payload)),
            ('missing-raw-log', lambda: self.v.validate_descriptor({'path':str(self.v.B/'missing-2510.stdout'),'sha256':'0'*64}))]
        for label, operation in controls:
            with self.assertRaises(ValueError) as rejected:
                operation()
            print('EXPECTED_REJECTION '+label+': '+str(rejected.exception))

    def test_changed_bridge_or_warning_output(self):
        expected = self.v.logic_results(self.payload['rows'])
        omitted_warning = list(expected)
        index = next(i for i, line in enumerate(expected) if line.split('\t')[1]=='MATCHED_EVALUATION' and line.split('\t')[-1])
        fields = omitted_warning[index].split('\t'); fields[-1] = ''
        omitted_warning[index] = '\t'.join(fields)
        for changed in [expected[:-1], list(reversed(expected)), omitted_warning]:
            with self.assertRaisesRegex(ValueError, 'condition results'):
                self.v.verify_logic_lines(changed, self.payload['rows'])

    def test_changed_native_bridge(self):
        bridge = self.v.logic_bridge(self.payload['rows'])
        for changed in [bridge.replace('CL01-truth-table','forged-case'),bridge.replace('END\n','',1),bridge+'GLOBAL\tUA==\tZm9yZ2Vk\n']:
            with self.assertRaisesRegex(ValueError,'bridge'):
                self.v.verify_bridge_text(changed,bridge)

    def test_typed_resource_floors(self):
        baseline = self.v.read(self.v.B/'validation/Batch-2506-build2/verification.json')
        self.v.verify_resource_evidence(baseline)
        for value in [True,524287]:
            changed=copy.deepcopy(baseline);changed['resources'][-1]['freePhysicalKiB']=value
            with self.assertRaisesRegex(ValueError,'resource floors'):
                self.v.verify_resource_evidence(changed)


if __name__ == '__main__':
    unittest.main()
