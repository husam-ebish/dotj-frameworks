"""Bounded explicit-path execution shared by this feature's producers."""
import importlib.util
import json
import os
from pathlib import Path
import re
import time
from corpus import descriptor, sha

B = Path('D:/AI/Implementation/dotj Frameworks')
JDK = B/'toolchains/jdk-qualified/jdk-21.0.12.1+1/bin'
SDK = B/'toolchains/dotnet/sdk/10.0.401'
DOTNET = B/'toolchains/dotnet/dotnet.exe'
GUARD = B/'worktrees/dotj-core-task-completion-v1/tools/oracle/dotj-core/public-task-v1/owned_process.py'
GUARD_SHA = 'a2a3701ae675fd563da61eb19ce41d79479bc1f435c1ec07af6c0ddefd67e125'
DOCKER = Path('C:/Users/husam/AppData/Local/Programs/DockerDesktop/resources/bin/docker.exe')
IMAGE = 'mcr.microsoft.com/dotnet/aspnet@sha256:222759b391a1aaf241166672c8f99b2d4ada452e7b5319f3c6e8f265a37b5ad4'
MODULE = 'org.dotj.build.evaluation.candidate'

def overrides(out):
    return dict(TEMP=str(out/'tmp'), TMP=str(out/'tmp'), HOME=str(out/'home'), USERPROFILE=str(out/'home'),
        APPDATA=str(out/'home/roaming'), LOCALAPPDATA=str(out/'home/local'), DOTNET_CLI_HOME=str(out/'home'),
        NUGET_PACKAGES=str(out/'cache'), DOTNET_ROOT=str(B/'toolchains/dotnet'), DOTNET_MULTILEVEL_LOOKUP='0',
        DOTNET_ROLL_FORWARD='Disable', DOTNET_CLI_TELEMETRY_OPTOUT='1', DOTNET_SKIP_FIRST_TIME_EXPERIENCE='1',
        DOTNET_NOLOGO='1', DOTNET_CLI_UI_LANGUAGE='en-US', DOTNET_EnableDiagnostics='0', DOTNET_DbgEnableMiniDump='0',
        DOTNET_DbgMiniDumpName=str(out/'tmp/dotnet.dmp'), DOTNET_GCHeapHardLimit='8000000', DOTNET_gcServer='0',
        DOTNET_PROCESSOR_COUNT='2', MSBUILDDISABLENODEREUSE='1', MSBUILDUSEREXTENSIONSPATH=str(out/'home/msbuild'),
        MSBUILD_EXE_PATH=str(SDK/'MSBuild.dll'))

def vm(out):
    return ['-Xms16m','-Xmx128m','-XX:ActiveProcessorCount=2','-XX:+UseSerialGC','-XX:ReservedCodeCacheSize=32m',
        '-XX:-UsePerfData','-Djava.io.tmpdir='+str(out/'tmp'),'-Duser.home='+str(out/'home'),
        '-Duser.language=en','-Duser.country=US','-Dfile.encoding=UTF-8',
        '-XX:ErrorFile='+str(out/'tmp/hs_err_pid%p.log'),'-XX:HeapDumpPath='+str(out/'tmp')]

class Run:
    def __init__(self, out, linux=False):
        self.out=Path(out).resolve()
        assert self.out.is_relative_to(B) and self.out!=B and not self.out.exists()
        self.out.mkdir(parents=True)
        for part in ('tmp','home','cache','empty','classes'):(self.out/part).mkdir()
        assert sha(GUARD)==GUARD_SHA
        spec=importlib.util.spec_from_file_location('trace_owned_guard',GUARD)
        self.guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.guard)
        self.env={k:v for k,v in os.environ.items() if not k.upper().startswith(('JAVA','_JAVA','JDK_','CLASSPATH','DOTNET','MSBUILD','COMPLUS','CORECLR','COR_'))}
        self.env.update(overrides(self.out))
        self.receipt=dict(status='RUNNING',guard=descriptor(GUARD),operations=[],resources=[],inputs=[],outputs=[],
                          environmentOverrides=overrides(self.out))
        self.deadline=time.monotonic()+180 if linux else None
        self.save()
    def save(self):
        (self.out/'receipt.json').write_text(json.dumps(self.receipt,indent=2)+'\n',encoding='utf-8')
    def __call__(self,label,argv,seconds=120,check=True,cleanup=False):
        if self.deadline:
            seconds=min(seconds,self.deadline-time.monotonic()-(0 if cleanup else 40))
            if seconds<=0:raise TimeoutError('Aggregate cleanup reserve exhausted')
        op=dict(label=label);self.receipt['operations'].append(op);self.save()
        if not cleanup:
            _,samples=self.guard.wait_resources(min(time.monotonic()+160,self.deadline-40) if self.deadline else time.monotonic()+160)
            self.receipt['resources'].extend(samples)
        def prelaunch():
            start=time.monotonic();sample=self.guard.memory();self.receipt['resources'].append(sample)
            if time.monotonic()-start>2 or not self.guard.resource_ready(sample):raise ValueError('Fresh resource floor unavailable')
        def update(value):op['process']=value;self.save()
        result=self.guard.run(list(map(str,argv)),self.out,self.env,label,seconds,on_update=update,prelaunch=None if cleanup else prelaunch)
        for stream in ('stdout','stderr'):op[stream]=descriptor(self.out/(label+'.'+stream))
        self.save()
        if check and (result.get('exitCode')!=0 or any(result.get(k) for k in ('timedOut','outputLimitExceeded','cleanupError','error'))):
            raise ValueError('Failed '+label)
        return (self.out/(label+'.stdout')).read_text(encoding='utf-8-sig').strip()
    def finish(self,error=None):
        self.receipt['status']='FAILED' if error else 'PASS'
        if error:self.receipt['error']=repr(error)
        self.save()

def docker_argv(name, mounts, environment, command):
    argv=[str(DOCKER),'create','--pull=never','--name',name,'--label','dotj.owner=task132',
        '--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges',
        '--cpus','2','--memory','512m','--memory-swap','512m','--pids-limit','64','--ulimit','core=0',
        '--stop-timeout','2','--workdir','/work']
    for source,target,readonly in mounts:
        argv += ['--mount',f'type=bind,source={source},target={target}'+(',readonly' if readonly else '')]
    for key,value in environment.items():argv += ['--env',key+'='+value]
    return argv+['--entrypoint','/usr/bin/timeout',IMAGE,'-s','KILL','25',*command]

def container(run, name, argv):
    record=dict(name=name,image=IMAGE,owner='task132',cid=None,absenceVerified=False)
    run.receipt['container']=record
    cid=None;attempted=False
    def inspect(identity,label,cleanup=False):
        raw=run(label,[DOCKER,'inspect','--type','container',identity],10,False,cleanup)
        op=run.receipt['operations'][-1]
        if op['process']['exitCode']!=0:
            assert 'No such' in (run.out/(label+'.stderr')).read_text(), 'Absence not established'
            return None
        values=json.loads(raw);assert len(values)==1
        value=values[0]
        assert value['Name']=='/'+name and value['Config']['Labels'].get('dotj.owner')=='task132' and value['Config']['Image']==IMAGE
        return value
    try:
        assert inspect(name,'container-initial') is None
        attempted=True
        cid=run('container-create',argv,15)
        assert re.fullmatch('[0-9a-f]{64}',cid)
        record['cid']=cid;record['createdInspect']=inspect(cid,'container-created');run.save()
        run('container-start',[DOCKER,'start',cid],10)
        exit_text=run('container-wait',[DOCKER,'wait',cid],30)
        run('container-logs',[DOCKER,'logs',cid],10,False)
        terminal=inspect(cid,'container-terminal');record['terminalInspect']=terminal
        assert exit_text=='0' and terminal['State']['ExitCode']==0 and not terminal['State']['Running'] and not terminal['State']['OOMKilled']
    finally:
        if attempted:
            value=inspect(cid or name,'container-cleanup-owned',True)
            if value is not None:
                cid=value['Id'];record['cid']=cid;record['cleanupInspect']=value
                if 'terminalInspect' not in record:
                    record['terminalInspect']=value
                    run('container-failed-logs',[DOCKER,'logs',cid],10,False,True)
                run('container-remove',[DOCKER,'rm','-f',cid],10,True,True)
            record['absenceVerified']=inspect(name,'container-absence',True) is None
            # Independent name lookup also covers a late-returning timed-out create.
            record['lateAbsenceVerified']=inspect(name,'container-late-absence',True) is None
            run.save()
