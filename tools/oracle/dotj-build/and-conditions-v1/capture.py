"""One fresh eight-case native capture. Launch only after root's runtime grant."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import time
import uuid


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


verify=load('and_verify',Path(__file__).with_name('verify.py'))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True,type=Path)
    parser.add_argument('--input-lock-sha256',required=True)
    parser.add_argument('--checkpoint',required=True,type=Path)
    parser.add_argument('--checkpoint-sha256',required=True)
    args=parser.parse_args();out=args.out.resolve()
    verify.require(os.name=='nt' and out.is_relative_to(verify.ROOT) and out!=verify.ROOT and not out.exists(),'new private D: output required')
    verify.verify_checkpoint(args.checkpoint,args.checkpoint_sha256,args.input_lock_sha256)
    lock=verify.verify_inputs(args.input_lock_sha256)
    # Reuse the exact previously qualified wait/deadline/owned-process cleanup implementation.
    native=load('unchanged_lifecycle_native_helper',verify.REPO/'tools/oracle/dotj-build/lifecycle-behavior-v1/capture.py')
    guard=native.load_resource_guard()
    out.mkdir(parents=True)
    record={'schemaVersion':1,'status':'RUNNING','runId':str(uuid.uuid4()),'commands':[],
            'resources':[],'fixtureRoot':str(out/'fixtures'),'inputLockSha256':args.input_lock_sha256,
            'checkpointSha256':args.checkpoint_sha256,'limits':lock['limits'],'copiedInputs':[],
            'acceptedTasksAdded':0,'numberedBatchCredit':0,'candidateComparisonsPerformed':0}
    def save(): (out/'capture.json').write_bytes((json.dumps(record,indent=2)+'\n').encode())
    save();aggregate_deadline=time.monotonic()+540
    try:
        for name in ['tmp','home','cache','logs']:(out/name).mkdir()
        shutil.copytree(verify.DATA/'fixtures',out/'fixtures')
        for item in lock['copiedInputs']:
            root={'repo':verify.REPO,'root':verify.ROOT}[item['base']]
            target=out/item['target'];target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(root/item['path'],target)
            verify.require(verify.sha(target)==item['sha256'],'copied input changed')
            record['copiedInputs'].append({'target':item['target'],'sha256':verify.sha(target)})
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
            return native.run_native_command(label,argv,out,env,overrides,record,save,guard,aggregate_deadline)
        dotnet=verify.ROOT/'toolchains/dotnet/dotnet.exe';sdk=verify.ROOT/'toolchains/dotnet/sdk/10.0.401'
        binary=out/'CaptureImports.dll'
        run('compile-probe',[str(dotnet),'exec',str(sdk/'Roslyn/bincore/csc.dll'),'/nologo','/noconfig','/nostdlib+',
            '/target:exe','/nullable:enable','/deterministic+','/langversion:14','/out:'+str(binary),
            *['/reference:'+str(verify.ROOT/p) for p in lock['compilerReferences']],str(out/'CaptureImportPathsV1.cs')])
        config=out/'CaptureImports.runtimeconfig.json';config.write_bytes((json.dumps(lock['runtimeConfig'],indent=2)+'\n').encode())
        record['binary']={'path':str(binary),'sha256':verify.sha(binary)}
        record['runtimeConfig']={'path':str(config),'sha256':verify.sha(config)}
        command,stdout=run('native-eight-cases',[str(dotnet),'exec','--runtimeconfig',str(config),
            '--depsfile',str(sdk/'MSBuild.deps.json'),str(binary),str(out/'fixtures'),str(out/'plan.json')])
        record['payload']=json.loads(stdout)
        verify.bind_stdout(command['stdout'],record['payload'],out)
        verify.validate_payload(record['payload'])
        verify.classify(record['payload'])
        verify.verify_fixtures(out/'fixtures',verify.read(verify.EVIDENCE/'plan.json')['fixtures'])
        verify.verify_inputs(args.input_lock_sha256)
        record['status']='PASS_NATIVE_AND_CAPTURE';save()
        verify.validate_capture(out/'capture.json',args.input_lock_sha256,args.checkpoint,args.checkpoint_sha256)
    except Exception as error:
        record.update(failureStatusBeforeFinal=record['status'],status='FAILED',error=str(error));save();raise
    print(json.dumps({'status':record['status'],'report':str(out/'capture.json'),'scenarios':8,'nativeScenarioProcesses':1,'candidateComparisons':0}))


if __name__=='__main__':main()
