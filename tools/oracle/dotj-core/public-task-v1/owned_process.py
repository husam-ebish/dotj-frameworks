"""Task-fixture-only Windows process ownership. No PID-based or global cleanup.

Children start suspended, enter a kill-on-close Job, then resume through their
owned process handle. The outer controller Job bounds the entire descendant
tree if the Python inner coordinator stalls. Output goes directly to files;
there is no interrupted communicate()/lost final pipe-drain window.
"""
import ctypes
import subprocess
import time
from ctypes import wintypes as w
from pathlib import Path

OUTPUT_POLL_SECONDS=0.1
OUTPUT_LIMITS={
    'compiler':{'stdout':2*1024**2,'stderr':2*1024**2},
    'runtime':{'stdout':2*1024**2,'stderr':512*1024},
    'controller':{'stdout':2*1024**2,'stderr':512*1024},
}

def output_profile(label):
    return 'controller' if label=='controller' else 'compiler' if label.startswith('compile-') else 'runtime'

class Job:
    def __init__(self):
        self.k=ctypes.WinDLL('kernel32',use_last_error=True)
        self.n=ctypes.WinDLL('ntdll',use_last_error=True)
        self.k.CreateJobObjectW.argtypes=[w.LPVOID,w.LPCWSTR]; self.k.CreateJobObjectW.restype=w.HANDLE
        self.k.SetInformationJobObject.argtypes=[w.HANDLE,ctypes.c_int,w.LPVOID,w.DWORD]; self.k.SetInformationJobObject.restype=w.BOOL
        self.k.AssignProcessToJobObject.argtypes=[w.HANDLE,w.HANDLE]; self.k.AssignProcessToJobObject.restype=w.BOOL
        self.k.TerminateJobObject.argtypes=[w.HANDLE,w.UINT]; self.k.TerminateJobObject.restype=w.BOOL
        self.k.CloseHandle.argtypes=[w.HANDLE]; self.k.CloseHandle.restype=w.BOOL
        self.k.QueryInformationJobObject.argtypes=[w.HANDLE,ctypes.c_int,w.LPVOID,w.DWORD,w.LPVOID];self.k.QueryInformationJobObject.restype=w.BOOL
        self.n.NtResumeProcess.argtypes=[w.HANDLE]; self.n.NtResumeProcess.restype=ctypes.c_long
        class Basic(ctypes.Structure):
            _fields_=[('processTime',ctypes.c_longlong),('jobTime',ctypes.c_longlong),('flags',w.DWORD),('minWS',ctypes.c_size_t),('maxWS',ctypes.c_size_t),('active',w.DWORD),('affinity',ctypes.c_size_t),('priority',w.DWORD),('scheduling',w.DWORD)]
        class IO(ctypes.Structure):
            _fields_=[(x,ctypes.c_ulonglong) for x in ['readOps','writeOps','otherOps','readBytes','writeBytes','otherBytes']]
        class Extended(ctypes.Structure):
            _fields_=[('basic',Basic),('io',IO),('processMemory',ctypes.c_size_t),('jobMemory',ctypes.c_size_t),('peakProcess',ctypes.c_size_t),('peakJob',ctypes.c_size_t)]
        self.handle=self.k.CreateJobObjectW(None,None)
        if not self.handle:raise ctypes.WinError(ctypes.get_last_error())
        limits=Extended(); limits.basic.flags=0x2000 # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.k.SetInformationJobObject(self.handle,9,ctypes.byref(limits),ctypes.sizeof(limits)):
            self.close(); raise ctypes.WinError(ctypes.get_last_error())
    def assign(self,process):
        if not self.k.AssignProcessToJobObject(self.handle,w.HANDLE(int(process._handle))):raise ctypes.WinError(ctypes.get_last_error())
    def resume(self,process):
        status=self.n.NtResumeProcess(w.HANDLE(int(process._handle)))
        if status!=0:raise OSError('NtResumeProcess failed: '+str(status))
    def terminate(self):
        if not self.k.TerminateJobObject(self.handle,125):raise ctypes.WinError(ctypes.get_last_error())
    def empty(self):
        class Accounting(ctypes.Structure):
            _fields_=[(x,ctypes.c_longlong) for x in ['user','kernel','periodUser','periodKernel']]+[(x,w.DWORD) for x in ['faults','total','active','terminated']]
        info=Accounting()
        if not self.k.QueryInformationJobObject(self.handle,1,ctypes.byref(info),ctypes.sizeof(info),None):raise ctypes.WinError(ctypes.get_last_error())
        return info.active==0
    def close(self):
        if self.handle:
            handle,self.handle=self.handle,None
            if not self.k.CloseHandle(handle):raise ctypes.WinError(ctypes.get_last_error())

def run(argv,cwd,env,label,timeout,*,launch=None,job_factory=None,now=None,on_update=None,prelaunch=None,stream_limits=None):
    """One attempt, 100ms growth checks, five-second owned cleanup, raw retention.

    Limits trigger termination, not truncation. Output can exceed a threshold
    between checks and during shutdown; the retained size reports that overshoot.
    """
    launch=launch or subprocess.Popen; job_factory=job_factory or Job; now=now or time.monotonic
    cwd=Path(cwd); started=now(); process=None; job=None; assigned=False
    record={'argv':[str(x) for x in argv],'cwd':str(cwd),'timeoutSeconds':timeout,'cleanupLimitSeconds':5,'launched':False,'timedOut':False}
    limits=dict(stream_limits or OUTPUT_LIMITS[output_profile(label)])
    if set(limits)!={'stdout','stderr'} or any(type(n) is not int or n<=0 for n in limits.values()):raise ValueError('positive per-stream output limits required')
    record.update(outputProfile=output_profile(label),outputLimitsBytes=limits,outputPollSeconds=OUTPUT_POLL_SECONDS,outputLimitExceeded=False)
    paths={stream:cwd/(label+'.'+stream) for stream in ['stdout','stderr']}
    record.update(stdoutPath=str(paths['stdout']),stderrPath=str(paths['stderr']))
    on_update=on_update or (lambda record:None)
    def sample_output():
        sizes={name:path.stat().st_size for name,path in paths.items()}
        record['outputSizesBytes']=sizes
        overflow={name:{'limitBytes':limits[name],'observedBytes':size} for name,size in sizes.items() if size>limits[name]}
        if overflow:
            record.update(outputLimitExceeded=True,outputOverflow=overflow,failureReason='OUTPUT_LIMIT_EXCEEDED')
        return bool(overflow)
    on_update(record)
    try:
        with paths['stdout'].open('xb') as stdout,paths['stderr'].open('xb') as stderr:
            try:
                job=job_factory()
                if prelaunch is not None:prelaunch()
                process=launch(record['argv'],cwd=cwd,env=env,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,
                               creationflags=0x00000004|0x08000000) # suspended + no window
                record.update(launched=True,processId=process.pid)
                on_update(record)
                job.assign(process); assigned=True; job.resume(process)
                record['jobAssigned']=True;record['resumed']=True;on_update(record)
                while True:
                    if sample_output():on_update(record);break
                    remaining=timeout-(now()-started)
                    if remaining<=0:raise subprocess.TimeoutExpired(argv,timeout)
                    if process.poll() is not None:break
                    try:process.wait(timeout=min(OUTPUT_POLL_SECONDS,remaining))
                    except subprocess.TimeoutExpired:pass # one absolute deadline, never restart the timeout
            except subprocess.TimeoutExpired:
                record['timedOut']=True
            except BaseException as error:
                record['error']=str(error)
            finally:
                cleanup_start=now(); cleanup_deadline=cleanup_start+5
                try:
                    if process is not None and process.poll() is None:
                        if assigned:job.terminate()
                        else:process.kill() # owned HANDLE; unassigned child is still suspended
                    elif assigned and not job.empty():
                        job.terminate() # exited root may still own descendants; handle remains authoritative
                    if assigned:
                        while not job.empty():
                            remaining=cleanup_deadline-now()
                            if remaining<=0:raise TimeoutError('owned job descendants did not exit within cleanup budget')
                            time.sleep(min(0.01,remaining))
                    if job is not None:job.close(); job=None # kills any still-owned descendants even if root exited
                    if process is not None:
                        remaining=cleanup_deadline-now()
                        if remaining<=0:raise TimeoutError('cleanup budget exhausted')
                        process.wait(timeout=remaining)
                except BaseException as error:record['cleanupError']=str(error)
                finally:
                    if job is not None:
                        try:job.close()
                        except BaseException as error:record['cleanupError']=str(error)
                record['cleanupSeconds']=now()-cleanup_start
                if record['cleanupSeconds']>5:record['cleanupError']='cleanup exceeded five seconds'
                record['exitCode']=process.returncode if process is not None else None
    finally:
        record['seconds']=now()-started
        record['stdoutPath']=str(paths['stdout']); record['stderrPath']=str(paths['stderr'])
        if all(path.exists() for path in paths.values()):sample_output() # include exited-root/final-write overflow
        on_update(record)
    return record

def memory():
    """Synchronous, bounded local Win32 query; no CIM child or shell."""
    class Status(ctypes.Structure):
        _fields_=[('length',w.DWORD),('load',w.DWORD)]+[(name,ctypes.c_ulonglong) for name in ['totalPhysical','freePhysical','totalCommit','freeCommit','totalVirtual','freeVirtual','extendedVirtual']]
    s=Status(); s.length=ctypes.sizeof(s)
    k=ctypes.WinDLL('kernel32',use_last_error=True)
    k.GlobalMemoryStatusEx.argtypes=[ctypes.POINTER(Status)]; k.GlobalMemoryStatusEx.restype=w.BOOL
    if not k.GlobalMemoryStatusEx(ctypes.byref(s)):raise ctypes.WinError(ctypes.get_last_error())
    # ullAvailPageFile is available system commit, NOT process virtual address space.
    return {'freePhysicalBytes':s.freePhysical,'freeVirtualBytes':s.freeCommit}

def resource_ready(sample):
    return all(type(sample.get(k)) is int and sample[k]>=floor for k,floor in [('freePhysicalBytes',512*1024**2),('freeVirtualBytes',16*1024**3)])

def wait_resources(deadline,*,query=None,now=None,sleep=None):
    query=query or memory; now=now or time.monotonic; sleep=sleep or time.sleep
    end=min(now()+120,deadline-35); samples=[]
    while now()<end:
        start=now(); sample=query(); finished=now(); samples.append(sample)
        if finished-start>2:raise ValueError('local memory query exceeded two-second freshness bound')
        if resource_ready(sample) and finished<end:return finished,samples
        delay=min(5,end-now())
        if delay>0:sleep(delay)
    raise ValueError('resource floor unavailable; no child launched')
