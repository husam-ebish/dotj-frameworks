"""The negative cases catch silent metadata loss and false representation claims."""
import copy
import json
import unittest
import tempfile
import shutil
import subprocess
import sys
from pathlib import Path
import verify

class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.ledger = json.loads((verify.EVIDENCE/'selected-lifecycle-representation-v1.json').read_text())

    def test_complete_retained_inventory(self):
        self.assertEqual(verify.validate_ledger(self.ledger), {'callables':47,'properties':2,'identities':24})

    def test_missing_extra_duplicate_and_case_mutation_are_refused(self):
        for mutation in ['missing','extra','duplicate','case','visibility','parameter']:
            with self.subTest(mutation=mutation):
                ledger=copy.deepcopy(self.ledger)
                if mutation=='missing': ledger['callables'].pop()
                if mutation=='extra':
                    row=copy.deepcopy(ledger['callables'][0]);row['metadata']['metadataToken']+=1;ledger['callables'].append(row)
                if mutation=='duplicate': ledger['callables'].append(copy.deepcopy(ledger['callables'][0]))
                if mutation=='case': ledger['callables'][0]['metadata']['declaringType']='microsoft.Build.Evaluation.Project'
                if mutation=='visibility': ledger['callables'][0]['metadata']['public']=True
                if mutation=='parameter': ledger['callables'][0]['metadata']['parameters'][0]['optional']=True
                with self.assertRaisesRegex(ValueError,'retained inventory'):
                    verify.validate_ledger(ledger)

    def test_unapproved_jdk_substitution_is_refused(self):
        self.ledger['identities'][21]['representation']={'status':'EXACT','java':'java.lang.String','gaps':[]}
        with self.assertRaisesRegex(ValueError,'representation'):
            verify.validate_ledger(self.ledger)

    def test_broken_evidence_link_is_refused(self):
        self.ledger['callables'][0]['evidence'][0]['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'evidence'):
            verify.validate_ledger(self.ledger)

    def test_separate_accessor_property_and_identity_records_cannot_disappear(self):
        for category in ['callables','properties','identities']:
            with self.subTest(category=category):
                d=copy.deepcopy(self.ledger);d[category].pop()
                with self.assertRaisesRegex(ValueError,'retained inventory'): verify.validate_ledger(d)

    def test_forged_module_identity_is_refused(self):
        self.ledger['callables'][0]['moduleVersionId']='00000000-0000-0000-0000-000000000000'
        with self.assertRaisesRegex(ValueError,'module identity'): verify.validate_ledger(self.ledger)

class OutputTests(unittest.TestCase):
    def setUp(self):
        self.scenario={'id':'LCB_TEST','actions':[{'id':'same','cleanup':False,'valueKind':'bool'},
                       {'id':'dispose','cleanup':True,'valueKind':'null'}]}
        self.data={'schemaVersion':1,'id':'LCB_TEST','runtime':'.NET 10.0.12',
                   'msbuildPath':'p','frameworkPath':'q','corePath':'r','actions':[
                       {'id':'same','cleanup':False,'success':True,'value':True},
                       {'id':'dispose','cleanup':True,'success':True,'value':None}]}

    def test_type_strict_success_and_explicit_null(self):
        self.assertEqual(verify.validate_payload(self.data,self.scenario),self.data)
        for mutation in ['boolInt','absent','extra','order','duplicate']:
            with self.subTest(mutation=mutation):
                d=copy.deepcopy(self.data)
                if mutation=='boolInt': d['actions'][0]['value']=1
                if mutation=='absent': del d['actions'][1]['value']
                if mutation=='extra': d['actions'][0]['undeclared']=None
                if mutation=='order': d['actions'].reverse()
                if mutation=='duplicate': d['actions'].append(d['actions'][0])
                with self.assertRaisesRegex(ValueError,'output schema'): verify.validate_payload(d,self.scenario)

    def test_hresult_bool_is_not_int(self):
        d=copy.deepcopy(self.data)
        d['actions'][0]={'id':'same','cleanup':False,'success':False,
            'exception':{'type':'Synthetic.TestException','hresult':True,'message':'unit fixture only','diagnostic':None}}
        with self.assertRaisesRegex(ValueError,'output schema'): verify.validate_payload(d,self.scenario)

    def test_non_object_actions_use_the_schema_refusal_error(self):
        for action in ['not-an-object',None,[],7,1.5,True]:
            with self.subTest(action=action):
                data=copy.deepcopy(self.data);data['actions'][0]=action
                try:verify.validate_payload(data,self.scenario)
                except Exception as error:
                    self.assertIsInstance(error,ValueError)
                    self.assertIn('output schema action must be an object',str(error))
                else:self.fail('Non-object action must be refused')

    def test_stdout_binding_rejects_forged_duplicate_parsed_observation(self):
        with tempfile.TemporaryDirectory(dir=verify.ROOT/'validation/task19-static') as folder:
            base=Path(folder); stdout=base/'native.stdout';stderr=base/'native.stderr'
            stdout.write_text(json.dumps(self.data));stderr.write_bytes(b'')
            record={'schemaVersion':1,'status':'PASS_NATIVE_LIFECYCLE_PASS','fixtureRoot':str(base/'fixtures'),
                    'commands':[{'label':'LCB_TEST','exitCode':0,'stdout':{'path':str(stdout),'sha256':verify.sha(stdout)},
                                 'stderr':{'path':str(stderr),'sha256':verify.sha(stderr)},'parsed':copy.deepcopy(self.data)}]}
            record['commands'][0]['parsed']['actions'][0]['value']=False
            path=base/'report.json';path.write_text(json.dumps(record))
            with self.assertRaisesRegex(ValueError,'raw stdout binding'): verify.bind_capture(path)

class CliAndFixtureTests(unittest.TestCase):
    def test_cli_non_object_actions_retain_refusal_without_traceback(self):
        storage=verify.ROOT/'validation/task19-fix1';storage.mkdir(exist_ok=True)
        original=verify.ROOT/'validation/task19-native-v3-pass1'
        for action in ['not-an-object',None,[]]:
            with self.subTest(action=action):
                case=Path(tempfile.mkdtemp(prefix='malformed-action-',dir=storage));root=case/'capture'
                shutil.copytree(original,root);report=verify.read(root/'capture.json')
                def relocate(value,key=None):
                    if key=='parsed':return value
                    if type(value) is str:return value.replace(str(original),str(root))
                    if type(value) is list:return [relocate(v) for v in value]
                    if type(value) is dict:return {k:relocate(v,k) for k,v in value.items()}
                    return value
                report=relocate(report);command=next(c for c in report['commands'] if c['label']=='LCB01')
                command['parsed']['actions'][0]=action;raw=Path(command['stdout']['path'])
                raw.write_text(json.dumps(command['parsed']));command['stdout']['sha256']=verify.sha(raw)
                (root/'capture.json').write_text(json.dumps(report))
                argv=[sys.executable,'-B',str(verify.HERE/'verify.py'),'--capture',str(root/'capture.json'),
                    '--capture',str(verify.ROOT/'validation/task19-native-v3-pass2/capture.json'),
                    '--ledger',str(verify.EVIDENCE/'selected-lifecycle-representation-v1.json'),
                    '--observation-lock',str(verify.EVIDENCE/'lifecycle-behavior-observations-v1.json'),
                    '--observation-lock-sha256','a36da26c1af46d663e551905d48dccde378ccf476de4b164f99dc8468ec139a3',
                    '--out',str(case/'result')]
                process=subprocess.run(argv,capture_output=True);(case/'stdout').write_bytes(process.stdout);(case/'stderr').write_bytes(process.stderr)
                result=case/'result/verification.json';proof={'argv':argv,'exitCode':process.returncode,'verificationRecordExists':result.exists(),'mutation':action,'compilerNativeJvmLaunched':False}
                if result.exists():proof['result']=verify.read(result)
                (case/'proof.json').write_text(json.dumps(proof,indent=2)+'\n');print('Malformed-action CLI evidence: '+str(case),flush=True)
                self.assertEqual(process.returncode,1)
                self.assertTrue(result.is_file(),'Schema refusal must retain verification.json')
                self.assertEqual(proof['result']['status'],'REFUSED')
                self.assertIn('output schema action must be an object',proof['result']['error'])
                self.assertNotIn(b'Traceback',process.stderr)

    def test_compiler_profile_pins_the_observed_xml_overload_dependency(self):
        # Actual CS0012 showed that resolving the retained string/XmlReader overload group consumes this ref.
        lock=verify.read(verify.EVIDENCE/'lifecycle-behavior-input-lock-v1.json')
        xml='toolchains/dotnet/packs/Microsoft.NETCore.App.Ref/10.0.12/ref/net10.0/System.Xml.ReaderWriter.dll'
        self.assertIn(xml,lock['compilerReferences'])
        self.assertEqual({Path(p).name for p in lock['compilerReferences']}, {
            'System.Runtime.dll','System.Console.dll','System.Collections.dll','System.Linq.dll',
            'System.Text.Json.dll','System.Runtime.InteropServices.dll','System.Memory.dll',
            'System.IO.FileSystem.dll','System.Runtime.Extensions.dll','System.Xml.ReaderWriter.dll',
            'Microsoft.Build.dll','Microsoft.Build.Framework.dll'})
        self.assertEqual(len(lock['inputs']),30,'The diagnosed XML reference and pinned reviewed Python helper are the only added inputs')
        helper=[p for p in lock['inputs'] if p['base']=='repo' and p['path']=='dotj-build/evaluation-candidate/verify.py']
        self.assertEqual(helper,[{'base':'repo','path':'dotj-build/evaluation-candidate/verify.py',
            'sha256':'06f2801799fce596a4154080d5f44b69fde82c19871103ed4af26f74261c0dce'}])
        pins=[p for p in lock['inputs'] if p['base']=='root' and p['path']==xml]
        self.assertEqual(pins,[{'base':'root','path':xml,
            'sha256':'942964d32f72ba10288593f212e3a52c4811b65ca4d5f1a3979c92d2d526aa4c'}])

    def test_capture_entrypoint_loads_adjacent_checker_with_embedded_python(self):
        process=subprocess.run([sys.executable,'-B',str(verify.HERE/'capture.py'),'--help'],capture_output=True)
        self.assertEqual(process.returncode,0,process.stderr.decode())
        self.assertIn(b'--out',process.stdout)

    def test_verify_entrypoint_help_needs_no_global_pythonpath(self):
        process=subprocess.run([sys.executable,'-B',str(verify.HERE/'verify.py'),'--help'],capture_output=True)
        self.assertEqual(process.returncode,0,process.stderr.decode())
        self.assertIn(b'--observation-lock-sha256',process.stdout)

    def test_cli_refuses_fake_exact_representation(self):
        with tempfile.TemporaryDirectory(dir=verify.ROOT/'validation/task19-static') as folder:
            base=Path(folder)
            ledger=verify.read(verify.EVIDENCE/'selected-lifecycle-representation-v1.json')
            ledger['identities'][21]['representation']={'status':'EXACT','java':'java.lang.String','gaps':[]}
            source=base/'ledger.json';source.write_text(json.dumps(ledger))
            process=subprocess.run([sys.executable,'-B',str(verify.HERE/'verify.py'),'--static','--ledger',str(source),'--out',str(base/'result')],capture_output=True)
            self.assertNotEqual(process.returncode,0,'CLI must refuse unsupported-as-exact')
            result=verify.read(base/'result/verification.json')
            self.assertEqual(result['status'],'REFUSED')
            self.assertIn('representation',result['error'])

    def test_cli_copied_inputs_baseline_and_input_lock_forgery(self):
        # A private checkout copy exercises the real CLI; immutable production inputs remain untouched.
        for mutation in ['baseline','inputLock','fixtureAndManifest','plan']:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory(dir=verify.ROOT/'validation/task19-static') as folder:
                base=Path(folder);repo=base/'repo'
                lock=verify.read(verify.EVIDENCE/'lifecycle-behavior-input-lock-v1.json')
                paths=[x['path'] for x in lock['inputs'] if x['base']=='repo']+[
                    'tools/oracle/dotj-build/lifecycle-behavior-v1/verify.py',
                    'planning/stage-2/repos/dotj-build/evidence/lifecycle-behavior-input-lock-v1.json',
                    'planning/stage-2/repos/dotj-build/evidence/selected-lifecycle-representation-v1.json']
                for relative in paths:
                    target=repo/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(verify.REPO/relative,target)
                evidence=repo/'planning/stage-2/repos/dotj-build/evidence'
                if mutation=='inputLock':
                    path=evidence/'lifecycle-behavior-input-lock-v1.json';d=verify.read(path);d['inputs'].pop();path.write_text(json.dumps(d))
                if mutation=='plan': (evidence/'lifecycle-behavior-plan-v1.json').write_text('{}')
                if mutation=='fixtureAndManifest':
                    fixtures=repo/'tools/oracle/dotj-build/lifecycle-behavior-v1/fixtures'
                    (fixtures/'valid.proj').write_text('<Project/>');m=verify.read(fixtures/'manifest-v1.json')
                    m['fixtures'][0]['sha256']=verify.sha(fixtures/'valid.proj');(fixtures/'manifest-v1.json').write_text(json.dumps(m))
                process=subprocess.run([sys.executable,'-B',str(repo/'tools/oracle/dotj-build/lifecycle-behavior-v1/verify.py'),
                    '--static','--ledger',str(evidence/'selected-lifecycle-representation-v1.json'),'--out',str(base/'result')],capture_output=True)
                result=verify.read(base/'result/verification.json')
                if mutation=='baseline':
                    self.assertEqual(process.returncode,0,process.stderr.decode());self.assertEqual(result['status'],'PASS_STATIC_ONLY')
                else:
                    self.assertNotEqual(process.returncode,0);self.assertEqual(result['status'],'REFUSED')
                    self.assertIn('input',result['error'])

    def test_fixture_content_and_missing_file_are_bound_to_trusted_manifest(self):
        for mutation in ['content','missing','manifestForgery','extra','unexpectedMissingFile']:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory(dir=verify.ROOT/'validation/task19-static') as folder:
                root=Path(folder)/'fixtures';shutil.copytree(verify.HERE/'fixtures',root)
                if mutation=='content': (root/'valid.proj').write_text('<Project/>')
                if mutation=='missing': (root/'valid.proj').unlink()
                if mutation=='extra': (root/'unplanned.proj').write_text('<Project/>')
                if mutation=='unexpectedMissingFile': (root/'missing.proj').write_text('<Project/>')
                if mutation=='manifestForgery':
                    (root/'valid.proj').write_text('<Project/>')
                    m=verify.read(root/'manifest-v1.json');m['fixtures'][0]['sha256']=verify.sha(root/'valid.proj')
                    (root/'manifest-v1.json').write_text(json.dumps(m))
                with self.assertRaisesRegex(ValueError,'fixture'): verify.verify_fixtures(root)

class ObservationPinTests(unittest.TestCase):
    def test_external_observation_pin_and_report_raw_file_bytes(self):
        for mutation in ['baseline','externalPin','rawBytes','reportBytes','runIdentity','missingPass']:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory(dir=verify.ROOT/'validation/task19-static') as folder:
                base=Path(folder);reports=[];paths=[];entries=[]
                for number in [1,2]:
                    root=base/str(number);root.mkdir();raw=root/'raw.stdout';raw.write_bytes(b'unit-only raw fixture')
                    path=root/'capture.json';path.write_bytes(b'{"unitOnly":true}')
                    reports.append({'runId':'unit-'+str(number),'fixtureRoot':str(root/'fixtures')});paths.append(path)
                    entries.append({'runId':'unit-'+str(number),'root':str(root),'reportSha256':verify.sha(path),
                        'files':[{'path':'raw.stdout','sha256':verify.sha(raw)}]})
                lock={'schemaVersion':1,'status':'LOCKED_NATIVE_LIFECYCLE_PAIR','inputLockSha256':verify.INPUT_LOCK_SHA,'passes':entries}
                path=base/'observations.json';path.write_text(json.dumps(lock));expected=verify.sha(path)
                if mutation=='externalPin': expected='0'*64
                if mutation=='rawBytes': (base/'1/raw.stdout').write_bytes(b'forged with unchanged receipt')
                if mutation=='reportBytes': paths[0].write_bytes(b'{"unitOnly":false}')
                if mutation=='runIdentity': reports[0]['runId']='forged-run'
                if mutation=='missingPass': reports.pop();paths.pop()
                if mutation=='baseline': verify.validate_observation_lock(path,expected,paths,reports)
                else:
                    with self.assertRaisesRegex(ValueError,'observation'): verify.validate_observation_lock(path,expected,paths,reports)

class ResourceTelemetryTests(unittest.TestCase):
    def setUp(self):
        self.labels=['compile']+['LCB'+str(i).zfill(2) for i in range(1,9)]
        self.report={'resourceWaits':[],'resources':[]}
        for label in self.labels:
            self.report['resourceWaits'].append({'before':label,'limitSeconds':120,'pollSeconds':5,'seconds':5,'status':'READY'})
            self.report['resources'].append({'before':label,'utc':'unit-only','waitSeconds':0,'freeVirtualKiB':16777216,'freePhysicalKiB':1})
            self.report['resources'].append({'before':label,'utc':'unit-only','waitSeconds':5,'freeVirtualKiB':16777216,'freePhysicalKiB':524288})

    def test_nine_ordered_wait_groups_preserve_low_readings_before_ready(self):
        verify.validate_resource_waits(self.report,self.labels)

    def test_cli_static_telemetry_baseline_and_forgery_controls(self):
        for mutation in ['baseline','duplicate','bool','fakeReady','late']:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory(dir=verify.ROOT/'validation/task19-static') as folder:
                root=Path(folder);d=copy.deepcopy(self.report)
                if mutation=='duplicate':d['resourceWaits'].append(copy.deepcopy(d['resourceWaits'][0]))
                if mutation=='bool':d['resources'][1]['freePhysicalKiB']=True
                if mutation=='fakeReady':d['resources'][1]['freePhysicalKiB']=524287
                if mutation=='late':d['resourceWaits'][0]['seconds']=120
                source=root/'unit-only-telemetry.json';source.write_text(json.dumps(d))
                p=subprocess.run([sys.executable,'-B',str(verify.HERE/'verify.py'),'--static','--ledger',str(verify.EVIDENCE/'selected-lifecycle-representation-v1.json'),
                    '--resource-telemetry',str(source),'--out',str(root/'result')],capture_output=True)
                self.assertEqual(p.returncode,0 if mutation=='baseline' else 1,p.stderr.decode())
                result=verify.read(root/'result/verification.json')
                self.assertEqual(result['status'],'PASS_STATIC_ONLY' if mutation=='baseline' else 'REFUSED')
                if mutation=='baseline':self.assertEqual(result['nativeOutcomes'],'UNOBSERVED')
                else:self.assertIn('resource wait',result['error'])

    def test_forged_missing_extra_order_type_or_deadline_telemetry_is_refused(self):
        for mutation in ['missingGroup','extraGroup','case','boolKiB','boolTime','readyBelowFloor','late','limit','poll','resourcesOrder','earlyReady','missingReading','nonObjectGroup','nonObjectReading','hugeTime']:
            with self.subTest(mutation=mutation):
                d=copy.deepcopy(self.report)
                if mutation=='missingGroup':d['resourceWaits'].pop()
                if mutation=='extraGroup':d['resourceWaits'].append(copy.deepcopy(d['resourceWaits'][0]))
                if mutation=='case':d['resourceWaits'][0]['before']='Compile'
                if mutation=='boolKiB':d['resources'][1]['freePhysicalKiB']=True
                if mutation=='boolTime':d['resourceWaits'][0]['seconds']=True
                if mutation=='readyBelowFloor':d['resources'][1]['freePhysicalKiB']=524287
                if mutation=='late':d['resourceWaits'][0]['seconds']=120
                if mutation=='limit':d['resourceWaits'][0]['limitSeconds']=121
                if mutation=='poll':d['resourceWaits'][0]['pollSeconds']=6
                if mutation=='resourcesOrder':d['resources'].reverse()
                if mutation=='earlyReady':d['resources'][0]['freePhysicalKiB']=524288
                if mutation=='missingReading':d['resources']=d['resources'][:-2]
                if mutation=='nonObjectGroup':d['resourceWaits'][0]='forged'
                if mutation=='nonObjectReading':d['resources'][0]=False
                if mutation=='hugeTime':d['resourceWaits'][0]['seconds']=10**1000
                with self.assertRaisesRegex(ValueError,'resource wait'):verify.validate_resource_waits(d,self.labels)

if __name__=='__main__': unittest.main()
