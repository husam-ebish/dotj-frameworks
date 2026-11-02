"""Forgery controls against the exact successor contract consumed by qualification."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import contract as c
import copy,unittest
class ContractForgeryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=c.frozen();cls.value=c.read(c.HERE/'CONTRACT.json');c.validate_contract(cls.value,cls.rows)
    def reject(self,change):
        value=copy.deepcopy(self.value);change(value)
        with self.assertRaises(ValueError):c.validate_contract(value,self.rows)
    def test_missing_id(self):self.reject(lambda x:x['nativeRecords'].pop())
    def test_forged_property(self):self.reject(lambda x:x['nativeRecords'][0]['expectedFields'].__setitem__(0,c.enc('forged')))
    def test_suppressed_warning(self):self.reject(lambda x:next(r for r in x['nativeRecords'] if r['id']=='BOOL-PREC-14')['expectedFields'].__setitem__(3,''))
    def test_runtime_fault_parity_forgery(self):self.reject(lambda x:next(r for r in x['nativeRecords'] if r['id']=='BOOL-EMPTY-06').__setitem__('nativePairedParityEligible',True))
    def test_boolean_type_forgery(self):self.reject(lambda x:x.__setitem__('schemaVersion',True))
    def test_path_normalization_forgery(self):self.reject(lambda x:x.__setitem__('normalization','Normalize every differing value/path/message.'))
if __name__=='__main__':unittest.main(verbosity=2)
