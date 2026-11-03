"""Task128 prerequisite compiler/inventory/preflight; no Java product edits or builds."""
import hashlib
import importlib.util
import json
import os
import re
from pathlib import Path
import shutil
import sys
import time

B = Path('D:/AI/Implementation/dotj Frameworks')
A = B / 'agents/batch2521-build-items-evaluation-v1'
HERE = Path(__file__).resolve().parent
GUARD = B / 'worktrees/dotj-core-task-completion-v1/tools/oracle/dotj-core/public-task-v1/owned_process.py'
GUARD_SHA = 'a2a3701ae675fd563da61eb19ce41d79479bc1f435c1ec07af6c0ddefd67e125'
DOTNET = B / 'toolchains/dotnet/dotnet.exe'
SDK = B / 'toolchains/dotnet/sdk/10.0.401'
IMAGE = 'mcr.microsoft.com/dotnet/aspnet@sha256:222759b391a1aaf241166672c8f99b2d4ada452e7b5319f3c6e8f265a37b5ad4'
DOCKER = Path('C:/Users/husam/AppData/Local/Programs/DockerDesktop/resources/bin/docker.exe')

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def descriptor(p):
    p = Path(p)
    return dict(path=str(p), sha256=sha(p), bytes=p.stat().st_size)

def write(p, value):
    Path(p).write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')

def guard():
    if sha(GUARD) != GUARD_SHA:
        raise ValueError('Guard identity differs')
    spec = importlib.util.spec_from_file_location('task128_guard', GUARD)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

def environment(out):
    env = {k:v for k,v in os.environ.items() if not k.upper().startswith(
        ('MSBUILD','DOTNET','COMPLUS','CORECLR','COR_','JAVA','_JAVA','JDK_'))}
    env.update(TEMP=str(out/'tmp'), TMP=str(out/'tmp'), HOME=str(out/'home'),
        USERPROFILE=str(out/'home'), DOTNET_CLI_HOME=str(out/'home'), NUGET_PACKAGES=str(out/'cache'),
        DOTNET_ROOT=str(B/'toolchains/dotnet'), DOTNET_MULTILEVEL_LOOKUP='0',
        DOTNET_ROLL_FORWARD='Disable', DOTNET_CLI_TELEMETRY_OPTOUT='1',
        DOTNET_SKIP_FIRST_TIME_EXPERIENCE='1', DOTNET_CLI_UI_LANGUAGE='en-US',
        DOTNET_EnableDiagnostics='0', DOTNET_DbgEnableMiniDump='0',
        DOTNET_DbgMiniDumpName=str(out/'tmp/dotnet.dmp'),
        DOTNET_GCHeapHardLimit='8000000', DOTNET_PROCESSOR_COUNT='2', DOTNET_gcServer='0',
        MSBUILDDISABLENODEREUSE='1', MSBUILDUSEREXTENSIONSPATH=str(out/'home/msbuild'),
        APPDATA=str(out/'home/roaming'), LOCALAPPDATA=str(out/'home/local'))
    return env

def main():
    mode = sys.argv[1]
    out = A / sys.argv[2]
    if out.parent != A or out.exists():
        raise ValueError('New immediate attempt directory required')
    out.mkdir()
    shutil.copyfile(__file__, out/'prerequisite.py')
    for name in ('tmp','home','cache'):
        (out/name).mkdir()
    g = guard()
    receipt = dict(mode=mode, status='RUNNING', script=descriptor(__file__), guard=descriptor(GUARD),
        operations=[], resources=[], inputs=[], outputs=[])
    def save(): write(out/'receipt.json', receipt)
    env = environment(out)
    receipt['environmentOverrides'] = {k:v for k,v in env.items() if os.environ.get(k) != v}
    receipt['inheritedEnvironmentNames'] = sorted(k for k in env if os.environ.get(k) == env[k])
    save()
    aggregate_deadline = time.monotonic()+180 if mode.startswith('linux') else None
    def run(label, argv, seconds=30, check=True, cleanup=False):
        def update(p):
            operation['process'] = p
            save()
        operation = dict(label=label)
        receipt['operations'].append(operation)
        if aggregate_deadline is not None:
            seconds = min(seconds, aggregate_deadline-time.monotonic()-(0 if cleanup else 40))
            if seconds <= 0: raise TimeoutError('Aggregate launch reserve exhausted')
        if not cleanup:
            _, samples = g.wait_resources(min(time.monotonic()+160, aggregate_deadline-40) if aggregate_deadline else time.monotonic()+160)
            receipt['resources'].extend(samples)
        def fresh():
            started = time.monotonic()
            sample = g.memory()
            receipt['resources'].append(sample)
            if time.monotonic()-started > 2 or not g.resource_ready(sample):
                raise ValueError('Fresh resource floor unavailable')
        process = g.run(list(map(str,argv)), out, env, label, seconds, on_update=update, prelaunch=None if cleanup else fresh)
        operation['stdout'] = descriptor(out/(label+'.stdout'))
        operation['stderr'] = descriptor(out/(label+'.stderr'))
        save()
        if check and (process.get('exitCode') != 0 or process.get('timedOut') or
            process.get('outputLimitExceeded') or process.get('cleanupError') or process.get('error')):
            raise ValueError('Failed '+label)
        return (out/(label+'.stdout')).read_text(encoding='utf-8-sig').strip()
    try:
        if mode == 'red':
            jdk=B/'toolchains/jdk-qualified/jdk-21.0.12.1+1/bin'
            old=B/'agents/batch2518-build-ordering-preparation-v1/task106-product-dev-attempt02/dotj-build-evaluation-candidate.jar'
            if sha(old)!='6bc95bc7ed6d702ed58f455f10fe35ed0c71389dd175034afefaee2e259e089f': raise ValueError('Retained JAR differs')
            src=out/'src';src.mkdir();classes=out/'classes';classes.mkdir();empty=out/'empty';empty.mkdir()
            shutil.copyfile(HERE/'BaselineRed.java',src/'BaselineRed.java')
            shutil.copytree(A/'corpus-input-v1/IP01',out/'IP01')
            shutil.copytree(A/'supplemental-input-v1/NEG-items',out/'NEG-items')
            receipt['inputs']=[descriptor(old),descriptor(src/'BaselineRed.java'),descriptor(out/'IP01/main.proj'),descriptor(out/'NEG-items/main.proj')]
            receipt['inputs'] += [descriptor(jdk/n) for n in ('javap.exe','javac.exe','jar.exe','java.exe')]
            vm=['-Xms16m','-Xmx128m','-XX:ActiveProcessorCount=2','-XX:+UseSerialGC','-XX:ReservedCodeCacheSize=32m',
                '-Djava.io.tmpdir='+str(out/'tmp'),'-Duser.home='+str(out/'home'),'-Duser.language=en','-Duser.country=US',
                '-Dfile.encoding=UTF-8','-XX:ErrorFile='+str(out/'tmp/hs_err_pid%p.log'),'-XX:HeapDumpPath='+str(out/'tmp')]
            module='org.dotj.build.evaluation.candidate'
            run('old-result-abi',[jdk/'javap.exe',*['-J'+v for v in vm],'-classpath',old,'-p','-s','org.dotj.internal.build.evaluation.ProjectEvaluationComponent$Result'],120)
            run('compile-red',[jdk/'javac.exe',*['-J'+v for v in vm],'--release','21','-implicit:none','-sourcepath',empty,
                '--module-path',old,'--patch-module',module+'='+str(src),'-d',classes,src/'BaselineRed.java'],120)
            consumer=out/'red-consumer.jar'
            run('compile-red-jar',[jdk/'jar.exe',*['-J'+v for v in vm],'--create','--file',consumer,'--date=2020-01-01T00:00:00Z','-C',classes,'.'],120)
            output=run('baseline-red',[jdk/'java.exe',*vm,'--limit-modules','java.base,java.xml,'+module,'--module-path',old,
                '--patch-module',module+'='+str(consumer),'-m',module+'/org.dotj.internal.build.evaluation.BaselineRed',out/'IP01',out/'NEG-items',old],120,False)
            process=receipt['operations'][-1]['process']
            if process['exitCode']!=1 or output.splitlines()!=['IP01\tUNSUPPORTED_ELEMENT','NEG-items\tUNSUPPORTED_ELEMENT']:
                raise ValueError('Genuine behavior RED not established')
            if sha(old)!=receipt['inputs'][0]['sha256']:raise ValueError('Retained product changed')
            receipt['outputs']=[descriptor(consumer)]
            receipt['redMeaning']='Both inputs succeed natively; old entrypoint rejects ItemGroup. No new accessor used.'
        elif mode == 'prepare':
            source = HERE/'CaptureItemsV1.cs'
            shutil.copyfile(source, out/source.name)
            shutil.copyfile(HERE/'read-items.ps1', out/'read-items.ps1')
            lock = json.loads((HERE.parents[3]/'planning/stage-2/repos/dotj-build/evidence/lifecycle-behavior-input-lock-v1.json').read_text())
            refs = [B/p for p in lock['compilerReferences']]
            refs.append(B/'toolchains/dotnet/packs/Microsoft.NETCore.App.Ref/10.0.12/ref/net10.0/System.Security.Cryptography.dll')
            refs.append(B/'toolchains/dotnet/packs/Microsoft.NETCore.App.Ref/10.0.12/ref/net10.0/System.Text.Encoding.Extensions.dll')
            receipt['inputs'] = list(map(descriptor, [source, HERE/'read-items.ps1',DOTNET,SDK/'Roslyn/bincore/csc.dll',*refs]))
            # Traverse the installed SDK's declared managed runtime dependencies only.
            deps_path = SDK/'MSBuild.deps.json'
            deps = json.loads(deps_path.read_text())
            target = next(iter(deps['targets'].values()))
            pending = ['Microsoft.Build/18.9.11']; seen = set(); closure=[]
            while pending:
                key = pending.pop()
                if key in seen: continue
                seen.add(key)
                node = target[key]
                for name, version in node.get('dependencies',{}).items():
                    pending.append(name+'/'+version)
                for rel in node.get('runtime',{}):
                    path = SDK/Path(rel).name
                    shutil.copyfile(path,out/path.name)
                    closure.append(dict(package=key, runtimeAsset=rel, original=descriptor(path), retained=descriptor(out/path.name)))
            receipt['managedClosure'] = closure
            receipt['dependencyManifest'] = descriptor(deps_path)
            write(out/'CaptureItemsV1.runtimeconfig.json', lock['runtimeConfig'])
            run('compile-observer', [DOTNET,'exec',SDK/'Roslyn/bincore/csc.dll','/nologo','/noconfig','/nostdlib+',
                '/target:exe','/nullable:enable','/deterministic+','/langversion:14','/out:'+str(out/'CaptureItemsV1.dll'),
                *['/reference:'+str(p) for p in refs],out/source.name],120)
            run('compiled-inventory',[DOTNET,'exec','--runtimeconfig',B/'toolchains/powershell-oracle.runtimeconfig.json',
                B/'toolchains/powershell-7.6.0-fxdependent/pwsh.dll','-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',out/'read-items.ps1','-ImplementationRoot',B],120)
            receipt['outputs'] = [descriptor(out/'CaptureItemsV1.dll'),descriptor(out/'CaptureItemsV1.runtimeconfig.json'),descriptor(out/'compiled-inventory.stdout')]
        elif mode in ('windows','windows-corpus','windows-supplemental'):
            observer = A/sys.argv[3]
            work=out/'work'; work.mkdir()
            receipt['inputs'] = [descriptor(p) for p in sorted(observer.glob('*.dll'))] + [descriptor(observer/'CaptureItemsV1.runtimeconfig.json')]
            env['MSBUILD_EXE_PATH'] = str(observer/'Microsoft.Build.dll')
            receipt['environmentOverrides']['MSBUILD_EXE_PATH'] = env['MSBUILD_EXE_PATH']
            if mode in ('windows-corpus','windows-supplemental'):
                source=A/sys.argv[4]
                shutil.copytree(source,work/'fixtures')
                receipt['corpusSource'] = descriptor(source/'manifest.json')
                receipt['corpusInputs'] = [descriptor(p) for p in sorted((work/'fixtures').rglob('*')) if p.is_file()]
                env['DOTNET_ReadyToRun']='0'; receipt['environmentOverrides']['DOTNET_ReadyToRun']='0'
                observer_mode='corpus' if mode=='windows-corpus' else 'supplemental'
                run('native-windows',[DOTNET,observer/'CaptureItemsV1.dll',observer_mode,work/'fixtures',work/'fixtures/manifest.json',observer])
                receipt['corpusAfter'] = [descriptor(p) for p in sorted((work/'fixtures').rglob('*')) if p.is_file()]
            else:
                run('native-windows',[DOTNET,observer/'CaptureItemsV1.dll','preflight',work,observer])
        elif mode in ('linux','linux-corpus','linux-supplemental'):
            observer = A/sys.argv[3]
            name = 'dotj-task128-'+out.name
            corpus_mode=mode in ('linux-corpus','linux-supplemental')
            supplemental_mode=mode=='linux-supplemental'
            if corpus_mode:
                work=A/'native-linux-corpus-root-v1'
                source=A/sys.argv[4];slot=sys.argv[5]
                if slot not in ('pass1','pass2','v3-pass1','v3-pass2','supplemental-pass1','supplemental-pass2') or (work/slot).exists(): raise ValueError('Fresh declared Linux slot required')
                if not work.is_dir(): raise ValueError('Provisioned case-sensitive corpus root required')
                receipt['corpusSource'] = descriptor(source/'manifest.json')
                receipt['corpusInputs'] = [descriptor(p) for p in sorted(source.rglob('*')) if p.is_file()]
            elif len(sys.argv)>5:
                work=Path(sys.argv[5]).resolve()
                approved=B/'verification/linux-case-capability-v1/case-root'
                if work!=approved.resolve() or not work.is_dir() or any(work.iterdir()):
                    raise ValueError('Only the approved empty case-sensitive root is allowed')
            else:
                work=out/'work'; work.mkdir()
            receipt['fixtureRoot']=str(work)
            for folder in ('tmp','home','cache'): (work/folder).mkdir(exist_ok=True)
            script='supplemental.sh' if supplemental_mode else 'capture.sh' if corpus_mode else 'preflight.sh'
            shutil.copyfile(HERE/script, out/script)
            jdk = B/'toolchains/jdk-linux21/jdk-21.0.12.1+1'
            receipt['inputs'] = [descriptor(observer/p) for p in ('CaptureItemsV1.cs','CaptureItemsV1.dll','CaptureItemsV1.runtimeconfig.json')]
            receipt['inputs'] += [descriptor(out/script),descriptor(DOCKER),descriptor(jdk/'bin/java')]
            receipt['inputs'] += [descriptor(p) for p in sorted(observer.glob('*.dll')) if p.name!='CaptureItemsV1.dll']
            receipt['container'] = dict(name=name, image=IMAGE, owner='task128', cid=None, absenceVerified=False)
            cid = None
            created = False
            def inspect(identity,label,cleanup=False):
                raw=run(label,[DOCKER,'inspect','--type','container',identity],10,False,cleanup)
                process=receipt['operations'][-1]['process']
                if process['exitCode'] != 0:
                    return None
                values=json.loads(raw)
                if len(values)!=1: raise ValueError('Expected one owned container')
                value=values[0]
                if value['Name'] != '/'+name or value['Config']['Labels'].get('dotj.owner')!='task128' or value['Config']['Image']!=IMAGE:
                    raise ValueError('Container ownership mismatch')
                return value
            try:
                if inspect(name,'container-initial') is not None:
                    raise ValueError('Deterministic name already exists; no launch')
                previous = receipt['operations'][-1]
                if 'No such' not in (out/'container-initial.stderr').read_text():
                    raise ValueError('Initial absence was not established')
                argv=[DOCKER,'create','--pull=never','--name',name,'--label','dotj.owner=task128',
                    '--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges',
                    '--cpus','2','--memory','512m','--memory-swap','512m','--pids-limit','64',
                    '--ulimit','core=0',
                    '--stop-timeout','2','--workdir','/work',
                    '--mount',f'type=bind,source={observer},target=/observer,readonly',
                    '--mount',f'type=bind,source={jdk},target=/jdk,readonly',
                    '--mount',f'type=bind,source={work},target=/work',
                    '--mount',f'type=bind,source={out / script},target=/run.sh,readonly']
                if corpus_mode:
                    argv+=['--mount',f'type=bind,source={source},target=/corpus,readonly']
                container_env=dict(HOME='/work/home',TMPDIR='/work/tmp',DOTNET_CLI_HOME='/work/home',
                    DOTNET_GCHeapHardLimit='8000000',DOTNET_PROCESSOR_COUNT='2',DOTNET_gcServer='0',
                    DOTNET_ROLL_FORWARD='Disable',DOTNET_EnableDiagnostics='0',DOTNET_DbgEnableMiniDump='0',
                    DOTNET_DbgMiniDumpName='/work/tmp/dotnet.dmp',DOTNET_CLI_TELEMETRY_OPTOUT='1',
                    DOTNET_SKIP_FIRST_TIME_EXPERIENCE='1',DOTNET_MULTILEVEL_LOOKUP='0',DOTNET_CLI_UI_LANGUAGE='en-US',
                    MSBUILD_EXE_PATH='/observer/Microsoft.Build.dll',MSBUILDDISABLENODEREUSE='1',
                    MSBUILDUSEREXTENSIONSPATH='/work/home/msbuild',LANG='C.UTF-8',LC_ALL='C.UTF-8')
                if corpus_mode or (len(sys.argv)>4 and sys.argv[4]=='disable-readytorun'):
                    container_env['DOTNET_ReadyToRun']='0'
                for k,v in container_env.items(): argv+=['--env',k+'='+v]
                argv+=['--entrypoint','/usr/bin/timeout',IMAGE,'-s','KILL','25','/bin/sh','/run.sh']
                if corpus_mode: argv.append(slot)
                receipt['container']['environment']=container_env
                created=True # Enables exact-name recovery if create output is interrupted.
                cid=run('container-create',argv,15)
                if not re.fullmatch('[0-9a-f]{64}',cid): raise ValueError('No exact CID')
                receipt['container']['cid']=cid; save()
                value=inspect(cid,'container-created')
                receipt['container']['createdInspect']=value; save()
                if value is None: raise ValueError('Created container missing')
                run('container-start',[DOCKER,'start',cid],10)
                exit_text=run('container-wait',[DOCKER,'wait',cid],30)
                run('container-logs',[DOCKER,'logs',cid],10,False)
                value=inspect(cid,'container-terminal')
                receipt['container']['terminalInspect']=value; save()
                if exit_text!='0' or value is None or value['State']['OOMKilled']:
                    raise ValueError('Container runtime failed: '+exit_text)
                if corpus_mode:
                    names=('supplemental.stdout','supplemental.stderr') if supplemental_mode else ('native.stdout','native.stderr','materialized-case-profile.tsv')
                    receipt['outputs'] += [descriptor(work/slot/n) for n in names]
                    receipt['corpusAfter'] = [descriptor(p) for p in sorted((work/slot/'fixtures').rglob('*')) if p.is_file()]
                else:
                    for filename in ('runtimes.stdout','runtimes.stderr','java.stdout','java.stderr','observer.stdout','observer.stderr','directory-probe.json'):
                        receipt['outputs'].append(descriptor(work/filename))
            finally:
                if created:
                    value=inspect(cid or name,'container-cleanup-owned',True)
                    if value is not None:
                        cid=value['Id']; receipt['container']['cid']=cid
                        receipt['container']['cleanupInspect']=value; save()
                        run('container-remove',[DOCKER,'rm','-f',cid],10,True,True)
                    value=inspect(cid or name,'container-absence',True)
                    receipt['container']['absenceVerified']=(value is None and 'No such' in (out/'container-absence.stderr').read_text())
                    if not receipt['container']['absenceVerified']: raise ValueError('Container cleanup absence unproven')
                retained=out/'retained-output'; retained.mkdir()
                actual_output=work/slot if corpus_mode else work
                for path in actual_output.iterdir() if actual_output.exists() else []:
                    if path.is_file() and path.suffix in ('.stdout','.stderr','.json','.tsv'):
                        shutil.copyfile(path,retained/path.name)
                        receipt.setdefault('retainedOutputs',[]).append(dict(actual=descriptor(path),retained=descriptor(retained/path.name)))
        else:
            raise ValueError('Unknown mode')
        receipt['status'] = 'GENUINE_BASELINE_RED' if mode=='red' else 'CAPTURED_PENDING_CONTRACT_REVIEW' if mode.endswith(('-corpus','-supplemental')) else 'PASS_PREREQUISITE_OPERATION_NOT_FEATURE_QUALIFICATION'
    except BaseException as e:
        receipt.update(status='FAILED', error=dict(type=type(e).__name__,message=str(e)))
        raise
    finally:
        save()
    print(json.dumps(dict(status=receipt['status'],receipt=str(out/'receipt.json'))))

if __name__ == '__main__': main()
