"""STATIC PREPARED: supplement native runtime requires a separate root grant."""
import argparse,importlib.util,json,os,shutil,time,uuid
from pathlib import Path
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
verify=load('exists_sites_verify',Path(__file__).with_name('verify.py'))
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True,type=Path);p.add_argument('--input-lock-sha256',required=True);p.add_argument('--checkpoint',required=True,type=Path);p.add_argument('--checkpoint-sha256',required=True);a=p.parse_args();out=a.out.resolve()
 verify.require(os.name=='nt' and out.is_relative_to(verify.ROOT) and out!=verify.ROOT and not out.exists(),'new private D: output required')
 verify.verify_checkpoint(a.checkpoint,a.checkpoint_sha256,a.input_lock_sha256);lock=verify.verify_inputs(a.input_lock_sha256)
 native=load('immutable_native_command_helper',verify.REPO/'tools/oracle/dotj-build/lifecycle-behavior-v1/capture.py');guard=native.load_resource_guard()
 out.mkdir(parents=True);cwd=out/'unrelated-cwd';r={'schemaVersion':1,'status':'RUNNING','runId':str(uuid.uuid4()),'commands':[],'resources':[],'fixtureRoot':str(out/'fixtures'),'workingDirectory':str(cwd),'inputLockSha256':a.input_lock_sha256,'checkpointSha256':a.checkpoint_sha256,'limits':lock['limits'],'copiedInputs':[],'acceptedTasksAdded':0,'numberedBatchCredit':0,'candidateComparisons':0,'compilerProcesses':0}
 def save():(out/'capture.json').write_bytes((json.dumps(r,indent=2)+'\n').encode())
 save();deadline=time.monotonic()+540
 try:
  for name in ['tmp','home','cache','unrelated-cwd/logs']:(out/name).mkdir(parents=True)
  shutil.copytree(verify.DATA/'fixtures',out/'fixtures')
  for item in lock['copiedInputs']:
   root={'root':verify.ROOT,'repo':verify.REPO}[item['base']];target=out/item['target'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/item['path'],target)
   verify.require(verify.sha(target)==item['sha256'],'copied source/binary input changed');r['copiedInputs'].append({'target':item['target'],'sha256':verify.sha(target)})
  plan=verify.read(verify.EVIDENCE/'plan.json');r['markerPlacement']=verify.validate_layout(out/'fixtures',cwd,plan)
  r['binary']={'path':str(out/'CaptureImports.dll'),'sha256':verify.sha(out/'CaptureImports.dll')};r['runtimeConfig']={'path':str(out/'CaptureImports.runtimeconfig.json'),'sha256':verify.sha(out/'CaptureImports.runtimeconfig.json')};save()
  env=os.environ.copy()
  for key in list(env):
   if key.upper().startswith(('MSBUILD','DOTNET_','COMPLUS_','CORECLR_','COR_')) or key in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS']:env.pop(key)
  overrides=dict(TEMP=str(out/'tmp'),TMP=str(out/'tmp'),USERPROFILE=str(out/'home'),HOME=str(out/'home'),APPDATA=str(out/'home/AppData/Roaming'),LOCALAPPDATA=str(out/'home/AppData/Local'),DOTNET_ROOT=str(verify.ROOT/'toolchains/dotnet'),DOTNET_CLI_HOME=str(out/'home'),NUGET_PACKAGES=str(out/'cache'),DOTNET_CLI_TELEMETRY_OPTOUT='1',DOTNET_SKIP_FIRST_TIME_EXPERIENCE='1',DOTNET_NOLOGO='1',DOTNET_MULTILEVEL_LOOKUP='0',DOTNET_ROLL_FORWARD='Disable',DOTNET_CLI_UI_LANGUAGE='en-US',VSLANG='1033',MSBUILD_EXE_PATH=str(verify.ROOT/'toolchains/dotnet/sdk/10.0.401/MSBuild.dll'),MSBUILDDISABLENODEREUSE='1',MSBUILDUSEREXTENSIONSPATH=str(out/'home/msbuild-user'),DOTNET_GCHeapHardLimit='8000000',DOTNET_gcServer='0',DOTNET_PROCESSOR_COUNT='2');env.update(overrides)
  argv=[str(verify.ROOT/'toolchains/dotnet/dotnet.exe'),'exec','--runtimeconfig',str(out/'CaptureImports.runtimeconfig.json'),'--depsfile',str(verify.ROOT/'toolchains/dotnet/sdk/10.0.401/MSBuild.deps.json'),str(out/'CaptureImports.dll'),str(out/'fixtures'),str(out/'plan.json')]
  command,stdout=native.run_native_command('native-two-sites',argv,cwd,env,overrides,r,save,guard,deadline)
  r['payload']=json.loads(stdout);verify.bind_stdout(command['stdout'],r['payload'],out);verify.validate_payload(r['payload'])
  verify.require(all(x['evaluation']['success'] is True for x in r['payload']['rows']),'native supplement case failed; retain evidence and stop without retry')
  r['markerPlacement']=verify.validate_layout(out/'fixtures',cwd,plan);verify.verify_inputs(a.input_lock_sha256)
  r['status']='PASS_NATIVE_EXISTS_SITES_CAPTURE';save();verify.validate_capture(out/'capture.json',a.input_lock_sha256,a.checkpoint,a.checkpoint_sha256)
 except Exception as e:r.update(failureStatusBeforeFinal=r['status'],status='FAILED',error=str(e));save();raise
 print(json.dumps({'status':r['status'],'report':str(out/'capture.json'),'nativeScenarioProcesses':1,'freshCollections':2,'compilerProcesses':0,'candidateComparisons':0}))
if __name__=='__main__':main()
