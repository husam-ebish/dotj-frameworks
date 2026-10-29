"""Python-only resource scheduling tests; no compiler, JVM or native tool runs."""
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


BASE = Path(__file__).resolve().parent


def prepare_test_storage():
    parent = Path(r'D:\AI\Implementation\dotj Frameworks\validation').resolve(strict=True)
    if os.name != 'nt' or parent.drive.casefold() != 'd:':
        raise RuntimeError('Resource tests require the Windows D: validation root')
    root = Path(tempfile.mkdtemp(prefix='task-10-resource-wait-focused-', dir=parent)).resolve(strict=True)
    if not root.is_relative_to(parent):
        raise RuntimeError('Resource test output escaped the D: validation root')
    for folder in ['tmp', 'cases', 'pycache']:
        (root/folder).mkdir()
    os.environ.update(TEMP=str(root/'tmp'), TMP=str(root/'tmp'),
                      PYTHONDONTWRITEBYTECODE='1', PYTHONPYCACHEPREFIX=str(root/'pycache'))
    tempfile.tempdir = str(root/'tmp')
    sys.dont_write_bytecode = True
    sys.pycache_prefix = str(root/'pycache')
    manifest = {'executable':sys.executable, 'argv':sys.argv, 'cwd':str(Path.cwd()),
                'resolvedOutputParent':str(parent), 'resolvedRunRoot':str(root),
                'resolvedTempRoot':tempfile.gettempdir(),
                'environment':{key:os.environ.get(key) for key in
                               ['TEMP', 'TMP', 'PYTHONDONTWRITEBYTECODE', 'PYTHONPYCACHEPREFIX']},
                'dontWriteBytecode':sys.dont_write_bytecode, 'pycachePrefix':sys.pycache_prefix}
    (root/'environment.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    print('Resource guard test evidence: '+str(root), flush=True)
    return root


TEST_RUN_ROOT = prepare_test_storage()
spec = importlib.util.spec_from_file_location('candidate_verify', BASE/'verify.py')
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


class Clock:
    def __init__(self):
        self.now = 0.0
        self.sleeps = []

    def monotonic(self):
        return self.now

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds


class ResourceGuardTest(unittest.TestCase):
    def setUp(self):
        self.output = Path(tempfile.mkdtemp(prefix=self._testMethodName+'-', dir=TEST_RUN_ROOT/'cases')).resolve(strict=True)
        if not self.output.is_relative_to(TEST_RUN_ROOT/'cases'):
            raise RuntimeError('Resource test case escaped its validated D: root')
        (self.output/'logs').mkdir()
        self.record = {'status':'PREPARED', 'commands':[], 'resources':[]}
        self.clock = Clock()
        self.real_run = subprocess.run
        self.readings = []
        self.command_timeouts = []
        self.query_starts = []
        self.query_timeouts = []
        self.launch_times = []
        self.save_seconds = 0
        self.prelaunch_save_seconds = 0

    def save(self):
        (self.output/'verification.json').write_text(json.dumps(self.record), encoding='utf-8')
        preparing = self.record['commands'] and 'passed' not in self.record['commands'][-1]
        self.clock.now += self.prelaunch_save_seconds if preparing else self.save_seconds

    def invoke(self, readings, *, exit_code=0, query_seconds=0):
        """Replace only the OS memory query and time; launch a real Python child."""
        readings = iter(readings)
        last = None
        query_durations = iter(query_seconds) if isinstance(query_seconds, list) else None

        def operating_system_run(arguments, **options):
            nonlocal last
            if arguments[0] != 'powershell':
                self.command_timeouts.append(options['timeout'])
                self.launch_times.append(self.clock.now)
                return self.real_run(arguments, **options)
            try:
                last = next(readings)
            except StopIteration:
                pass
            self.query_starts.append(self.clock.now)
            self.query_timeouts.append(options['timeout'])
            self.clock.now += next(query_durations) if query_durations is not None else query_seconds
            self.readings.append(self.clock.now)
            if isinstance(last, BaseException):
                raise last
            return subprocess.CompletedProcess(arguments, 0, last, 'query diagnostic')

        marker = self.output/'launched.txt'
        arguments = [sys.executable, '-I', '-B', '-c',
                     'from pathlib import Path; import json, os, sys, tempfile; '
                     'Path(sys.argv[1]).open("a").write("launched\\n"); '
                     'Path(sys.argv[1]).with_name("child-environment.json").write_text(json.dumps({'
                     '"TEMP":os.environ.get("TEMP"), "TMP":os.environ.get("TMP"), '
                     '"dontWriteBytecode":sys.dont_write_bytecode, "pycachePrefix":sys.pycache_prefix, '
                     '"resolvedTempRoot":tempfile.gettempdir()})); '
                     'print("child output"); print("child diagnostic", file=sys.stderr); '
                     'sys.exit(int(sys.argv[2]))', str(marker), str(exit_code)]
        with ExitStack() as stack:
            stack.enter_context(patch.object(verify.subprocess, 'run', operating_system_run))
            stack.enter_context(patch.object(verify.time, 'monotonic', self.clock.monotonic))
            stack.enter_context(patch.object(verify.time, 'sleep', self.clock.sleep))
            verify.run_command('test-child', arguments, self.output, os.environ.copy(), self.record, self.save)
        return marker

    def assert_deferred_without_child(self):
        saved = json.loads((self.output/'verification.json').read_text())
        self.assertEqual('DEFERRED_RESOURCES', saved['status'])
        self.assertEqual('test-child', saved['deferredBefore'])
        self.assertEqual('DEFERRED_RESOURCES', saved['resourceWaits'][0]['status'])
        self.assertGreaterEqual(saved['resourceWaits'][0]['seconds'], 120)
        self.assertEqual([], saved['commands'])
        self.assertEqual([], self.launch_times)
        self.assertFalse((self.output/'launched.txt').exists())

    def test_test_outputs_and_real_child_use_recorded_d_storage(self):
        # Catches implicit host-temp use or a child that can write bytecode caches.
        self.invoke(['{"freeVirtualKiB":16777216,"freePhysicalKiB":524288}'])
        parent = json.loads((TEST_RUN_ROOT/'environment.json').read_text())
        child = json.loads((self.output/'child-environment.json').read_text())
        self.assertEqual('d:', Path(parent['resolvedOutputParent']).drive.casefold())
        self.assertTrue(self.output.is_relative_to(TEST_RUN_ROOT))
        for key in ['TEMP', 'TMP']:
            self.assertEqual(str(TEST_RUN_ROOT/'tmp'), parent['environment'][key])
            self.assertEqual(str(TEST_RUN_ROOT/'tmp'), child[key])
        self.assertEqual(str(TEST_RUN_ROOT/'tmp'), child['resolvedTempRoot'])
        self.assertTrue(child['dontWriteBytecode'])
        self.assertTrue(parent['dontWriteBytecode'])

    def test_ready_reading_whose_save_crosses_deadline_never_launches(self):
        # Catches READY authorization using elapsed time captured before persistence.
        self.save_seconds = 3
        with self.assertRaises(RuntimeError):
            self.invoke(['{"freeVirtualKiB":0,"freePhysicalKiB":0}']*5+
                        ['{"freeVirtualKiB":16777216,"freePhysicalKiB":524288}'],
                        query_seconds=[19, 19, 19, 19, 19, 8])
        self.assertEqual([0, 22, 44, 66, 88, 110], self.query_starts)
        self.assert_deferred_without_child()

    def test_command_preparation_save_crossing_deadline_never_launches(self):
        # Catches losing the guard deadline between READY and the process boundary.
        self.prelaunch_save_seconds = 7
        with self.assertRaises(RuntimeError):
            self.invoke(['{"freeVirtualKiB":0,"freePhysicalKiB":0}']*5+
                        ['{"freeVirtualKiB":16777216,"freePhysicalKiB":524288}'], query_seconds=19)
        self.assertEqual([0, 19, 38, 57, 76, 95], self.query_starts)
        self.assert_deferred_without_child()

    def test_three_second_saves_leave_two_second_poll_sleeps(self):
        # Catches adding a full five-second sleep after evidence I/O consumed three.
        self.save_seconds = 3
        with self.assertRaises(RuntimeError):
            self.invoke(['{"freeVirtualKiB":0,"freePhysicalKiB":0}'])
        self.assertEqual(list(range(0, 120, 5)), self.query_starts)
        self.assertTrue(all(seconds == 2 for seconds in self.clock.sleeps))
        self.assert_deferred_without_child()

    def test_save_consuming_poll_interval_adds_no_sleep(self):
        # Catches sleeping after persistence already exceeded the target interval.
        self.save_seconds = 6
        with self.assertRaises(RuntimeError):
            self.invoke(['{"freeVirtualKiB":0,"freePhysicalKiB":0}'])
        self.assertEqual(list(range(0, 120, 6)), self.query_starts)
        self.assertEqual([], self.clock.sleeps)
        self.assert_deferred_without_child()

    def test_slow_queries_add_no_sleep_and_keep_remaining_deadline_cap(self):
        # Catches treating the five-second target as a hard query cap or adding delay.
        with self.assertRaises(RuntimeError):
            self.invoke(['{"freeVirtualKiB":0,"freePhysicalKiB":0}'], query_seconds=[19]*6+[6])
        self.assertEqual([0, 19, 38, 57, 76, 95, 114], self.query_starts)
        self.assertEqual([20, 20, 20, 20, 20, 20, 6], self.query_timeouts)
        self.assertEqual([], self.clock.sleeps)
        self.assert_deferred_without_child()

    def test_ready_launch_records_guard_and_preparation_save_latency(self):
        # Catches omitting persistence latency from the wait while retaining child120s.
        self.save_seconds = 3
        self.prelaunch_save_seconds = 3
        marker = self.invoke(['{"freeVirtualKiB":16777216,"freePhysicalKiB":524288}'])
        self.assertTrue(marker.exists())
        self.assertEqual([6], self.launch_times)
        self.assertEqual(6, self.record['resourceWaits'][0]['seconds'])
        self.assertEqual([120], self.command_timeouts)

    def test_exact_floors_launch_immediately_with_saved_reading(self):
        # Catches treating equality as low or always sleeping before a ready command.
        marker = self.invoke(['{"freeVirtualKiB":16777216,"freePhysicalKiB":524288}'])
        self.assertTrue(marker.exists())
        self.assertEqual([], self.clock.sleeps)
        self.assertIn('waitSeconds', self.record['resources'][0])
        self.assertEqual(0, self.record['resources'][0]['waitSeconds'])
        self.assertEqual('READY', self.record['resourceWaits'][0]['status'])
        self.assertTrue(self.record['commands'][0]['passed'])

    def test_each_floor_independently_blocks_until_deadline_without_launch(self):
        # Catches using AND for low resources, lowering either floor, or unbounded waiting.
        for memory in ['{"freeVirtualKiB":16777216,"freePhysicalKiB":524287}',
                       '{"freeVirtualKiB":16777215,"freePhysicalKiB":524288}']:
            with self.subTest(memory=memory):
                self.clock = Clock()
                self.readings = []
                self.record = {'status':'PREPARED', 'commands':[], 'resources':[]}
                with self.assertRaises(RuntimeError):
                    self.invoke([memory])
                saved = json.loads((self.output/'verification.json').read_text())
                self.assertEqual('DEFERRED_RESOURCES', saved['status'])
                self.assertEqual('test-child', saved['deferredBefore'])
                self.assertEqual(120, self.clock.now)
                self.assertEqual(120, saved['resourceWaits'][0]['seconds'])
                self.assertEqual(24, len(saved['resources']))
                self.assertEqual(list(range(0, 120, 5)), [r['waitSeconds'] for r in saved['resources']])
                self.assertEqual([], saved['commands'])
                self.assertFalse((self.output/'launched.txt').exists())

    def test_transient_low_memory_recovers_and_preserves_every_reading(self):
        # Catches immediate deferral, skipping either floor, or erasing low readings.
        try:
            marker = self.invoke([
                '{"freeVirtualKiB":20000000,"freePhysicalKiB":180080}',
                '{"freeVirtualKiB":10000000,"freePhysicalKiB":600000}',
                '{"freeVirtualKiB":16777216,"freePhysicalKiB":524288}'])
        except RuntimeError as error:
            self.fail('Transient low memory must wait and recover: '+str(error))
        self.assertTrue(marker.exists())
        saved = json.loads((self.output/'verification.json').read_text())
        self.assertEqual([0, 5, 10], [r['waitSeconds'] for r in saved['resources']])
        self.assertEqual([180080, 600000, 524288], [r['freePhysicalKiB'] for r in saved['resources']])
        self.assertEqual([5, 5], self.clock.sleeps)
        self.assertEqual(10, saved['resourceWaits'][0]['seconds'])
        self.assertEqual(1, len(saved['commands']))
        self.assertEqual([120], self.command_timeouts)
        self.assertLess(saved['commands'][0]['seconds'], 10)
        self.assertEqual(b'child output\r\n', (self.output/'logs/test-child.stdout').read_bytes())

    def test_query_time_counts_toward_wait_budget_and_final_sleep_is_capped(self):
        # Catches ignoring memory-query time or oversleeping the remaining budget.
        with self.assertRaises(RuntimeError):
            self.invoke(['{"freeVirtualKiB":0,"freePhysicalKiB":0}'], query_seconds=3)
        self.assertEqual(120, self.clock.now)
        self.assertLessEqual(max(self.clock.sleeps), 5)
        self.assertTrue(all(b-a <= 5 for a, b in zip(self.readings, self.readings[1:])))
        self.assertEqual('DEFERRED_RESOURCES', self.record['status'])
        self.assertEqual([], self.record['commands'])

    def test_late_ready_query_never_launches_after_wait_deadline(self):
        # Catches allowing a slow OS query to authorize a launch after expiry.
        with self.assertRaises(RuntimeError):
            self.invoke(['{"freeVirtualKiB":16777216,"freePhysicalKiB":524288}'], query_seconds=121)
        self.assertEqual('DEFERRED_RESOURCES', self.record['status'])
        self.assertEqual([], self.record['commands'])
        self.assertFalse((self.output/'launched.txt').exists())

    def test_failed_command_retains_diagnostics_and_is_never_retried(self):
        # Catches retrying a launched failure or losing its stdout/stderr evidence.
        with self.assertRaises(RuntimeError):
            self.invoke(['{"freeVirtualKiB":16777216,"freePhysicalKiB":524288}'], exit_code=7)
        saved = json.loads((self.output/'verification.json').read_text())
        self.assertEqual('COMMAND_FAILED', saved['status'])
        self.assertEqual(1, len(saved['commands']))
        self.assertEqual(7, saved['commands'][0]['exitCode'])
        self.assertEqual(b'child diagnostic\r\n', (self.output/'logs/test-child.stderr').read_bytes())
        self.assertEqual('launched\n', (self.output/'launched.txt').read_text())
        self.assertEqual([], self.clock.sleeps)

    def test_query_errors_fail_closed_with_original_diagnostics(self):
        # Catches swallowing OS query failures, retrying them, or losing diagnostics.
        for error in [subprocess.CalledProcessError(9, ['powershell'], output='query output', stderr='CIM denied'),
                      subprocess.TimeoutExpired(['powershell'], 20, output=b'partial output', stderr=b'query timeout'),
                      OSError('powershell unavailable')]:
            with self.subTest(error=type(error).__name__):
                self.record = {'status':'PREPARED', 'commands':[], 'resources':[]}
                self.readings = []
                with self.assertRaises(Exception):
                    self.invoke([error])
                self.assertTrue((self.output/'verification.json').exists(), 'Memory query failure must save evidence')
                saved = json.loads((self.output/'verification.json').read_text())
                self.assertEqual('RESOURCE_QUERY_FAILED', saved['status'])
                self.assertEqual('test-child', saved['failedBefore'])
                self.assertIn(type(error).__name__, saved['resources'][0]['error'])
                if getattr(error, 'stderr', None):
                    self.assertIn('CIM denied' if isinstance(error, subprocess.CalledProcessError) else 'query timeout',
                                  saved['resources'][0]['stderr'])
                self.assertEqual(1, len(self.readings))
                self.assertEqual([], saved['commands'])
                self.assertFalse((self.output/'launched.txt').exists())

    def test_malformed_memory_never_launches_or_silently_weakens_floors(self):
        # Catches accepting missing, nonnumeric, negative, boolean, or fractional values.
        for data in ['not JSON', '{}', '[]',
                     '{"freeVirtualKiB":"99999999","freePhysicalKiB":99999999}',
                     '{"freeVirtualKiB":99999999,"freePhysicalKiB":-1}',
                     '{"freeVirtualKiB":99999999,"freePhysicalKiB":true}',
                     '{"freeVirtualKiB":99999999,"freePhysicalKiB":524288.5}']:
            with self.subTest(data=data):
                self.record = {'status':'PREPARED', 'commands':[], 'resources':[]}
                with self.assertRaises(Exception):
                    self.invoke([data])
                self.assertTrue((self.output/'verification.json').exists(), 'Malformed memory must save evidence')
                saved = json.loads((self.output/'verification.json').read_text())
                self.assertEqual('RESOURCE_QUERY_FAILED', saved['status'])
                self.assertEqual(data, saved['resources'][0]['stdout'])
                self.assertEqual([], saved['commands'])
                self.assertFalse((self.output/'launched.txt').exists())


if __name__ == '__main__':
    unittest.main()
