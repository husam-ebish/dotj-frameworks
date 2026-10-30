"""Native scheduling boundary exercised with real Python children, never .NET/JVM."""
from contextlib import ExitStack
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
ROOT=Path(r'D:\AI\Implementation\dotj Frameworks')

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result

capture=module('owned_lifecycle_capture',HERE/'capture.py')
guard=module('reviewed_candidate_guard',capture.verify.REPO/'dotj-build/evaluation-candidate/verify.py')

class Clock:
    def __init__(self):self.now=0;self.sleeps=[]
    def monotonic(self):return self.now
    def sleep(self,n):self.now+=n;self.sleeps.append(n)

class NativeGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'validation/task19-static')
        self.addCleanup(self.temp.cleanup);self.out=Path(self.temp.name);(self.out/'logs').mkdir()
        self.record={'status':'RUNNING','commands':[],'resources':[]};self.clock=Clock()
        self.save_delay=0;self.prep_delay=0;self.pid_delay=0;self.query_starts=[];self.query_caps=[];self.native_caps=[];self.launches=[]
        self.env=os.environ.copy();self.env.update(TEMP=str(self.out),TMP=str(self.out))

    def save(self):
        (self.out/'record.json').write_text(json.dumps(self.record))
        entry=self.record['commands'][-1] if self.record['commands'] else None
        self.clock.now+=self.pid_delay if entry and 'processId' in entry else (self.prep_delay if entry else self.save_delay)

    def invoke(self,readings,*,query_seconds=0,aggregate=540,exit_code=0):
        readings=iter(readings);last=None;durations=iter(query_seconds) if isinstance(query_seconds,list) else None
        real_popen=subprocess.Popen
        def query(argv,**options):
            nonlocal last
            if argv[0]!='powershell':raise AssertionError('Only the OS query is replaced')
            try:last=next(readings)
            except StopIteration:pass
            self.query_starts.append(self.clock.now);self.query_caps.append(options['timeout'])
            self.clock.now+=next(durations) if durations is not None else query_seconds
            if isinstance(last,BaseException):raise last
            return subprocess.CompletedProcess(argv,0,last,'query diagnostic')
        def child(argv,**options):
            self.launches.append(self.clock.now);process=real_popen(argv,**options);communicate=process.communicate
            def observed_communicate(*args,**kwargs):
                self.native_caps.append(kwargs.get('timeout'));return communicate(*args,**kwargs)
            process.communicate=observed_communicate;return process
        marker=self.out/'launched.txt'
        argv=[sys.executable,'-I','-B','-c','from pathlib import Path;import sys;Path(sys.argv[1]).open("a").write("launched\\n");print("child stdout");'+('print("child stderr",file=sys.stderr);' if exit_code else '')+'sys.exit('+str(exit_code)+')',str(marker)]
        with ExitStack() as stack:
            stack.enter_context(patch.object(guard.subprocess,'run',query))
            stack.enter_context(patch.object(capture.subprocess,'Popen',child))
            stack.enter_context(patch.object(guard.time,'monotonic',self.clock.monotonic))
            stack.enter_context(patch.object(guard.time,'sleep',self.clock.sleep))
            return capture.run_native_command('python-test',argv,self.out,self.env,{},self.record,self.save,guard,aggregate)

    def test_transient_low_floors_recover_and_launch_one_python_child_with_native30_cap(self):
        try:self.invoke(['{"freeVirtualKiB":20000000,"freePhysicalKiB":180000}',
                         '{"freeVirtualKiB":10000000,"freePhysicalKiB":600000}',
                         '{"freeVirtualKiB":16777216,"freePhysicalKiB":524288}'])
        except Exception as error:self.fail('Transient memory must wait and recover: '+str(error))
        self.assertEqual([0,5,10],self.query_starts);self.assertEqual([10],self.launches)
        self.assertEqual([30],self.native_caps);self.assertEqual('launched\n',(self.out/'launched.txt').read_text())
        self.assertEqual([180000,600000,524288],[x['freePhysicalKiB'] for x in self.record['resources']])

    def test_exact_floors_launch_without_sleep(self):
        self.invoke(['{"freeVirtualKiB":16777216,"freePhysicalKiB":524288}'])
        self.assertEqual([0],self.launches);self.assertEqual([],self.clock.sleeps);self.assertEqual([30],self.native_caps)

    def test_each_low_floor_defers_at120_with_no_child(self):
        for reading in ['{"freeVirtualKiB":16777216,"freePhysicalKiB":524287}',
                        '{"freeVirtualKiB":16777215,"freePhysicalKiB":524288}']:
            with self.subTest(reading=reading):
                self.clock=Clock();self.record={'status':'RUNNING','commands':[],'resources':[]}
                with self.assertRaises(RuntimeError):self.invoke([reading])
                self.assertEqual(120,self.clock.now);self.assertEqual([],self.record['commands']);self.assertEqual([],self.launches)
                self.assertEqual('DEFERRED_RESOURCES',self.record['status'])

    def test_ready_guard_save_crossing_deadline_never_launches(self):
        self.save_delay=3
        with self.assertRaises(RuntimeError):self.invoke(['{"freeVirtualKiB":0,"freePhysicalKiB":0}']*5+['{"freeVirtualKiB":16777216,"freePhysicalKiB":524288}'],query_seconds=[19]*5+[8])
        self.assertEqual([],self.launches);self.assertEqual([],self.record['commands']);self.assertGreaterEqual(self.clock.now,120)

    def test_preparation_save_crossing_deadline_removes_unlaunched_entry(self):
        self.prep_delay=7
        with self.assertRaises(RuntimeError):self.invoke(['{"freeVirtualKiB":0,"freePhysicalKiB":0}']*5+['{"freeVirtualKiB":16777216,"freePhysicalKiB":524288}'],query_seconds=19)
        self.assertEqual([],self.launches);self.assertEqual([],self.record['commands']);self.assertGreaterEqual(self.clock.now,120)

    def test_slow_queries_and_saves_consume_poll_and_remaining_query_budget(self):
        self.save_delay=3
        with self.assertRaises(RuntimeError):self.invoke(['{"freeVirtualKiB":0,"freePhysicalKiB":0}'],query_seconds=19)
        self.assertEqual([0,22,44,66,88,110],self.query_starts);self.assertEqual([20,20,20,20,20,10],self.query_caps)
        self.assertEqual([],self.clock.sleeps);self.assertEqual([],self.launches)

    def test_malformed_or_failed_query_never_launches_or_retries(self):
        for reading in ['{}','{"freeVirtualKiB":99999999,"freePhysicalKiB":true}',
                        '{"freeVirtualKiB":99999999,"freePhysicalKiB":524288.5}',
                        subprocess.TimeoutExpired(['powershell'],20,output=b'partial',stderr=b'diagnostic')]:
            with self.subTest(reading=str(reading)):
                self.record={'status':'RUNNING','commands':[],'resources':[]}
                with self.assertRaises(Exception):self.invoke([reading])
                self.assertEqual('RESOURCE_QUERY_FAILED',self.record['status']);self.assertEqual([],self.launches)
                self.assertEqual([],self.record['commands']);self.assertTrue((self.out/'record.json').exists())

    def test_aggregate_headroom_check_after_wait_and_prep_never_launches_late(self):
        self.prep_delay=6
        with self.assertRaisesRegex(RuntimeError,'aggregate'):self.invoke(['{"freeVirtualKiB":16777216,"freePhysicalKiB":524288}'],aggregate=40)
        self.assertEqual([],self.launches);self.assertEqual([],self.record['commands'])

    def test_aggregate_budget_is_checked_inside_wait_evidence_save(self):
        with self.assertRaisesRegex(RuntimeError,'aggregate'):self.invoke(['{"freeVirtualKiB":0,"freePhysicalKiB":0}'],aggregate=50)
        self.assertLess(self.clock.now,120);self.assertEqual([],self.launches)

    def test_pid_save_latency_counts_inside_native30_execution_budget(self):
        self.pid_delay=3
        self.invoke(['{"freeVirtualKiB":16777216,"freePhysicalKiB":524288}'])
        self.assertEqual([27],self.native_caps)

    def test_launched_failure_retains_both_streams_and_never_retries(self):
        with self.assertRaises(RuntimeError):self.invoke(['{"freeVirtualKiB":16777216,"freePhysicalKiB":524288}'],exit_code=7)
        self.assertEqual([0],self.launches);self.assertEqual(7,self.record['commands'][0]['exitCode'])
        self.assertEqual('launched\n',(self.out/'launched.txt').read_text())
        self.assertIn(b'child stdout',(self.out/'logs/python-test.stdout').read_bytes())
        self.assertIn(b'child stderr',(self.out/'logs/python-test.stderr').read_bytes())

if __name__=='__main__':unittest.main()
