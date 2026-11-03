"""Finite native-only missing-projection capture. Plan mode never launches a child."""
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from corpus import descriptor, sha, read_contract, materialize, verify_fixtures, PROFILES
from owned import B, SDK, DOTNET, GUARD, IMAGE, DOCKER, Run, overrides, docker_argv, container

HERE=Path(__file__).resolve().parent
CONFIG={'runtimeOptions':{'tfm':'net10.0','framework':{'name':'Microsoft.NETCore.App','version':'10.0.12'},'rollForward':'Disable'}}

def compile_argv(out):
    refs=sorted((B/'toolchains/dotnet/packs/Microsoft.NETCore.App.Ref/10.0.12/ref/net10.0').glob('*.dll'))
    refs += [SDK/'Microsoft.Build.dll',SDK/'Microsoft.Build.Framework.dll']
    return [str(DOTNET),'exec',str(SDK/'Roslyn/bincore/csc.dll'),'/nologo','/noconfig','/nostdlib+',
            '/target:exe','/nullable:enable','/deterministic+','/out:'+str(out/'CaptureImports.dll'),
            *['/reference:'+str(p) for p in refs],str(HERE/'CaptureCycleTraceProjection.cs')]

def native_argv(out,binary,profile):
    return [str(DOTNET),'exec','--runtimeconfig',str(binary/'CaptureImports.runtimeconfig.json'),
            '--depsfile',str(SDK/'MSBuild.deps.json'),str(binary/'CaptureImports.dll'),str(out/'fixtures'),PROFILES[profile]]

def linux_spec(out,binary,profile,work_root):
    slot=out.name
    env=dict(HOME='/work/'+slot+'/home',TMPDIR='/work/'+slot+'/tmp',DOTNET_CLI_HOME='/work/'+slot+'/home',LANG='C.UTF-8',LC_ALL='C.UTF-8',
        DOTNET_ReadyToRun='0',DOTNET_EnableDiagnostics='0',DOTNET_DbgEnableMiniDump='0',DOTNET_DbgMiniDumpName='/work/tmp/dotnet.dmp',
        DOTNET_CLI_TELEMETRY_OPTOUT='1',DOTNET_SKIP_FIRST_TIME_EXPERIENCE='1',DOTNET_ROLL_FORWARD='Disable',
        DOTNET_CLI_UI_LANGUAGE='en-US',DOTNET_GCHeapHardLimit='8000000',DOTNET_gcServer='0',DOTNET_PROCESSOR_COUNT='2',
        MSBUILDDISABLENODEREUSE='1',MSBUILDUSEREXTENSIONSPATH='/work/home/msbuild',MSBUILD_EXE_PATH='/sdk/MSBuild.dll')
    name='dotj-task132-'+out.name
    mounts=[(work_root,'/work',False),(out/'fixtures','/corpus',True),(binary,'/observer',True),(SDK,'/sdk',True),(HERE/'capture-linux.sh','/run.sh',True)]
    return name,env,docker_argv(name,mounts,env,['/bin/sh','/run.sh',slot,PROFILES[profile]])

def plan(contract_path,artifacts,work_root=None):
    contract=read_contract(contract_path);binary=artifacts/'native-compile-v1'
    argv=compile_argv(binary)
    inputs=[descriptor(p) for p in [HERE/'CaptureCycleTraceProjection.cs',HERE/'capture-linux.sh',HERE/'capture_reference.py',HERE/'owned.py',HERE/'corpus.py',GUARD,DOTNET,SDK/'Roslyn/bincore/csc.dll',SDK/'MSBuild.deps.json']]
    inputs += [descriptor(arg[len('/reference:'):]) for arg in argv if arg.startswith('/reference:')]
    runs=[]
    for row in contract['nativeSchedule']['runs']:
        out=artifacts/row['attempt']
        run=dict(**row,attemptPath=str(out),environmentOverrides=overrides(out),
                 outerArgv=[str(B/'toolchains/python-3.13.9/python.exe'),'-B',str(HERE/'capture_reference.py'),'capture',
                     '--contract',str(contract_path),'--artifacts',str(artifacts),'--run',row['attempt']],
                 fixtureHashes={c['id']:{n:v['sha256'] for n,v in c['files'].items()} for c in contract['cases'] if c['id'] in row['ids']})
        if row['platform']=='windows':run.update(argv=native_argv(out,binary,row['profile']),timeoutSeconds=30)
        else:
            assert work_root is not None, 'Explicit provisioned case-enabled work root required'
            run['outerArgv'] += ['--work-root',str(work_root)]
            name,env,args=linux_spec(out,binary,row['profile'],work_root)
            run.update(argv=args,containerEnvironment=env,containerName=name,innerSeconds=25,aggregateSeconds=180,cleanupReserveSeconds=40,
                       lifecycle=['inspect-name-absent','create','inspect-CID-owner-image','start','wait','logs','inspect-terminal-exit0-notOOM',
                                  'finally inspect-owned','rm -f owned CID','inspect-name-absent','late inspect-name-absent'])
        runs.append(run)
    return dict(status='FINITE_RECIPE_FOR_REVIEW',contract=descriptor(contract_path),inputs=inputs,compile=dict(argv=argv,attempt=str(binary),
        environmentOverrides=overrides(binary),timeoutSeconds=120,runtimeConfig=CONFIG),runs=runs,newRowPasses=190,
        resources=dict(freePhysicalBytes=512*1024**2,freeCommitBytes=16*1024**3,nativeHeapMiB=128,processors=2,
                       processOwnership='suspended process assigned kill-on-close Job before resume; final empty Job checks'),
        compiledDescriptor='Filled by compile receipt, checked before any capture',nativeChain=False)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['plan','compile','capture'])
    parser.add_argument('--contract',type=Path,required=True);parser.add_argument('--artifacts',type=Path,required=True)
    parser.add_argument('--work-root',type=Path);parser.add_argument('--run');args=parser.parse_args()
    assert args.artifacts.resolve().is_relative_to(B)
    if args.mode=='plan':
        path=args.artifacts/'native-recipe-v1.json';assert not path.exists()
        path.write_text(json.dumps(plan(args.contract,args.artifacts,args.work_root),indent=2)+'\n',encoding='utf-8')
        print(json.dumps(descriptor(path)));return
    contract=read_contract(args.contract);binary=args.artifacts/'native-compile-v1'
    row=next((r for r in contract['nativeSchedule']['runs'] if r['attempt']==args.run),None)
    out=binary if args.mode=='compile' else args.artifacts/row['attempt']
    run=Run(out,args.mode=='capture' and row['platform']=='linux');error=None
    run.receipt['inputs']=[descriptor(args.contract),descriptor(__file__),descriptor(HERE/'owned.py'),descriptor(HERE/'corpus.py')]
    try:
        if args.mode=='compile':
            shutil.copyfile(HERE/'CaptureCycleTraceProjection.cs',out/'CaptureCycleTraceProjection.cs')
            run.receipt['inputs'].append(descriptor(HERE/'CaptureCycleTraceProjection.cs'))
            argv=compile_argv(out)
            run.receipt['inputs'] += [descriptor(arg[len('/reference:'):]) for arg in argv if arg.startswith('/reference:')]
            run('compile-probe',argv)
            (out/'CaptureImports.runtimeconfig.json').write_text(json.dumps(CONFIG,indent=2)+'\n',encoding='utf-8')
            run.receipt['outputs']=[descriptor(out/n) for n in ('CaptureImports.dll','CaptureImports.runtimeconfig.json')]
        else:
            receipt=json.loads((binary/'receipt.json').read_text());assert receipt['status']=='PASS'
            for item in receipt['outputs']:assert sha(item['path'])==item['sha256']
            for item in receipt['outputs']:assert sha(binary/Path(item['path']).name)==item['sha256']
            run.receipt['inputs'] += [descriptor(binary/'receipt.json'),*receipt['outputs']]
            run.receipt['inputs'] += [descriptor(binary/n) for n in ('CaptureImports.dll','CaptureImports.runtimeconfig.json')]
            run.receipt['selection']=row
            materialize(contract,out/'fixtures',row['ids'])
            run.receipt['fixtureInputs']=[descriptor(p) for p in sorted((out/'fixtures').rglob('*')) if p.is_file()]
            if row['platform']=='windows':
                raw=run('capture',native_argv(out,binary,row['profile']),30)
                rawpath=out/'capture.stdout';actual=out/'fixtures'
            else:
                assert args.work_root and args.work_root.is_dir() and not (args.work_root/out.name).exists()
                work=args.work_root/out.name
                name,env,argv=linux_spec(out,binary,row['profile'],args.work_root);run.receipt['containerEnvironment']=env
                container(run,name,argv)
                rawpath=work/'native.stdout';raw=rawpath.read_text();actual=work/'evaluation/fixtures'
                measured=(work/'case-profile.tsv').read_text().splitlines()
                assert measured and all(line.endswith('\tfalse\tfalse') for line in measured)
                run.receipt['caseProfile']=descriptor(work/'case-profile.tsv')
            parsed=json.loads(raw)
            assert parsed['runtime']=='.NET 10.0.12' and parsed['profile']==PROFILES[row['profile']]
            assert [r['id'] for r in parsed['rows']]==row['ids']
            assert all(r['cleanup']['afterUnload']==0 and r['cleanup']['disposed'] and r['taskMarkerAbsent'] for r in parsed['rows'])
            verify_fixtures(contract,out/'fixtures',row['ids']);verify_fixtures(contract,actual,row['ids'])
            (out/'parsed.json').write_text(json.dumps(parsed,indent=2)+'\n',encoding='utf-8')
            run.receipt['outputs']=[descriptor(rawpath),descriptor(out/'parsed.json')]
            run.receipt['rawParsedEquality']=json.loads(rawpath.read_text(encoding='utf-8-sig'))==json.loads((out/'parsed.json').read_text())
            run.receipt['actualFixturePath']=str(actual)
            run.receipt['fixtureRoot']=str(actual) if row['platform']=='windows' else '/work/'+out.name+'/evaluation/fixtures'
            run.receipt['fixturesUnchanged']=True
    except BaseException as caught:error=caught;raise
    finally:run.finish(error)
    print(json.dumps(dict(status='PASS',receipt=str(out/'receipt.json'),sha256=sha(out/'receipt.json'))))

if __name__=='__main__':main()
