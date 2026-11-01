"""Focused typed/evidence boundary tests; synthetic payloads are not native observations."""
import copy,importlib.util,json,unittest
from pathlib import Path
S=importlib.util.spec_from_file_location('cache_verify',Path(__file__).with_name('verify.py'));v=importlib.util.module_from_spec(S);S.loader.exec_module(v)
class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.plan={'cases':[{'id':'one','globals':{'Mode':'Alpha'}}], 'conditionOccurrences':[{'fixture':'one/main.proj','raw':"'$(Mode)' == 'Alpha' Or 'x' == 'y' And 'a' == 'b'"}]}
        self.fingerprint={'runtime':'.NET 10.0.12','msbuildAssembly':'Microsoft.Build, Version=15.1.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a','resolvedAssemblies':{'msbuildPath':'D:/sdk/Microsoft.Build.dll','frameworkPath':'D:/sdk/Microsoft.Build.Framework.dll','corePath':'D:/runtime/System.Private.CoreLib.dll'}}
        self.payload={'runtime':'.NET 10.0.12','msbuildAssembly':self.fingerprint['msbuildAssembly'],**self.fingerprint['resolvedAssemblies'],'profile':'Default','rows':[{'id':'one','globals':{'Mode':'Alpha'},'profile':'Default','evaluation':{'success':True,'properties':{'P':'Alpha','Q':''},'imports':[],'duplicateImports':None,'duplicateGetterFailure':{'type':'System.InvalidOperationException','message':'getter unavailable'}},'diagnostics':[{'kind':'warning','code':'MSB4130','file':'D:/pass/fixtures/one/main.proj','line':3,'column':8,'endLine':0,'endColumn':0,'message':'Condition '+self.plan['conditionOccurrences'][0]['raw']}],'cleanup':{'before':0,'loaded':1,'afterUnload':0,'disposed':True},'taskMarkerAbsent':True}]}
    def valid(self,p=None):return v.validate_payload(p or self.payload,self.plan,self.fingerprint,'D:/pass/fixtures')
    def rejects(self,change):
        p=copy.deepcopy(self.payload);change(p)
        with self.assertRaises(ValueError):self.valid(p)
    def test_accepts_unknown_warning_multiplicity_and_preserves_full_payload(self):
        self.valid();p=copy.deepcopy(self.payload);p['rows'][0]['diagnostics']*=3;self.valid(p);p['rows'][0]['diagnostics']=[];self.valid(p)
    def test_rejects_boolean_globals(self):self.rejects(lambda p:p['rows'][0]['globals'].update(Mode=True))
    def test_rejects_boolean_integer_position(self):self.rejects(lambda p:p['rows'][0]['diagnostics'][0].update(line=True))
    def test_rejects_missing_full_warning_field(self):self.rejects(lambda p:p['rows'][0]['diagnostics'][0].pop('endColumn'))
    def test_rejects_unexpected_warning(self):self.rejects(lambda p:p['rows'][0]['diagnostics'][0].update(code='MSB9999'))
    def test_rejects_raw_condition_spelling_drift(self):self.rejects(lambda p:p['rows'][0]['diagnostics'][0].update(message="Condition '$(Mode)' == 'alpha'"))
    def test_rejects_unowned_warning_path(self):self.rejects(lambda p:p['rows'][0]['diagnostics'][0].update(file='D:/elsewhere/main.proj'))
    def test_rejects_extra_rows_and_duplicate_ids(self):self.rejects(lambda p:p['rows'].append(copy.deepcopy(p['rows'][0])))
    def test_rejects_native_error_but_leaves_input_intact(self):
        p=copy.deepcopy(self.payload);p['rows'][0]['evaluation']={'success':False,'type':'Microsoft.Build.Exceptions.InvalidProjectFileException','code':'MSB4092','file':'D:/pass/fixtures/one/main.proj','line':1,'column':2,'endLine':0,'endColumn':0,'message':'parse','hresult':-1};before=copy.deepcopy(p)
        with self.assertRaises(ValueError):self.valid(p)
        self.assertEqual(p,before)
    def test_rejects_missing_cleanup(self):self.rejects(lambda p:p['rows'][0]['cleanup'].update(afterUnload=1))
    def test_pair_retains_warning_owner_and_count(self):
        other=copy.deepcopy(self.payload);other['rows'][0]['diagnostics'][0]['line']=7
        with self.assertRaises(ValueError):v.compare_payloads(self.payload,other,'D:/pass/fixtures','D:/pass/fixtures',self.plan,self.fingerprint)
    def test_path_only_pair_normalization(self):
        other=json.loads(json.dumps(self.payload).replace('D:/pass/fixtures','D:/second/fixtures'))
        v.compare_payloads(self.payload,other,'D:/pass/fixtures','D:/second/fixtures',self.plan,self.fingerprint)
        other['rows'][0]['globals']['Mode']='alpha'
        with self.assertRaises(ValueError):v.compare_payloads(self.payload,other,'D:/pass/fixtures','D:/second/fixtures',self.plan,self.fingerprint)
    def test_rejects_non_numeric_resource_values(self):
        for value in [True,'524288',-1,None]:
            with self.assertRaises(ValueError):v.validate_memory({'freePhysicalKiB':value,'freeVirtualKiB':16777216})
    def test_memory_floors(self):
        self.assertTrue(v.validate_memory({'freePhysicalKiB':524288,'freeVirtualKiB':16777216}))
        self.assertFalse(v.validate_memory({'freePhysicalKiB':524287,'freeVirtualKiB':16777216}))
    def test_provenance_rejects_forged_stdout_and_boolean_pid(self):
        import tempfile
        with tempfile.TemporaryDirectory(dir=v.PRIVATE/'tmp') as temp:
            root=Path(temp);p=root/'stdout';p.write_text(json.dumps(self.payload),encoding='utf-8');d={'path':str(p),'sha256':v.sha(p)}
            v.bind_stdout(d,self.payload,root)
            changed=copy.deepcopy(self.payload);changed['rows'][0]['globals']['Mode']='Beta'
            with self.assertRaises(ValueError):v.bind_stdout(d,changed,root)
            d['sha256']='0'*64
            with self.assertRaises(ValueError):v.bind_stdout(d,self.payload,root)
        with self.assertRaises(ValueError):v.validate_process({'processId':True,'exitCode':0})
    def test_no_observation_credit_from_static_intentions(self):
        self.assertEqual(v.static_summary()['status'],'STATIC_UNOBSERVED')
        self.assertEqual(v.static_summary()['counts'],{'groups':6,'cases':8,'fixtureFiles':10,'conditionOccurrences':22,'nativeProcessesProposed':2})
if __name__=='__main__':unittest.main()
