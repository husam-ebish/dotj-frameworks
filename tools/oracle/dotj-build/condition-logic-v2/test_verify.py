"""Behavior controls: reject lost/raw/typed/warning evidence, never native simulation."""
import copy, importlib.util, pathlib, unittest, os
p=pathlib.Path(__file__).with_name('verify.py')
s=importlib.util.spec_from_file_location('logic_v2',p); v=importlib.util.module_from_spec(s); s.loader.exec_module(v)
PRIVATE_ROOT=v.B/'agents/validation-performance/condition-logic-v2-native-preparation-20261030'
os.environ.update(TEMP=str(PRIVATE_ROOT),TMP=str(PRIVATE_ROOT))

def payload(root=r'D:\one\fixtures'):
    return {'runtime':'.NET 10.0.12','msbuildAssembly':'pinned','msbuildPath':'mb','frameworkPath':'fw','corePath':'core','profile':'Default','rows':[
      {'id':'probe','globals':{},'profile':'Default','evaluation':{'success':True,'properties':{'P':'alpha','Q':''},'imports':[{'owner':root+r'\probe\main.proj','project':root+r'\probe\one.props','line':1,'column':2}],'duplicateImports':None,'duplicateGetterFailure':{'type':'System.InvalidOperationException','message':'duplicate access unavailable'}},'diagnostics':[{'kind':'warning','code':'MSB4130','file':root+r'\probe\main.proj','line':1,'column':2,'endLine':0,'endColumn':0,'message':'condition warning '+root+r'\probe\main.proj'}],'cleanup':{'before':0,'loaded':1,'afterUnload':0,'disposed':True},'taskMarkerAbsent':True}]}
PLAN={'cases':[{'id':'probe','globals':{},'conditionWarningCandidate':True}]}
LOCK={'msbuildAssembly':'pinned','resolvedAssemblies':{'msbuildPath':'mb','frameworkPath':'fw','corePath':'core'}}
class Controls(unittest.TestCase):
    def reject(self,data):
        with self.assertRaises(ValueError):v.validate_payload(data,PLAN,LOCK)
    def test_bool_does_not_equal_integer(self):self.assertFalse(v.typed_equal({'n':True},{'n':1}))
    def test_path_fields_normalized_only(self):
        p=payload(); p['rows'][0]['evaluation']['properties']['P']=r'D:\one\fixtures\literal'
        n=v.normalize(p,r'D:\one\fixtures');self.assertEqual(n['rows'][0]['evaluation']['imports'][0]['owner'],r'<FIXTURE_ROOT>\probe\main.proj'); self.assertEqual(n['rows'][0]['evaluation']['properties']['P'],r'D:\one\fixtures\literal')
    def test_matching_pair_retains_warning(self):
        result=v.compare_payloads(payload(),payload(r'E:\two\fixtures'),r'D:\one\fixtures',r'E:\two\fixtures',PLAN,LOCK)
        self.assertEqual(result.get('conditionWarningCount'),1); self.assertEqual(result.get('privateDiagnosticDisposition'),'NOT_IMPLEMENTED')
    def test_property_pair_drift_rejected(self):
        p=payload();p['rows'][0]['evaluation']['properties']['Q']='different'
        with self.assertRaises(ValueError):v.compare_payloads(payload(),p,r'D:\one\fixtures',r'D:\one\fixtures',PLAN,LOCK)
    def test_missing_warning_is_observer_gap(self):
        p=payload();p['rows'][0]['diagnostics']=[];self.reject(p)
    def test_unexpected_warning_rejected(self):
        p=payload();p['rows'][0]['diagnostics'][0]['code']='MSB9999';self.reject(p)
    def test_warning_on_undeclared_case_rejected(self):
        plan=copy.deepcopy(PLAN);plan['cases'][0]['conditionWarningCandidate']=False
        with self.assertRaises(ValueError):v.validate_payload(payload(),plan,LOCK)
    def test_cleanup_bool_as_int_rejected(self):
        p=payload();p['rows'][0]['cleanup']['before']=False;self.reject(p)
    def test_extra_raw_field_rejected(self):
        p=payload();p['rows'][0]['extra']='hidden';self.reject(p)
    def test_duplicate_rows_rejected(self):
        p=payload();p['rows']*=2;self.reject(p)
    def test_global_pair_drift_not_normalized(self):
        p=payload();p['rows'][0]['globals']={'P':'invented'};self.reject(p)
    def test_warning_message_drift_rejected(self):
        p=payload();p['rows'][0]['diagnostics'][0]['message']='silently rewritten'
        with self.assertRaises(ValueError):v.compare_payloads(payload(),p,r'D:\one\fixtures',r'D:\one\fixtures',PLAN,LOCK)
    def test_typed_failure_fields_retained(self):
        p=payload();p['rows'][0]['evaluation']={'success':False,'type':'Microsoft.Build.Exceptions.InvalidProjectFileException','code':'MSB4092','file':r'D:\one\fixtures\probe\main.proj','line':1,'column':2,'endLine':0,'endColumn':0,'message':'invalid syntax','hresult':-1}
        v.validate_payload(p,PLAN,LOCK);q=copy.deepcopy(p);q['rows'][0]['evaluation']['hresult']=False;self.reject(q)
class CaptureControls(unittest.TestCase):
    def test_environment_removes_injected_host_options_and_preserves_caller(self):
        cap=v.load('logic_capture_controls',pathlib.Path(__file__).with_name('capture.py'))
        original={'COMPLUS_JitStress':'2','dotnet_startup_hooks':'bad','MsBuildSDKsPath':'outside','Java_Tool_Options':'bad','temp':'old','Keep':'value'}
        before=dict(original);env,overrides=cap.environment(pathlib.Path('owned-output'),original)
        self.assertEqual(original,before);self.assertNotIn('COMPLUS_JitStress',env);self.assertNotIn('dotnet_startup_hooks',env);self.assertNotIn('MsBuildSDKsPath',env);self.assertNotIn('Java_Tool_Options',env);self.assertNotIn('temp',env)
        self.assertEqual(env['DOTNET_GCHeapHardLimit'],'8000000');self.assertEqual(env['DOTNET_PROCESSOR_COUNT'],'2');self.assertEqual(env['Keep'],'value')
    def test_raw_stdout_payload_drift_rejected(self):
        import tempfile,json
        with tempfile.TemporaryDirectory(dir=v.B/'agents/validation-performance/condition-logic-v2-native-preparation-20261030') as folder:
            root=pathlib.Path(folder);log=root/'stdout.json';log.write_text(json.dumps({'P':'actual'}),encoding='utf-8')
            with self.assertRaises(ValueError):v.bind_stdout({'path':str(log),'sha256':v.sha(log)},{'P':'invented'},root)
        self.assertFalse(root.exists(),'owned temporary control directory remained')
        (PRIVATE_ROOT/'python-control-temp-cleanup.json').write_text(json.dumps({'temporaryDirectory':str(root),'resolvedTemp':os.environ['TEMP'],'resolvedTmp':os.environ['TMP'],'ownedDirectoryAbsentAfterContext':not root.exists(),'syntheticFile':'stdout.json'}),encoding='utf-8')
    def test_fixture_root_prefix_does_not_normalize_unrelated_directory(self):
        p=payload();p['rows'][0]['diagnostics'][0]['message']=r'outside D:\one\fixtures-other\file.proj'
        n=v.normalize(p,r'D:\one\fixtures');self.assertEqual(n['rows'][0]['diagnostics'][0]['message'],r'outside D:\one\fixtures-other\file.proj')
    def test_source_freeze_contains_exact_six_document_bytes(self):
        import json,re
        data=v.read(v.E/'predecessor-transitions.json');self.assertEqual(len(data['transitions']),6)
        bodies=[]
        for item in data['transitions']:
            source=item['source'];retained=pathlib.Path(source['source']['copy']);self.assertEqual(v.sha(retained),source['source']['sha256'])
            if 'literal' in source:body=json.loads(source['literal'])
            else:
                text=retained.read_text(encoding='utf-8');expression=source['expression'];self.assertIn('"'+expression+'"',text)
                if item['oldRowOrSubcase']=='AC-SYNTAX-9':
                    method=re.search(r'Files.writeString\(p,("(?:\\.|[^"\\])*")\+expression\+("(?:\\.|[^"\\])*")\+body\+("(?:\\.|[^"\\])*")\)',text)
                    self.assertIsNotNone(method);body=json.loads(method[1])+expression+json.loads(method[2])+'<P>bad</P>'+json.loads(method[3])
                else:
                    lines=[line for line in text.splitlines() if 'Files.writeString(p,' in line and ('<P Condition=' in line if '/property/' in item['oldRowOrSubcase'] else '<Import Project=' in line)]
                    self.assertEqual(len(lines),1);match=re.search(r'Files.writeString\(p,("(?:\\.|[^"\\])*")\+inner\+("(?:\\.|[^"\\])*")\)',lines[0]);self.assertIsNotNone(match);body=json.loads(match[1])+expression+json.loads(match[2])
            file=v.D/'fixtures'/item['caseId']/'main.proj';self.assertEqual(file.read_bytes(),body.encode('utf-8'));self.assertEqual(v.sha(file),item['fixtureSha256']);bodies.append(body)
        self.assertIn('<P>value</P>',bodies[0]);self.assertIn('<P>bad</P>',bodies[3]);self.assertNotEqual(bodies[0],bodies[3])
if __name__=='__main__':unittest.main(verbosity=2)
