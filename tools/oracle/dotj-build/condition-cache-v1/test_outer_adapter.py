"""NPR-02: execute only fake subprocesses through the unchanged helper integration."""
import importlib.util,subprocess,tempfile,types,unittest
from pathlib import Path
s=importlib.util.spec_from_file_location('cache_outer_adapter_controls',Path(__file__).with_name('capture.py'));c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
class OuterCleanupAdapterControls(unittest.TestCase):
    def run_timeout(self,second_drain_times_out=False,kill_raises=False):
        original_run=subprocess.run;original_popen=subprocess.Popen
        with tempfile.TemporaryDirectory(dir=c.v.PRIVATE/'tmp') as temp:
            root=Path(temp);env,overrides=c.environment(root,{'PATH':'C:/ambient-untrusted-bin','CUSTOM':'retained'});entry={'argv':['synthetic-inner','owned-fixture-root='+str(root/'fixtures')]};events=[];timeouts=[]
            class Process:
                pid=45678
                returncode=None
                def communicate(self,timeout):
                    timeouts.append(timeout)
                    if len(timeouts)==1 or second_drain_times_out and len(timeouts)==2:raise subprocess.TimeoutExpired(entry['argv'],timeout)
                    self.returncode=0;return b'complete outer stdout',b'complete outer stderr'
                def kill(self):events.append(('owned-fallback-kill',self.pid));self.returncode=-9
            fake=Process()
            class Backend:
                PIPE=subprocess.PIPE
                TimeoutExpired=subprocess.TimeoutExpired
                def Popen(self,argv,**kwargs):
                    self_owner.assertIs(subprocess.run,original_run);self_owner.assertIs(subprocess.Popen,original_popen)
                    self_owner.assertEqual(kwargs['cwd'],c.v.R);self_owner.assertEqual(kwargs['env'],env)
                    events.append(('owned-child',list(argv),kwargs));return fake
                def run(self,argv,**kwargs):
                    self_owner.assertIs(subprocess.run,original_run);self_owner.assertIs(subprocess.Popen,original_popen)
                    self_owner.assertEqual(argv,[str(c.TASKKILL),'/PID','45678','/T','/F'])
                    self_owner.assertEqual(kwargs,{'capture_output':True,'timeout':20,'cwd':str(root),'env':env})
                    events.append(('actual-cleanup',list(argv),kwargs))
                    if kill_raises:raise subprocess.TimeoutExpired(argv,20,output=b'cleanup partial',stderr=b'cleanup error')
                    return types.SimpleNamespace(returncode=0,stdout=b'killed owned tree',stderr=b'')
            self_owner=self;guard=c.v.load('fresh_pinned_helper_for_mock_control',c.HELPER);original_helper_dependency=guard.subprocess;backend=Backend()
            with self.assertRaises(subprocess.TimeoutExpired) as error:c.run_outer(guard,entry,root,env,overrides,backend=backend)
            self.assertEqual(error.exception.output,b'complete outer stdout');self.assertEqual(error.exception.stderr,b'complete outer stderr')
            self.assertEqual(entry['processId'],45678);self.assertEqual(entry['controllerTimeoutSeconds'],600)
            self.assertIs(subprocess.run,original_run);self.assertIs(subprocess.Popen,original_popen);self.assertIs(guard.subprocess,original_helper_dependency)
            cleanup=entry['treeCleanup'];self.assertEqual(cleanup['argv'],[str(c.TASKKILL),'/PID','45678','/T','/F']);self.assertEqual(cleanup['cwd'],str(root));self.assertEqual(cleanup['requestedArgv'],['taskkill','/PID','45678','/T','/F']);self.assertEqual(cleanup['environmentOverrides'],overrides);self.assertEqual(cleanup['environmentSha256'],c.v.sha_environment(env));self.assertEqual(cleanup['timeoutSeconds'],20)
            self.assertEqual(timeouts,[600,5,5] if second_drain_times_out else [600,5]);self.assertTrue(any(e[0]=='actual-cleanup' for e in events))
            if kill_raises:self.assertIn('error',cleanup)
            else:self.assertEqual(cleanup['exitCode'],0)
            return events
    def test_outer_timeout_uses_absolute_taskkill_owned_cwd_env_actual_argv_without_global_patch(self):self.run_timeout()
    def test_outer_timeout_preserves_unchanged_bounded_fallback_drain(self):
        events=self.run_timeout(second_drain_times_out=True);self.assertIn(('owned-fallback-kill',45678),events)
    def test_outer_cleanup_timeout_still_recovers_streams_and_restores_helper_dependency(self):self.run_timeout(kill_raises=True)
if __name__=='__main__':unittest.main()
