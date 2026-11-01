import importlib.util,unittest
from pathlib import Path
s=importlib.util.spec_from_file_location('cache_c',Path(__file__).with_name('capture.py'));c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
class CaptureControls(unittest.TestCase):
    def test_environment_removes_injected_native_variables_and_places_temp_on_owned_D(self):
        out=c.v.PRIVATE/'unrun-pass';env,overrides=c.environment(out,{'PATH':'kept','dotnet_gcHeapHardLimit':'bad','MSBuildFoo':'bad','COMPLUS_X':'bad','JAVA_TOOL_OPTIONS':'bad','JDK_JAVA_OPTIONS':'bad','temp':'C:/bad'})
        self.assertNotIn('MSBuildFoo',env);self.assertNotIn('dotnet_gcHeapHardLimit',env);self.assertNotIn('temp',env)
        self.assertEqual(env['TEMP'],str(out/'tmp'));self.assertEqual(env['DOTNET_GCHeapHardLimit'],'8000000');self.assertEqual(env['DOTNET_PROCESSOR_COUNT'],'2');self.assertEqual(env['PATH'],'kept')
    def test_resource_wait_never_accepts_boolean_memory(self):
        record={}
        with self.assertRaises(ValueError):c.wait_resources(Path('.'),{},record,lambda:None,540,query=lambda timeout:{'freePhysicalKiB':True,'freeVirtualKiB':16777216},now=lambda:0,sleep=lambda n:None)
    def test_resource_wait_polls_until_ready_without_launch(self):
        record={};clock=[0];samples=iter([{'freePhysicalKiB':1,'freeVirtualKiB':16777216},{'freePhysicalKiB':524288,'freeVirtualKiB':16777216}])
        def sleep(n):clock[0]+=n
        c.wait_resources(Path('.'),{},record,lambda:None,540,query=lambda timeout:next(samples),now=lambda:clock[0],sleep=sleep)
        self.assertEqual(record['resourceWait']['status'],'READY');self.assertEqual(len(record['resources']),2);self.assertEqual(clock[0],5)
    def test_resource_wait_budget_exhaustion_has_no_launch(self):
        record={};clock=[0]
        with self.assertRaises(ValueError):c.wait_resources(Path('.'),{},record,lambda:None,540,query=lambda timeout:{'freePhysicalKiB':1,'freeVirtualKiB':16777216},now=lambda:clock[0],sleep=lambda n:clock.__setitem__(0,clock[0]+n))
        self.assertEqual(record['resourceWait']['status'],'DEFERRED_NO_NATIVE_LAUNCH')
class NativeStreamControls(unittest.TestCase):
    def test_native_timeout_retains_raw_streams_and_has_one_bounded_drain(self):
        import tempfile,subprocess,types
        class Process:
            pid=12345
            returncode=None
            calls=0
            def communicate(self,timeout):
                self.calls+=1
                if self.calls==1:raise subprocess.TimeoutExpired(['fake'],30,output=b'partial',stderr=b'problem')
                return b'full retained output',b'full retained error'
            def kill(self):self.returncode=-9
            def poll(self):return self.returncode
        fake=Process()
        with tempfile.TemporaryDirectory(dir=c.v.PRIVATE/'tmp') as temp:
            root=Path(temp);(root/'logs').mkdir();command={'argv':['fake']};record={'nativeLaunched':False}
            with self.assertRaises(subprocess.TimeoutExpired):c.run_native(command,root,{},record,lambda:None,launch=lambda *a,**k:fake,now=lambda:0,cleanup=lambda *a,**k:(fake.kill() or types.SimpleNamespace(returncode=0,stdout=b'killed',stderr=b'')))
            self.assertTrue(record['nativeLaunched']);self.assertEqual(command['processId'],12345)
            self.assertEqual(fake.calls,2);self.assertEqual((root/'logs/native.stdout').read_bytes(),b'full retained output');self.assertEqual((root/'logs/native.stderr').read_bytes(),b'full retained error')
            self.assertEqual(command['nativeCleanupTimeoutSeconds'],5)
    def test_prelaunch_os_failure_is_provable_no_native_launch(self):
        import tempfile
        with tempfile.TemporaryDirectory(dir=c.v.PRIVATE/'tmp') as temp:
            root=Path(temp);(root/'logs').mkdir();record={'nativeLaunched':False};command={'argv':['fake']}
            def reject(*args,**kwargs):raise OSError('synthetic refusal before process creation')
            with self.assertRaises(OSError):c.run_native(command,root,{},record,lambda:None,launch=reject,now=lambda:0)
            self.assertFalse(record['nativeLaunched']);self.assertNotIn('processId',command)
class CleanupDeadlineControls(unittest.TestCase):
    def test_kill_budget_is_subtracted_from_five_second_total(self):
        import tempfile,subprocess,types
        clock=[0];observed=[]
        class Process:
            pid=23456
            returncode=None
            def communicate(self,timeout):
                observed.append(timeout)
                if len(observed)==1:raise subprocess.TimeoutExpired(['fake'],30)
                return b'kept',b''
            def kill(self):self.returncode=-9
            def poll(self):return self.returncode
        fake=Process();kills=[]
        def cleanup(argv,**kwargs):
            kills.append(kwargs['timeout']);clock[0]+=2;fake.returncode=-9
            return types.SimpleNamespace(returncode=0,stdout=b'killed',stderr=b'')
        with tempfile.TemporaryDirectory(dir=c.v.PRIVATE/'tmp') as temp:
            root=Path(temp);(root/'logs').mkdir();command={'argv':['fake']}
            with self.assertRaises(subprocess.TimeoutExpired):c.run_native(command,root,{},dict(nativeLaunched=False),lambda:None,launch=lambda *a,**k:fake,now=lambda:clock[0],cleanup=cleanup)
            self.assertEqual(kills,[2]);self.assertLessEqual(observed[-1],3);self.assertEqual(command['nativeCleanup']['killBudgetSeconds'],2)
    def test_cleanup_deadline_overrun_is_recorded_without_extra_drain(self):
        import tempfile,subprocess,types
        clock=[0];calls=[]
        class Process:
            pid=23456
            returncode=None
            def communicate(self,timeout):calls.append(timeout);raise subprocess.TimeoutExpired(['fake'],timeout,output=b'partial')
            def kill(self):self.returncode=-9
            def poll(self):return self.returncode
        fake=Process()
        def cleanup(argv,**kwargs):clock[0]+=6;return types.SimpleNamespace(returncode=0,stdout=b'',stderr=b'')
        with tempfile.TemporaryDirectory(dir=c.v.PRIVATE/'tmp') as temp:
            root=Path(temp);(root/'logs').mkdir();command={'argv':['fake']}
            with self.assertRaises(subprocess.TimeoutExpired):c.run_native(command,root,{},dict(nativeLaunched=False),lambda:None,launch=lambda *a,**k:fake,now=lambda:clock[0],cleanup=cleanup)
            self.assertEqual(len(calls),1);self.assertIn('cleanupError',command)
class InterruptedExitedStreamControls(unittest.TestCase):
    def test_timeout_then_already_exited_recovers_full_streams_without_kill(self):
        import tempfile,subprocess
        clock=[0];timeouts=[]
        class Process:
            pid=34567
            returncode=None
            def communicate(self,timeout):
                timeouts.append(timeout)
                if len(timeouts)==1:
                    clock[0]+=30;self.returncode=0
                    raise subprocess.TimeoutExpired(['fake'],30)
                clock[0]+=1;return b'complete stdout after exit',b'complete stderr after exit'
            def poll(self):return self.returncode
        fake=Process()
        def forbidden_kill(*args,**kwargs):raise AssertionError('already-exited owned process must not be killed')
        with tempfile.TemporaryDirectory(dir=c.v.PRIVATE/'tmp') as temp:
            root=Path(temp);(root/'logs').mkdir();command={'argv':['fake']}
            with self.assertRaises(subprocess.TimeoutExpired):c.run_native(command,root,{},dict(nativeLaunched=False),lambda:None,launch=lambda *a,**k:fake,now=lambda:clock[0],cleanup=forbidden_kill)
            self.assertEqual(timeouts,[30,5]);self.assertEqual((root/'logs/native.stdout').read_bytes(),b'complete stdout after exit');self.assertEqual((root/'logs/native.stderr').read_bytes(),b'complete stderr after exit')
            self.assertTrue(command['timeout']);self.assertFalse(command['nativeCleanup']['killAttempted']);self.assertTrue(command['nativeCleanup']['recoveryCompleted']);self.assertLessEqual(command['nativeCleanup']['seconds'],5)
    def test_already_exited_unfinished_recovery_retains_partial_streams_and_failure(self):
        import tempfile,subprocess
        clock=[0];calls=[]
        class Process:
            pid=34567
            returncode=0
            def communicate(self,timeout):
                calls.append(timeout)
                if len(calls)==1:raise subprocess.TimeoutExpired(['fake'],30,output=b'initial partial')
                clock[0]+=timeout;raise subprocess.TimeoutExpired(['fake'],timeout,output=b'latest partial',stderr=b'latest error')
            def poll(self):return self.returncode
        fake=Process()
        def forbidden_kill(*args,**kwargs):raise AssertionError('no kill after exit')
        with tempfile.TemporaryDirectory(dir=c.v.PRIVATE/'tmp') as temp:
            root=Path(temp);(root/'logs').mkdir();command={'argv':['fake']}
            with self.assertRaises(subprocess.TimeoutExpired):c.run_native(command,root,{},dict(nativeLaunched=False),lambda:None,launch=lambda *a,**k:fake,now=lambda:clock[0],cleanup=forbidden_kill)
            self.assertEqual(calls,[30,5]);self.assertEqual((root/'logs/native.stdout').read_bytes(),b'latest partial');self.assertEqual((root/'logs/native.stderr').read_bytes(),b'latest error');self.assertIn('cleanupError',command)
if __name__=='__main__':unittest.main()
