"""Actual retained old-runner schema regression; no subprocess or resource query."""
import copy,importlib.util,shutil,tempfile,unittest
from pathlib import Path
B=Path(r'D:\AI\Implementation\dotj Frameworks');HERE=Path(__file__).resolve().parent
class ActualPackagingSchema(unittest.TestCase):
 def setUp(self):
  sp=importlib.util.spec_from_file_location('packaging_reader',HERE/'verify.py');self.v=importlib.util.module_from_spec(sp);sp.loader.exec_module(self.v)
  self.root=B/'validation/task24-candidate-red-v1/packaged94';self.receipt=self.v.read(self.root/'verification.json');self.cp=self.v.read(B/'orchestration/two-frameworks/task-24-product-red-checkpoint-v1.json')
  manifest=self.v.read(B/'validation/task24-harness01-snapshot-v1/manifest.json')
  self.expected={name:next(x['sha256'] for x in manifest['files'] if x['original']==str(self.root/file)) for name,file in [('candidateJar','dotj-build-evaluation-candidate.jar'),('testsJar','evaluation-contract-tests.jar')]}
  # Positive old-schema proof was captured against the live original source before repair.
  # After implementation, keep this schema regression on a frozen original-source view;
  # the runtime reader must still refuse reuse against the changed live evaluator.
  self.live_base=self.v.BASE;self.actual_receipt=copy.deepcopy(self.receipt)
  self.source_temp=tempfile.TemporaryDirectory(dir=B/'validation/task24-harness01-repair-v1');self.addCleanup(self.source_temp.cleanup)
  view=Path(self.source_temp.name)/'original-source-view'
  for relative,digest in self.receipt['sourceHashes'].items():
   original=self.live_base/relative;source=original
   if self.v.sha(original)!=digest:
    entry=next(x for x in manifest['files'] if x['original']==str(original) and x['sha256']==digest)
    source=B/'validation/task24-harness01-snapshot-v1'/entry['snapshot']
   target=view/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
  self.v.BASE=view
  for c in self.receipt['commands']:c['argv']=[x.replace(str(self.live_base),str(view)) for x in c['argv']]
 def test_actual_focused_receipt_derives_both_emitted_jars_without_top_level_keys(self):
  self.assertNotIn('candidateJar',self.receipt);self.assertNotIn('testsJar',self.receipt)
  try:actual=self.v.packaged_artifacts(self.receipt,self.root,self.cp,self.expected)
  except KeyError as e:self.fail('Actual successful old receipt schema cannot be read: '+str(e))
  self.assertEqual(actual['candidateJar'],{'path':str(self.root/'dotj-build-evaluation-candidate.jar'),'sha256':self.expected['candidateJar']})
  self.assertEqual(actual['testsJar'],{'path':str(self.root/'evaluation-contract-tests.jar'),'sha256':self.expected['testsJar']})
 def reject(self,receipt=None,cp=None,root=None,expected=None):
  with self.assertRaises(ValueError):self.v.packaged_artifacts(receipt if receipt is not None else self.receipt,root or self.root,cp or self.cp,expected if expected is not None else self.expected)
 def test_missing_documented_output_path_refused(self):self.reject(root=self.root/'not-a-packaging-output')
 def test_missing_or_malformed_receipt_and_command_fields_refused(self):
  for field in ['schemaVersion','status','sourceHashes','commands','runnerSha256','limits']:
   bad=copy.deepcopy(self.receipt);del bad[field];self.reject(receipt=bad)
  for field in ['argv','cwd','exitCode','stdout','stderr','passed']:
   bad=copy.deepcopy(self.receipt);del bad['commands'][0][field];self.reject(receipt=bad)
 def test_metadata_numeric_type_aliases_refused(self):
  for field,value in [('schemaVersion',True),('schemaVersion',1.0)]:
   bad=copy.deepcopy(self.receipt);bad[field]=value;self.reject(receipt=bad)
  for value in [False,0.0]:
   bad=copy.deepcopy(self.receipt);bad['commands'][0]['exitCode']=value;self.reject(receipt=bad)
  bad=copy.deepcopy(self.receipt);bad['limits']['maxHeapMiB']=128.0;self.reject(receipt=bad)
 def test_source_test_and_tool_closure_changes_refused(self):
  bad=copy.deepcopy(self.receipt);bad['sourceHashes']['tests/org/dotj/internal/build/evaluation/AndConditionTest.java']='0'*64;self.reject(receipt=bad)
  bad=copy.deepcopy(self.receipt);bad['sourceHashes']=[];self.reject(receipt=bad)
  cp=copy.deepcopy(self.cp);cp['inputs']=[x for x in cp['inputs'] if not x['path'].endswith('javac.exe')];self.reject(cp=cp)
 def test_missing_duplicate_or_failed_actual_command_refused(self):
  bad=copy.deepcopy(self.receipt);bad['commands'].pop();self.reject(receipt=bad)
  bad=copy.deepcopy(self.receipt);bad['commands'][2]=copy.deepcopy(bad['commands'][0]);self.reject(receipt=bad)
  bad=copy.deepcopy(self.receipt);bad['commands'][0]['exitCode']=7;self.reject(receipt=bad)
 def test_module_and_patch_paths_must_be_actual_documented_jars(self):
  for field in ['--module-path','--patch-module']:
   bad=copy.deepcopy(self.receipt);argv=bad['commands'][2]['argv'];argv[argv.index(field)+1]='forged.jar';self.reject(receipt=bad)
  bad=copy.deepcopy(self.receipt);bad['commands'][0]['cwd']=str(self.root.parent);self.reject(receipt=bad)
 def test_missing_wrong_or_outside_log_hash_path_refused(self):
  bad=copy.deepcopy(self.receipt);del bad['commands'][0]['stdout']['sha256'];self.reject(receipt=bad)
  bad=copy.deepcopy(self.receipt);bad['commands'][0]['stdout']['sha256']='0'*64;self.reject(receipt=bad)
  bad=copy.deepcopy(self.receipt);bad['commands'][0]['stdout']['path']=str(self.root/'verification.json');self.reject(receipt=bad)
 def test_reused_jar_hash_and_optional_claimed_descriptor_refused(self):
  expected=copy.deepcopy(self.expected);expected['candidateJar']='0'*64;self.reject(expected=expected)
  self.reject(expected={'candidateJar':False,'testsJar':self.expected['testsJar']})
  bad=copy.deepcopy(self.receipt);bad['candidateJar']={'path':'forged.jar','sha256':self.expected['candidateJar']};self.reject(receipt=bad)
 def test_missing_and_malformed_jar_refused_on_owned_clone(self):
  with tempfile.TemporaryDirectory(dir=B/'validation/task24-harness01-repair-v1') as folder:
   clone=Path(folder)/'packaging';clone.mkdir()
   for name in ['classes','test-classes','logs']:shutil.copytree(self.root/name,clone/name)
   for name in ['dotj-build-evaluation-candidate.jar','evaluation-contract-tests.jar']:shutil.copyfile(self.root/name,clone/name)
   bad=copy.deepcopy(self.receipt)
   for c in bad['commands']:
    c['cwd']=str(clone);c['argv']=[x.replace(str(self.root),str(clone)) for x in c['argv']]
    for k in ['stdout','stderr']:c[k]['path']=c[k]['path'].replace(str(self.root),str(clone))
   jar=clone/'dotj-build-evaluation-candidate.jar';jar.write_bytes(b'not-a-zip');self.reject(receipt=bad,root=clone)
   jar.unlink();self.reject(receipt=bad,root=clone)
 def test_changed_live_source_cannot_reuse_original_packaging(self):
  if self.v.sha(self.v.EVALUATOR)==self.v.OLD_SOURCE:self.skipTest('original-source phase; post-change refusal not applicable')
  original_view=self.v.BASE
  try:
   self.v.BASE=self.live_base
   self.reject(receipt=self.actual_receipt)
  finally:self.v.BASE=original_view
if __name__=='__main__':unittest.main()
