import copy,importlib.util,tempfile,unittest
from pathlib import Path
B=Path(r'D:\AI\Implementation\dotj Frameworks');HERE=Path(__file__).resolve().parent
class CandidateControls(unittest.TestCase):
 def setUp(self):
  sp=importlib.util.spec_from_file_location('candidate_extension',HERE/'verify.py');self.v=importlib.util.module_from_spec(sp);sp.loader.exec_module(self.v)
  self.temp=tempfile.TemporaryDirectory(dir=B/'validation/task24-product-static-v1');self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
 def rows(self):
  rows=[]
  for i in range(1,11):
   ident='BA08-malformed-right-side-parsed' if i==8 else 'BA'+str(i).zfill(2)+'-unit'
   rows.append({'id':ident,'globals':{},'evaluation':{'success':i!=8,'properties':{'P':'<FIXTURE_ROOT>\\P','Q':''},'imports':[]},'diagnostics':[]})
  return rows
 def test_bridge_preserves_scalar_paths_and_empty_values(self):
  value=self.v.bridge(self.rows());self.assertIn('PEZJWFRVUkVfUk9PVD5cUA==\t\t0',value)
  self.assertEqual(value.count('CASE\t'),10)
 def test_bridge_rejects_numeric_property_coercion(self):
  data=self.rows();data[0]['evaluation']['properties']['P']=1
  with self.assertRaises(ValueError):self.v.bridge(data)
 def test_bridge_requires_exact_unique_coverage(self):
  for rows in [self.rows()[:-1],self.rows()+[self.rows()[0]]]:
   with self.assertRaises(ValueError):self.v.bridge(rows)
  rows=self.rows();rows[1]['id']=rows[0]['id']
  with self.assertRaises(ValueError):self.v.bridge(rows)
 def test_bridge_rejects_owner_path_from_other_case(self):
  rows=self.rows();rows[0]['evaluation']['imports']=[{'owner':'<FIXTURE_ROOT>\\foreign\\main.proj','project':'<FIXTURE_ROOT>\\foreign\\x.props','line':1,'column':2}]
  with self.assertRaises(ValueError):self.v.bridge(rows)
 def test_root_observation_pin_cannot_be_rebased(self):
  with self.assertRaises(ValueError):self.v.native_sets('0'*64,self.v.SITE_PIN)
  with self.assertRaises(ValueError):self.v.native_sets(self.v.OLD_PIN,'0'*64)
 def test94_requires_exact_outcomes_not_only_count(self):
  rows=['UNIT'+str(i)+'\tDefault\tOK' for i in range(94)];good=self.root/'gold.tsv';out=self.root/'actual.tsv';good.write_text('\n'.join(rows));out.write_text('\n'.join(rows));self.v.verify94(out,good)
  rows[2]='UNIT2\tDefault\tFORGED';out.write_text('\n'.join(rows))
  with self.assertRaises(ValueError):self.v.verify94(out,good)
 def test94_rejects_missing_and_duplicated_keys(self):
  rows=['UNIT'+str(i)+'\tDefault\tOK' for i in range(94)];good=self.root/'gold.tsv';out=self.root/'actual.tsv';good.write_text('\n'.join(rows))
  for bad in [rows[:-1],rows[:-1]+[rows[0]]]:
   out.write_text('\n'.join(bad))
   with self.assertRaises(ValueError):self.v.verify94(out,good)
if __name__=='__main__':unittest.main()
