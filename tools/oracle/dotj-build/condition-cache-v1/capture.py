"""Standalone future native capture. Run only after separate root grant; never retries."""
import argparse,datetime,importlib.util,json,os,shutil,subprocess,time,uuid
from pathlib import Path
s=importlib.util.spec_from_file_location('cache_verify',Path(__file__).with_name('verify.py'));v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
HELPER=v.B/'orchestration/two-frameworks/task-19-capture-phase-v4.py'
QUERY=Path(r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe')
TASKKILL=Path(r'C:\Windows\System32\taskkill.exe')
MEMORY_SCRIPT='$ErrorActionPreference="Stop";$m=Get-CimInstance Win32_OperatingSystem;[pscustomobject]@{freeVirtualKiB=[uint64]$m.FreeVirtualMemory;freePhysicalKiB=[uint64]$m.FreePhysicalMemory}|ConvertTo-Json -Compress'
def environment(out,parent):
    env={k:x for k,x in parent.items() if not k.upper().startswith(('MSBUILD','DOTNET_','COMPLUS_','CORECLR_','COR_')) and k.upper() not in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS','JDK_JAVA_OPTIONS','JDK_JAVAC_OPTIONS','PYTHONPATH','PYTHONHOME','CLASSPATH','COREHOST_TRACE','COREHOST_TRACEFILE']}
    overrides=dict(TEMP=str(out/'tmp'),TMP=str(out/'tmp'),USERPROFILE=str(out/'home'),HOME=str(out/'home'),APPDATA=str(out/'home/AppData/Roaming'),LOCALAPPDATA=str(out/'home/AppData/Local'),DOTNET_ROOT=str(v.B/'toolchains/dotnet'),DOTNET_CLI_HOME=str(out/'home'),NUGET_PACKAGES=str(out/'cache'),DOTNET_CLI_TELEMETRY_OPTOUT='1',DOTNET_SKIP_FIRST_TIME_EXPERIENCE='1',DOTNET_NOLOGO='1',DOTNET_MULTILEVEL_LOOKUP='0',DOTNET_ROLL_FORWARD='Disable',DOTNET_CLI_UI_LANGUAGE='en-US',VSLANG='1033',MSBUILD_EXE_PATH=str(v.B/'toolchains/dotnet/sdk/10.0.401/MSBuild.dll'),MSBUILDDISABLENODEREUSE='1',MSBUILDUSEREXTENSIONSPATH=str(out/'home/msbuild-user'),DOTNET_GCHeapHardLimit='8000000',DOTNET_gcServer='0',DOTNET_PROCESSOR_COUNT='2',DOTNET_HOST_TRACE='1',DOTNET_HOST_TRACEFILE=str(out/'logs/native.host-trace.txt'))
    for k in list(env):
        if k.upper() in {name.upper() for name in overrides}:env.pop(k)
    env.update(overrides);return env,overrides

def wait_resources(out,env,record,save,aggregate_deadline,query=None,now=None,sleep=None):
    now=now or time.monotonic;sleep=sleep or time.sleep;start=now();deadline=min(start+120,aggregate_deadline-35)
    record['resourceWait']={'status':'WAITING','limitSeconds':120,'pollSeconds':5,'queryTimeoutSeconds':20,'seconds':0};record['resources']=[]
    def default_query(timeout):
        p=subprocess.run([str(QUERY),'-NoLogo','-NoProfile','-Command',MEMORY_SCRIPT],cwd=out,env=env,capture_output=True,timeout=timeout,check=True)
        return json.loads(p.stdout)
    query=query or default_query
    while now()<deadline:
        poll=now()
        try:
            memory=query(min(20,deadline-now()));ready=v.validate_memory(memory)
        except Exception:
            record['resourceWait'].update(status='QUERY_FAILED_NO_NATIVE_LAUNCH',seconds=now()-start);save();raise
        sampled=now();record['resources'].append(dict(memory,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),waitSeconds=sampled-start));record['resourceWait']['seconds']=sampled-start
        if ready and sampled<deadline:
            record['resourceWait']['status']='READY';save();return sampled
        save();delay=min(5-(now()-poll),deadline-now())
        if delay>0:sleep(delay)
    record['resourceWait'].update(status='DEFERRED_NO_NATIVE_LAUNCH',seconds=now()-start);save();raise ValueError('resource/aggregate wait exhausted before native launch')

def helper(lock):
    item=next(x for x in lock['executionPins'] if x['path']==str(HELPER));v.require(v.sha(HELPER)==item['sha256'],'owned cleanup helper changed')
    return v.load('unchanged_task19_owned_cleanup_function',HELPER)

def run_native(command,out,env,record,save,launch=None,now=None,cleanup=None):
    launch=launch or subprocess.Popen;now=now or time.monotonic;cleanup=cleanup or subprocess.run;start=now();process=None;stdout=stderr=b'';streams_recovered=False
    command['nativeCleanupTimeoutSeconds']=5
    try:
        process=launch(command['argv'],cwd=out,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        command['processId']=process.pid;record['nativeLaunched']=True;save()
        remaining=30-(now()-start)
        if remaining<=0:raise subprocess.TimeoutExpired(command['argv'],30)
        stdout,stderr=process.communicate(timeout=remaining);streams_recovered=True
        command['exitCode']=process.returncode
    except subprocess.TimeoutExpired as error:
        command['timeout']=True;stdout=error.stdout or b'';stderr=error.stderr or b'';raise
    finally:
        # Exit status and pipe recovery are separate. Even an exited process can
        # still have complete buffered streams after communicate was interrupted.
        live=process is not None and process.poll() is None
        if process is not None and (live or not streams_recovered):
            cleanup_start=now();cleanup_deadline=cleanup_start+5
            details={'limitSeconds':5,'killBudgetSeconds':2,'killAttempted':False,'recoveryCompleted':False};command['nativeCleanup']=details
            if live:
                killed_out=killed_err=b''
                try:
                    kill_remaining=cleanup_deadline-now()
                    if kill_remaining<=0:raise subprocess.TimeoutExpired([],0)
                    details.update(killAttempted=True,argv=[str(TASKKILL),'/PID',str(process.pid),'/T','/F'],cwd=str(out),environmentSha256=v.sha_environment(env))
                    result=cleanup(details['argv'],cwd=out,env=env,capture_output=True,timeout=min(2,kill_remaining))
                    killed_out,killed_err=result.stdout,result.stderr;details['exitCode']=result.returncode
                    if result.returncode!=0:command['cleanupError']='owned native taskkill failed'
                except (OSError,subprocess.SubprocessError) as error:
                    details['error']=str(error);killed_out=getattr(error,'stdout',None) or b'';killed_err=getattr(error,'stderr',None) or b'';command['cleanupError']='owned native taskkill failed or exhausted2-second budget'
                finally:
                    if details['killAttempted']:
                        for name,data in [('stdout',killed_out),('stderr',killed_err)]:
                            p=out/'logs'/('native-cleanup.'+name);p.write_bytes(data);details[name]=v.descriptor(p)
            # Use this same deadline whether the process was live or had exited.
            remaining=cleanup_deadline-now()
            if remaining>0:
                try:
                    stdout,stderr=process.communicate(timeout=remaining);streams_recovered=True;details['recoveryCompleted']=True
                except (OSError,subprocess.SubprocessError) as error:
                    if getattr(error,'stdout',None) is not None:stdout=error.stdout
                    if getattr(error,'stderr',None) is not None:stderr=error.stderr
                    details['recoveryError']=str(error);command['cleanupError']='native stream recovery failed within remaining total5-second cleanup budget'
            else:command['cleanupError']='native cleanup exceeded total5-second deadline;no additional drain'
            details['seconds']=now()-cleanup_start
            if details['seconds']>5:command['cleanupError']='native cleanup exceeded total5-second deadline'
        if process is not None:command['exitCode']=process.returncode
        command['seconds']=now()-start;command['finishedUtc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        for name,data in [('stdout',stdout),('stderr',stderr)]:
            p=out/'logs'/('native.'+name);p.write_bytes(data);command[name]=v.descriptor(p)
        trace=out/'logs/native.host-trace.txt'
        if trace.exists():command['hostTrace']=v.descriptor(trace)
        save()
    return stdout,stderr


def inner(a):
    started=time.monotonic();aggregate_deadline=started+540;out=a.out.resolve()
    lock,plan,fp=v.verify_inputs(a.input_lock_sha256);v.verify_checkpoint(a.checkpoint,a.checkpoint_sha256,a.input_lock_sha256)
    v.require(out.is_relative_to(v.PRIVATE) and (out/'controller.json').exists() and not (out/'capture.json').exists(),'fresh owned controller output required')
    record=dict(schemaVersion=1,status='PREPARING',runId=str(uuid.uuid4()),inputLockSha256=a.input_lock_sha256,checkpointSha256=a.checkpoint_sha256,fixtureRoot=str(out/'fixtures'),limits=lock['limits'],commands=[],resources=[],nativeLaunched=False,acceptedTasksAdded=0)
    def save():v.write(out/'capture.json',record)
    save();command=None;stdout=stderr=b''
    try:
        for name in ['home','cache','logs']:(out/name).mkdir()
        shutil.copytree(v.D/'fixtures',out/'fixtures')
        for item in lock['copiedInputs']:
            source={'repo':v.R,'root':v.B}[item['base']]/item['path'];target=out/item['target'];shutil.copyfile(source,target);v.require(v.sha(target)==item['sha256'],'copied input drift')
        env,overrides=environment(out,os.environ.copy())
        sampled=wait_resources(out,env,record,save,aggregate_deadline)
        # No mutation or long work between this final typed reading and launch.
        age=time.monotonic()-sampled
        v.require(age<=2 and time.monotonic()<aggregate_deadline-35,'resource sample expired before launch; no native launch')
        command=dict(label='native-condition-cache-v1',argv=v.native_argv(out),cwd=str(out),environmentOverrides=overrides,nativeTimeoutSeconds=30,resourceAgeSeconds=age,startedUtc=datetime.datetime.now(datetime.timezone.utc).isoformat());record['commands'].append(command);record['status']='LAUNCHING';save()
        v.require(time.monotonic()-sampled<=2 and time.monotonic()<aggregate_deadline-35,'resource sample expired while saving launch record')
        stdout,stderr=run_native(command,out,env,record,save)
        v.validate_process(command);v.require(stderr==b'','native stderr unexpected; raw evidence retained')
        record['payload']=json.loads(stdout);save()
        v.validate_payload(record['payload'],plan,fp,str(out/'fixtures'));v.verify_fixtures(out/'fixtures',plan);v.verify_inputs(a.input_lock_sha256)
        v.require(time.monotonic()<aggregate_deadline,'aggregate capture budget exhausted after native process;retain and stop')
        record['aggregateSeconds']=time.monotonic()-started
        record['status']='CAPTURED_PENDING_ROOT_REVIEW';save();v.validate_capture(out/'capture.json',a.input_lock_sha256,a.checkpoint,a.checkpoint_sha256)
    except Exception as error:
        record.update(status='FAILED_UNRESOLVED_CLEANUP' if command is not None and command.get('cleanupError') else 'FAILED_STOP_NO_RETRY' if record['nativeLaunched'] else 'STOPPED_PROVABLY_NO_NATIVE_LAUNCH',error=str(error));save();raise
    return {'status':record['status'],'report':str(out/'capture.json')}

def run_outer(guard,command,out,environment,overrides,backend=None):
    adapter=v.load('reviewed_condition_cache_outer_cleanup_adapter',Path(__file__).with_name('outer_cleanup_adapter.py'))
    return adapter.run_capture_process(guard,command['argv'],v.R,environment,command,cleanup_cwd=out,taskkill=TASKKILL,environment_overrides=overrides,timeout=600,backend=backend)

def controller(a):
    out=a.out.resolve();v.require(os.name=='nt' and out.is_relative_to(v.PRIVATE) and out!=v.PRIVATE and not out.exists(),'independent fresh private D: output required')
    lock,_,_=v.verify_inputs(a.input_lock_sha256);v.verify_checkpoint(a.checkpoint,a.checkpoint_sha256,a.input_lock_sha256);guard=helper(lock)
    out.mkdir();(out/'tmp').mkdir();env,overrides=environment(out,os.environ.copy())
    python=v.B/'toolchains/python-3.13.9/python.exe'
    command=dict(argv=[str(python),'-B',str(Path(__file__).resolve()),'--inner','--out',str(out),'--input-lock-sha256',a.input_lock_sha256,'--checkpoint',str(a.checkpoint.resolve()),'--checkpoint-sha256',a.checkpoint_sha256],cwd=str(v.R),environmentOverrides=overrides,timeoutSeconds=600)
    record=dict(status='RUNNING',command=command,outerCeilingSeconds=600);v.write(out/'controller.json',record);stdout=stderr=b''
    try:
        try:stdout,stderr=run_outer(guard,command,out,env,overrides)
        except subprocess.TimeoutExpired as error:stdout=error.stdout or b'';stderr=error.stderr or b'';raise
        v.validate_process(command);v.require(stderr==b'','inner stderr unexpected; retained')
        v.validate_capture(out/'capture.json',a.input_lock_sha256,a.checkpoint,a.checkpoint_sha256);record['status']='PASS_CAPTURE_CONTROLLER'
    except Exception as error:
        record.update(status='FAILED_STOP_NO_RETRY',error=str(error))
        if not isinstance(error,subprocess.TimeoutExpired) and (out/'capture.json').exists():
            child=v.read(out/'capture.json');native=child.get('commands',[])
            if child.get('nativeLaunched') is True and native and native[0].get('cleanupError'):
                record.update(status='FAILED_UNRESOLVED_CLEANUP',cleanupDisposition='No blind post-exit PID kill. Preserve ownership/creation evidence for root inspection;no retry.')

        raise
    finally:
        for name,data in [('stdout',stdout),('stderr',stderr)]:
            p=out/('controller.'+name);p.write_bytes(data);command[name]=v.descriptor(p)
        v.write(out/'controller.json',record)
    return {'status':record['status'],'report':str(out/'controller.json')}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inner',action='store_true');p.add_argument('--out',required=True,type=Path);p.add_argument('--input-lock-sha256',required=True);p.add_argument('--checkpoint',required=True,type=Path);p.add_argument('--checkpoint-sha256',required=True);a=p.parse_args()
    print(json.dumps(inner(a) if a.inner else controller(a)))
if __name__=='__main__':main()
