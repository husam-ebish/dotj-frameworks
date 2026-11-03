"""Owned Task128 product compilation and consumer execution, using the retained Job guard."""
import hashlib
import importlib.util
import json
import os
import re
from pathlib import Path
import shutil
import sys
import time

HERE=Path(__file__).resolve().parent
B=Path('D:/AI/Implementation/dotj Frameworks')
A=B/'agents/batch2521-build-items-evaluation-v1'
W=B/'worktrees/dotj-build-items-evaluation-v1'
JDK=B/'toolchains/jdk-qualified/jdk-21.0.12.1+1/bin'
GUARD=B/'worktrees/dotj-core-task-completion-v1/tools/oracle/dotj-core/public-task-v1/owned_process.py'
MODULE='org.dotj.build.evaluation.candidate'
IMAGE='mcr.microsoft.com/dotnet/aspnet@sha256:222759b391a1aaf241166672c8f99b2d4ada452e7b5319f3c6e8f265a37b5ad4'
DOCKER=Path('C:/Users/husam/AppData/Local/Programs/DockerDesktop/resources/bin/docker.exe')

def descriptor(path):
    path=Path(path)
    return dict(path=str(path),bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest())

def main():
    mode,name=sys.argv[1:3]
    out=A/name
    if out.parent!=A or out.exists():raise ValueError('New immediate attempt directory required')
    out.mkdir()
    shutil.copyfile(__file__,out/'product.py')
    if descriptor(GUARD)['sha256']!='a2a3701ae675fd563da61eb19ce41d79479bc1f435c1ec07af6c0ddefd67e125':raise ValueError('Guard differs')
    spec=importlib.util.spec_from_file_location('owned_guard',GUARD)
    guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
    for part in ('tmp','home','classes','empty'):(out/part).mkdir()
    env={k:v for k,v in os.environ.items() if not k.upper().startswith(('JAVA','_JAVA','JDK_','CLASSPATH'))}
    env.update(TEMP=str(out/'tmp'),TMP=str(out/'tmp'),HOME=str(out/'home'),USERPROFILE=str(out/'home'))
    vm=['-Xms16m','-Xmx128m','-XX:ActiveProcessorCount=2','-XX:+UseSerialGC','-XX:ReservedCodeCacheSize=32m',
        '-XX:-UsePerfData','-Djava.io.tmpdir='+str(out/'tmp'),'-Duser.home='+str(out/'home'),
        '-Duser.language=en','-Duser.country=US','-Dfile.encoding=UTF-8',
        '-XX:ErrorFile='+str(out/'tmp/hs_err_pid%p.log'),'-XX:HeapDumpPath='+str(out/'tmp')]
    receipt=dict(status='RUNNING',mode=mode,script=descriptor(out/'product.py'),guard=descriptor(GUARD),
        operations=[],resources=[],inputs=[],outputs=[],environmentOverrides={k:v for k,v in env.items() if os.environ.get(k)!=v})
    def save(): (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    deadline=time.monotonic()+180 if mode in ('capture-linux','private-linux') else None
    def run(label,argv,seconds=120,check=True,cleanup=False):
        operation=dict(label=label);receipt['operations'].append(operation);save()
        if deadline:
            seconds=min(seconds,deadline-time.monotonic()-(0 if cleanup else 40))
            if seconds<=0:raise TimeoutError('Aggregate reserve exhausted')
        if not cleanup:
            _,samples=guard.wait_resources(min(time.monotonic()+160,deadline-40) if deadline else time.monotonic()+160);receipt['resources'].extend(samples)
        def update(value): operation['process']=value;save()
        def prelaunch():
            started=time.monotonic();sample=guard.memory();receipt['resources'].append(sample)
            if time.monotonic()-started>2 or not guard.resource_ready(sample):raise ValueError('Fresh resource floor unavailable')
        result=guard.run(list(map(str,argv)),out,env,label,seconds,on_update=update,prelaunch=None if cleanup else prelaunch)
        operation['stdout']=descriptor(out/(label+'.stdout'));operation['stderr']=descriptor(out/(label+'.stderr'));save()
        if check and (result.get('exitCode')!=0 or any(result.get(k) for k in ('timedOut','outputLimitExceeded','cleanupError','error'))):
            raise ValueError('Failed '+label)
        return (out/(label+'.stdout')).read_text(encoding='utf-8-sig').strip()
    try:
        receipt['inputs']=[descriptor(JDK/n) for n in ('javac.exe','jar.exe','java.exe','javap.exe')]
        if mode=='build':
            source=W/'dotj-build/evaluation-candidate/src'
            sources=sorted(source.rglob('*.java'))
            for path in sources:
                target=out/'src'/path.relative_to(source);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
                receipt['inputs'].append(dict(origin=descriptor(path),retained=descriptor(target)))
            frozen=sorted((out/'src').rglob('*.java'))
            run('javac',[JDK/'javac.exe',*['-J'+v for v in vm],'--release','21','-implicit:none','-classpath',out/'empty','-sourcepath',out/'src','-d',out/'classes',*frozen])
            jar=out/'dotj-build-evaluation-candidate.jar'
            run('jar',[JDK/'jar.exe',*['-J'+v for v in vm],'--create','--file',jar,'--date=2020-01-01T00:00:00Z','-C',out/'classes','.'])
            run('module',[JDK/'jar.exe',*['-J'+v for v in vm],'--describe-module','--file',jar])
            run('result-abi',[JDK/'javap.exe',*['-J'+v for v in vm],'-classpath',jar,'-p','-s','org.dotj.internal.build.evaluation.ProjectEvaluationComponent$Result'])
            receipt['outputs']=[descriptor(jar)]+[descriptor(p) for p in sorted((out/'classes').rglob('*.class'))]
        elif mode=='proof':
            shutil.copyfile(HERE/'proof_controls.py',out/'proof_controls.py')
            sys.path.insert(0,str(HERE))
            import proof_controls
            proof_controls.execute(run,out,receipt)
        elif mode=='history':
            jar=A/sys.argv[3]/'dotj-build-evaluation-candidate.jar'
            receipt['inputs'].append(descriptor(jar))
            shutil.copyfile(HERE/'history.py',out/'history.py')
            sys.path.insert(0,str(HERE))
            import history
            history.execute(run,out,vm,receipt,jar)
        elif mode in ('capture-windows','private-windows','supplement-windows','junction-windows'):
            jar=(A/sys.argv[3]/'dotj-build-evaluation-candidate.jar').resolve()
            receipt['inputs'].append(descriptor(jar))
            src=out/'src';src.mkdir()
            extra={'private-windows':('ItemsPrivateTest.java',),'supplement-windows':('ItemsSupplementTest.java',),'junction-windows':('ItemsJunctionTest.java',)}.get(mode,())
            for name in ('ItemsJson.java','ItemsProductCapture.java')+extra:
                shutil.copyfile(HERE/name,src/name);receipt['inputs'].append(descriptor(src/name))
            shutil.copytree(A/('supplemental-input-v1' if mode=='supplement-windows' else 'corpus-input-v1'),out/'fixtures')
            receipt['fixtureInputs']=[descriptor(p) for p in sorted((out/'fixtures').rglob('*')) if p.is_file()]
            run('compile-consumer',[JDK/'javac.exe',*['-J'+v for v in vm],'--release','21','-implicit:none','-sourcepath',out/'empty',
                '--module-path',jar,'--patch-module',MODULE+'='+str(src),'-d',out/'classes',*sorted(src.glob('*.java'))])
            consumer=out/'consumer.jar'
            run('consumer-jar',[JDK/'jar.exe',*['-J'+v for v in vm],'--create','--file',consumer,'--date=2020-01-01T00:00:00Z','-C',out/'classes','.'])
            receipt['consumer']=descriptor(consumer)
            if mode=='junction-windows':
                controls=out/'controls'
                for kind in ('inside','outside'):
                    directory=controls/kind;directory.mkdir(parents=True)
                    target=directory/'target' if kind=='inside' else out/'outside-target'
                    target.mkdir();(target/'a.cs').write_text('owned fixture',encoding='utf-8')
                    quote=lambda p:"'"+str(p).replace("'","''")+"'"
                    command="$ErrorActionPreference='Stop'; New-Item -ItemType Junction -Path "+quote(directory/'alias')+' -Target '+quote(target)+' | Select-Object FullName,LinkType,Target | ConvertTo-Json'
                    run('junction-'+kind,['C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe','-NoProfile','-NonInteractive','-Command',command],15)
                run('junction',[JDK/'java.exe',*vm,'--limit-modules','java.base,java.xml,'+MODULE,'--module-path',jar,
                    '--patch-module',MODULE+'='+str(consumer),'-m',MODULE+'/org.dotj.internal.build.evaluation.ItemsJunctionTest',
                    controls,jar,descriptor(jar)['sha256']],30)
                receipt['outputs']=[descriptor(consumer),descriptor(out/'junction.stdout')]
                receipt['status']='PASS';return
            if mode=='supplement-windows':
                run('supplement',[JDK/'java.exe',*vm,'--limit-modules','java.base,java.xml,'+MODULE,'--module-path',jar,
                    '--patch-module',MODULE+'='+str(consumer),'-m',MODULE+'/org.dotj.internal.build.evaluation.ItemsSupplementTest',
                    out/'fixtures',jar,descriptor(jar)['sha256']],30)
                receipt['fixtureAfter']=[descriptor(p) for p in sorted((out/'fixtures').rglob('*')) if p.is_file()]
                receipt['outputs']=[descriptor(consumer),descriptor(out/'supplement.stdout')]
                receipt['status']='PASS';return
            if mode=='private-windows':
                run('private',[JDK/'java.exe',*vm,'--limit-modules','java.base,java.xml,'+MODULE,'--module-path',jar,
                    '--patch-module',MODULE+'='+str(consumer),'-m',MODULE+'/org.dotj.internal.build.evaluation.ItemsPrivateTest',
                    out/'controls','windows',jar,descriptor(jar)['sha256']],120)
                receipt['outputs']=[descriptor(consumer),descriptor(out/'private.stdout'),descriptor(out/'controls/results.tsv')]
                receipt['status']='PASS';return
            run('capture',[JDK/'java.exe',*vm,'--limit-modules','java.base,java.xml,'+MODULE,'--module-path',jar,
                '--patch-module',MODULE+'='+str(consumer),'-m',MODULE+'/org.dotj.internal.build.evaluation.ItemsProductCapture',
                out/'fixtures',out/'fixtures/manifest.json',jar,descriptor(jar)['sha256']],30)
            receipt['fixtureAfter']=[descriptor(p) for p in sorted((out/'fixtures').rglob('*')) if p.is_file()]
            receipt['outputs']=[descriptor(consumer),descriptor(out/'capture.stdout')]
        elif mode in ('capture-linux','private-linux'):
            build=A/sys.argv[3];consumer_dir=A/sys.argv[4];slot=sys.argv[5]
            if not re.fullmatch('product-v[0-9]+',slot):raise ValueError('Declared product slot required')
            jar=build/'dotj-build-evaluation-candidate.jar';consumer=consumer_dir/'consumer.jar'
            work=A/'native-linux-corpus-root-v1';source=A/'corpus-input-v1'
            if not work.is_dir() or (work/slot).exists():raise ValueError('Fresh case-enabled slot required')
            jdk=B/'toolchains/jdk-linux21/jdk-21.0.12.1+1';script=out/'product-capture.sh'
            shutil.copyfile(HERE/('private-linux.sh' if mode=='private-linux' else 'product-capture.sh'),script)
            receipt['inputs'] += [descriptor(p) for p in (jar,consumer,script,source/'manifest.json',DOCKER,jdk/'bin/java')]
            receipt['fixtureInputs']=[descriptor(p) for p in sorted(source.rglob('*')) if p.is_file()]
            name='dotj-task128-'+out.name
            receipt['container']=dict(name=name,image=IMAGE,owner='task128',cid=None,absenceVerified=False)
            cid=None;created=False
            def inspect(identity,label,cleanup=False):
                raw=run(label,[DOCKER,'inspect','--type','container',identity],10,False,cleanup)
                if receipt['operations'][-1]['process']['exitCode']!=0:return None
                values=json.loads(raw)
                if len(values)!=1:raise ValueError('Expected exact owned container')
                value=values[0]
                if value['Name']!='/'+name or value['Config']['Labels'].get('dotj.owner')!='task128' or value['Config']['Image']!=IMAGE:
                    raise ValueError('Owned container identity differs')
                return value
            try:
                if inspect(name,'container-initial') is not None or 'No such' not in (out/'container-initial.stderr').read_text():
                    raise ValueError('Initial owned absence unproven')
                argv=[DOCKER,'create','--pull=never','--name',name,'--label','dotj.owner=task128',
                    '--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges',
                    '--cpus','2','--memory','512m','--memory-swap','512m','--pids-limit','64','--ulimit','core=0',
                    '--stop-timeout','2','--workdir','/work',
                    '--mount',f'type=bind,source={jar},target=/product.jar,readonly',
                    '--mount',f'type=bind,source={consumer},target=/consumer.jar,readonly',
                    '--mount',f'type=bind,source={jdk},target=/jdk,readonly',
                    '--mount',f'type=bind,source={work},target=/work',
                    '--mount',f'type=bind,source={source},target=/corpus,readonly',
                    '--mount',f'type=bind,source={script},target=/run.sh,readonly']
                container_env=dict(HOME='/work/'+slot+'/home',TMPDIR='/work/'+slot+'/tmp',LANG='C.UTF-8',LC_ALL='C.UTF-8',
                    DOTNET_EnableDiagnostics='0',DOTNET_DbgEnableMiniDump='0',DOTNET_DbgMiniDumpName='/work/'+slot+'/tmp/dotnet.dmp',
                    DOTNET_CLI_TELEMETRY_OPTOUT='1',DOTNET_SKIP_FIRST_TIME_EXPERIENCE='1')
                for k,v in container_env.items():argv+=['--env',k+'='+v]
                argv+=['--entrypoint','/usr/bin/timeout',IMAGE,'-s','KILL','25','/bin/sh','/run.sh',slot,descriptor(jar)['sha256']]
                receipt['container']['environment']=container_env;created=True
                cid=run('container-create',argv,15)
                if not re.fullmatch('[0-9a-f]{64}',cid):raise ValueError('Exact CID required')
                receipt['container']['cid']=cid;save()
                print(json.dumps(dict(phase='launched',cid=cid,receipt=str(out/'receipt.json'))),flush=True)
                value=inspect(cid,'container-created');receipt['container']['createdInspect']=value;save()
                if value is None:raise ValueError('Created container missing')
                run('container-start',[DOCKER,'start',cid],10)
                exit_text=run('container-wait',[DOCKER,'wait',cid],30)
                run('container-logs',[DOCKER,'logs',cid],10,False)
                value=inspect(cid,'container-terminal');receipt['container']['terminalInspect']=value;save()
                if exit_text!='0' or value is None or value['State']['OOMKilled']:raise ValueError('Container failed '+exit_text)
                receipt['fixtureAfter']=[descriptor(p) for p in sorted((work/slot/'fixtures').rglob('*')) if p.is_file()]
            finally:
                if created:
                    value=inspect(cid or name,'container-cleanup-owned',True)
                    if value is not None:
                        cid=value['Id'];receipt['container']['cid']=cid;receipt['container']['cleanupInspect']=value;save()
                        if 'terminalInspect' not in receipt['container']:
                            receipt['container']['terminalInspect']=value
                            run('container-failed-logs',[DOCKER,'logs',cid],10,False,True)
                        run('container-remove',[DOCKER,'rm','-f',cid],10,True,True)
                    value=inspect(cid or name,'container-absence',True)
                    receipt['container']['absenceVerified']=value is None and 'No such' in (out/'container-absence.stderr').read_text()
                    if not receipt['container']['absenceVerified']:raise ValueError('Container absence unproven')
                retained=out/'retained-output';retained.mkdir()
                for path in (work/slot).iterdir() if (work/slot).exists() else []:
                    if path.is_file():
                        shutil.copyfile(path,retained/path.name)
                        receipt['outputs'].append(dict(actual=descriptor(path),retained=descriptor(retained/path.name)))
        else: raise ValueError('Unknown mode')
        receipt['status']='PASS'
    except BaseException as error:
        receipt['status']='FAILED';receipt['error']=repr(error);raise
    finally: save()

if __name__=='__main__':main()
