"""Prospective native-only capability. Legacy ownership.py remains strict180."""
import ctypes,os,json,time
from ctypes import wintypes as w
import importlib.util
from pathlib import Path
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
HERE=Path(__file__).resolve().parent
legacy=load('native_transport_legacy',HERE/'ownership.py')
policy=load('native_transport_policy',HERE/'native_policy_v2.py')
os_parent_pid=legacy.os_parent_pid
verify_job=legacy.verify_job
def consume(handle,protocol,phase,attempt,execution,review):
    # Direct --inner without an inherited capability fails before hashing/admission.
    if type(handle) is not int or handle<=0:raise ValueError('inherited owned-launch capability required')
    k=ctypes.WinDLL('kernel32',use_last_error=True)
    k.GetFileType.argtypes=[w.HANDLE];k.GetFileType.restype=w.DWORD
    if k.GetFileType(w.HANDLE(handle))!=3:raise ValueError('ownership capability must be a pipe')
    available=w.DWORD()
    k.PeekNamedPipe.argtypes=[w.HANDLE,w.LPVOID,w.DWORD,w.LPVOID,ctypes.POINTER(w.DWORD),w.LPVOID];k.PeekNamedPipe.restype=w.BOOL
    if not k.PeekNamedPipe(w.HANDLE(handle),None,0,None,ctypes.byref(available),None):raise ctypes.WinError(ctypes.get_last_error())
    if not 0<available.value<=4096:raise ValueError('complete bounded ownership envelope required before resume')
    import msvcrt
    fd=msvcrt.open_osfhandle(handle,os.O_RDONLY)
    try:raw=os.read(fd,available.value)
    finally:os.close(fd)
    envelope=protocol.loads(raw)
    deadline=policy.validate_envelope(envelope,phase=phase,attempt=attempt,execution=execution,review=review,guard_sha=protocol.GUARD_SHA,parent_pid=os_parent_pid(),child_pid=os.getpid(),now=time.monotonic())
    membership=verify_job(envelope,str(protocol.B/'toolchains/python-3.13.9/python.exe'))
    return envelope,membership,deadline

class LaunchCapability(legacy.LaunchCapability):
 def __init__(self,guard,protocol,phase,attempt,execution,review,started,deadline):
  self.attempt=attempt
  super().__init__(guard,protocol,phase,execution,review,started,deadline)
 def job_factory(self):
  outer=self;job=self.guard.Job()
  class BoundJob:
   def __getattr__(self,name):return getattr(job,name)
   def resume(self,process):
    envelope=dict(schemaVersion=1,phase=outer.phase,attemptId=outer.attempt,executionLockSha256=outer.execution,reviewSha256=outer.review,outerStartedMonotonic=outer.started,actualOuterDeadlineMonotonic=outer.deadline,parentPid=os.getpid(),childPid=process.pid,parentJobHandle=int(job.handle),guardSha256=outer.p.GUARD_SHA,policyId=policy.POLICY['policyId'],policySha256=policy.policy_sha(),controllerSeconds=1200,postverificationReserveSeconds=480)
    raw=json.dumps(envelope,allow_nan=False).encode('ascii')
    if len(raw)>4096:raise ValueError('ownership envelope bound')
    if os.write(outer.write_fd,raw)!=len(raw):raise ValueError('complete one-use native envelope')
    os.close(outer.write_fd);outer.write_fd=None;outer.record=envelope;job.resume(process)
  return BoundJob()
