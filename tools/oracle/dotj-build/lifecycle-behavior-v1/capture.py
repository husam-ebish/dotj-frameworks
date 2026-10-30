"""One fresh sequential eight-scenario pass; invoke only in a root-granted runtime window."""
import argparse
import datetime
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import uuid

# The pinned embedded Python deliberately omits the script directory from sys.path.
_spec=importlib.util.spec_from_file_location('dotj_lifecycle_verify',Path(__file__).with_name('verify.py'))
verify=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(verify)

def load_resource_guard():
    path=verify.REPO/'dotj-build/evaluation-candidate/verify.py'
    verify.require(verify.sha(path)=='06f2801799fce596a4154080d5f44b69fde82c19871103ed4af26f74261c0dce','reviewed resource helper bytes differ')
    spec=importlib.util.spec_from_file_location('reviewed_candidate_resource_guard',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def run_native_command(label,argv,out,env,overrides,record,save,guard,aggregate_deadline):
    def aggregate_check():
        if time.monotonic() >= aggregate_deadline-35:
            record.update(status='AGGREGATE_BUDGET_EXHAUSTED',failedBefore=label)
            save()
            raise RuntimeError('cooperative aggregate budget exhausted before '+label+'; no new native process launched')
    def guard_save():
        save()
        if record['status'] not in ['RESOURCE_QUERY_FAILED','DEFERRED_RESOURCES']:
            aggregate_check()
    aggregate_check()
    deadline=guard.wait_for_resources(label,out,env,record,guard_save)
    child=env.copy();trace=out/'logs'/(label+'.host-trace.txt')
    child.update(DOTNET_HOST_TRACE='1',DOTNET_HOST_TRACEFILE=str(trace))
    arguments=list(map(str,argv))
    command={'label':label,'argv':arguments,'cwd':str(out),'environmentOverrides':overrides,'nativeTimeoutSeconds':30}
    record['commands'].append(command);save()
    now=time.monotonic();record['resourceWaits'][-1]['seconds']=now-(deadline-120)
    if now>=deadline:
        record['commands'].pop();guard.defer_resources(label,deadline,record,save)
    if now>=aggregate_deadline-35:
        record['commands'].pop();aggregate_check()
    streams=[];process=None;execution_start=time.monotonic()
    try:
        process=subprocess.Popen(arguments,cwd=out,env=child,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        command['processId']=process.pid;save()
        remaining=30-(time.monotonic()-execution_start)
        if remaining<=0:raise subprocess.TimeoutExpired(arguments,30)
        stdout,stderr=process.communicate(timeout=remaining)
        command['exitCode']=process.returncode;streams=[('stdout',stdout),('stderr',stderr)]
    except subprocess.TimeoutExpired:
        command['timeout']=True
        if process is not None:
            process.kill()
            try:stdout,stderr=process.communicate(timeout=5)
            except subprocess.TimeoutExpired as error:
                command['cleanupError']='native stream drain exceeded5 seconds'
                streams=[('stdout',error.stdout or b''),('stderr',error.stderr or b'')]
            else:streams=[('stdout',stdout),('stderr',stderr)]
        raise
    finally:
        if process is not None and process.poll() is None:
            process.kill()
            try:stdout,stderr=process.communicate(timeout=5)
            except subprocess.TimeoutExpired as error:
                command['cleanupError']='native final cleanup exceeded5 seconds'
                streams=[('stdout',error.stdout or b''),('stderr',error.stderr or b'')]
            else:streams=[('stdout',stdout),('stderr',stderr)]
        for suffix,data in streams:
            log=out/'logs'/(label+'.'+suffix);log.write_bytes(data)
            command[suffix]={'path':str(log),'sha256':verify.sha(log)}
        if trace.exists():command['hostTrace']={'path':str(trace),'sha256':verify.sha(trace)}
        save()
    if command['exitCode']!=0 or stderr!=b'':
        raise RuntimeError(label+' failed; retained logs')
    return command,stdout

def main():
    aggregate_deadline=time.monotonic()+540
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args(); out=args.out.resolve()
    verify.require(os.name=='nt' and out.is_relative_to(verify.ROOT) and out!=verify.ROOT and not out.exists(),'new private D: output required')
    out.mkdir(parents=True)
    record={'schemaVersion':1,'status':'RUNNING','runId':str(uuid.uuid4()),'commands':[],'resources':[],
            'fixtureRoot':str(out/'fixtures'),'limits':{'heapMiB':128,'processors':2,'timeoutSeconds':30,
                'queryTimeoutSeconds':20,'minFreePhysicalKiB':524288,'minFreeVirtualKiB':16777216,
                'resourceWaitSeconds':120,'resourcePollSeconds':5,'aggregateCaptureSeconds':540,'nativeCleanupReserveSeconds':35},
            'acceptedTasksAdded':0,'publicQualification':False}
    def save(): (out/'capture.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    save()
    try:
        lock=verify.verify_inputs()
        guard=load_resource_guard()
        record['inputLockSha256']=verify.sha(verify.EVIDENCE/'lifecycle-behavior-input-lock-v1.json')
        for name in ['tmp','home','cache','logs']: (out/name).mkdir()
        shutil.copytree(verify.HERE/'fixtures',out/'fixtures')
        for path in [verify.HERE/'CaptureLifecycleBehaviorV1.cs',verify.HERE/'capture.py',
                     verify.EVIDENCE/'lifecycle-behavior-plan-v1.json',verify.EVIDENCE/'lifecycle-behavior-input-lock-v1.json']:
            shutil.copyfile(path,out/path.name)
        env=os.environ.copy()
        for key in list(env):
            if key.upper().startswith(('MSBUILD','DOTNET_','COMPLUS_','CORECLR_','COR_')) or key in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS']:
                env.pop(key)
        overrides=dict(TEMP=str(out/'tmp'),TMP=str(out/'tmp'),USERPROFILE=str(out/'home'),HOME=str(out/'home'),
            APPDATA=str(out/'home/AppData/Roaming'),LOCALAPPDATA=str(out/'home/AppData/Local'),
            DOTNET_ROOT=str(verify.ROOT/'toolchains/dotnet'),DOTNET_CLI_HOME=str(out/'home'),NUGET_PACKAGES=str(out/'cache'),
            DOTNET_CLI_TELEMETRY_OPTOUT='1',DOTNET_SKIP_FIRST_TIME_EXPERIENCE='1',DOTNET_NOLOGO='1',
            DOTNET_MULTILEVEL_LOOKUP='0',DOTNET_ROLL_FORWARD='Disable',DOTNET_CLI_UI_LANGUAGE='en-US',VSLANG='1033',
            MSBUILD_EXE_PATH=str(verify.ROOT/'toolchains/dotnet/sdk/10.0.401/MSBuild.dll'),
            MSBUILDDISABLENODEREUSE='1',MSBUILDUSEREXTENSIONSPATH=str(out/'home/msbuild-user'),
            DOTNET_GCHeapHardLimit='8000000',DOTNET_gcServer='0',DOTNET_PROCESSOR_COUNT='2')
        env.update(overrides)
        def run(label,argv):
            return run_native_command(label,argv,out,env,overrides,record,save,guard,aggregate_deadline)
        sdk=verify.ROOT/'toolchains/dotnet/sdk/10.0.401';dotnet=verify.ROOT/'toolchains/dotnet/dotnet.exe'
        binary=out/'CaptureLifecycleBehaviorV1.dll'
        references=[verify.ROOT/p for p in lock['compilerReferences']]
        run('compile',[str(dotnet),'exec',str(sdk/'Roslyn/bincore/csc.dll'),'/nologo','/noconfig','/nostdlib+',
            '/target:exe','/nullable:enable','/deterministic+','/langversion:14','/out:'+str(binary),
            *['/reference:'+str(p) for p in references],str(out/'CaptureLifecycleBehaviorV1.cs')])
        config=out/'CaptureLifecycleBehaviorV1.runtimeconfig.json'
        config.write_text(json.dumps(lock['runtimeConfig'],indent=2)+'\n',encoding='utf-8')
        record['binary']={'path':str(binary),'sha256':verify.sha(binary)}
        record['runtimeConfig']={'path':str(config),'sha256':verify.sha(config)}
        plan=verify.read(verify.EVIDENCE/'lifecycle-behavior-plan-v1.json')
        for scenario in plan['scenarios']:
            command,stdout=run(scenario['id'],[str(dotnet),'exec','--runtimeconfig',str(config),
                '--depsfile',str(sdk/'MSBuild.deps.json'),str(binary),str(out/'fixtures'),scenario['id']])
            command['parsed']=json.loads(stdout)
            verify.validate_payload(command['parsed'],scenario)
            save()
        verify.verify_inputs(); verify.verify_fixtures(out/'fixtures')
        record['status']='PASS_NATIVE_LIFECYCLE_PASS';save()
        verify.validate_capture(out/'capture.json')
    except Exception as error:
        record.update(failureStatusBeforeFinal=record['status'],status='FAILED',error=str(error));save();raise
    print(json.dumps({'status':record['status'],'report':str(out/'capture.json')}))

if __name__=='__main__': main()
