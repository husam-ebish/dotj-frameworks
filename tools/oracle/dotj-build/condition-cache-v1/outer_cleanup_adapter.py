"""Bind only the immutable task19 helper's owned-tree cleanup dependency.

The helper module receives a private subprocess facade for this synchronous call.
The standard-library module and the helper file are never modified. The helper's
600s child timeout,20s tree kill and5s+5s bounded drain behavior remain unchanged.
"""
import hashlib,json,subprocess
from pathlib import Path

def environment_sha256(environment):
    return hashlib.sha256(json.dumps(environment,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()

class _OwnedSubprocess:
    def __init__(self,backend,entry,cleanup_cwd,environment,taskkill,overrides):
        self._backend=backend;self._entry=entry;self._cwd=str(cleanup_cwd);self._environment=dict(environment);self._taskkill=str(taskkill);self._overrides=dict(overrides)
        self.PIPE=backend.PIPE;self.TimeoutExpired=backend.TimeoutExpired
    def Popen(self,*args,**kwargs):
        return self._backend.Popen(*args,**kwargs)
    def run(self,argv,**kwargs):
        pid=self._entry.get('processId')
        if type(pid) is not int or pid<=0:raise ValueError('actual owned helper child PID required for cleanup')
        expected=['taskkill','/PID',str(pid),'/T','/F']
        if list(argv)!=expected or kwargs!={'capture_output':True,'timeout':20}:raise ValueError('immutable helper cleanup call shape differs')
        cleanup=self._entry['treeCleanup'];actual=[self._taskkill,*expected[1:]]
        # Record the invocation sent to the backend,not ambient PATH inference.
        cleanup.update(requestedArgv=list(argv),argv=actual,cwd=self._cwd,environmentSha256=environment_sha256(self._environment),environmentOverrides=self._overrides,timeoutSeconds=20)
        return self._backend.run(actual,capture_output=True,timeout=20,cwd=self._cwd,env=self._environment)

def run_capture_process(helper,argv,cwd,environment,entry,*,cleanup_cwd,taskkill,environment_overrides,timeout=600,backend=None):
    if timeout!=600:raise ValueError('reviewed outer child timeout must remain600 seconds')
    cleanup_cwd=Path(cleanup_cwd).resolve();taskkill=Path(taskkill)
    if not cleanup_cwd.is_dir() or not taskkill.is_absolute():raise ValueError('existing owned cleanup directory and absolute pinned taskkill required')
    original=helper.subprocess
    if original is not subprocess:raise ValueError('fresh helper-local subprocess dependency required')
    facade=_OwnedSubprocess(backend or subprocess,entry,cleanup_cwd,environment,taskkill,environment_overrides)
    # Only this freshly loaded helper module's dependency name is rebound.
    helper.subprocess=facade
    try:return helper.run_capture_process(argv,cwd,environment,entry,timeout=timeout)
    finally:helper.subprocess=original
