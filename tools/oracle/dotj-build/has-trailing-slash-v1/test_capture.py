"""Deterministic static and mock controls. No native/compiler/JVM subprocess."""
import copy, json, os, tempfile, unittest, xml.etree.ElementTree as ET
from pathlib import Path
import capture as c
import verify as v
import packaged as p

def mock_payload():
    # Synthetic strings are type controls, never expected native observations.
    result={k:'MOCK_TYPE_CONTROL' for k in ['runtime','msbuildAssembly','msbuildPath','frameworkPath','corePath']}
    result.update(profile='Default',rows=[])
    for item in c.read(c.C/'manifest.json')['cases']:
        result['rows'].append({'id':item['id'],'globals':item['globals'],'profile':'Default','evaluation':{'success':True,'properties':{'P':'MOCK_ONLY','Q':''},'imports':[],'duplicateImports':None,'duplicateGetterFailure':{'type':'MOCK','message':'MOCK'}},'diagnostics':[],'cleanup':{'before':0,'loaded':1,'afterUnload':0,'disposed':True},'taskMarkerAbsent':True})
    return result
class StaticControls(unittest.TestCase):
    def test_01_corpus_exact_rows_and_classifications(self):
        rows=c.read(c.C/'case-classifications.json')['cases'];self.assertEqual(len(rows),38)
        self.assertEqual(sum(r['category']=='semantic' for r in rows),32);self.assertEqual(sum(r['category']=='boundary' for r in rows),6)
        self.assertEqual(len({r['id'] for r in rows}),38)
        self.assertTrue(all(r['nativeExpected']=='UNOBSERVED' for r in rows))
    def test_02_every_fixture_xml_parses_and_is_bounded(self):
        count=0
        for case in c.read(c.C/'manifest.json')['cases']:
            files=list((c.C/'fixtures'/case['id']).rglob('*'));self.assertLessEqual(sum(p.is_file() for p in files),16)
            for path in files:
                if path.is_file():self.assertLessEqual(path.stat().st_size,65536)
                if path.suffix in ['.proj','.props']:ET.parse(path);count+=1
        self.assertEqual(count,47)
    def test_03_four_condition_sites_and_inert_targets(self):
        sites=set()
        for path in (c.C/'fixtures').rglob('*'):
            if path.suffix in ['.props','.proj']:
                for node in ET.parse(path).iter():
                    if 'Condition' in node.attrib:sites.add(node.tag)
        self.assertTrue({'PropertyGroup','P','Q','Import','ImportGroup'}.issubset(sites))
        text=(c.C/'fixtures/HT18-inert-targets/main.proj').read_text()
        self.assertIn('InitialTargets="Never"',text);self.assertIn('must-not-exist.txt',text)
    def test_04_cache_order_same_raw_fresh_values(self):
        cases=c.read(c.C/'manifest.json')['cases'][13:16]
        xml=[(c.C/'fixtures'/x['id']/'main.proj').read_bytes() for x in cases]
        self.assertEqual(xml[0],xml[1]);self.assertEqual(xml[1],xml[2])
        self.assertEqual([x['globals']['Shared'] for x in cases],['first/','second','third\\'])
    def test_05_schema_mock_valid(self):self.assertIs(c.schema_validate(mock_payload(),c.read(c.HERE/'observation-schema.json'))['rows'][0]['taskMarkerAbsent'],True)
    def test_06_schema_rejects_missing_extra_types_order(self):
        mutations=[lambda x:x.pop('runtime'),lambda x:x.update(extra=0),lambda x:x['rows'].reverse(),lambda x:x['rows'][0]['cleanup'].update(before=False),lambda x:x['rows'][0]['evaluation']['properties'].update(P=1),lambda x:x['rows'][0].update(taskMarkerAbsent=False),lambda x:x['rows'][0]['globals'].update(Injected='x'),lambda x:x['rows'][0]['evaluation'].update(success=1)]
        for mutation in mutations:
            data=mock_payload();mutation(data)
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):c.schema_validate(data,c.read(c.HERE/'observation-schema.json'))
    def test_07_full_failure_and_event_payload_preserved(self):
        data=mock_payload();data['rows'][0]['evaluation']={'success':False,'type':'MOCK_EXCEPTION','code':'MOCK_CODE','file':'D:\\fixture\\main.proj','line':2,'column':3,'endLine':4,'endColumn':5,'message':'MOCK_FULL_MESSAGE','hresult':-123}
        data['rows'][0]['diagnostics']=[{'kind':'error','code':None,'file':None,'line':1,'column':2,'endLine':3,'endColumn':4,'message':'MOCK_FULL_EVENT'}]
        self.assertEqual(c.schema_validate(data,c.read(c.HERE/'observation-schema.json')),data)
    def test_08_duplicate_json_keys_rejected(self):
        with self.assertRaises(ValueError):json.loads('{"a":1,"a":2}',object_pairs_hook=c.unique_pairs)
    def test_09_pair_preserves_properties_globals_order_and_messages(self):
        data=mock_payload();root=r'D:\owned\fixtures'
        data['rows'][0]['evaluation']['properties']['P']=root
        data['rows'][0]['diagnostics']=[{'kind':'warning','code':'C','file':root+r'\main.proj','line':1,'column':2,'endLine':3,'endColumn':4,'message':'full '+root+r'\main.proj suffix'}]
        normalized=v.normalize(data,root)
        self.assertEqual(normalized['rows'][0]['evaluation']['properties']['P'],root)
        self.assertEqual(normalized['rows'][0]['diagnostics'][0]['message'],'full <OWNED_FIXTURE_ROOT>\\main.proj suffix')
        self.assertEqual(data['rows'][0]['diagnostics'][0]['file'],root+r'\main.proj')
    def test_10_bounded_parser_retains_oversize_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'oversize';path.write_bytes(b'x'*100)
            with self.assertRaises(ValueError):c.bounded(path,99)
            self.assertEqual(path.stat().st_size,100)
    def test_11_environment_whitelist_D_paths_and_limits(self):
        env=c.environment(c.B/'validation/MOCK_ONLY')
        self.assertFalse(any(k in env for k in ['JAVA_TOOL_OPTIONS','CLASSPATH','PYTHONPATH','COMPLUS_Version']))
        self.assertEqual(env['DOTNET_GCHeapHardLimit'],'8000000');self.assertEqual(env['DOTNET_PROCESSOR_COUNT'],'2')
        for key in ['TEMP','TMP','HOME','USERPROFILE','APPDATA','LOCALAPPDATA','NUGET_PACKAGES']:self.assertTrue(env[key].startswith('D:'))
        self.assertEqual(env['DOTNET_ROLL_FORWARD'],'Disable')
    def test_12_output_confinement(self):
        with self.assertRaises(ValueError):c.confined('C:/temp/new')
        with self.assertRaises(ValueError):c.confined(c.B)
    def test_13_jar_only_command_no_source_fallback(self):
        commands=p.commands(c.B/'validation/MOCK_ONLY',p.BASELINE,Path('MOCK-BRIDGE'),'red')
        compiler=commands[0]['argv'];runtime=commands[1]['argv']
        self.assertIn('-implicit:none',compiler);self.assertIn('-sourcepath',compiler)
        self.assertNotIn('ProjectEvaluationComponent.java',' '.join(compiler))
        self.assertEqual(sum(x.endswith('.java') for x in compiler),1)
        self.assertIn('--patch-module',runtime);self.assertIn('--limit-modules',runtime)
        self.assertEqual(commands[0]['allowedOutputClasses'],['org/dotj/internal/build/evaluation/HasTrailingSlashPackagedTest.class'])
    def test_14_baseline_and_current_source_identity(self):
        self.assertEqual(c.sha(p.BASELINE),p.BASELINE_SHA)
        source=c.W/'dotj-build/evaluation-candidate/src/org/dotj/internal/build/evaluation/ProjectEvaluationComponent.java'
        self.assertEqual(c.sha(source),'713ab126bc156137dcd6ff87109cfbc4417101bc67beccb36b9c25ab8e4ae08e')
    def test_15_boundary_bridge_never_implies_native_parity(self):
        payload=mock_payload();receipt={'payload':payload,'fixtureRoot':str(c.B/'MOCK_ONLY')}
        text=p.bridge(receipt)
        self.assertEqual(text.count('CASE\t'),38);self.assertEqual(text.count('PRIVATE_NATIVE_PARSE_BOUNDARY'),4);self.assertEqual(text.count('PRIVATE_DECLARED_BOUNDARY'),2)
        self.assertNotIn('MOCK_EXCEPTION',text)
    def test_16_no_guess_on_unexpected_semantic_diagnostics(self):
        payload=mock_payload();payload['rows'][0]['diagnostics']=[{'kind':'warning','code':'OTHER','message':'MOCK'}]
        with self.assertRaises(ValueError):p.bridge({'payload':payload,'fixtureRoot':'MOCK'})
    def test_17_native_flags_and_guard_source_pin(self):
        self.assertEqual(c.sha(c.GUARD),c.GUARD_SHA)
        self.assertEqual(c.sha(c.OBSERVER),'146c884247995aefe942836456be66f8fc65067eb5c10c34da1a5c9729402277')
        self.assertEqual(c.sha(c.GUARD.with_name('run-comparison.py')),'82fe3fbfbcafcabb18912ff752eea4457b3b4608a41c695d0341b6465657701c')
    def test_18_resource_floors_typed(self):
        guard=c.owned();good={'freePhysicalBytes':512*1024**2,'freeVirtualBytes':16*1024**3}
        self.assertTrue(guard.resource_ready(good))
        for bad in [{},dict(good,freePhysicalBytes=True),dict(good,freeVirtualBytes=16*1024**3-1),dict(good,freePhysicalBytes=512*1024**2-1)]:self.assertFalse(guard.resource_ready(bad))
    def test_19_resource_immediate_revalidation_no_launch(self):
        class Guard:
            def wait_resources(self,deadline):return 0,[{'MOCK':'ready'}]
            def memory(self):return {'freePhysicalBytes':0,'freeVirtualBytes':0}
            def resource_ready(self,sample):return False
        with self.assertRaises(ValueError):c.resource_check(Guard(),float('inf'),[])
    def test_20_guard_mock_owned_success_and_raw_files(self):
        guard=c.owned();events=[]
        class Job:
            def assign(self,p):events.append('assign')
            def resume(self,p):events.append('resume')
            def empty(self):return True
            def close(self):events.append('close')
        class Process:
            pid=123;returncode=0
            def poll(self):return 0
            def wait(self,timeout):return 0
        def launch(argv,**kw):kw['stdout'].write(b'MOCK_RAW_STDOUT');kw['stderr'].write(b'MOCK_RAW_STDERR');return Process()
        with tempfile.TemporaryDirectory() as directory:
            result=guard.run(['MOCK_NOT_EXECUTED'],directory,{},'native',30,launch=launch,job_factory=Job)
            c.successful(result);self.assertEqual(events,['assign','resume','close'])
            self.assertEqual(Path(result['stdoutPath']).read_bytes(),b'MOCK_RAW_STDOUT')
    def test_21_guard_mock_overflow_retains_overshoot(self):
        guard=c.owned()
        class Job:
            def assign(self,p):pass
            def resume(self,p):pass
            def empty(self):return True
            def close(self):pass
        class Process:
            pid=123;returncode=0
            def poll(self):return 0
            def wait(self,timeout):return 0
        def launch(argv,**kw):kw['stdout'].write(b'OVERSHOOT');kw['stdout'].flush();return Process()
        with tempfile.TemporaryDirectory() as directory:
            result=guard.run(['MOCK_NOT_EXECUTED'],directory,{},'native',30,launch=launch,job_factory=Job,stream_limits={'stdout':2,'stderr':2})
            self.assertTrue(result['outputLimitExceeded']);self.assertEqual(Path(result['stdoutPath']).read_bytes(),b'OVERSHOOT')
            with self.assertRaises(ValueError):c.successful(result)
    def test_22_fixture_copy_tamper_detected(self):
        import shutil
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'fixtures';shutil.copytree(c.C/'fixtures',root);c.verify_fixture_copy(root)
            (root/'HT01-literal-separators/main.proj').write_text('tampered')
            with self.assertRaises(ValueError):c.verify_fixture_copy(root)
    def test_23_mock_pair_checks_raw_controller_and_payload(self):
        import shutil
        with tempfile.TemporaryDirectory() as directory:
            receipts=[]
            for index in range(2):
                root=Path(directory)/str(index);root.mkdir();fixtures=root/'fixtures';shutil.copytree(c.C/'fixtures',fixtures)
                payload=mock_payload();fp=c.read(c.C/'evidence/native-fingerprint.json')
                payload.update({k:fp[k] for k in ['runtime','msbuildAssembly']});payload.update(fp['resolvedAssemblies'])
                stdout=root/'native.stdout';stderr=root/'native.stderr';c.write(stdout,payload);stderr.write_bytes(b'')
                command={'launched':True,'exitCode':0,'timedOut':False,'processId':100+index}
                c.write(root/'native-process.json',command)
                c.write(root/'controller-receipt.json',{'process':command,'inputLockSha256':'MOCK_LOCK','checkpointSha256':'MOCK_CHECKPOINT'})
                receipt={'status':'CAPTURED_PENDING_ROOT_REVIEW','commands':[command],'observation':c.descriptor(stdout),'stderr':c.descriptor(stderr),'payload':payload,'fixtureRoot':str(fixtures),'fixtureInputs':c.verify_fixture_copy(fixtures),'retainedRaw':[c.descriptor(stdout),c.descriptor(stderr)],'inputLockSha256':'MOCK_LOCK','checkpointSha256':'MOCK_CHECKPOINT'}
                path=root/'receipt.json';c.write(path,receipt);receipts.append(path)
            result=v.compare(receipts[0],c.sha(receipts[0]),receipts[1],c.sha(receipts[1]));self.assertEqual(result['uniqueCases'],38)
            controller=receipts[1].parent/'controller-receipt.json';bad=c.read(controller);bad['process']['exitCode']=1;c.write(controller,bad)
            with self.assertRaises(ValueError):v.compare(receipts[0],c.sha(receipts[0]),receipts[1],c.sha(receipts[1]))
    def test_24_python_sources_parse_without_compilation(self):
        import ast
        for source in c.HERE.glob('*.py'):ast.parse(source.read_text(encoding='utf-8'),filename=str(source))
class ResourceCompositionControls(unittest.TestCase):
    def scenario(self,wait_seconds,query_seconds=0,below_floor=False):
        """Real reviewed guard, fake clock/process/job; no OS process launch."""
        from types import SimpleNamespace
        from unittest.mock import patch
        real=c.owned();clock=[0.0];events=[];samples=[]
        payload=mock_payload();fp=c.read(c.C/'evidence/native-fingerprint.json')
        payload.update({k:fp[k] for k in ['runtime','msbuildAssembly']});payload.update(fp['resolvedAssemblies'])
        class Job:
            def assign(self,process):events.append('assign')
            def resume(self,process):events.append('resume')
            def empty(self):return True
            def terminate(self):events.append('terminate');process.returncode=125
            def close(self):events.append('close')
        class Process:
            pid=987;returncode=None
            def poll(self):
                if self.returncode is None and clock[0]-self.started>=29:self.returncode=0
                return self.returncode
            def wait(self,timeout):
                if self.poll() is not None:return self.returncode
                clock[0]+=min(timeout,29-(clock[0]-self.started))
                if self.poll() is None:raise real.subprocess.TimeoutExpired(['MOCK_ONLY'],timeout)
                return self.returncode
        process=Process()
        def launch(argv,**kwargs):
            process.started=clock[0];events.append(('launch',clock[0]))
            kwargs['stdout'].write(json.dumps(payload).encode());kwargs['stdout'].flush();return process
        class Adapter:
            def wait_resources(self,deadline):
                events.append('wait');clock[0]+=wait_seconds
                sample={'freePhysicalBytes':512*1024**2,'freeVirtualBytes':16*1024**3};samples.append(sample)
                return clock[0],samples
            def memory(self):
                clock[0]+=query_seconds
                return {'freePhysicalBytes':0 if below_floor else 512*1024**2,'freeVirtualBytes':16*1024**3}
            def resource_ready(self,sample):return real.resource_ready(sample)
            def run(self,*args,**kwargs):
                events.append(('guard-start',clock[0]))
                return real.run(*args,**kwargs,launch=launch,job_factory=Job,now=lambda:clock[0])
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory)
            with patch.object(c.time,'monotonic',lambda:clock[0]),patch.object(c,'verify_pins',lambda args:None):
                try:c.run_native(SimpleNamespace(lock_sha256='MOCK_LOCK',checkpoint_sha256='MOCK_CHECKPOINT'),out,Adapter());error=None
                except ValueError as caught:error=caught
            receipt=c.read(out/'receipt.json')
        return receipt,events,error
    def test_delayed_readiness_keeps_full_native_budget(self):
        for wait in [0,5,31]:
            with self.subTest(waitSeconds=wait):
                receipt,events,error=self.scenario(wait)
                self.assertIsNone(error);self.assertEqual(receipt['status'],'CAPTURED_PENDING_ROOT_REVIEW')
                self.assertEqual(events[:2],['wait',('guard-start',wait)])
                self.assertEqual(receipt['commands'][0]['timeoutSeconds'],30)
                self.assertAlmostEqual(receipt['commands'][0]['seconds'],29)
                self.assertNotIn('terminate',events)
                self.assertEqual(len(receipt['resourceSamples']),2)
    def test_stale_prelaunch_query_rejects_before_launch(self):
        receipt,events,error=self.scenario(31,query_seconds=2.01)
        self.assertIsNotNone(error);self.assertFalse(receipt['commands'][0]['launched'])
        self.assertFalse(any(isinstance(event,tuple) and event[0]=='launch' for event in events))
    def test_below_floor_prelaunch_query_rejects_before_launch(self):
        receipt,events,error=self.scenario(31,below_floor=True)
        self.assertIsNotNone(error);self.assertFalse(receipt['commands'][0]['launched'])
        self.assertFalse(any(isinstance(event,tuple) and event[0]=='launch' for event in events))
if __name__=='__main__':unittest.main(verbosity=2)
