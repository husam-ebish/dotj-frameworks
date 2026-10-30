"""Synthetic supplement checker controls; never native qualification."""
import copy,importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent;B=Path(r'D:\AI\Implementation\dotj Frameworks')
class Controls(unittest.TestCase):
 def setUp(self):
  self.assertTrue((HERE/'verify.py').is_file(),'supplement checker feature missing')
  s=importlib.util.spec_from_file_location('supplement_checker',HERE/'verify.py');self.v=importlib.util.module_from_spec(s);s.loader.exec_module(self.v)
  self.temp=tempfile.TemporaryDirectory(dir=B/'validation/task24-exists-sites-static-v1');self.addCleanup(self.temp.cleanup);self.out=Path(self.temp.name)
 def payload(self):
  rows=[]
  for ident in self.v.CASE_IDS:
   rows.append({'id':ident,'globals':{},'profile':'Default','evaluation':{'success':True,'properties':{'P':'Synthetic','Q':''},'imports':[],'duplicateImports':None,'duplicateGetterFailure':{'type':'System.InvalidOperationException','message':'synthetic'}},'diagnostics':[],'cleanup':{'before':0,'loaded':1,'afterUnload':0,'disposed':True},'taskMarkerAbsent':True})
  return {'runtime':'.NET 10.0.12','profile':'Default','msbuildAssembly':'synthetic','msbuildPath':'a','frameworkPath':'b','corePath':'c','rows':rows}
 def layout(self):
  fixtures=self.out/'fixtures';cwd=self.out/'unrelated-cwd';cwd.mkdir();shutil.copytree(self.v.DATA/'fixtures',fixtures);shutil.copyfile(self.v.DATA/'cwd/cwd-only.marker',cwd/'cwd-only.marker')
  return fixtures,cwd,self.v.read(self.v.EVIDENCE/'plan.json')
 def test_exact_two_case_payload_acceptance_and_order(self):
  self.v.validate_payload(self.payload())
  for change in [lambda r:r.pop(),lambda r:r.append(copy.deepcopy(r[0])),lambda r:r.reverse(),lambda r:r[0].update(id='BA01-old-case')]:
   data=self.payload();change(data['rows'])
   with self.assertRaises(ValueError):self.v.validate_payload(data)
 def test_metadata_rejects_numeric_aliases(self):
  good={'schemaVersion':1,'commands':[{'label':'native-two-sites','exitCode':0,'nativeTimeoutSeconds':30}],'limits':{'heapMiB':128,'processors':2}}
  self.v.validate_metadata(good,good['limits'])
  for field,value in [('schemaVersion',True),('schemaVersion',1.0)]:
   bad=copy.deepcopy(good);bad[field]=value
   with self.assertRaises(ValueError):self.v.validate_metadata(bad,good['limits'])
  for field,value in [('exitCode',False),('exitCode',0.0),('nativeTimeoutSeconds',30.0)]:
   bad=copy.deepcopy(good);bad['commands'][0][field]=value
   with self.assertRaises(ValueError):self.v.validate_metadata(bad,good['limits'])
  bad=copy.deepcopy(good);bad['limits']['heapMiB']=128.0
  with self.assertRaises(ValueError):self.v.validate_metadata(bad,good['limits'])
 def test_valid_marker_placement_records_all_roles(self):
  f,c,p=self.layout();roles=self.v.validate_layout(f,c,p)
  self.assertEqual(len(roles),10)
  self.assertEqual(sum(x['exists'] for x in roles),3)
  self.assertTrue(next(x for x in roles if x['role']=='process-cwd:cwd-only.marker')['exists'])
 def test_cwd_marker_hash_and_missing_copy_are_rejected(self):
  f,c,p=self.layout();(c/'cwd-only.marker').write_bytes(b'wrong source')
  with self.assertRaises(ValueError):self.v.validate_layout(f,c,p)
  (c/'cwd-only.marker').unlink()
  with self.assertRaises(ValueError):self.v.validate_layout(f,c,p)
 def test_probe_marker_never_exists_in_process_cwd(self):
  f,c,p=self.layout();(c/'probe.marker').write_bytes(b'wrong placement')
  with self.assertRaises(ValueError):self.v.validate_layout(f,c,p)
 def test_fixture_marker_root_owner_copies_and_extra_files_rejected(self):
  f,c,p=self.layout();(f/self.v.CASE_IDS[0]/'sub/probe.marker').write_bytes(b'owned-probe-marker\n')
  with self.assertRaises(ValueError):self.v.validate_layout(f,c,p)
 def test_actual_cwd_is_distinct_from_fixture_roots(self):
  f,c,p=self.layout()
  with self.assertRaises(ValueError):self.v.validate_layout(f,f/self.v.CASE_IDS[0],p)
 def test_raw_stdout_binding_precedes_path_normalization(self):
  raw=self.out/'stdout';data=self.payload();raw.write_bytes(json.dumps(data).encode());d={'path':str(raw),'sha256':self.v.sha(raw)}
  self.v.bind_stdout(d,data,self.out);data['rows'][0]['cleanup']['disposed']=1
  with self.assertRaises(ValueError):self.v.bind_stdout(d,data,self.out)
 def test_external_pin_and_log_hash_cannot_be_rebased(self):
  file=self.out/'lock.json';file.write_bytes(b'{"x":1}')
  with self.assertRaises(ValueError):self.v.read_pinned(file,'0'*64)
  with self.assertRaises(ValueError):self.v.bind_stdout({'path':str(file),'sha256':'0'*64},{'x':1},self.out)
 def test_only_declared_paths_normalize_and_scalar_values_remain_exact(self):
  data=self.payload();root=r'D:\fixture';ev=data['rows'][0]['evaluation'];ev['properties']['P']=root+'\\P'
  ev['imports']=[{'owner':root+'\\main.proj','project':root+'\\sub.props','line':1,'column':2}]
  result=self.v.normalize(data,root)
  self.assertEqual(result['rows'][0]['evaluation']['properties']['P'],root+'\\P')
  self.assertEqual(result['rows'][0]['evaluation']['imports'][0]['owner'],'<FIXTURE_ROOT>\\main.proj')
  data['rows'][0]['evaluation']['imports'][0]['owner']=root+'-other\\main.proj'
  self.assertEqual(self.v.normalize(data,root)['rows'][0]['evaluation']['imports'][0]['owner'],root+'-other\\main.proj')
 def test_missing_null_empty_boolean_integer_are_distinct(self):
  for a,b in [({}, {'x':None}),({'x':None},{'x':''}),({'x':True},{'x':1}),({'x':1},{'x':1.0})]:self.assertFalse(self.v.typed_equal(a,b))
 def test_payload_cleanup_and_property_types_are_not_coerced(self):
  for kind in ['cleanup','property','globals']:
   data=self.payload()
   if kind=='cleanup':data['rows'][0]['cleanup']['afterUnload']=False
   elif kind=='property':data['rows'][0]['evaluation']['properties']['Q']=None
   else:data['rows'][0]['globals']={'P':'injected'}
   with self.assertRaises(ValueError):self.v.validate_payload(data)
 def test_directory_cannot_masquerade_as_absent_owner_marker(self):
  f,c,p=self.layout();(f/self.v.CASE_IDS[0]/'sub/probe.marker').mkdir()
  with self.assertRaises(ValueError):self.v.validate_layout(f,c,p)
 def test_directory_cannot_masquerade_as_absent_cwd_marker(self):
  f,c,p=self.layout();(c/'probe.marker').mkdir()
  with self.assertRaises(ValueError):self.v.validate_layout(f,c,p)
if __name__=='__main__':unittest.main()
