"""PURE controls. No compiler, JVM, native observer, or Windows ownership proof."""
import copy
import importlib.util
import json
import math
import os
from pathlib import Path
import tempfile
import struct
import sys
import zipfile
import contextlib
import io
sys.path.insert(0,str(Path(__file__).resolve().parent))
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('jdk_contract', HERE / 'jdk_contract.py')
c = None
if (HERE / 'jdk_contract.py').exists():
    c = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c)


class Preparation(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(c, 'separate JDK contract implementation is required')

    def test_admission_reserves_entire_child_cleanup_post_and_metadata(self):
        sample = {'freePhysicalBytes': 536870912, 'freeVirtualBytes': 17179869184}
        c.admission(900, 415, 414, 414.5, sample)
        for now in [415.001, float('nan'), float('inf'), True]:
            with self.subTest(now=now), self.assertRaises(ValueError):
                c.admission(900, now, 414, 414.5, sample)
        for bad in [{'freePhysicalBytes': 536870911, 'freeVirtualBytes': 17179869184},
                    {'freePhysicalBytes': 536870912, 'freeVirtualBytes': 17179869183}]:
            with self.assertRaises(ValueError): c.admission(900, 100, 99, 99.5, bad)
        with self.assertRaises(ValueError): c.admission(900, 100, 97.9, 99.5, sample)
        self.assertEqual(c.wait_cutoff(900, 400), 415)
        self.assertEqual(c.wait_cutoff(900, 100), 220)

    def test_policy_rejects_override_boolean_and_extra_fields(self):
        c.validate_policy(c.POLICY)
        for key, value in [('controllerSeconds', 1200), ('childSeconds', True), ('cleanupSeconds', 6)]:
            p = copy.deepcopy(c.POLICY); p[key] = value
            with self.assertRaises(ValueError): c.validate_policy(p)
        p = copy.deepcopy(c.POLICY); p['callerDeadline'] = 900
        with self.assertRaises(ValueError): c.validate_policy(p)

    def test_exact_compile_and_runtime_tokens_and_consistent_home(self):
        compile_plan = c.operation('baseline-compile')
        argv = compile_plan['argv']; index = argv.index('--release')
        self.assertEqual(argv[index:index+2], ['--release', '21'])
        self.assertIn('-implicit:none', argv)
        self.assertEqual(argv[argv.index('-encoding')+1], 'UTF-8')
        e = compile_plan['environment']
        self.assertEqual(e['HOME'], e['USERPROFILE'])
        self.assertEqual(e['HOMEDRIVE'] + e['HOMEPATH'], e['HOME'])
        c.validate_operation(compile_plan)
        bad = copy.deepcopy(compile_plan); bad['environment']['HOMEPATH'] = '\\old\\home'
        with self.assertRaises(ValueError): c.validate_operation(bad)
        bad = copy.deepcopy(compile_plan); bad['argv'].append('extra.java')
        with self.assertRaises(ValueError): c.validate_operation(bad)
        runtime = c.operation('baseline-runtime')
        self.assertEqual(runtime['argv'][runtime['argv'].index('--limit-modules')+1],
                         'java.base,java.xml,org.dotj.build.evaluation.candidate')
        self.assertEqual(runtime['argv'][-1], '8a788c21b54c120c089c3ec9fcc863505a6ab7f9bbf138adc8a7372a63436698')
        with self.assertRaises(ValueError): c.operation('arbitrary')

    def test_envelope_actual_identity_deadline_and_one_use(self):
        e = dict(schemaVersion=1, operation='baseline-compile', attemptId='baseline-compile-attempt01',
                 sourceLockSha256='a'*64, reviewSha256='b'*64, policySha256='c'*64,
                 guardSha256=c.GUARD_SHA, outerStartedMonotonic=10, actualOuterDeadlineMonotonic=910,
                 parentPid=123, childPid=456, parentJobHandle=789)
        args = dict(operation='baseline-compile', source='a'*64, review='b'*64, policy='c'*64,
                    parent_pid=123, child_pid=456, now=20)
        self.assertEqual(c.validate_envelope(e, **args), 910)
        for key, value in [('parentPid', 999), ('childPid', 123), ('parentJobHandle', True),
                           ('actualOuterDeadlineMonotonic', 1810), ('outerStartedMonotonic', float('nan')),
                           ('operation', 'baseline-runtime')]:
            b = dict(e); b[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError): c.validate_envelope(b, **args)
        use = c.OneUse(); use.take()
        with self.assertRaises(ValueError): use.take()
        for handle in [0, -1, True, None]:
            with self.assertRaises(ValueError): c.capability_handle(handle)

    def test_descriptor_inventory_tamper_duplicate_and_reparse(self):
        with tempfile.TemporaryDirectory(dir=c.TEST_ROOT) as folder:
            root = Path(folder); f = root/'one'; f.write_bytes(b'original')
            d = c.descriptor(f); c.verify_inventory(root, [d])
            with self.assertRaises(ValueError): c.verify_inventory(root, [d, d])
            (root/'extra').write_bytes(b'extra')
            with self.assertRaises(ValueError): c.verify_inventory(root, [d])
            (root/'extra').unlink(); f.write_bytes(b'tampered')
            with self.assertRaises(ValueError): c.pin(d)
            with self.assertRaises(ValueError): c.regular_attributes(0x400, False)
            with self.assertRaises(ValueError): c.regular_attributes(0, True)

    def test_historical_resolution_requires_exact_unique_authorized_relation(self):
        original = dict(path='D:/original/source', sha256='1'*64, sizeBytes=3)
        archived = dict(path='D:/archive/source', sha256='1'*64, sizeBytes=3)
        entries = [dict(original=original, archived=archived, relation='EXACT_RAW')]
        self.assertEqual(c.resolve_historical(original, entries), archived)
        with self.assertRaises(ValueError): c.resolve_historical(original, entries+entries)
        changed = dict(original); changed['sha256'] = '2'*64
        with self.assertRaises(ValueError): c.resolve_historical(changed, entries)
        changed = copy.deepcopy(entries); changed[0]['archived']['sizeBytes'] = 4
        with self.assertRaises(ValueError): c.resolve_historical(original, changed)

    def test_output_inventory_rejects_shadow_extra_and_missing(self):
        with tempfile.TemporaryDirectory(dir=c.TEST_ROOT) as folder:
            root = Path(folder)
            with self.assertRaises(ValueError): c.class_output(root)
            file = root/c.CLASS_RELATIVE; file.parent.mkdir(parents=True)
            def class_bytes(name):
                raw=name.encode('ascii')
                return b'\xca\xfe\xba\xbe'+struct.pack('>HHH',0,65,3)+b'\x01'+struct.pack('>H',len(raw))+raw+b'\x07\x00\x01'+struct.pack('>HHH',0x21,2,0)+b'\x00'*8
            # Synthetic classfile FORMAT CONTROL ONLY; never an actual producer output/fit artifact.
            raw=class_bytes('org/dotj/internal/build/evaluation/OrderingBaselineTest');file.write_bytes(raw)
            d = c.class_output(root); self.assertEqual(d['sizeBytes'], len(raw))
            file.write_bytes(class_bytes('org/dotj/internal/build/evaluation/ProjectEvaluationComponent'))
            with self.assertRaises(ValueError):c.class_output(root)
            file.write_bytes(raw)
            extra = file.with_name('ProjectEvaluationComponent.class'); extra.write_bytes(b'forged')
            with self.assertRaises(ValueError): c.class_output(root)

    def test_runtime_refuses_unresolved_or_unlinked_compile_output(self):
        for value in [None, {}, {'status':'COMPILE_COMPLETE'}, {'output': {'sha256':'0'*64}}]:
            with self.assertRaises(ValueError): c.validate_compile_link(value, 'a'*64, verify_files=False)

    def test_red_requires_real_product_failure_checkpoints_and_complete_postclosure(self):
        stdout = ('BASELINE_ORIGIN '+str(c.BASE_JAR)+' '+c.BASE_JAR_SHA+' classes=20\n'
                  'ORDERING_BASELINE_BEGIN ORD-HISTORY-BOOL-BOUND-ordering\n')
        stderr = ('Exception in thread "main" org.dotj.internal.build.evaluation.ProjectEvaluationComponent$ProfileRejected: Trailing condition syntax outside selected profile\n'
                  '\tat org.dotj.build.evaluation.candidate/org.dotj.internal.build.evaluation.ProjectEvaluationComponent$State$ConditionParser.parse(ProjectEvaluationComponent.java:419)\n'
                  '\tat org.dotj.build.evaluation.candidate/org.dotj.internal.build.evaluation.ProjectEvaluationComponent.evaluate(ProjectEvaluationComponent.java:104)\n'
                  '\tat org.dotj.build.evaluation.candidate/org.dotj.internal.build.evaluation.OrderingBaselineTest.main(OrderingBaselineTest.java:60)\n')
        self.assertEqual(c.classify_red(stdout, stderr, 1, True), 'GENUINE_BASELINE_PRODUCT_RED')
        for out, err, code, post in [(stdout,stderr,0,True),(stdout,stderr,125,True),
            (stdout,stderr,1,False),(stdout,stderr+'java.lang.OutOfMemoryError\n',1,True),
            (stdout+'ORDERING_BASELINE_END ORD-HISTORY-BOOL-BOUND-ordering\n',stderr,1,True),
            ('',stderr,1,True),(stdout,'arbitrary failure',1,True),
            (stdout,stderr.replace('ConditionParser.parse','ConditionParser.other'),1,True),
            (stdout,stderr.replace('ProjectEvaluationComponent.evaluate','Other.evaluate'),1,True)]:
            with self.subTest(code=code,post=post), self.assertRaises(ValueError): c.classify_red(out,err,code,post)

    def test_fit_rejects_shortened_or_over_budget_closure(self):
        c.validate_fit_times(295, 299, 595)
        for values in [(296,1,297),(1,301,302),(295,300,596),(1,1,1),(float('nan'),1,2)]:
            with self.assertRaises(ValueError): c.validate_fit_times(*values)

    def test_actual_baseline_module_bytes_reject_wrong_module_identity(self):
        import jdk_jar
        self.assertTrue(callable(getattr(jdk_jar,'verify_module',None)), 'module identity validation required')
        with zipfile.ZipFile(c.BASE_JAR) as jar:raw=jar.read('module-info.class')
        self.assertEqual(jdk_jar.verify_module(raw)['requires'],['java.base','java.xml'])
        with self.assertRaises(ValueError):jdk_jar.verify_module(raw.replace(b'org.dotj.build.evaluation.candidate',b'org.dotj.build.evaluation.incorrect'))
        with self.assertRaises(ValueError):jdk_jar.verify_module(raw[:-3])

    def test_old_boolean_red_raw_cannot_be_mislabeled_ordering_red(self):
        root=c.B/'validation/Batch-2516-baseline-red-v1'
        with self.assertRaises(ValueError):
            c.classify_red((root/'run-java-red.stdout').read_text(),(root/'run-java-red.stderr').read_text(),1,True)

    def test_actual_retained_native_data_and_baseline_provenance(self):
        import jdk_stage
        self.assertTrue((HERE/'stage-inputs.json').exists(), 'complete concrete stage graph required')
        ctx=jdk_stage.HistoricalContext(c.read(HERE/'stage-inputs.json'))
        evidence=jdk_stage.native_contract(ctx)
        self.assertEqual(evidence['rowsPerPass'],308)
        self.assertFalse(evidence['transitiveInputsTraversed'])
        self.assertFalse(evidence['freshNativeQualification'])
        self.assertEqual(jdk_stage.archive_relations(ctx)['archivedOriginals'],9)
        self.assertEqual(jdk_stage.baseline_provenance(ctx)['jarSha256'],'97b027c56221716cc748aa03a80d24d65a180e13fb0deb07b059c2bbdd290b1c')
        forged=copy.deepcopy(ctx.graph);forged['auditReferences']['nativeProofs'][0]['parent']['sha256']='0'*64
        with self.assertRaises(ValueError):jdk_stage.native_contract(jdk_stage.HistoricalContext(forged))

    def test_inner_bypass_and_free_timeout_rejected_before_any_launch(self):
        import jdk_runner
        original=sys.argv
        try:
            fixed=['jdk_runner.py','--operation=baseline-compile','--source-lock-sha256='+'a'*64,
                   '--review-sha256='+'b'*64,'--bootstrap-sha256='+'c'*64]
            sys.argv=fixed+['--inner']
            with self.assertRaises(ValueError):jdk_runner.main()
            sys.argv=fixed+['--timeout=1']
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:jdk_runner.main()
            self.assertEqual(raised.exception.code,2)
        finally:sys.argv=original

    def test_bootstrap_never_assigns_reserved_powershell_home_variables(self):
        # Explicit root-requested static guard: PowerShell parser accepts this
        # syntax, but the case-insensitive read-only HOME assignment fails later.
        import re
        self.assertIsNone(re.search(r'(?im)\$(?:home|codex_home)\s*=',(HERE/'jdk_bootstrap.ps1').read_text()))

    def test_outer_deadline_reserves_cleanup_and_finalization_and_rejects_overrun(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        import jdk_runner as runner
        # Exercise the actual outer call wiring, without starting any process.
        for scenario in ['stalled', 'exhausted', 'overrun', 'write-overrun', 'success']:
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory(dir=c.TEST_ROOT) as folder:
                root=Path(folder)/'operation'; clock=[100.0]; calls=[]; receipts={}
                envelope={'fake':'PURE_CONTROL'}
                cap=SimpleNamespace(handle=123,record=envelope,launch=object(),job_factory=object(),close=lambda:None)
                def capability(*args):
                    if scenario=='exhausted':clock[0]=994.0
                    return cap
                def run(argv,cwd,env,label,timeout,**kwargs):
                    calls.append((timeout,kwargs))
                    if scenario=='stalled':clock[0]+=timeout+5
                    elif scenario=='overrun':clock[0]=1000.01
                    else:clock[0]=110.0
                    return dict(launched=True,jobAssigned=True,resumed=True,exitCode=-1 if scenario=='stalled' else 0,
                                timedOut=scenario=='stalled',outputLimitExceeded=False,error=None,cleanupError=None,cleanupSeconds=5)
                def save(path,value):
                    receipts[Path(path).name]=copy.deepcopy(value)
                    if scenario=='write-overrun':clock[0]=1000.02
                args=SimpleNamespace(operation='baseline-compile',source_lock_sha256='a'*64,review_sha256='b'*64,bootstrap_sha256='c'*64)
                child=dict(failure=None,status='COMPILE_COMPLETE_PENDING_ROOT_REVIEW',sourceLockSha256='a'*64,ownershipEnvelope=envelope)
                with contextlib.ExitStack() as stack:
                    for target,value in [('approval',lambda *a:({},{})),('bootstrap',lambda *a:{}),
                                         ('guard_module',lambda:SimpleNamespace(run=run))]:stack.enter_context(patch.object(runner,target,value))
                    stack.enter_context(patch.object(runner.time,'monotonic',lambda:clock[0]))
                    stack.enter_context(patch.object(runner.ownership,'LaunchCapability',capability))
                    for target,value in [('operation',lambda op:dict(cwd=str(root),attemptId='pure',operation=op)),
                                         ('sha',lambda p:'a'*64),('environment',lambda p:{}),('descriptor',lambda p:{}),
                                         ('read',lambda p:child),('fresh_json',save)]:stack.enter_context(patch.object(runner.c,target,value))
                    code=runner.outer(args)
                self.assertEqual(code,0 if scenario=='success' else 1)
                self.assertEqual(len(calls),0 if scenario=='exhausted' else 1)
                if calls:
                    self.assertEqual(calls[0][0],894.0)
                    self.assertIs(calls[0][1]['launch'],cap.launch)
                    self.assertIs(calls[0][1]['job_factory'],cap.job_factory)
                receipt=receipts['receipt.json']
                self.assertEqual(receipt['actualOuterDeadlineMonotonic'],1000.0)
                if scenario=='stalled':
                    self.assertTrue(receipt['process']['timedOut'])
                    self.assertEqual(receipt['seconds'],899.0)
                if scenario in ['overrun','exhausted']:self.assertIsNotNone(receipt['failure'])
                if scenario=='write-overrun':
                    self.assertGreater(receipts['deadline-failure.json']['seconds'],900)
                    self.assertIsNotNone(receipts['deadline-failure.json']['failure'])

    def test_review_never_approves_unknown_output_or_unbounded_operation(self):
        self.assertTrue((HERE/'jdk-controller-policy-v1.json').exists(),'concrete policy required')
        value=dict(schemaVersion=1,independentReviewer='PURE_SCHEMA_CONTROL_NOT_AN_APPROVAL',
                   operation='baseline-compile',attemptId='baseline-compile-attempt01',sourceLockSha256='a'*64,
                   policySha256=c.sha(HERE/'jdk-controller-policy-v1.json'),guardSha256=c.GUARD_SHA,
                   jdkInvocationApproved=True,invocationCountApproved=1,
                   fitEvidence=dict(path=str(c.TEST_ROOT/'input-fit-fix1/timing.json'),sha256='b'*64,sizeBytes=1),
                   compilerProof=None,compilerControllerProof=None,compiledOutput=None)
        # Schema-only controls never write reviews, stage outputs, or actual fit proofs.
        c.validate_review(value,'baseline-compile','a'*64,verify_files=False)
        for key,v in [('invocationCountApproved',True),('sourceLockSha256','d'*64),('compiledOutput',{'sha256':'f'*64})]:
            bad=copy.deepcopy(value);bad[key]=v
            with self.assertRaises(ValueError):c.validate_review(bad,'baseline-compile','a'*64,verify_files=False)
        bad=copy.deepcopy(value);bad['argv']=['arbitrary']
        with self.assertRaises(ValueError):c.validate_review(bad,'baseline-compile','a'*64,verify_files=False)
        bad=copy.deepcopy(value);bad.update(operation='baseline-runtime',attemptId='baseline-runtime-attempt01')
        with self.assertRaises(ValueError):c.validate_review(bad,'baseline-runtime','a'*64,verify_files=False)


if __name__ == '__main__':
    unittest.main(verbosity=2)
