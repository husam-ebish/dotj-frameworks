"""New JDK-specific capability, using fixed qualified ownership mechanics.
No native producer import or constant retarget. Win32 is the explicit OS boundary.
"""
import ctypes
import json
import os
import subprocess
import time
from ctypes import wintypes as w
import jdk_contract as c
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


def consume(handle, operation, source, review, policy):
    c.capability_handle(handle)
    k=ctypes.WinDLL('kernel32',use_last_error=True)
    k.GetFileType.argtypes=[w.HANDLE];k.GetFileType.restype=w.DWORD
    c.require(k.GetFileType(w.HANDLE(handle))==3,'inherited pipe required')
    available=w.DWORD()
    k.PeekNamedPipe.argtypes=[w.HANDLE,w.LPVOID,w.DWORD,w.LPVOID,ctypes.POINTER(w.DWORD),w.LPVOID];k.PeekNamedPipe.restype=w.BOOL
    if not k.PeekNamedPipe(w.HANDLE(handle),None,0,None,ctypes.byref(available),None):raise ctypes.WinError(ctypes.get_last_error())
    c.require(0<available.value<=4096,'complete bounded capability before resume')
    import msvcrt
    fd=msvcrt.open_osfhandle(handle,os.O_RDONLY)
    try:raw=os.read(fd,available.value)
    finally:os.close(fd)
    e=c.loads(raw)
    deadline=c.validate_envelope(e,operation=operation,source=source,review=review,policy=policy,
                                 parent_pid=os_parent_pid(),child_pid=os.getpid(),now=time.monotonic())
    proof=verify_job(e,str(c.PYTHON/'python.exe'))
    return e,proof,deadline


class LaunchCapability:
    def __init__(self,guard,operation,source,review,policy,started):
        self.guard=guard;self.operation=operation;self.source=source;self.review=review;self.policy=policy
        self.started=started;self.deadline=started+900;self.use=c.OneUse();self.record=None
        self.read_fd,self.write_fd=os.pipe()
        import msvcrt
        self.handle=msvcrt.get_osfhandle(self.read_fd);os.set_handle_inheritable(self.handle,True)

    def job_factory(self):
        outer=self;job=self.guard.Job()
        class BoundJob:
            def __getattr__(self,name):return getattr(job,name)
            def resume(self,process):
                e=dict(schemaVersion=1,operation=outer.operation,attemptId=outer.operation+'-attempt01',
                       sourceLockSha256=outer.source,reviewSha256=outer.review,policySha256=outer.policy,
                       guardSha256=c.GUARD_SHA,outerStartedMonotonic=outer.started,actualOuterDeadlineMonotonic=outer.deadline,
                       parentPid=os.getpid(),childPid=process.pid,parentJobHandle=int(job.handle))
                raw=json.dumps(e,allow_nan=False).encode('ascii')
                c.require(len(raw)<=4096,'bounded capability')
                c.require(os.write(outer.write_fd,raw)==len(raw),'complete one-use envelope')
                os.close(outer.write_fd);outer.write_fd=None;outer.record=e;job.resume(process)
        return BoundJob()

    def launch(self,argv,**kwargs):
        self.use.take()
        info=subprocess.STARTUPINFO();info.lpAttributeList={'handle_list':[self.handle]}
        try:return subprocess.Popen(argv,**kwargs,startupinfo=info,close_fds=True)
        finally:
            if self.read_fd is not None:os.close(self.read_fd);self.read_fd=None

    def close(self):
        for name in ['read_fd','write_fd']:
            fd=getattr(self,name)
            if fd is not None:os.close(fd);setattr(self,name,None)

