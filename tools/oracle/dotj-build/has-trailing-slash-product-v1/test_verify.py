"""Affected adapter controls: hidden product output and lost result membership."""
import importlib.util, unittest
from pathlib import Path

s=importlib.util.spec_from_file_location('predicate_successor_under_test',Path(__file__).with_name('verify.py'))
v=importlib.util.module_from_spec(s);s.loader.exec_module(v)

class AdapterControls(unittest.TestCase):
    def test_exact_consumer_membership(self):
        v.validate_classes(['pkg/ProjectEvaluationComponentTest.class'],{'pkg/ProjectEvaluationComponentTest.class'})
    def test_hidden_product_even_if_claimed_expected(self):
        names={'org/dotj/internal/build/evaluation/ProjectEvaluationComponent.class'}
        with self.assertRaisesRegex(ValueError,'hidden product'):v.validate_classes(names,names)
    def test_unexpected_compiler_output(self):
        with self.assertRaisesRegex(ValueError,'membership'):v.validate_classes({'C.class','Surprise.class'},{'C.class'})
    def test_missing_compiler_output(self):
        with self.assertRaisesRegex(ValueError,'membership'):v.validate_classes(set(),{'C.class'})
    def test_altered_result_not_reclassified_as_boundary(self):
        expected=['HT01\tMATCHED_EVALUATION\teWVz']
        with self.assertRaisesRegex(ValueError,'result fields'):v.validate_lines(['HT01\tPRIVATE_DECLARED_BOUNDARY\tCONDITION_PROFILE'],expected)
    def test_reordered_and_missing_results(self):
        for actual in [['second','first'],['first']]:
            with self.subTest(actual=actual),self.assertRaisesRegex(ValueError,'membership'):v.validate_lines(actual,['first','second'])

if __name__=='__main__':unittest.main()
