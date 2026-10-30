"""Synthetic evidence controls only: no synthetic record is native qualification."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = Path(r'D:\AI\Implementation\dotj Frameworks')


class EvidenceControls(unittest.TestCase):
    def setUp(self):
        path = HERE/'verify.py'
        self.assertTrue(path.is_file(), 'And evidence checker feature is missing')
        spec = importlib.util.spec_from_file_location('and_checker', path)
        self.v = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.v)
        self.tmp = tempfile.TemporaryDirectory(prefix='checker-', dir=ROOT/'validation/task24-static')
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)

    def payload(self, root=r'D:\private\fixtures'):
        rows = []
        for i, ident in enumerate(self.v.CASE_IDS):
            ev = {'success':True,'properties':{'P':'literal','Q':''},'imports':[],
                  'duplicateImports':None,'duplicateGetterFailure':{'type':'System.InvalidOperationException','message':'synthetic'}}
            if i == 7:
                ev = {'success':False,'type':'Microsoft.Build.Exceptions.InvalidProjectFileException',
                      'code':'SYNTHETIC','file':root+'\\x.proj','line':2,'column':3,
                      'endLine':0,'endColumn':0,'message':'synthetic '+root+'\\x.proj','hresult':-1}
            rows.append({'id':ident,'globals':{'EmptyPath':''} if i==3 else {},'profile':'Default',
                         'evaluation':ev,'diagnostics':[], 'cleanup':{'before':0,'loaded':1,'afterUnload':0,'disposed':True},'taskMarkerAbsent':True})
        return {'runtime':'.NET 10.0.12','msbuildAssembly':'synthetic',
                'msbuildPath':str(ROOT/'toolchains/dotnet/sdk/10.0.401/Microsoft.Build.dll'),
                'frameworkPath':str(ROOT/'toolchains/dotnet/sdk/10.0.401/Microsoft.Build.Framework.dll'),
                'corePath':str(ROOT/'toolchains/dotnet/shared/Microsoft.NETCore.App/10.0.12/System.Private.CoreLib.dll'),
                'profile':'Default','rows':rows}

    def test_typed_comparison_rejects_bool_integer_alias(self):
        self.assertFalse(self.v.typed_equal({'x':True}, {'x':1}))
        self.assertFalse(self.v.typed_equal([False], [0]))

    def test_missing_null_and_empty_are_distinct(self):
        for left,right in [({}, {'x':None}),({'x':None},{'x':''}),({'x':[]},{'x':{}})]:
            self.assertFalse(self.v.typed_equal(left,right))

    def test_valid_synthetic_body_and_declared_root_normalization(self):
        data=self.payload();self.v.validate_payload(data)
        norm=self.v.normalize(data,r'D:\private\fixtures')
        self.assertEqual(norm['rows'][7]['evaluation']['file'],'<FIXTURE_ROOT>\\x.proj')
        self.assertEqual(data['rows'][7]['evaluation']['file'],r'D:\private\fixtures\x.proj')

    def test_properties_globals_and_nonpath_strings_never_normalized(self):
        data=self.payload();root=r'D:\private\fixtures'
        data['rows'][0]['evaluation']['properties']['P']=root+'\\P'
        data['rows'][3]['globals']['EmptyPath']=root+'\\global'
        data['msbuildAssembly']=root
        norm=self.v.normalize(data,root)
        self.assertEqual(norm['rows'][0]['evaluation']['properties']['P'],root+'\\P')
        self.assertEqual(norm['rows'][3]['globals']['EmptyPath'],root+'\\global')
        self.assertEqual(norm['msbuildAssembly'],root)

    def test_similar_root_is_not_normalized(self):
        data=self.payload();data['rows'][7]['evaluation']['file']=r'D:\private\fixtures-other\x'
        self.assertEqual(self.v.normalize(data,r'D:\private\fixtures')['rows'][7]['evaluation']['file'],r'D:\private\fixtures-other\x')

    def test_exact_eight_case_order_and_coverage(self):
        for edit in [lambda r:r.pop(), lambda r:r.append(copy.deepcopy(r[0])),lambda r:r.reverse(),lambda r:r[0].update(id='foreign')]:
            data=self.payload();edit(data['rows'])
            with self.assertRaises(ValueError):self.v.validate_payload(data)

    def test_cleanup_types_and_task_marker_required(self):
        for field,value in [('disposed',1),('afterUnload',False),('afterUnload',1),('before',1),('loaded',-1)]:
            data=self.payload();data['rows'][0]['cleanup'][field]=value
            with self.assertRaises(ValueError):self.v.validate_payload(data)
        data=self.payload();data['rows'][0]['taskMarkerAbsent']=False
        with self.assertRaises(ValueError):self.v.validate_payload(data)

    def test_success_properties_and_failure_shape_not_coerced(self):
        for field,value in [('P',None),('P',True),('Q',0)]:
            data=self.payload();data['rows'][0]['evaluation']['properties'][field]=value
            with self.assertRaises(ValueError):self.v.validate_payload(data)
        data=self.payload();del data['rows'][7]['evaluation']['hresult']
        with self.assertRaises(ValueError):self.v.validate_payload(data)

    def test_import_order_is_observable(self):
        data=self.payload();edge={'owner':'a','project':'b','line':1,'column':2}
        data['rows'][0]['evaluation']['imports']=[edge,dict(edge,project='c')]
        other=copy.deepcopy(data);other['rows'][0]['evaluation']['imports'].reverse()
        self.assertFalse(self.v.typed_equal(data,other))

    def test_raw_binding_precedes_normalization(self):
        raw=self.dir/'native.stdout';data=self.payload();raw.write_bytes(json.dumps(data).encode())
        descriptor={'path':str(raw),'sha256':self.v.sha(raw)}
        self.v.bind_stdout(descriptor,data,self.dir)
        data['rows'][7]['evaluation']['file']='<FIXTURE_ROOT>\\x.proj'
        with self.assertRaises(ValueError):self.v.bind_stdout(descriptor,data,self.dir)

    def test_raw_hash_and_external_lock_tampering_rejected(self):
        raw=self.dir/'native.stdout';data=self.payload();raw.write_bytes(json.dumps(data).encode())
        with self.assertRaises(ValueError):self.v.bind_stdout({'path':str(raw),'sha256':'0'*64},data,self.dir)
        lock=self.dir/'lock.json';lock.write_bytes(b'{"inputs":[]}')
        with self.assertRaises(ValueError):self.v.read_pinned(lock,'0'*64)

    def test_duplicate_json_keys_rejected(self):
        p=self.dir/'duplicate.json';p.write_bytes(b'{"x":1,"x":2}')
        with self.assertRaises(ValueError):self.v.read(p)

    def test_input_coverage_rejects_added_missing_and_changed_files(self):
        root=self.dir/'fixtures';root.mkdir();f=root/'main.proj';f.write_bytes(b'original')
        entries=[{'path':'main.proj','sha256':self.v.sha(f),'bytes':8}]
        self.v.verify_fixtures(root,entries)
        f.write_bytes(b'changed')
        with self.assertRaises(ValueError):self.v.verify_fixtures(root,entries)
        f.write_bytes(b'original');(root/'extra.props').write_bytes(b'x')
        with self.assertRaises(ValueError):self.v.verify_fixtures(root,entries)
        f.unlink()
        with self.assertRaises(ValueError):self.v.verify_fixtures(root,entries)

    def test_log_paths_cannot_escape_owned_capture(self):
        raw=self.dir/'native.stdout';data=self.payload();raw.write_bytes(json.dumps(data).encode())
        outside=self.dir/'child';outside.mkdir()
        with self.assertRaises(ValueError):self.v.bind_stdout({'path':str(raw),'sha256':self.v.sha(raw)},data,outside)

    def test_no_native_assumption_for_ba08(self):
        data=self.payload();data['rows'][7]['evaluation']=copy.deepcopy(data['rows'][0]['evaluation'])
        self.v.validate_payload(data)
        self.assertEqual(self.v.classify(data)['malformedEvidence'][0]['nativeSuccess'],True)
        self.assertEqual(self.v.classify(data)['successfulNativeComparisons'],7)

    def test_raw_bool_integer_mutation_is_rejected(self):
        raw=self.dir/'native.stdout';data=self.payload();raw.write_bytes(json.dumps(data).encode())
        data['rows'][0]['cleanup']['disposed']=1
        with self.assertRaises(ValueError):self.v.bind_stdout({'path':str(raw),'sha256':self.v.sha(raw)},data,self.dir)

    def test_embedded_nonprefix_path_is_never_normalized(self):
        data=self.payload();data['rows'][7]['evaluation']['file']=r'otherD:\private\fixtures\x'
        self.assertEqual(self.v.normalize(data,r'D:\private\fixtures')['rows'][7]['evaluation']['file'],r'otherD:\private\fixtures\x')

    def test_resource_floor_and_wait_types_are_enforced(self):
        record={'commands':[{'label':'compile-probe'},{'label':'native-eight-cases'}],
                'resourceWaits':[{'before':label,'status':'READY','limitSeconds':120,'pollSeconds':5,'seconds':0.1} for label in ['compile-probe','native-eight-cases']],
                'resources':[{'before':label,'freePhysicalKiB':524288,'freeVirtualKiB':16777216,'waitSeconds':0.1} for label in ['compile-probe','native-eight-cases']]}
        self.v.validate_resources(record)
        for field,value in [('freePhysicalKiB',524287),('freeVirtualKiB',16777215),('freePhysicalKiB',True)]:
            bad=copy.deepcopy(record);bad['resources'][-1][field]=value
            with self.assertRaises(ValueError):self.v.validate_resources(bad)
        bad=copy.deepcopy(record);bad['resourceWaits'][0]['status']='DEFERRED_RESOURCES'
        with self.assertRaises(ValueError):self.v.validate_resources(bad)

    def test_candidate_refusal_does_not_count_as_native_success(self):
        data=self.payload();data['rows'][0]['evaluation']=copy.deepcopy(data['rows'][7]['evaluation'])
        with self.assertRaises(ValueError):self.v.classify(data)

    def test_native_lock_excludes_later_candidate_evidence_but_requires_native_inputs(self):
        self.v.ROOT=self.dir;self.v.REPO=self.dir/'repo';self.v.HERE=self.v.REPO/'tools/oracle/dotj-build/and-conditions-v1'
        self.v.DATA=self.v.REPO/'dotj-build/evaluation-candidate/and-conditions-v1';self.v.EVIDENCE=self.v.DATA/'evidence'
        data=self.v.DATA;tools=self.v.HERE
        for folder in [data/'fixtures',data/'evidence',tools]:folder.mkdir(parents=True)
        fixture=data/'fixtures/main.proj';fixture.write_bytes(b'<Project/>')
        plan={'cases':[{'id':x} for x in self.v.CASE_IDS],'fixtures':[{'path':'main.proj','bytes':10,'sha256':self.v.sha(fixture)}]}
        (data/'evidence/plan.json').write_bytes(json.dumps(plan).encode())
        for file in [data/'.gitattributes',data/'evidence/grammar.json',data/'evidence/capture.schema.json',tools/'capture.py',tools/'verify.py',tools/'test_verify.py']:file.write_bytes(b'static')
        legacy=data/'evidence/historical-candidate-lock.json'
        legacy.write_bytes(json.dumps({'inputs':[{'base':'repo','path':'src/ProjectEvaluationComponent.java','sha256':'0'*64}]}).encode())
        inputs=[{'base':'repo','path':p.relative_to(self.v.REPO).as_posix(),'sha256':self.v.sha(p)} for p in self.v.REPO.rglob('*') if p.is_file()]
        lock=data/'evidence/input-lock.json';lock.write_bytes(json.dumps({'inputs':inputs}).encode())
        pin=self.v.sha(lock);self.v.verify_inputs(pin)
        (data/'evidence/observations.json').write_bytes(b'later native observations')
        (data/'evidence/candidate-verification.json').write_bytes(b'later changed evaluator evidence')
        (tools/'coordinate-candidate.py').write_bytes(b'later product coordinator')
        candidate=self.v.REPO/'src/ProjectEvaluationComponent.java';candidate.parent.mkdir()
        candidate.write_bytes(b'changed evaluator excluded from native inputs')
        try:self.v.verify_inputs(pin)
        except ValueError as error:self.fail('native-only lock was invalidated by later candidate evidence: '+str(error))
        altered=copy.deepcopy(inputs);altered=[x for x in altered if not x['path'].endswith('/capture.py')]
        lock.write_bytes(json.dumps({'inputs':altered}).encode())
        with self.assertRaises(ValueError):self.v.verify_inputs(self.v.sha(lock))

    def synthetic_capture_for_metadata_controls(self):
        """Real validator/files, with installed-input checks already covered separately.

        Dependency doubles avoid rehashing the installed SDK per metadata mutation.
        This payload has no process provenance and is never native evidence.
        """
        v=self.v;out=self.dir/'synthetic-metadata-capture';out.mkdir()
        shutil.copytree(v.DATA/'fixtures',out/'fixtures')
        original=v.read(v.EVIDENCE/'input-lock.json')
        payload=self.payload(str(out/'fixtures'))
        lock={'copiedInputs':[],'runtimeConfig':original['runtimeConfig'],'compilerReferences':[],
              'resolvedAssemblies':{key:Path(payload[key]).relative_to(v.ROOT).as_posix() for key in ['msbuildPath','frameworkPath','corePath']},
              'msbuildAssembly':'synthetic','limits':copy.deepcopy(original['limits'])}
        for name,body in [('binary.dll',b'SYNTHETIC-NOT-COMPILED'),('runtime.json',json.dumps(lock['runtimeConfig']).encode())]:(out/name).write_bytes(body)
        record={'schemaVersion':1,'status':'PASS_NATIVE_AND_CAPTURE','runId':'SYNTHETIC-UNIT-ONLY',
                'inputLockSha256':'unit-input','checkpointSha256':'unit-checkpoint','fixtureRoot':str(out/'fixtures'),
                'commands':[],'copiedInputs':[],'binary':{'path':str(out/'binary.dll'),'sha256':v.sha(out/'binary.dll')},
                'runtimeConfig':{'path':str(out/'runtime.json'),'sha256':v.sha(out/'runtime.json')},
                'payload':payload,'limits':copy.deepcopy(lock['limits']),
                'resourceWaits':[],'resources':[]}
        for label in ['compile-probe','native-eight-cases']:
            command={'label':label,'exitCode':0,'nativeTimeoutSeconds':30,'cwd':str(out),
                     'environmentOverrides':{'DOTNET_GCHeapHardLimit':'8000000','DOTNET_PROCESSOR_COUNT':'2','DOTNET_ROLL_FORWARD':'Disable'}}
            for name,body in [('stdout',json.dumps(payload).encode() if label=='native-eight-cases' else b''),('stderr',b''),('hostTrace',b'SYNTHETIC-NOT-A-HOST-TRACE')]:
                file=out/(label+'.'+name);file.write_bytes(body);command[name]={'path':str(file),'sha256':v.sha(file)}
            record['commands'].append(command)
            record['resourceWaits'].append({'before':label,'status':'READY','limitSeconds':120,'pollSeconds':5,'seconds':0.1})
            record['resources'].append({'before':label,'freePhysicalKiB':524288,'freeVirtualKiB':16777216,'waitSeconds':0.1})
        sdk=v.ROOT/'toolchains/dotnet/sdk/10.0.401';dotnet=str(v.ROOT/'toolchains/dotnet/dotnet.exe')
        record['commands'][0]['argv']=[dotnet,'exec',str(sdk/'Roslyn/bincore/csc.dll'),'/nologo','/noconfig','/nostdlib+',
            '/target:exe','/nullable:enable','/deterministic+','/langversion:14','/out:'+record['binary']['path'],str(out/'CaptureImportPathsV1.cs')]
        record['commands'][1]['argv']=[dotnet,'exec','--runtimeconfig',record['runtimeConfig']['path'],'--depsfile',str(sdk/'MSBuild.deps.json'),record['binary']['path'],str(out/'fixtures'),str(out/'plan.json')]
        inputs=patch.object(v,'verify_inputs',return_value=lock);inputs.start();self.addCleanup(inputs.stop)
        checkpoint=patch.object(v,'verify_checkpoint',return_value={});checkpoint.start();self.addCleanup(checkpoint.stop)
        def validate(value):
            path=out/'capture.json';path.write_bytes(json.dumps(value).encode())
            return v.validate_capture(path,'unit-input',out/'checkpoint.json','unit-checkpoint')
        validate(record)
        return record,validate

    def test_capture_schema_version_rejects_boolean_alias(self):
        record,validate=self.synthetic_capture_for_metadata_controls()
        record['schemaVersion']=True
        with self.assertRaises(ValueError):validate(record)

    def test_command_exit_code_rejects_boolean_and_float_aliases(self):
        record,validate=self.synthetic_capture_for_metadata_controls()
        for index in [0,1]:
            for value in [False,0.0]:
                with self.subTest(command=index,value=value):
                    altered=copy.deepcopy(record);altered['commands'][index]['exitCode']=value
                    with self.assertRaises(ValueError):validate(altered)

    def test_native_timeout_rejects_float_alias(self):
        record,validate=self.synthetic_capture_for_metadata_controls()
        for index in [0,1]:
            with self.subTest(command=index):
                altered=copy.deepcopy(record);altered['commands'][index]['nativeTimeoutSeconds']=30.0
                with self.assertRaises(ValueError):validate(altered)

    def test_capture_limits_reject_numeric_type_aliases(self):
        record,validate=self.synthetic_capture_for_metadata_controls()
        for field,value in record['limits'].items():
            with self.subTest(field=field):
                altered=copy.deepcopy(record);altered['limits'][field]=float(value)
                with self.assertRaises(ValueError):validate(altered)


if __name__ == '__main__': unittest.main()
