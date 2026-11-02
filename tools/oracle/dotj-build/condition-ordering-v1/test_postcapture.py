"""Fix2 pure retained-byte regression controls; no process/runtime launch."""
import copy
import importlib.util
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parent
def load(name,file):
    spec=importlib.util.spec_from_file_location(name,file);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
p=load('postcapture_test_protocol',HERE/'protocol.py')
binding=load('postcapture_test_binding',HERE/'runtime_binding.py') if (HERE/'runtime_binding.py').exists() else None
predecessor=load('postcapture_test_predecessor',HERE/'finalize_first_capture.py') if (HERE/'finalize_first_capture.py').exists() else None

def inputs():
    proposal=p.read(HERE/'execution-proposal.json');plan=proposal['invocations'][0]
    out=Path(plan['output']);parent=p.read(p.A/'controllers/pass1-part01/parent-receipt.json');child=p.read(out/'receipt.json')
    coord=p.read(p.B/'orchestration/two-frameworks/batch2518-first-native-coordination-v1.json')
    approval=p.read(plan['reviewPath']);value=p.read(out/'native.stdout');raw=(out/'native.stderr').read_bytes()
    return parent,child,coord,approval,plan,value,raw

class PostcaptureControls(unittest.TestCase):
    def test_old_literal_assertion_really_rejects_all_three_retained_paths(self):
        *_,value,raw=inputs();text=raw.decode('utf-8')
        for key in ['corePath','msbuildPath','frameworkPath']:
            with self.subTest(key=key):self.assertNotIn(value[key].casefold(),text.casefold())

    def test_corroborated_binding_accepts_actual_trace_and_exact_observer_modules(self):
        self.assertIsNotNone(binding,'new faithful binding verifier required')
        *_,value,raw=inputs();proof=binding.verify(value,raw)
        self.assertEqual(3,len(proof['moduleBindings']))
        self.assertTrue(all(x['absoluteAssemblyPathLiterallyPrinted'] is False for x in proof['moduleBindings']))

    def test_wrong_module_runtime_and_path_are_rejected(self):
        self.assertIsNotNone(binding,'new faithful binding verifier required')
        *_,value,raw=inputs()
        for key in ['runtime','corePath','msbuildPath','frameworkPath','msbuildAssembly']:
            bad=copy.deepcopy(value);bad[key]='wrong'
            with self.subTest(key=key),self.assertRaises(ValueError):binding.verify(bad,raw)

    def test_missing_or_contradictory_trace_context_is_rejected(self):
        self.assertIsNotNone(binding,'new faithful binding verifier required')
        *_,value,raw=inputs();text=raw.decode('utf-8')
        for fragment in ['Loaded library from '+str(p.B/'toolchains/dotnet/shared/Microsoft.NETCore.App/10.0.12/coreclr.dll'),
                         'Processing TPA for deps entry [Microsoft.Build, 18.9.11, lib/net10.0/Microsoft.Build.dll, local_path: <not_set>] with fx level: 0',
                         'Processing TPA for deps entry [Microsoft.Build.Framework, 18.9.11, lib/net10.0/Microsoft.Build.Framework.dll, local_path: <not_set>] with fx level: 0',
                         'Processing TPA for deps entry [Microsoft.NETCore.App.Runtime.win-x64, 10.0.12, System.Private.CoreLib.dll, local_path: <not_set>] with fx level: 1',
                         'Deps file: '+str(p.B/'toolchains/dotnet/sdk/10.0.401/MSBuild.deps.json')]:
            self.assertIn(fragment,text)
            with self.subTest(fragment=fragment),self.assertRaises(ValueError):binding.verify(value,text.replace(fragment,'REMOVED').encode())
        for extra in ['Loaded library from C:\\wrong\\coreclr.dll','Deps file: C:\\wrong\\MSBuild.deps.json','Processing TPA for deps entry [Microsoft.Build, 0.0, lib/net10.0/Microsoft.Build.dll, local_path: <not_set>] with fx level: 0']:
            with self.subTest(extra=extra),self.assertRaises(ValueError):binding.verify(value,(text+'\n'+extra+'\n').encode())

    def test_wrong_closed_binary_hash_is_rejected(self):
        self.assertIsNotNone(binding,'new faithful binding verifier required')
        *_,value,raw=inputs();contract=p.read(HERE/'runtime-binding-contract.json')
        bad=copy.deepcopy(contract);bad['binaryPins'][0]['sha256']='0'*64
        with self.assertRaises(ValueError):binding.verify(value,raw,bad)

    def test_exact_metadata_failure_documents_are_accepted_without_changing_exits(self):
        self.assertIsNotNone(predecessor,'closed pure finalizer required')
        parent,child,coord,approval,plan,value,raw=inputs()
        result=predecessor.validate_documents(parent,child,coord,approval,plan,value,raw)
        self.assertEqual({'SUCCESS':56,'PROJECT_ERROR':16},result['outcomeCounts'])
        self.assertEqual(1,parent['process']['exitCode']);self.assertEqual(0,child['process']['exitCode'])

    def test_arbitrary_failed_parent_or_changed_authority_is_rejected(self):
        self.assertIsNotNone(predecessor,'closed pure finalizer required')
        base=inputs()
        mutations=[(0,lambda x:x.update(failure={'type':'ValueError','message':'arbitrary failure'})),
                   (1,lambda x:x.update(failure={'type':'ValueError','message':'arbitrary failure'})),
                   (0,lambda x:x.update(phase='pass1-part02')),
                   (1,lambda x:x.update(executionLockSha256='0'*64)),
                   (3,lambda x:x.update(executionLockSha256='0'*64)),
                   (2,lambda x:x.update(approvalSha256='0'*64))]
        for index,mutate in mutations:
            args=copy.deepcopy(base);mutate(args[index])
            with self.subTest(index=index),self.assertRaises(ValueError):predecessor.validate_documents(*args)

    def test_missing_bounds_job_deadline_cleanup_or_count_proof_is_rejected(self):
        self.assertIsNotNone(predecessor,'closed pure finalizer required')
        base=inputs()
        mutations=[(0,lambda x:x['process'].update(timedOut=True)),(0,lambda x:x['process'].update(jobAssigned=False)),
                   (0,lambda x:x['process'].update(cleanupError='failure')),(1,lambda x:x['process'].update(exitCode=1)),
                   (1,lambda x:x['process'].update(outputLimitExceeded=True)),(1,lambda x:x['process'].update(timeoutSeconds=31)),
                   (1,lambda x:x['ownershipProof'].update(duplicatedJobHandleClosed=False)),
                   (1,lambda x:x.update(actualOuterDeadlineMonotonic=x['actualOuterDeadlineMonotonic']+1)),
                   (1,lambda x:x.update(nativeExecutions={'state':'KNOWN','value':0})),
                   (1,lambda x:x.update(nativeExecutions={'state':'UNKNOWN','value':None})),
                   (1,lambda x:x.update(nativeExecutions={'state':'KNOWN','value':True})),
                   (0,lambda x:x.update(controllerExecutions={'state':'KNOWN','value':0}))]
        for index,mutate in mutations:
            args=copy.deepcopy(base);mutate(args[index])
            with self.subTest(index=index),self.assertRaises(ValueError):predecessor.validate_documents(*args)

    def test_bad_rows_progress_or_receipt_raw_binding_is_rejected(self):
        self.assertIsNotNone(predecessor,'closed pure finalizer required')
        base=inputs()
        mutations=[(5,lambda x:x['rows'].pop()),(5,lambda x:x['rows'][0].update(id='OTHER')),
                   (1,lambda x:x.update(progress=[])),(1,lambda x:x['raw']['stdout'].update(sha256='0'*64)),
                   (0,lambda x:x['raw'].pop('stderr')),(1,lambda x:x['process']['outputSizesBytes'].update(stdout=0))]
        for index,mutate in mutations:
            args=copy.deepcopy(base);mutate(args[index])
            with self.subTest(index=index),self.assertRaises(ValueError):predecessor.validate_documents(*args)

    def test_predecessor_adapter_requires_independent_finalization_review(self):
        self.assertIsNotNone(predecessor,'closed pure finalizer required')
        with self.assertRaises(ValueError):predecessor.approved_finalization('0'*64,'0'*64)

    def test_all_capture_inputs_and_original_freezer_are_still_exact_snapshot_bytes(self):
        snapshot=p.read(p.A/'postcapture-fix2-snapshot-v1/archive-lock.json')
        for entry in snapshot['profileEntries']:
            relative=entry['repositoryRelativePath']
            if '/fixtures/' in relative or '/partitions/' in relative or relative.endswith(('/manifest.json','/freeze_contract.py','/dispatch-witnesses.json','/protocol.py')):
                with self.subTest(path=relative):p.pin(entry['original'])
        for entry in snapshot['actualCaptureEntries']:
            with self.subTest(raw=entry['original']['path']):p.pin(entry['original']);p.pin(entry['archived'])

    def test_retained_phase_is_excluded_from_every_future_producer_launch(self):
        proposal=p.read(HERE/'execution-proposal.json')
        self.assertEqual(7,len(proposal['remainingProducerPhases']))
        self.assertNotIn('pass1-part01',proposal['remainingProducerPhases'])
        self.assertEqual(0,proposal['remainingApprovedNativeInvocations'])

    def test_segmented_plan_covers_both_locks_and_every_required_assertion(self):
        segmented=load('segmented_plan_controls',HERE/'segmented_closure.py')
        plan=segmented.build_plan(p.sha(HERE/'execution-lock.json'))
        self.assertEqual('35ef28faf73f6dd31596867f724c37ec5050163ad47ac18775ab362f6901897e',plan['predecessorExecutionLockSha256'])
        ids=[i for stage in plan['stages'] if stage['kind']=='DESCRIPTORS' for i in stage['descriptorIds']]
        segmented.validate_descriptor_coverage(plan,ids)
        self.assertGreaterEqual(plan['uniqueDescriptorCount'],7711)
        self.assertGreater(plan['requiredDescriptorReferences'],plan['uniqueDescriptorCount'])
        self.assertTrue(all(len(s['descriptorIds'])<=128 for s in plan['stages'] if s['kind']=='DESCRIPTORS'))
        self.assertEqual({'SCALAR_SCHEMA','ARCHIVE_RELATIONS','BINARY_REUSE','CURRENT_FIXTURES','ARCHIVED_FIXTURES','CAPTURE_SEMANTICS','FINAL_INVENTORY'},{s['kind'] for s in plan['stages'] if s['kind']!='DESCRIPTORS'})

    def test_segmented_coverage_rejects_missing_duplicate_reordered_or_false_zero(self):
        segmented=load('segmented_coverage_controls',HERE/'segmented_closure.py')
        segmented.validate_descriptor_coverage({'uniqueDescriptorCount':3},[0,1,2])
        for ids in [[0,2],[0,1,1,2],[1,0,2],[False,1,2],[]]:
            with self.subTest(ids=ids),self.assertRaises(ValueError):segmented.validate_descriptor_coverage({'uniqueDescriptorCount':3},ids)
        with self.assertRaises(ValueError):segmented.validate_descriptor_coverage({'uniqueDescriptorCount':True},[0])

if __name__=='__main__':unittest.main(verbosity=2)
