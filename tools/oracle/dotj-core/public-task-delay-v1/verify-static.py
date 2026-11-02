"""New pure static/contract negative controls. Never spawns real children.

SYNTHETIC fixtures are parser test inputs, not actual native captures or results.
"""
import ast
import base64
import contextlib
import copy
import io
import importlib.util
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import contract as c
import phase_tools as phase

A=c.B/'agents/batch2517-task-delay-native-preparation-v1'
ART=A/'static-control-fixtures'
ART.mkdir(exist_ok=True)
SCHEMA=c.read(c.HERE/'schema.json')
MANIFEST=c.read(c.HERE/'fixture-manifest.json')

def synthetic_rows(partition):
    result={}
    for case in MANIFEST['rows']:
        if case['partition']!=partition:continue
        row={k:False if t=='b' else 0 if t=='i' else '' for k,t in SCHEMA['fields'].items()}
        row['kind']='SYNTHETIC_PARSER_ONLY'
        result[case['id']]=row
    return result

def encode(rows):
    identity=SCHEMA['globalIdentity']
    lines=['META\t'+identity['profile']+'\t'+identity['runtime']+'\t'+identity['manifestSha256']]
    for cid,row in rows.items():
        lines.append('BEGIN\t'+cid)
        for key,value in row.items():
            kind=SCHEMA['fields'][key]
            value=('true' if value else 'false') if kind=='b' else str(value) if kind=='i' else base64.b64encode(value.encode()).decode()
            lines.append(cid+'.'+key+'\t'+kind+'\t'+value)
        lines.append('END\t'+cid)
    return ('\n'.join(lines)+'\n').encode()

class StaticControls(unittest.TestCase):
    def setUp(self):
        self.raw=encode(synthetic_rows('ordinary'))

    def badwire(self,raw):
        with self.assertRaises((ValueError,UnicodeError)):
            c.wire(raw,SCHEMA,MANIFEST,'ordinary')

    def test_valid_synthetic_wire_is_only_parser_input(self):
        parsed=c.wire(self.raw,SCHEMA,MANIFEST,'ordinary')
        self.assertEqual(parsed,synthetic_rows('ordinary'))
        with self.assertRaises(ValueError):c.invariants(parsed,MANIFEST)

    def test_unknown_key(self):self.badwire(self.raw.replace(b'.kind\t',b'.unknown\t',1))
    def test_bool_as_integer(self):self.badwire(self.raw.replace(b'.hresult\ti\t0',b'.hresult\ti\ttrue',1))
    def test_integer_overflow(self):self.badwire(self.raw.replace(b'.hresult\ti\t0',b'.hresult\ti\t2147483648',1))
    def test_integer_leading_zero(self):self.badwire(self.raw.replace(b'.hresult\ti\t0',b'.hresult\ti\t00',1))
    def test_integer_plus_sign(self):self.badwire(self.raw.replace(b'.hresult\ti\t0',b'.hresult\ti\t+0',1))
    def test_boolean_numeric(self):self.badwire(self.raw.replace(b'.completed\tb\tfalse',b'.completed\tb\t0',1))
    def test_wrong_type_tag(self):self.badwire(self.raw.replace(b'.hresult\ti\t',b'.hresult\tb\t',1))
    def test_duplicate_field(self):self.badwire(self.raw.replace(b'D001.message\t',b'D001.kind\t',1))
    def test_duplicate_case(self):self.badwire(self.raw+self.raw[self.raw.index(b'BEGIN'):])
    def test_missing_case(self):self.badwire(self.raw[:self.raw.rindex(b'BEGIN')])
    def test_missing_end(self):self.badwire(self.raw.replace(b'END\tD001\n',b'',1))
    def test_unknown_case_identity(self):self.badwire(self.raw.replace(b'BEGIN\tD001',b'BEGIN\tD999',1))
    def test_wrong_global_identity(self):self.badwire(self.raw.replace(b'10.0.12',b'10.0.11',1))
    def test_invalid_base64(self):self.badwire(self.raw.replace(b'.kind\ts\t',b'.kind\ts\t!',1))
    def test_embedded_nul(self):self.badwire(self.raw.replace(b'BEGIN',b'BE\0GIN',1))
    def test_invalid_utf8(self):self.badwire(self.raw.replace(b'BEGIN',b'BE\xffGIN',1))
    def test_nonfinal_newline(self):self.badwire(self.raw[:-1])
    def test_alternative_line_separator(self):self.badwire(self.raw.replace(b'BEGIN',b'BE\vGIN',1))
    def test_crlf_only_normalization(self):self.assertEqual(c.wire(self.raw.replace(b'\n',b'\r\n'),SCHEMA,MANIFEST,'ordinary'),synthetic_rows('ordinary'))
    def test_output_cap_remains_two_mib(self):self.badwire(b'x'*(2*1024**2+1))
    def test_json_duplicate_keys(self):
        with self.assertRaises(ValueError):json.loads('{"x":1,"x":2}',object_pairs_hook=c.unique_pairs)
    def test_manifest_duplicate_id(self):
        m=copy.deepcopy(MANIFEST);m['rows'][1]['id']=m['rows'][0]['id']
        with self.assertRaises(ValueError):c.validate_manifest(m)
    def test_manifest_bool_count(self):
        m=copy.deepcopy(MANIFEST);m['caseCount']=True
        with self.assertRaises(ValueError):c.validate_manifest(m)
    def test_manifest_tick_not_string(self):
        m=copy.deepcopy(MANIFEST);m['rows'][0]['value']=0
        with self.assertRaises(ValueError):c.validate_manifest(m)
    def test_manifest_noncanonical_tick(self):
        m=copy.deepcopy(MANIFEST);m['rows'][0]['value']='-0'
        with self.assertRaises(ValueError):c.validate_manifest(m)
    def test_parameter_identity(self):
        case=next(x for x in MANIFEST['rows'] if x['expectedKind']=='argument')
        row=synthetic_rows(case['partition'])[case['id']]
        row.update(kind='argument',exceptionType='System.ArgumentOutOfRangeException',paramName='WRONG',hresult=-2146233086,actualValueKind='null',message='SYNTHETIC')
        with self.assertRaises(ValueError):c.invariants({case['id']:row},MANIFEST)
    def test_unknown_exception_not_success(self):
        row=synthetic_rows('ordinary')['D006'];row['kind']='runtimeFault';row['exceptionType']='UnknownException'
        with self.assertRaises(ValueError):c.invariants({'D006':row},MANIFEST)
    def test_outpath_escape(self):
        with self.assertRaises(ValueError):c.confined('C:/temp/output')
    def test_outpath_root(self):
        with self.assertRaises(ValueError):c.confined(c.B)
    def test_no_overwrite(self):
        with self.assertRaises(ValueError):c.fresh_output(ART)
    def test_stale_hash(self):
        pin=c.descriptor(c.HERE/'schema.json');pin['sha256']='0'*64
        with self.assertRaises(ValueError):c.validate_pin(pin)
    def test_pin_bool_size(self):
        pin=c.descriptor(c.HERE/'schema.json');pin['sizeBytes']=True
        with self.assertRaises(ValueError):c.validate_pin(pin)
    def test_partial_failure_counted_one(self):self.assertEqual(c.count_attempt({'launched':True,'exitCode':-1,'cleanupError':'SYNTHETIC'}),1)
    def test_deferred_no_child_zero(self):self.assertEqual(c.count_attempt({'launched':False,'failure':'resources'}),0)
    def test_launch_flag_integer_rejected(self):
        with self.assertRaises(ValueError):c.count_attempt({'launched':1})
    def test_exit_code_bool_rejected(self):
        with self.assertRaises(ValueError):c.successful({'launched':True,'exitCode':False,'timedOut':False,'jobAssigned':True,'resumed':True})
    def test_cleanup_failure_rejected(self):
        with self.assertRaises(ValueError):c.successful({'launched':True,'exitCode':0,'timedOut':False,'jobAssigned':True,'resumed':True,'cleanupError':'SYNTHETIC'})
    def approval(self):
        return {'version':1,'status':'APPROVED_FOR_ONE_PHASE','phase':'source-compile','inputLockSha256':'a'*64,'commandSha256':'b'*64,'artifactBindingSha256':None,'reviewer':'root','reviewReceiptSha256':'c'*64,'parentTimeoutSeconds':180}
    def test_phase_approval_misbinding(self):
        with self.assertRaises(ValueError):c.validate_approval(self.approval(),'native-capture','a'*64,'b'*64,None)
    def test_artifact_approval_misbinding(self):
        with self.assertRaises(ValueError):c.validate_approval(self.approval(),'source-compile','a'*64,'b'*64,'d'*64)
    def test_command_approval_misbinding(self):
        with self.assertRaises(ValueError):c.validate_approval(self.approval(),'source-compile','a'*64,'e'*64,None)
    def test_approval_extra_field(self):
        a=self.approval();a['override']='native-capture'
        with self.assertRaises(ValueError):c.validate_approval(a,'source-compile','a'*64,'b'*64,None)
    def test_cli_no_selector_override(self):
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):phase.parser('source-compile').parse_args(['--input-lock','x','--input-lock-sha256','y','--mode','verify'])
    def test_cli_no_abbreviation(self):
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):phase.parser('native-capture').parse_args(['--input-l','x','--input-lock-sha256','y'])
    def test_input_manifest_cap_separate_from_output_cap(self):
        f=ART/'SYNTHETIC-large-input.json';f.write_text(json.dumps({'padding':'x'*(2*1024**2+1)}),encoding='utf-8')
        self.assertGreater(f.stat().st_size,2*1024**2);self.assertEqual(len(c.read(f)['padding']),2*1024**2+1)
        with self.assertRaises(ValueError):c.read(f,limit=2*1024**2)
    def test_payload_manifest_fits_explicit_input_cap(self):self.assertLess((c.HERE/'toolchain-payload-lock.json').stat().st_size,16*1024**2)
    def test_consumed_golden_forgery_rejected(self):
        # A fixture claiming a capture but lacking source/artifact provenance is not evidence.
        f=ART/'SYNTHETIC-forged-receipt.json'
        f.write_text(json.dumps({'phase':'native-capture','status':'CAPTURED_PENDING_ROOT_REVIEW','artifactBinding':c.descriptor(c.HERE/'schema.json')}),encoding='utf-8')
        with self.assertRaises((ValueError,KeyError)):c.consumed_capture(f,c.sha(f),SCHEMA,MANIFEST)
    def test_consumed_receipt_stale_hash_rejected(self):
        with self.assertRaises(ValueError):c.consumed_capture(c.HERE/'schema.json','0'*64,SCHEMA,MANIFEST)
    def test_source_expected_is_not_observed(self):
        self.assertEqual(MANIFEST['status'],'DESIGNED_NOT_OBSERVED')
        self.assertEqual(len(MANIFEST['rows'])*len(SCHEMA['fields']),SCHEMA['scalarCount'])
    def test_python_sources_parse(self):
        for f in c.HERE.glob('*.py'):ast.parse(f.read_text(encoding='utf-8-sig'),filename=str(f))
    def test_fixed_sibling_bootstrap(self):
        for f in c.HERE.glob('*.py'):
            if f.name in ['phase_tools.py','contract.py']:continue
            self.assertIn('sys.path.insert(0',f.read_text(encoding='utf-8-sig'),str(f))
    def test_no_product_classes_on_baseline_classpath(self):
        text=(c.HERE/'phase_tools.py').read_text()
        self.assertIn("'-implicit:none'",text);self.assertIn("'--module-path',lock['baselineJar']['path']",text)
        self.assertNotIn('src/main/java',text)
    def test_new_delay_admission_full_120_seconds_without_child(self):
        source=c.read(c.HERE/'source-input-lock.json')['ownedGuard']['path']
        spec=importlib.util.spec_from_file_location('SYNTHETIC_delay_resource_guard',source)
        guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
        clock=[0.0]
        def now():return clock[0]
        def sleep(seconds):clock[0]+=seconds
        with self.assertRaises(ValueError):
            guard.wait_resources(now()+160,query=lambda:{'freePhysicalBytes':0,'freeVirtualBytes':0},now=now,sleep=sleep)
        self.assertEqual(clock[0],120.0)
    def test_new_delay_stale_admission_sample_rejected_without_child(self):
        source=c.read(c.HERE/'source-input-lock.json')['ownedGuard']['path']
        spec=importlib.util.spec_from_file_location('SYNTHETIC_delay_stale_guard',source)
        guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
        clock=[0.0]
        def query():clock[0]+=2.01;return {'freePhysicalBytes':1024**3,'freeVirtualBytes':32*1024**3}
        with self.assertRaises(ValueError):guard.wait_resources(160,query=query,now=lambda:clock[0],sleep=lambda seconds:None)

class Fix1Controls(unittest.TestCase):
    """Only changed-source controls for I01-I03/R01-R02; all fixtures synthetic."""
    def race(self,canceled=False):
        row={k:False if kind=='b' else 0 if kind=='i' else '' for k,kind in SCHEMA['fields'].items()}
        row.update(kind='canceled' if canceled else 'success',status='Canceled' if canceled else 'RanToCompletion',completed=True,
            successful=not canceled,canceled=canceled,exceptionNull=True,tokenCanBeCanceled=True,tokenRequested=True,callbackCalls=1,winner='cancel' if canceled else 'timer')
        for prefix in ['await','repeat']:
            row[prefix+'Type']='System.Threading.Tasks.TaskCanceledException' if canceled else 'returned'
            row[prefix+'TaskIdentity']=canceled;row[prefix+'TokenEqual']=canceled
            row[prefix+'Message']='A task was canceled.' if canceled else '';row[prefix+'Hresult']=-2146233029 if canceled else 0
        return row
    def rejected(self,field,value,canceled=False):
        row=self.race(canceled);row[field]=value
        with self.assertRaises(ValueError):c.invariants({'D109':row},MANIFEST)
    def test_fix1_both_race_winners_valid(self):
        for canceled in [False,True]:c.invariants({'D109':self.race(canceled)},MANIFEST)
    def test_fix1_different_valid_winners_compare(self):c.compare({'D109':self.race(False)},{'D109':self.race(True)},MANIFEST)
    def test_fix1_pending_race_rejected(self):
        row=self.race();row.update(kind='pending',status='WaitingForActivation',completed=False,successful=False)
        with self.assertRaises(ValueError):c.invariants({'D109':row},MANIFEST)
    def test_fix1_unknown_race_kind_rejected(self):self.rejected('kind','unexpected')
    def test_fix1_wrong_winner_rejected(self):self.rejected('winner','cancel')
    def test_fix1_wrong_status_rejected(self):self.rejected('status','WaitingForActivation')
    def test_fix1_incomplete_flag_rejected(self):self.rejected('completed',False)
    def test_fix1_wrong_success_flag_rejected(self):self.rejected('successful',True,True)
    def test_fix1_wrong_cancel_flag_rejected(self):self.rejected('canceled',True)
    def test_fix1_fault_flag_rejected(self):self.rejected('faulted',True)
    def test_fix1_wrong_success_await_rejected(self):self.rejected('awaitType','System.Threading.Tasks.TaskCanceledException')
    def test_fix1_missing_repeat_task_identity_rejected(self):self.rejected('repeatTaskIdentity',False,True)
    def test_fix1_missing_repeat_token_identity_rejected(self):self.rejected('repeatTokenEqual',False,True)
    def test_fix1_success_with_cancel_error_payload_rejected(self):self.rejected('awaitMessage','A task was canceled.')
    def test_fix1_wrong_tce_hresult_rejected(self):self.rejected('repeatHresult',0,True)
    def test_fix1_bool_tce_hresult_rejected(self):self.rejected('repeatHresult',True,True)
    def test_fix1_wrong_tce_message_rejected(self):self.rejected('awaitMessage','forged',True)
    def test_fix1_top_level_error_payload_rejected(self):self.rejected('exceptionType','System.Exception')
    def test_fix1_unrelated_stable_field_mutation_rejected(self):
        one=self.race();two=self.race(True);two['shape']='SYNTHETIC_FORGERY'
        with self.assertRaises(ValueError):c.compare({'D109':one},{'D109':two},MANIFEST)
    def test_fix1_stable_field_comparison_not_whole_row_skip(self):
        self.assertEqual(set(SCHEMA['fields'])-c.RACE_VARYING_FIELDS,set(SCHEMA['raceComparison']['stableFields']))
        self.assertEqual(c.RACE_VARYING_FIELDS,set(SCHEMA['raceComparison']['allowedVaryingFields']))
        # A schema-extension stable field must still compare even when core outcomes are valid.
        one=self.race();two=self.race(True);one['syntheticStableExtension']='a';two['syntheticStableExtension']='b'
        with self.assertRaises(ValueError):c.compare({'D109':one},{'D109':two},MANIFEST)
    def test_fix1_added_large_no_token_inputs(self):
        expected=[('DelayInt','2147483647'),('DelaySpan','21474836480000'),('DelaySpan','42949672940000'),('DelaySpan','42949672949999')]
        rows=MANIFEST['rows'][109:]
        self.assertEqual([(r['api'],r['value']) for r in rows],expected)
        self.assertTrue(all(r['token']=='none' and r['expectedKind']=='pending' for r in rows))
        self.assertTrue(any(r['api']=='DelaySpan' and r['value']=='42949672950000' and r['expectedKind']=='argument' for r in MANIFEST['rows']))
    def test_fix1_original109_ids_preserved(self):
        old=c.read(A/'history/fix1-before/profile/fixture-manifest.json')
        self.assertEqual(MANIFEST['rows'][:109],old['rows'])
    def test_fix1_large_vectors_do_not_await_multiday_duration(self):
        source=(c.HERE/'PublicTaskDelayOracle.cs').read_text()
        self.assertIn('milliseconds >= 0 && milliseconds <= 10',source)
        self.assertIn('"DelaySpan" => Task.Delay(new TimeSpan(value))',source)
        self.assertIn('"DelayInt" => Task.Delay(checked((int)value))',source)
    def test_fix1_exact_long_wrapper_controls(self):
        design=c.read(c.HERE/'private-control-design.json');self.assertEqual(design['controlCount'],30)
        for control,number in zip(design['controls'][26:],[2147483647,2147483648,4294967294,4294967294]):
            text=json.dumps(control)
            self.assertIn('long '+str(number),text);self.assertIn('original carrier unchanged',text)
            self.assertIn('No cancellation registration',text);self.assertIn('finite schedule',text)
    def check_shared(self,source):
        body=source.split('private static void Shared(',1)[1].split('private static void Dispatch(',1)[0]
        self.assertIn('one.GetAwaiter().OnCompleted(() => { Interlocked.Increment(ref firstCalls); firstCompleted.Set(); });',body)
        self.assertIn('two.GetAwaiter().UnsafeOnCompleted(() => { Interlocked.Increment(ref secondCalls); secondCompleted.Set(); });',body)
        self.assertLess(body.index('secondCompleted.Set();'),body.index('source.CancelAsync()'))
        self.assertIn('firstCalls == 1 && secondCalls == 1',body)
        self.assertIn('row["callbackCalls"] = firstCalls + secondCalls;',body)
        self.assertNotIn('row["callbackCalls"] = 2;',body)
        self.assertIn('Wait(firstCompleted',body);self.assertIn('Wait(secondCompleted',body);self.assertIn('finally',body)
    def test_fix1_shared_observation_source_control(self):self.check_shared((c.HERE/'PublicTaskDelayOracle.cs').read_text())
    def test_fix1_shared_control_rejects_archived_literal_observation(self):
        with self.assertRaises(AssertionError):self.check_shared((A/'history/fix1-before/profile/PublicTaskDelayOracle.cs').read_text())
    def context(self):
        import root_phase as root
        return {'version':1,'phase':'source-compile','outerDirectory':str(ART/'SYNTHETIC-outer'),'phaseDirectory':str(ART/'SYNTHETIC-inner'),
            'inputLockSha256':'a'*64,'descriptorSha256':'b'*64,'approvalSha256':'c'*64,'assessmentSha256':'d'*64,'artifactBindingSha256':None,
            'startedMonotonic':100.0,'deadlineMonotonic':280.0,'timeoutSeconds':180,'rootLauncher':{},'outerImplementation':{},'ownerProcessId':123}
    def validate_context(self,value,now=110.0):
        import root_phase as root
        root.context_check(value,'source-compile','a'*64,'b'*64,'c'*64,ART/'SYNTHETIC-inner',now)
    def test_fix1_valid_outer_context(self):self.validate_context(self.context())
    def test_fix1_wrong_outer_phase(self):
        value=self.context();value['phase']='native-capture'
        with self.assertRaises(ValueError):self.validate_context(value)
    def test_fix1_wrong_outer_approval_binding(self):
        value=self.context();value['approvalSha256']='e'*64
        with self.assertRaises(ValueError):self.validate_context(value)
    def test_fix1_unknown_outer_selector(self):
        value=self.context();value['verifyOnly']=True
        with self.assertRaises(ValueError):self.validate_context(value)
    def test_fix1_expired_outer_deadline(self):
        with self.assertRaises(ValueError):self.validate_context(self.context(),280.0)
    def test_fix1_fresh_inner_clock_cannot_reset_outer_budget(self):
        import root_phase as root
        with self.assertRaises(ValueError):root.reserve(280.0,250.0,30)
    def test_fix1_child_and_cleanup_fit_exact_deadline(self):
        import root_phase as root
        root.reserve(280.0,155.0,120)
        with self.assertRaises(ValueError):root.reserve(280.0,155.001,120)
    def test_fix1_closure_overhead_consumes_outer_budget(self):
        import root_phase as root
        root.reserve(280.0,110.0,120)
        with self.assertRaises(ValueError):root.reserve(280.0,160.0,120)
    def test_fix1_direct_inner_parser_requires_outer_context(self):
        argv=['--input-lock','a','--input-lock-sha256','b','--descriptor','c','--descriptor-sha256','d','--approval','e','--approval-sha256','f']
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):phase.execution_parser('source-compile').parse_args(argv)
    def test_fix1_inner_parser_rejects_selector_override(self):
        argv=['--input-lock','a','--input-lock-sha256','b','--descriptor','c','--descriptor-sha256','d','--approval','e','--approval-sha256','f','--outer-context','g','--outer-context-sha256','h','--mode','verify']
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):phase.execution_parser('source-compile').parse_args(argv)
    def test_fix1_timeout_without_inner_proof_unknown(self):
        import root_phase as root
        self.assertIsNone(root.workload_count(None,'a'*64))
        self.assertIsNone(root.workload_count({'outerContext':{'sha256':'a'*64},'actualLaunches':0,'status':'PREPARING'},'a'*64))
    def test_fix1_final_deferred_zero_evidence(self):
        import root_phase as root
        self.assertEqual(root.workload_count({'outerContext':{'sha256':'a'*64},'actualLaunches':0,'finalized':True,'status':'DEFERRED_NO_CHILD'},'a'*64),0)
    def test_fix1_partial_actual_child_count_one(self):
        import root_phase as root
        self.assertEqual(root.workload_count({'outerContext':{'sha256':'a'*64},'actualLaunches':1,'finalized':False},'a'*64),1)
    def test_fix1_counter_bool_or_wrong_context_unknown(self):
        import root_phase as root
        self.assertIsNone(root.workload_count({'outerContext':{'sha256':'a'*64},'actualLaunches':True},'a'*64))
        self.assertIsNone(root.workload_count({'outerContext':{'sha256':'b'*64},'actualLaunches':1},'a'*64))
    def closure_fixture(self):
        root=ART/'SYNTHETIC-fix1-payload';root.mkdir(exist_ok=True)
        for f in root.iterdir():
            if f.is_file():f.unlink()
        f=root/'python._pth';f.write_text('SYNTHETIC\n');data={'payloads':{'synthetic':{'root':str(root),'files':[c.descriptor(f)]}}}
        payload=ART/'SYNTHETIC-fix1-payload.json';payload.write_text(json.dumps(data))
        archive=ART/'SYNTHETIC-fix1-archive.json';archive.write_text(json.dumps({'entries':[]}))
        source=ART/'SYNTHETIC-fix1-sources.json';source.write_text(json.dumps({'sources':[],'licenses':[],'historicalArchive':c.descriptor(archive)}))
        return {'payload':c.descriptor(payload),'sourceInputs':c.descriptor(source)},root
    def test_fix1_full_payload_positive(self):
        lock,root=self.closure_fixture();self.assertEqual(phase.check_full_payload(lock),{'synthetic':1})
    def test_fix1_full_payload_byte_tamper(self):
        lock,root=self.closure_fixture();(root/'python._pth').write_text('FORGED\n')
        with self.assertRaises(ValueError):phase.check_full_payload(lock)
    def test_fix1_full_payload_extra_inventory(self):
        lock,root=self.closure_fixture();(root/'unexpected.dll').write_text('SYNTHETIC')
        with self.assertRaises(ValueError):phase.check_full_payload(lock)
    def test_fix1_full_payload_missing_inventory(self):
        lock,root=self.closure_fixture();(root/'python._pth').unlink()
        with self.assertRaises(ValueError):phase.check_full_payload(lock)
    def test_fix1_inner_only_receipt_not_outer_proof(self):
        import root_phase as root
        f=ART/'SYNTHETIC-fix1-inner-only.json';f.write_text(json.dumps({'phase':'native-capture','status':'CAPTURED_PENDING_ROOT_REVIEW'}))
        with self.assertRaises(ValueError):root.consume_root(f,c.sha(f),'native-capture')
    def test_fix1_full_payload_before_admission_source_order(self):
        source=(c.HERE/'phase_tools.py').read_text().split('def execute(phase):',1)[1].split('def verify_capture',1)[0]
        self.assertLess(source.index('check_full_payload(lock)'),source.index('guard.wait_resources'))
        self.assertLess(source.index('guard.wait_resources'),source.index('guard.run('))
        self.assertIn("reserve(outer_context['deadlineMonotonic']",source)
    def test_fix1_root_watchdog_source(self):
        source=(c.HERE/'root_phase.py').read_text();self.assertIn("guard.run(argv,out,env,'controller',180",source)
        self.assertIn("'deadlineMonotonic':started+180",source)
        for phase_name in ['source-compile','baseline-compile','baseline-red','native-capture']:
            self.assertIn('root_phase.run("'+phase_name+'")',(c.HERE/('root-'+phase_name+'.py')).read_text())
    def test_fix1_changed_python_sources_parse(self):
        for name in ['contract.py','phase_tools.py','root_phase.py','verify-static.py']:
            ast.parse((c.HERE/name).read_text(),filename=name)
    def test_fix1_bootstrap_and_json_document_caps(self):
        import root_phase as root
        path=ART/'SYNTHETIC-fix1-bootstrap.json';path.write_bytes(b'{"padding":"123456789"}')
        self.assertEqual(root.bootstrap_pin(path),c.descriptor(path))
        with self.assertRaises(ValueError):root.bootstrap_pin(path,limit=8)
        with self.assertRaises(ValueError):c.read(path,limit=8)

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Fix1Controls)
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    evidence={'classification':'NEW_PURE_PYTHON_STATIC_CONTROLS_ONLY','testsRun':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
        'realChildren':0,'nativeObservations':0,'compilers':0,'javaRuns':0,'oldControlsRerun':0,'raw':stream.getvalue()}
    evidence['scope']='Fix1 I01-I03/R01-R02 focused controls only; original54 controls not rerun.'
    (A/'fix1-static-controls-result-v1.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
    (A/'fix1-static-controls-raw-v1.txt').write_text(stream.getvalue(),encoding='utf-8')
    print(stream.getvalue());sys.exit(0 if result.wasSuccessful() else 1)
