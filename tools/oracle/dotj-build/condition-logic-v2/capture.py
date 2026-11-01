"""One root-granted, fresh logic-v2 capture using the qualified unchanged observer DLL."""
import argparse,importlib.util,json,os,shutil,time,uuid
from pathlib import Path
s=importlib.util.spec_from_file_location('logic_v2_verify',Path(__file__).with_name('verify.py'));v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
def environment(out,parent):
    child={k:val for k,val in parent.items() if not k.upper().startswith(('MSBUILD','DOTNET_','COMPLUS_','CORECLR_','COR_')) and k.upper() not in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS']}
    overrides=dict(TEMP=str(out/'tmp'),TMP=str(out/'tmp'),USERPROFILE=str(out/'home'),HOME=str(out/'home'),APPDATA=str(out/'home/AppData/Roaming'),LOCALAPPDATA=str(out/'home/AppData/Local'),DOTNET_ROOT=str(v.B/'toolchains/dotnet'),DOTNET_CLI_HOME=str(out/'home'),NUGET_PACKAGES=str(out/'cache'),DOTNET_CLI_TELEMETRY_OPTOUT='1',DOTNET_SKIP_FIRST_TIME_EXPERIENCE='1',DOTNET_NOLOGO='1',DOTNET_MULTILEVEL_LOOKUP='0',DOTNET_ROLL_FORWARD='Disable',DOTNET_CLI_UI_LANGUAGE='en-US',VSLANG='1033',MSBUILD_EXE_PATH=str(v.B/'toolchains/dotnet/sdk/10.0.401/MSBuild.dll'),MSBUILDDISABLENODEREUSE='1',MSBUILDUSEREXTENSIONSPATH=str(out/'home/msbuild-user'),DOTNET_GCHeapHardLimit='8000000',DOTNET_gcServer='0',DOTNET_PROCESSOR_COUNT='2')
    # Case-insensitive Windows environment keys: remove aliases before overlay.
    for key in list(child):
        if key.upper() in {x.upper() for x in overrides}:child.pop(key)
    child.update(overrides);return child,overrides

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);p.add_argument('--input-lock-sha256',required=True);p.add_argument('--checkpoint',type=Path,required=True);p.add_argument('--checkpoint-sha256',required=True);a=p.parse_args();out=a.out.resolve()
    v.require(os.name=='nt' and out.is_relative_to(v.B/'agents/validation-performance/condition-logic-v2-native-preparation-20261030') and not out.exists(),'fresh owned private output required')
    v.verify_checkpoint(a.checkpoint,a.checkpoint_sha256,a.input_lock_sha256);lock,plan=v.verify_inputs(a.input_lock_sha256)
    native=v.load('unchanged_owned_native_resource_helper',v.T.parent/'lifecycle-behavior-v1/capture.py');guard=native.load_resource_guard()
    out.mkdir(parents=True);record={'schemaVersion':1,'status':'RUNNING','runId':str(uuid.uuid4()),'commands':[],'resources':[],'limits':lock['limits'],'inputLockSha256':a.input_lock_sha256,'checkpointSha256':a.checkpoint_sha256,'fixtureRoot':str(out/'fixtures'),'acceptedTasksAdded':0,'numberedBatchCredit':0,'candidateComparisonsPerformed':0}
    def save():(out/'capture.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    save();deadline=time.monotonic()+540
    try:
        for name in ['tmp','home','cache','logs']:(out/name).mkdir()
        shutil.copytree(v.D/'fixtures',out/'fixtures')
        for item in lock['copiedInputs']:
            origin={'repo':v.R,'root':v.B}[item['base']]/item['path'];target=out/item['target'];shutil.copyfile(origin,target);v.require(v.sha(target)==item['sha256'],'copied input differs')
        env,overrides=environment(out,os.environ.copy())
        argv=[str(v.B/'toolchains/dotnet/dotnet.exe'),'exec','--runtimeconfig',str(out/'CaptureImports.runtimeconfig.json'),'--depsfile',str(v.B/'toolchains/dotnet/sdk/10.0.401/MSBuild.deps.json'),str(out/'CaptureImports.dll'),str(out/'fixtures'),str(out/'manifest.json')]
        command,stdout=native.run_native_command('native-logic-v2',argv,out,env,overrides,record,save,guard,deadline)
        record['payload']=json.loads(stdout);save();v.bind_stdout(command['stdout'],record['payload'],out)
        v.validate_payload(record['payload'],plan,lock);v.verify_fixtures(out/'fixtures',plan['fixtures']);v.verify_inputs(a.input_lock_sha256)
        record['status']='PASS_NATIVE_LOGIC_V2_CAPTURE';save();v.validate_capture(out/'capture.json',a.input_lock_sha256,a.checkpoint,a.checkpoint_sha256)
    except Exception as error:record.update(status='FAILED_STOP_NO_RETRY',error=str(error));save();raise
    print(json.dumps({'status':record['status'],'report':str(out/'capture.json'),'collections':len(plan['cases']),'nativeProcesses':1}))
if __name__=='__main__':main()
