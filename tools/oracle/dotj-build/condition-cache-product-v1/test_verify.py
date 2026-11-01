"""Qualification mutations catch wrong warning lifetime, spelling, values and provenance."""
import base64, copy, importlib.util, unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('cache_product_controls',Path(__file__).with_name('verify.py'))
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

class QualificationControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=v.observations();cls.lines=v.v3.logic_results(cls.rows)
        cls.red=v.read(v.B/'validation/Batch-2511-cache-product-red-run1/verification.json')
    def reject(self,lines):
        with self.assertRaisesRegex(ValueError,'ordered values/imports/warnings'):v.validate_result_lines(lines,self.rows)
    def change(self,row,field,value):
        lines=list(self.lines);parts=lines[row].split('\t');parts[field]=v.v3.encode(value);lines[row]='\t'.join(parts);self.reject(lines)
    def test_real_native_expectations(self):v.validate_result_lines(self.lines,self.rows)
    def test_real_baseline_red_rejected(self):self.reject(self.red['cache']['actual'])
    def test_order_omission_and_duplicate(self):
        for lines in [self.lines[::-1],self.lines[:-1],self.lines+[self.lines[0]]]:self.reject(lines)
    def test_stale_true_and_false_values(self):
        self.change(1,2,'Alpha');self.change(2,2,'');self.change(2,3,'Alpha')
    def test_warning_not_per_evaluation_or_location(self):
        first=base64.b64decode(self.lines[0].split('\t')[5]).decode()
        self.change(1,5,first);self.change(0,5,first+'|'+first.replace('@3:8','@4:8'))
    def test_whitespace_and_case_not_folded(self):
        self.change(4,5,'');self.change(5,5,'')
        raw=base64.b64decode(self.lines[4].split('\t')[5]).decode();self.change(4,5,raw.replace('  ',' '))
    def test_skipped_validation_does_not_consume_warning(self):self.change(7,5,'')
    def test_owner_location_and_imports(self):
        raw=base64.b64decode(self.lines[3].split('\t')[5]).decode();self.change(3,5,raw.replace('main.proj@2:18','child.proj@2:18'));self.change(3,4,'')
    def test_source_fallback_rejected(self):
        fake=copy.deepcopy(self.red);fake['commands'][0]['argv'].remove('-implicit:none')
        with self.assertRaisesRegex(ValueError,'source fallback'):v.validate_commands(fake,Path(fake['checkpoint']['path']).parent/'Batch-2511-cache-product-red-run1')
    def test_false_exit_and_wrong_jar_rejected(self):
        out=v.B/'validation/Batch-2511-cache-product-red-run1'
        for change in [lambda r:r['commands'][0].update(exitCode=False),lambda r:r['candidateJar'].update(path='wrong.jar')]:
            fake=copy.deepcopy(self.red);change(fake)
            with self.assertRaisesRegex(ValueError,'typed process|actual JAR'):v.validate_commands(fake,out)

if __name__=='__main__':unittest.main()
