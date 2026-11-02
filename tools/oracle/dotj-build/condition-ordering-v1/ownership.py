"""New launch-capability seam; no process starts on import.

The inherited object is a one-use pipe, never a Job HANDLE. The child duplicates
the parent Job HANDLE only after resume, queries actual membership, and closes
the duplicate immediately. The qualified guard continues to own/kill/close the
original Job. This seam has pure controls; Windows integration is NOT OBSERVED.
"""
import ctypes
import os
import subprocess
import time
from ctypes import wintypes as w

FIELDS={'schemaVersion','phase','executionLockSha256','reviewSha256','outerStartedMonotonic','actualOuterDeadlineMonotonic','parentPid','childPid','parentJobHandle','guardSha256'}

def validate(envelope,*,phase,execution,review,guard_sha,parent_pid,child_pid,now):
    def require(ok,message):
        if not ok:raise ValueError(message)
    require(type(envelope) is dict and set(envelope)==FIELDS,'exact inherited ownership envelope')
    require(type(envelope['schemaVersion']) is int and envelope['schemaVersion']==1,'ownership version')
    for key,value in [('phase',phase),('executionLockSha256',execution),('reviewSha256',review),('guardSha256',guard_sha)]:require(envelope[key]==value,'ownership binding '+key)
    for key,value in [('parentPid',parent_pid),('childPid',child_pid)]:require(type(envelope[key]) is int and envelope[key]==value and value>0,'actual OS '+key)
    require(type(envelope['parentJobHandle']) is int and envelope['parentJobHandle']>0,'parent Job HANDLE')
    start=envelope['outerStartedMonotonic'];deadline=envelope['actualOuterDeadlineMonotonic']
    require(type(start) in [int,float] and type(deadline) in [int,float] and deadline==start+180 and start<=now<deadline and deadline-now<=180,'actual finite owned180 envelope')
    return deadline

def os_parent_pid():
    n=ctypes.WinDLL('ntdll',use_last_error=True);k=ctypes.WinDLL('kernel32',use_last_error=True)
    class Basic(ctypes.Structure):
        _fields_=[('exitStatus',w.LONG),('peb',w.LPVOID),('affinity',ctypes.c_size_t),('priority',w.LONG),('pid',ctypes.c_size_t),('parent',ctypes.c_size_t)]
    n.NtQueryInformationProcess.argtypes=[w.HANDLE,w.ULONG,w.LPVOID,w.ULONG,w.LPVOID];n.NtQueryInformationProcess.restype=w.LONG
    k.GetCurrentProcess.restype=w.HANDLE
    value=Basic();status=n.NtQueryInformationProcess(k.GetCurrentProcess(),0,ctypes.byref(value),ctypes.sizeof(value),None)
    if status!=0:raise OSError('actual parent process query failed: '+str(status))
    if value.pid!=os.getpid():raise ValueError('actual current process identity')
    return value.parent

def verify_job(envelope,expected_python):
    k=ctypes.WinDLL('kernel32',use_last_error=True)
    k.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD];k.OpenProcess.restype=w.HANDLE
    k.GetCurrentProcess.restype=w.HANDLE
    k.CloseHandle.argtypes=[w.HANDLE];k.CloseHandle.restype=w.BOOL
    k.DuplicateHandle.argtypes=[w.HANDLE,w.HANDLE,w.HANDLE,ctypes.POINTER(w.HANDLE),w.DWORD,w.BOOL,w.DWORD];k.DuplicateHandle.restype=w.BOOL
    k.IsProcessInJob.argtypes=[w.HANDLE,w.HANDLE,ctypes.POINTER(w.BOOL)];k.IsProcessInJob.restype=w.BOOL
    k.QueryFullProcessImageNameW.argtypes=[w.HANDLE,w.DWORD,w.LPWSTR,ctypes.POINTER(w.DWORD)];k.QueryFullProcessImageNameW.restype=w.BOOL
    parent=k.OpenProcess(0x0040|0x1000,False,envelope['parentPid']) # DUP_HANDLE | QUERY_LIMITED_INFORMATION
    if not parent:raise ctypes.WinError(ctypes.get_last_error())
    duplicated=w.HANDLE()
    try:
        name=ctypes.create_unicode_buffer(32768);length=w.DWORD(len(name))
        if not k.QueryFullProcessImageNameW(parent,0,name,ctypes.byref(length)):raise ctypes.WinError(ctypes.get_last_error())
        if os.path.normcase(os.path.realpath(name.value))!=os.path.normcase(os.path.realpath(expected_python)):raise ValueError('actual parent executable binding')
        if not k.DuplicateHandle(parent,w.HANDLE(envelope['parentJobHandle']),k.GetCurrentProcess(),ctypes.byref(duplicated),0,False,2):raise ctypes.WinError(ctypes.get_last_error())
        member=w.BOOL()
        if not k.IsProcessInJob(k.GetCurrentProcess(),duplicated,ctypes.byref(member)):raise ctypes.WinError(ctypes.get_last_error())
        if not member.value:raise ValueError('current inner process is not in actual declared controller Job')
    finally:
        if duplicated.value:
            if not k.CloseHandle(duplicated):raise ctypes.WinError(ctypes.get_last_error())
        if not k.CloseHandle(parent):raise ctypes.WinError(ctypes.get_last_error())
    return dict(actualParentPid=envelope['parentPid'],actualChildPid=os.getpid(),actualJobMembershipVerified=True,parentExecutable=expected_python,duplicatedJobHandleClosed=True)

def consume(handle,protocol,phase,execution,review):
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
    deadline=validate(envelope,phase=phase,execution=execution,review=review,guard_sha=protocol.GUARD_SHA,parent_pid=os_parent_pid(),child_pid=os.getpid(),now=time.monotonic())
    membership=verify_job(envelope,str(protocol.B/'toolchains/python-3.13.9/python.exe'))
    return envelope,membership,deadline

class LaunchCapability:
    """One guarded spawn, with envelope written after Job.assign and before resume."""
    def __init__(self,guard,protocol,phase,execution,review,started,deadline):
        self.guard=guard;self.p=protocol;self.phase=phase;self.execution=execution;self.review=review;self.started=started;self.deadline=deadline
        self.read_fd,self.write_fd=os.pipe();self.handle=None;self.record=None
        import msvcrt
        self.handle=msvcrt.get_osfhandle(self.read_fd);os.set_handle_inheritable(self.handle,True)
    def job_factory(self):
        outer=self;job=self.guard.Job()
        class BoundJob:
            def __getattr__(self,name):return getattr(job,name)
            def resume(self,process):
                envelope=dict(schemaVersion=1,phase=outer.phase,executionLockSha256=outer.execution,reviewSha256=outer.review,
                              outerStartedMonotonic=outer.started,actualOuterDeadlineMonotonic=outer.deadline,parentPid=os.getpid(),childPid=process.pid,parentJobHandle=int(job.handle),guardSha256=outer.p.GUARD_SHA)
                import json
                raw=json.dumps(envelope,allow_nan=False).encode('ascii')
                if len(raw)>4096:raise ValueError('ownership envelope bound')
                if os.write(outer.write_fd,raw)!=len(raw):raise ValueError('complete one-use launch envelope write')
                os.close(outer.write_fd);outer.write_fd=None;outer.record=envelope
                job.resume(process)
        return BoundJob()
    def launch(self,argv,**kwargs):
        info=subprocess.STARTUPINFO();info.lpAttributeList={'handle_list':[self.handle]}
        # Native guard still creates suspended+no-window; ownership pipe alone is inherited.
        try:return subprocess.Popen(argv,**kwargs,startupinfo=info,close_fds=True)
        finally:
            if self.read_fd is not None:os.close(self.read_fd);self.read_fd=None
    def close(self):
        for name in ['read_fd','write_fd']:
            fd=getattr(self,name)
            if fd is not None:os.close(fd);setattr(self,name,None)
