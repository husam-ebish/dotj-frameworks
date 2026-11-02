"""New pure controls only. No process, compiler, JVM or evaluator execution."""
import copy
import importlib.util
import json
import pathlib
import re
from decimal import Decimal
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('ordering_protocol', HERE / 'protocol.py')
p = None
if (HERE / 'protocol.py').exists():
    p = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(p)


def witness_eligibility(token):
    """Independent source-contract probe for this fix's unsigned decimal subset.

    NumericExpressionNode delegates to invariant finite decimal conversion and
    Version.TryParse; Version requires 2..4 nonnegative Int32 components. This
    intentionally does not implement general conversion or any product logic.
    """
    text=token[1:-1] if token.startswith("'") and token.endswith("'") else token
    numeric=bool(re.fullmatch(r'[0-9]+(?:\.[0-9]+)?',text)) and Decimal(text).is_finite()
    components=text.split('.')
    version=2<=len(components)<=4 and all(re.fullmatch(r'[0-9]+',c) and 0<=int(c)<=2147483647 for c in components)
    return numeric,version


def witness_dispatch(left,right):
    ln,lv=witness_eligibility(left);rn,rv=witness_eligibility(right)
    if ln and rn:return 'NUMERIC_PAIR'
    if lv and rv:return 'VERSION_PAIR'
    if ln and rv:return 'NUMERIC_VERSION'
    if lv and rn:return 'VERSION_NUMERIC'
    return 'NONNUMERIC'


class ProfileControls(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(p, 'new ordering protocol is required')

    def test_manifest_interface_and_all_twelve_groups(self):
        manifest = p.read(HERE / 'manifest.json')
        p.manifest(manifest)
        self.assertEqual(set(manifest['groups']), set(c['group'] for c in manifest['cases']))
        self.assertEqual(12, len(manifest['groups']))

    def test_fixture_bytes_and_xml(self):
        p.fixtures(p.read(HERE / 'manifest.json'), HERE / 'fixtures')

    def test_manifest_rejects_malicious_shapes(self):
        base = p.read(HERE / 'manifest.json')
        changes = [('duplicate', lambda x: x['cases'].append(x['cases'][0])),
                   ('path', lambda x: x['cases'][0].update(id='../escape')),
                   ('long', lambda x: x['cases'][0].update(id='a'*97)),
                   ('unicode', lambda x: x['cases'][0].update(id='é')),
                   ('global', lambda x: x['cases'][0].update(globals={'N': 1})),
                   ('duplicate-file', lambda x: x['cases'][0]['files'].append(x['cases'][0]['files'][0])),
                   ('bool', lambda x: x.update(schemaVersion=True)),
                   ('unknown', lambda x: x.update(unexpected=1))]
        for name, mutate in changes:
            with self.subTest(name=name):
                value = copy.deepcopy(base); mutate(value)
                with self.assertRaises(ValueError): p.manifest(value)

    def test_success_error_fault_shapes(self):
        for kind in ['SUCCESS','PROJECT_ERROR','UNEXPECTED_NONFATAL_RUNTIME_FAULT']:
            p.row(p.example_row(kind), 'ORD-TEST', {})

    def test_fix1_all_four_both_directions_are_genuine_mixed_witnesses(self):
        cases={c['id']:c for c in p.read(HERE/'manifest.json')['cases']}
        for op in ['LT','LE','GT','GE']:
            for label in ['equal-major','fractional']:
                for direction in ['NV','VN']:
                    case=cases[f'ORD-MIX-{op}-{direction}-{label}']
                    left,_,right=re.fullmatch(r'(.+?)(<=|>=|<|>)(.+)',case['condition']).groups()
                    with self.subTest(id=case['id']):
                        self.assertEqual('NUMERIC_VERSION' if direction=='NV' else 'VERSION_NUMERIC',witness_dispatch(left,right))
                        self.assertEqual((True,False) if direction=='NV' else (False,True),witness_eligibility(left))
                        self.assertEqual((False,True) if direction=='NV' else (True,False),witness_eligibility(right))

    def test_fix1_former_mislabeled_inputs_are_not_mixed(self):
        for left,right,expected in [('6',"'6.0'",'NUMERIC_PAIR'),("'6.0'",'6','NUMERIC_PAIR'),('6.5',"'6.0.0'",'VERSION_PAIR'),("'6.0.0'",'6.5','VERSION_PAIR')]:
            with self.subTest(left=left,right=right):
                self.assertEqual(expected,witness_dispatch(left,right))
                self.assertNotIn(witness_dispatch(left,right),['NUMERIC_VERSION','VERSION_NUMERIC'])
        self.assertEqual((True,False),witness_eligibility('6.5000000000'))
        self.assertEqual(Decimal('6.5'),Decimal('6.5000000000'))
        self.assertGreater(int('5000000000'),2147483647)

    def test_fix1_project_error_identity_is_exact_emitter_catch(self):
        for exception in ['System.NullReferenceException','System.OutOfMemoryException','System.StackOverflowException','System.AccessViolationException','System.Exception','Microsoft.Build.Exceptions.InvalidProjectFileExceptionExtra','']:
            bad=p.example_row('PROJECT_ERROR');bad['evaluation']['type']=exception
            with self.subTest(exception=exception),self.assertRaises(ValueError):p.row(bad,'ORD-TEST',{})

    def test_fix1_success_getter_requires_exactly_one_emitter_alternative(self):
        for imports,failure in [(None,None),([],{ 'type':'System.InvalidOperationException','message':'control'})]:
            bad=p.example_row('SUCCESS');bad['evaluation'].update(duplicateImports=imports,duplicateGetterFailure=failure)
            with self.subTest(imports=imports,failure=failure),self.assertRaises(ValueError):p.row(bad,'ORD-TEST',{})
        for failure_type in ['System.NullReferenceException','System.OutOfMemoryException','System.Exception','']:
            bad=p.example_row('SUCCESS');bad['evaluation']['duplicateGetterFailure']['type']=failure_type
            with self.subTest(failure_type=failure_type),self.assertRaises(ValueError):p.row(bad,'ORD-TEST',{})

    def test_fix1_incompatible_fault_error_success_shapes_fail_closed(self):
        for kind,mutations in [
            ('PROJECT_ERROR',[lambda e:e.update(outcome='runtime-fault-v3'),lambda e:e.update(stack='invented'),lambda e:e.pop('hresult')]),
            ('UNEXPECTED_NONFATAL_RUNTIME_FAULT',[lambda e:e.update(success=False),lambda e:e.pop('stack'),lambda e:e.update(type='Microsoft.Build.Exceptions.InvalidProjectFileException')]),
            ('SUCCESS',[lambda e:e.pop('duplicateGetterFailure'),lambda e:e.pop('duplicateImports'),lambda e:e.update(outcome='runtime-fault-v3')])]:
            for i,mutate in enumerate(mutations):
                bad=p.example_row(kind);mutate(bad['evaluation'])
                with self.subTest(kind=kind,mutation=i),self.assertRaises(ValueError):p.row(bad,'ORD-TEST',{})

    def test_row_rejects_wrong_types_and_presence(self):
        changes = [('boolint',lambda r:r['cleanup'].update(loaded=True)),
                   ('missing',lambda r:r['evaluation']['properties'].pop('Q')),
                   ('marker',lambda r:r.update(taskMarkerAbsent=False)),
                   ('extra',lambda r:r['evaluation'].update(stack='invented')),
                   ('globals',lambda r:r.update(globals={'N':'1'})),
                   ('nullarray',lambda r:r['evaluation'].update(imports=None)),
                   ('alias',lambda r:r['evaluation'].update(success=1)),
                   ('cleanup',lambda r:r['cleanup'].update(afterUnload=1)),
                   ('id',lambda r:r.update(id='ORD-OTHER'))]
        for name, mutate in changes:
            with self.subTest(name=name):
                r=p.example_row('SUCCESS');mutate(r)
                with self.assertRaises(ValueError):p.row(r,'ORD-TEST',{})

    def test_runtime_fault_requires_stack_and_is_never_project_error(self):
        r=p.example_row('UNEXPECTED_NONFATAL_RUNTIME_FAULT')
        self.assertEqual('UNEXPECTED_NONFATAL_RUNTIME_FAULT',p.row(r,'ORD-TEST',{}))
        for key in ['stack','type','message','hresult']:
            bad=copy.deepcopy(r);bad['evaluation'].pop(key)
            with self.subTest(key=key),self.assertRaises(ValueError):p.row(bad,'ORD-TEST',{})

    def test_project_error_stack_is_unavailable(self):
        r=p.example_row('PROJECT_ERROR');r['evaluation']['stack']='not emitted'
        with self.assertRaises(ValueError):p.row(r,'ORD-TEST',{})

    def test_progress_missing_duplicate_reordered_and_unknown(self):
        expected=['ORD-A','ORD-B']
        valid='DOTJ_OBSERVER_V3 BEGIN ORD-A\nDOTJ_OBSERVER_V3 END ORD-A\nDOTJ_OBSERVER_V3 BEGIN ORD-B\nDOTJ_OBSERVER_V3 END ORD-B\n'
        self.assertEqual(4,len(p.progress(valid,expected,True)))
        for bad in [valid.replace('END ORD-A','END ORD-B'),valid+valid,valid.replace('END ORD-B\n',''),valid.replace('ORD-B','ORD-X')]:
            with self.subTest(value=bad),self.assertRaises(ValueError):p.progress(bad,expected,True)

    def test_fault_or_missing_receipt_is_typed_unknown(self):
        self.assertEqual({'state':'UNKNOWN','value':None},p.execution_count(None))
        self.assertEqual({'state':'KNOWN','value':0},p.execution_count({'launched':False}))
        self.assertEqual({'state':'KNOWN','value':1},p.execution_count({'launched':True}))
        self.assertEqual('FATAL_OR_CLEANUP_FAILURE',p.process_outcome(None))
        with self.assertRaises(ValueError):p.execution_count({'launched':0})

    def test_budget_reserves_actual_outer_deadline_and_fresh_admission(self):
        p.admission(200,130,129,{'freePhysicalBytes':512*1024**2,'freeVirtualBytes':16*1024**3},30)
        for deadline,now,sampled,sample,child in [
            (164,130,129,{'freePhysicalBytes':512*1024**2,'freeVirtualBytes':16*1024**3},30),
            (200,130,127,{'freePhysicalBytes':512*1024**2,'freeVirtualBytes':16*1024**3},30),
            (200,130,131,{'freePhysicalBytes':512*1024**2,'freeVirtualBytes':16*1024**3},30),
            (200,130,129,{'freePhysicalBytes':0,'freeVirtualBytes':16*1024**3},30),
            (200,130,129,{'freePhysicalBytes':512*1024**2,'freeVirtualBytes':True},30),
            (200,130,129,{'freePhysicalBytes':512*1024**2,'freeVirtualBytes':16*1024**3},120)]:
            with self.subTest(deadline=deadline,child=child),self.assertRaises(ValueError):p.admission(deadline,now,sampled,sample,child)

    def test_missing_or_wrong_approval_rejected(self):
        with self.assertRaises(ValueError):p.approval(None,'a'*64,'pass1-part01')
        value=p.example_approval('a'*64,'pass1-part01')
        p.approval(value,'a'*64,'pass1-part01')
        for key,v in [('independentReviewer',''),('executionLockSha256','b'*64),('nativeApproved',1),('newCompilerExecutions',True),('phase','pass2-part01')]:
            bad=copy.deepcopy(value);bad[key]=v
            with self.subTest(key=key),self.assertRaises(ValueError):p.approval(bad,'a'*64,'pass1-part01')

    def test_exact_history_resolver_rejects_arbitrary_fallback(self):
        d={'path':'C:/exact/source','sha256':'a'*64,'sizeBytes':2}
        a={'path':'D:/exact/archive','sha256':'a'*64,'sizeBytes':2}
        self.assertEqual(a,p.resolve_history(d,[{'original':d,'archived':a}]))
        for changed in [dict(d,path='C:/other/source'),dict(d,sha256='b'*64),dict(d,sizeBytes=True)]:
            with self.subTest(value=changed),self.assertRaises(ValueError):p.resolve_history(changed,[{'original':d,'archived':a}])

    def test_duplicate_json_keys_and_nonfinite_numbers_rejected(self):
        for raw in ['{"a":1,"a":2}','{"a":NaN}','{"a":Infinity}']:
            with self.subTest(raw=raw),self.assertRaises(ValueError):p.loads(raw)

    def test_only_fixture_root_normalizes(self):
        value={'file':'D:/run/fixtures/A/main.proj','message':'raw C:/elsewhere D:/run/fixtures/A/main.proj','stack':'raw D:/run/fixtures/A/main.proj'}
        normalized=p.normalize(value,'D:/run/fixtures')
        self.assertEqual('raw C:/elsewhere <fixture-root>/A/main.proj',normalized['message'])
        self.assertEqual('raw D:/run/fixtures/A/main.proj',normalized['stack'])

    def test_native_binding_rejects_wrong_assembly_runtime_and_order(self):
        fp={'runtime':'.NET 10.0.12','msbuildAssembly':'Microsoft.Build, Version=15.1.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a',
            'msbuildPath':'D:/pinned/Microsoft.Build.dll','frameworkPath':'D:/pinned/Microsoft.Build.Framework.dll','corePath':'D:/pinned/System.Private.CoreLib.dll','profile':'Default'}
        value=dict(fp,rows=[p.example_row('SUCCESS')]);cases=[{'id':'ORD-TEST','globals':{}}]
        self.assertEqual(['SUCCESS'],p.observation(value,cases,fp))
        for key in fp:
            bad=copy.deepcopy(value);bad[key]='arbitrary'
            with self.subTest(key=key),self.assertRaises(ValueError):p.observation(bad,cases,fp)
        for rows in [[],value['rows']*2,[dict(value['rows'][0],id='ORD-OTHER')]]:
            bad=dict(value,rows=rows)
            with self.subTest(rows=len(rows)),self.assertRaises(ValueError):p.observation(bad,cases,fp)

    def test_native_fault_cannot_hide_fatal_or_project_error(self):
        for fatal in ['System.OutOfMemoryException','System.StackOverflowException','System.AccessViolationException','System.Runtime.InteropServices.SEHException','System.Threading.ThreadAbortException','Microsoft.Build.Exceptions.InvalidProjectFileException']:
            bad=p.example_row('UNEXPECTED_NONFATAL_RUNTIME_FAULT');bad['evaluation']['type']=fatal
            with self.subTest(fatal=fatal),self.assertRaises(ValueError):p.row(bad,'ORD-TEST',{})

    def test_pin_rejects_changed_hash_and_size(self):
        descriptor=p.descriptor(HERE/'protocol.py');p.pin(descriptor)
        for key,v in [('sha256','0'*64),('sizeBytes',descriptor['sizeBytes']+1),('sizeBytes',True),('path',str(HERE/'absent.py'))]:
            bad=dict(descriptor);bad[key]=v
            with self.subTest(key=key,v=v),self.assertRaises(ValueError):p.pin(bad)

    def test_native_argv_rejects_old_manifest_and_output_retarget(self):
        spec=importlib.util.spec_from_file_location('ordering_runner_controls',HERE/'native_runner.py')
        runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
        proposal=p.read(HERE/'execution-proposal.json');phase=proposal['invocations'][0]['phase']
        argv=runner.native_argv(phase);runner.validate_argv(argv,phase)
        for index,value in [(-1,str(HERE.parent/'condition-boolean-v1/manifest.json')),(-2,'C:/arbitrary/fixtures'),(0,'dotnet.exe')]:
            bad=list(argv);bad[index]=value
            with self.subTest(index=index),self.assertRaises(ValueError):runner.validate_argv(bad,phase)
        with self.assertRaises(ValueError):runner.phase_plan('pass99-part99')

    def test_process_receipt_rejects_wrong_caps_pid_budget_or_partial(self):
        argv=['D:/pinned/dotnet.exe','exec','observer.dll'];cwd=pathlib.Path('D:/fresh')
        r=dict(argv=argv,cwd=str(cwd),timeoutSeconds=30,cleanupLimitSeconds=5,outputPollSeconds=0.1,outputProfile='runtime',outputLimitsBytes={'stdout':2097152,'stderr':524288},launched=True,processId=1234,exitCode=0,jobAssigned=True,resumed=True,timedOut=False,outputLimitExceeded=False,cleanupSeconds=0.1,seconds=1.2,outputSizesBytes={'stdout':100,'stderr':100})
        p.process_receipt(r,argv,cwd,30,'runtime')
        changes=[('outputLimitsBytes',{'stdout':4194304,'stderr':524288}),('processId',True),('timeoutSeconds',180),('jobAssigned',False),('resumed',False),('cleanupSeconds',6),('exitCode',True),('timedOut',True),('seconds',36),('cleanupError','not empty'),('outputSizesBytes',{'stdout':100,'stderr':524289})]
        for key,value in changes:
            bad=copy.deepcopy(r);bad[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):p.process_receipt(bad,argv,cwd,30,'runtime')

    def test_schema_anchors_resolve_exact_observer_bytes(self):
        schema=p.read(HERE/'selected-schema.json');p.pin(schema['emitter'])
        lines=pathlib.Path(schema['emitter']['path']).read_text().splitlines()
        for field in schema['fields']:
            with self.subTest(field=field['path']):
                if field['availability']=='EMITTED':
                    self.assertTrue(field['emitterLines'])
                    self.assertTrue(all(field['emitterText'] in lines[n-1] for n in field['emitterLines']))
                else:self.assertEqual('ProjectError.stack',field['path'])

    def test_partitions_cover_every_id_once_without_splitting_cache_sequence(self):
        proposal=p.read(HERE/'execution-proposal.json');expected=[x['id'] for x in p.read(HERE/'manifest.json')['cases']]
        for pass_no in [1,2]:
            phases=[v for v in proposal['invocations'] if v['passNumber']==pass_no]
            self.assertEqual(expected,[i for phase in phases for i in phase['caseIds']])
            self.assertTrue(all(0<len(phase['caseIds'])<=80 for phase in phases))
            self.assertEqual(1,sum(any(i.startswith('ORD-CACHE-') for i in phase['caseIds']) for phase in phases))

    def test_history_single_transition_is_exact_old_fixture(self):
        ledger=p.read(HERE/'transition-ledger.json');self.assertEqual([],ledger['extraDispositionCandidates'])
        self.assertEqual(['BOOL-BOUND-ordering'],[x['oldId'] for x in ledger['transitions']])
        t=ledger['transitions'][0];p.pin(t['oldFixture']);p.pin(t['newFixture'])
        self.assertEqual(t['oldFixture']['sha256'],t['newFixture']['sha256'])

    def test_ownership_direct_inner_requires_capability(self):
        spec=importlib.util.spec_from_file_location('ordering_ownership_controls',HERE/'ownership.py')
        own=importlib.util.module_from_spec(spec);spec.loader.exec_module(own)
        for handle in [None,0,-1,True,'123']:
            with self.subTest(handle=handle),self.assertRaises(ValueError):own.consume(handle,p,'pass1-part01','a'*64,'b'*64)

    def test_ownership_binds_actual_pids_job_phase_and_deadline(self):
        spec=importlib.util.spec_from_file_location('ordering_ownership_envelope_controls',HERE/'ownership.py')
        own=importlib.util.module_from_spec(spec);spec.loader.exec_module(own)
        value=dict(schemaVersion=1,phase='pass1-part01',executionLockSha256='a'*64,reviewSha256='b'*64,outerStartedMonotonic=10.0,actualOuterDeadlineMonotonic=190.0,parentPid=123,childPid=456,parentJobHandle=789,guardSha256=p.GUARD_SHA)
        def validate(v):return own.validate(v,phase='pass1-part01',execution='a'*64,review='b'*64,guard_sha=p.GUARD_SHA,parent_pid=123,child_pid=456,now=11)
        self.assertEqual(190.0,validate(value))
        for key,v in [('parentPid',999),('childPid',True),('parentJobHandle',0),('phase','pass2-part01'),('actualOuterDeadlineMonotonic',9999),('outerStartedMonotonic',12),('guardSha256','c'*64),('executionLockSha256','d'*64),('reviewSha256','e'*64)]:
            bad=dict(value);bad[key]=v
            with self.subTest(key=key),self.assertRaises(ValueError):validate(bad)

    def test_baseline_jar_module_and_no_source_class_leak(self):
        spec=importlib.util.spec_from_file_location('ordering_jar_controls',HERE/'jar_inputs.py')
        jar=importlib.util.module_from_spec(spec);spec.loader.exec_module(jar)
        result=jar.verify_jar(p.BASE_JAR,p.BASE_JAR_SHA,HERE/'java');self.assertEqual('org.dotj.build.evaluation.candidate',result['module']['name'])
        with self.assertRaises(ValueError):jar.verify_jar(p.BASE_JAR,'0'*64,HERE/'java')
        for raw in [b'',b'not a class',b'\xca\xfe\xba\xbe']:
            with self.subTest(raw=raw),self.assertRaises(ValueError):jar.module_descriptor(raw)


if __name__=='__main__': unittest.main(verbosity=2)
