"""The owned controller timeout cleans its own Python process tree, with no .NET/JVM."""
import ctypes
from ctypes import wintypes
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(r'D:\AI\Implementation\dotj Frameworks')
spec=importlib.util.spec_from_file_location('lifecycle_phase_v3',ROOT/'orchestration/two-frameworks/task-19-capture-phase-v3.py')
phase=importlib.util.module_from_spec(spec);spec.loader.exec_module(phase)
kernel=ctypes.WinDLL('kernel32',use_last_error=True)
kernel.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD];kernel.OpenProcess.restype=wintypes.HANDLE
kernel.WaitForSingleObject.argtypes=[wintypes.HANDLE,wintypes.DWORD];kernel.WaitForSingleObject.restype=wintypes.DWORD
kernel.CloseHandle.argtypes=[wintypes.HANDLE];kernel.CloseHandle.restype=wintypes.BOOL

class ControllerTests(unittest.TestCase):
    def test_expiry_kills_owned_parent_and_descendant_and_retains_complete_streams(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'validation/task19-static') as folder:
            out=Path(folder);marker=out/'child.pid';entry={};env=os.environ.copy();env.update(TEMP=str(out),TMP=str(out))
            code=('import subprocess,sys,time;from pathlib import Path;'
                  'p=subprocess.Popen([sys.executable,"-I","-B","-c","import time;time.sleep(60)"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);'
                  'Path(sys.argv[1]).write_text(str(p.pid));'
                  'print("owned parent stdout",flush=True);print("owned parent stderr",file=sys.stderr,flush=True);time.sleep(60)')
            error=None
            try:
                with self.assertRaises(subprocess.TimeoutExpired) as raised:
                    phase.run_capture_process([sys.executable,'-I','-B','-c',code,str(marker)],out,env,entry,timeout=1)
                error=raised.exception
                self.assertTrue(marker.exists(),'The real descendant must have started before timeout')
                pid=int(marker.read_text());handle=kernel.OpenProcess(0x00100000|0x1000,False,pid)
                try:
                    terminated=not handle or kernel.WaitForSingleObject(handle,2000)==0
                    self.assertTrue(terminated,'Controller expiry left its own Python descendant running')
                finally:
                    if handle:kernel.CloseHandle(handle)
                self.assertIn(b'owned parent stdout',error.output)
                self.assertIn(b'owned parent stderr',error.stderr)
                self.assertEqual(0,entry['treeCleanup']['exitCode'])
                self.assertEqual(['taskkill','/PID',str(entry['processId']),'/T','/F'],entry['treeCleanup']['argv'])
                self.assertEqual(1,entry['controllerTimeoutSeconds'])
            finally:
                # Cleanup is limited to the descendant PID written by this test's own child.
                if marker.exists():
                    pid=int(marker.read_text());handle=kernel.OpenProcess(0x00100000|0x1000,False,pid)
                    if handle:
                        try:
                            if kernel.WaitForSingleObject(handle,0)!=0:
                                subprocess.run(['taskkill','/PID',str(pid),'/T','/F'],capture_output=True,timeout=10)
                        finally:kernel.CloseHandle(handle)

    def test_nonzero_child_exits_once_with_both_streams(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'validation/task19-static') as folder:
            out=Path(folder);marker=out/'launches';entry={}
            code='from pathlib import Path;import sys;Path(sys.argv[1]).open("a").write("once\\n");print("out");print("err",file=sys.stderr);sys.exit(7)'
            stdout,stderr=phase.run_capture_process([sys.executable,'-I','-B','-c',code,str(marker)],out,os.environ.copy(),entry,timeout=5)
            self.assertEqual(7,entry['exitCode']);self.assertEqual('once\n',marker.read_text())
            self.assertIn(b'out',stdout);self.assertIn(b'err',stderr)

if __name__=='__main__':unittest.main()
