"""Finite pinned Linux container launch profile for OP02C native references."""
import importlib.util
from pathlib import Path
import re
import time

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('op02c_windows_helpers',HERE/'capture_windows.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
B=shared.B
DOCKER=Path('C:/Users/husam/AppData/Local/Programs/DockerDesktop/resources/bin/docker.exe')
IMAGE='mcr.microsoft.com/dotnet/aspnet@sha256:222759b391a1aaf241166672c8f99b2d4ada452e7b5319f3c6e8f265a37b5ad4'


def create_argv(name, output, environment, command):
    shared.wire.require(re.fullmatch('dotj-task149-[a-z0-9-]+',name) is not None,'INVALID_CONTAINER_OWNER_NAME')
    argv=[str(DOCKER),'create','--pull=never','--name',name,'--label','dotj.owner=task149',
          '--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges',
          '--cpus','2','--memory','512m','--memory-swap','512m','--pids-limit','64','--ulimit','core=0',
          '--stop-timeout','2','--workdir','/work']
    mounts=[(B/'toolchains/dotnet-linux-10.0.401','/sdk',True),
            (B/'toolchains/jdk-linux21/jdk-21.0.12.1+1','/jdk',True),
            (HERE/'reference','/reference',True),(HERE/'java','/java-source',True),
            (output,'/work',False),(output/'tmp','/tmp',False)]
    for source,target,readonly in mounts:
        argv+=['--mount',f'type=bind,source={source},target={target}'+(',readonly' if readonly else '')]
    for key,value in sorted(environment.items()):argv+=['--env',key+'='+value]
    return argv+['--entrypoint','/usr/bin/timeout',IMAGE,'-s','KILL','25',*command]


class ContainerRun:
    """Exact owned name/CID lifecycle; no ambient container enumeration/cleanup."""
    def __init__(self,output):
        self.output=output
        self.runner=shared.NativeRun(output)
        self.deadline=time.monotonic()+180
        self.record={'owner':'task149','image':IMAGE,'cid':None,'absenceVerified':False}

    def operation(self,label,argv,cleanup=False):
        remaining=self.deadline-time.monotonic()-(0 if cleanup else 40)
        shared.wire.require(remaining>0,'CONTAINER_AGGREGATE_DEADLINE')
        normal=30 if label=='wait' else 15
        record=self.runner.run(argv,self.output,self.runner.caller,label,min(normal,remaining),cleanup=cleanup)
        if record.get('guardValidationFailed'):
            self.record.setdefault('cleanupGuardFailures',[]).append(label)
        return record,Path(record['stdoutPath']).read_bytes(),Path(record['stderrPath']).read_bytes()

    def inspect(self,name,label,cleanup=False):
        record,stdout,stderr=self.operation(label,[str(DOCKER),'inspect','--type','container',name],cleanup)
        if record['exitCode']!=0:
            shared.wire.require(b'No such' in stderr,'CONTAINER_ABSENCE_UNKNOWN')
            return None
        values=shared.wire.strict_json(stdout);shared.wire.require(len(values)==1)
        value=values[0]
        shared.wire.require(value['Name']=='/'+self.record['name'] and value['Config']['Labels'].get('dotj.owner')=='task149' and value['Config']['Image']==IMAGE,'CONTAINER_OWNER_MISMATCH')
        return value

    def run(self,name,environment,command,argv=None):
        self.record['name']=name
        attempted=False
        try:
            attempted=True
            r,stdout,_=self.operation('create',argv or create_argv(name,self.output,environment,command))
            shared.wire.require(r['exitCode']==0,'CONTAINER_CREATE_FAILED')
            cid=stdout.decode('ascii').strip();shared.wire.require(re.fullmatch('[a-f0-9]{64}',cid) is not None)
            self.record['cid']=cid
            self.record['createdInspect']=self.inspect(cid,'created-inspect')
            validate_container(self.record['createdInspect'])
            r,_,_=self.operation('start',[str(DOCKER),'start',cid]);shared.wire.require(r['exitCode']==0)
            r,stdout,_=self.operation('wait',[str(DOCKER),'wait',cid]);shared.wire.require(r['exitCode']==0)
            self.record['exitCode']=int(stdout.strip())
            self.operation('logs',[str(DOCKER),'logs',cid])
            terminal=self.inspect(cid,'terminal-inspect');self.record['terminalInspect']=terminal
            shared.wire.require(not terminal['State']['Running'] and not terminal['State']['OOMKilled'] and terminal['State']['ExitCode']==self.record['exitCode'])
            shared.wire.require(self.record['exitCode']==0,'CONTAINER_COMMAND_FAILED')
        finally:
            if attempted:
                # A fully verified terminal CID cannot be reused as another
                # container. Keep that exact identity for removal; failed or
                # incomplete attempts still need a fresh ownership inspection.
                terminal=self.record.get('terminalInspect')
                state=terminal.get('State',{}) if terminal else {}
                value=terminal if (self.record.get('exitCode')==0 and state.get('ExitCode')==0 and
                                   state.get('Running') is False and state.get('OOMKilled') is False) else None
                if value is None:
                    value=self.inspect(self.record['cid'] or name,'cleanup-inspect',True)
                if value is not None:
                    self.record['cid']=value['Id'];self.record['cleanupInspect']=value
                    r,_,_=self.operation('remove',[str(DOCKER),'rm','-f',value['Id']],True);shared.wire.require(r['exitCode']==0)
                self.record['absenceVerified']=self.inspect(name,'removed-absence',True) is None
                self.record['lateAbsenceVerified']=self.inspect(name,'late-absence',True) is None
                shared.save(self.output/'container-receipt.json',self.record)
        shared.wire.require(not self.record.get('cleanupGuardFailures'),'CONTAINER_CLEANUP_GUARD_FAILURE')
        return self.record


def prepare_output(output):
    """Case-enable the empty assigned root before retained inputs populate it."""
    shared.wire.require(not any(output.iterdir()),'LINUX_OUTPUT_NOT_EMPTY_FOR_CASE_SETUP')
    logs=output.parent/(output.name+'-case-preparation')
    shared.wire.require(not logs.exists(),'CASE_PREPARATION_EXISTS');logs.mkdir()
    runner=shared.NativeRun(logs)
    for action,args in [('set',['setCaseSensitiveInfo',str(output),'enable']),('query',['queryCaseSensitiveInfo',str(output)])]:
        r=runner.run(['C:/Windows/System32/fsutil.exe','file',*args],logs,dict(runner.caller),'case-'+action,15)
        raw=Path(r['stdoutPath']).read_bytes()
        shared.wire.require(r['exitCode']==0 and b' is enabled' in raw and b'Failed' not in raw,'LINUX_CASE_PROFILE_UNAVAILABLE')
    shared.save(output/'case-preparation.json',{'operations':shared.file_descriptor(logs/'native-operations.json'),'verified':True})

def linux_environment():
    return {'PATH':'/usr/bin:/bin','HOME':'/work/home','TMPDIR':'/work/tmp','LANG':'C.UTF-8','LC_ALL':'C.UTF-8',
            'DOTNET_ROOT':'/sdk','DOTNET_CLI_HOME':'/work/home','NUGET_PACKAGES':'/work/cache',
            'NUGET_HTTP_CACHE_PATH':'/work/cache/http','DOTNET_MULTILEVEL_LOOKUP':'0',
            'DOTNET_CLI_TELEMETRY_OPTOUT':'1','DOTNET_SKIP_FIRST_TIME_EXPERIENCE':'1','DOTNET_NOLOGO':'1',
            'DOTNET_PROCESSOR_COUNT':'2','DOTNET_ROLL_FORWARD':'Disable','MSBUILDDISABLENODEREUSE':'1',
            'MSBUILDUSEREXTENSIONSPATH':'/work/home/msbuild','DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE':'true',
            'DOTNET_CLI_USE_MSBUILD_SERVER':'0','DOTNET_EnableDiagnostics':'0','DOTNET_DbgEnableMiniDump':'0',
            'DOTJ_FIXTURE_REMOVE':'synthetic-remove'}


def validate_container(value):
    host=value['HostConfig']
    shared.wire.require(host['NetworkMode']=='none' and host['ReadonlyRootfs'] is True and
                        set(host['CapDrop'])=={'ALL'} and 'no-new-privileges' in host['SecurityOpt'] and
                        host['NanoCpus']==2000000000 and host['Memory']==536870912 and
                        host['MemorySwap']==536870912 and host['PidsLimit']==64, 'CONTAINER_CAPS_CHANGED')
    mounts={m['Destination']:m for m in value['Mounts']}
    for path in ('/sdk','/jdk','/reference','/java-source'):
        shared.wire.require(mounts[path]['RW'] is False,'WRITABLE_TOOL_MOUNT')
    shared.wire.require(mounts['/work']['RW'] is True and mounts['/tmp']['RW'] is True)


def native_operation(output,work,label,argv,cwd,environment):
    """Shell owns waitpid for one child; metadata comes from live /proc identity."""
    import shlex
    local=work/label;local.mkdir()
    for part in ('home','tmp','cache'):(local/part).mkdir()
    # The whole capture is mounted at /work, preserving exact native request paths.
    rel=local.relative_to(output).as_posix();base='/work/'+rel
    script=local/'operation.sh'
    lines=['set -eu','umask 077','cd '+shlex.quote(cwd),
           'env -0 > '+shlex.quote(base+'/caller-environment.bin'),
           'read up rest < /proc/uptime; printf "%s\\n" "$up" > '+shlex.quote(base+'/start.uptime'),
           shlex.join(['/usr/bin/env','-i',*[k+'='+v for k,v in environment.items()],*argv])+
           ' > '+shlex.quote(base+'/stdout.bin')+' 2> '+shlex.quote(base+'/stderr.bin')+' &',
           'child=$!','printf "%s\\n" "$child" > '+shlex.quote(base+'/pid'),
           'cat /proc/$child/stat > '+shlex.quote(base+'/identity.stat'),
           'set +e','wait "$child"','code=$?','set -e',
           'printf "%s\\n" "$code" > '+shlex.quote(base+'/exit'),
           'read up rest < /proc/uptime; printf "%s\\n" "$up" > '+shlex.quote(base+'/end.uptime'),
           'stat -f -c "%T" /work > '+shlex.quote(base+'/filesystem.txt')]
    script.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    command_scripts=[]
    for arg in argv:
        if isinstance(arg,str) and arg.startswith('/work/'):
            path=output/arg[len('/work/'):]
            if path.is_file() and path.suffix=='.sh':command_scripts.append(shared.file_descriptor(path))
    shared.save(local/'prelaunch-native.json',{'wrapperScript':shared.file_descriptor(script),
                'commandScripts':command_scripts,'argv':argv,'cwd':cwd,'configuredEnvironment':environment,
                'clockDomain':'Linux /proc/uptime monotonic nanoseconds','outerOwnershipProfile':'reported-exit-join/4'})
    group=ContainerRun(local)
    # create_argv's output must be the full capture, while host receipts stay in
    # the exact operation slot; avoid remapping /work and changing native paths.
    original=create_argv
    command=['/bin/sh','/work/'+script.relative_to(output).as_posix()]
    name='dotj-task149-'+output.name.lower()+'-'+work.name.lower()+'-'+label.lower()
    group_argv=original(name,output,linux_environment(),command)
    container=group.run(name,linux_environment(),command,argv=group_argv)
    start=int(float((local/'start.uptime').read_text())*1e9);end=int(float((local/'end.uptime').read_text())*1e9)
    pid=int((local/'pid').read_text());stat=(local/'identity.stat').read_text();tail=stat[stat.rfind(')')+2:].split()
    shared.wire.require(int(stat.split(' ',1)[0])==pid and len(tail)>=20,'NATIVE_IDENTITY_MISSING')
    raw=(local/'caller-environment.bin').read_bytes()
    caller=dict(entry.decode('utf-8').split('=',1) for entry in raw.split(b'\0') if entry)
    shared.save(local/'native-caller-environment.json',caller)
    native={'argv':argv,'cwd':cwd,'environment':environment,'exitCode':int((local/'exit').read_text()),
            'identity':{'pid':pid,'startIdentity':'linux-proc-startticks:'+tail[19]},
            'startNanos':start,'endNanos':end,'deadlineNanos':start+25000000000,
            'stdoutPath':str(local/'stdout.bin'),'stderrPath':str(local/'stderr.bin')}
    shared.wire.require(native['exitCode'] not in (124,137) and end<=native['deadlineNanos'],'INNER_TIMEOUT')
    shared.save(local/'native-record.json',native)
    return native,{'identity':container['cid'],'caps':container['createdInspect']['HostConfig'],
                  'exitCode':container['exitCode'],'removed':container['absenceVerified'] and container['lateAbsenceVerified']}

def run_capture(contract,fixtures,output):
    import shlex
    caller=shared.wire.controlled_snapshot()
    for part in ('home','tmp','cache','reference','boundary','preparation'):(output/part).mkdir()
    shared.wire.require((output/'case-preparation.json').is_file(),'LINUX_CASE_PREPARATION_MISSING')
    (output/'global.json').write_bytes(shared.wire.json_bytes({'sdk':{'version':'10.0.401','rollForward':'disable'}}))
    props=['-p:BaseIntermediateOutputPath=/work/fixture/obj/','-p:MSBuildProjectExtensionsPath=/work/fixture/obj/',
           '-p:OutputPath=/work/fixture/bin/','-p:UseSharedCompilation=false','-p:BuildInParallel=false']
    prepare_reference_fixture(output,props)
    shared.wire.require((output/'CaseProbe').exists() and (output/'caseprobe').exists())
    shared.wire.require((output/'filesystem.txt').read_text().strip() in ('9p','v9fs'),'UNMEASURED_FILESYSTEM_PROFILE')
    for name in ('Program.cs','Reference.csproj','NuGet.Config'):
        shared.wire.require((output/'fixture/source'/name).read_bytes()==(HERE/'reference'/name).read_bytes(),'REFERENCE_SOURCE_CHANGED')
    classes,probe_inputs=shared.copy_probe_classes(output)
    inputs=[shared.file_descriptor(p) for p in sorted((output/'fixture').rglob('*')) if p.is_file()]
    tool=B/'toolchains/dotnet-linux-10.0.401/dotnet'
    native_inputs=[dict(shared.file_descriptor(tool),path='/sdk/dotnet')]
    network={'isolation':'Docker NetworkMode none, read-only root, cap-drop ALL, no-new-privileges.',
             'observation':'Exact owned container creation and terminal inspect retained; writable filesystem measured as case-enabled 9p.',
             'unqualifiedScope':'Selected Windows-backed 9p/NTFS profile only; no generic ext4 claim.'}
    rows={};groups={}
    for definition in fixtures['referenceRows']:
        if definition['platform']!='linux':continue
        row=output/Path(definition['files'][0]).parent;row.mkdir()
        cwd=row/fixtures['corpus']['cwd'];cwd.mkdir(parents=True)
        roots={k:row/('effects-'+k) for k in ('source','priorSDK','siblings','staging')}
        for root in roots.values():root.mkdir();(root/'sentinel.txt').write_bytes(b'OP02C preservation sentinel\n')
        mode=next(v['modes'][0] for v in fixtures['cohortDefinitions'] if v['id']==definition['cohort'])
        selected={'path':'/sdk/dotnet','sha256':shared.wire.sha256(tool.read_bytes())}
        if mode=='invalid-start':selected={'path':'/work/'+row.relative_to(output).as_posix()+'/missing','sha256':'0'*64}
        native_cwd='/work/'+cwd.relative_to(output).as_posix()
        native_roots={k:'/work/'+v.relative_to(output).as_posix() for k,v in roots.items()}
        request=shared.prepare_request(contract,fixtures,definition['id'],'linux',definition['engine'],mode,selected,native_cwd,
                                       linux_environment(),native_roots,native_inputs+inputs)
        raw=shared.wire.json_bytes(request);request_path=row/'request.json';request_path.write_bytes(raw)
        before=shared.snapshot_roots(roots);shared.save(row/'effects-before.json',before)
        argv=['/sdk/dotnet','run','--project','/work/fixture/source/Reference.csproj','--no-build',*props,
              '--','--mode',mode,'--request','/work/'+request_path.relative_to(output).as_posix(),'--',*request['argv']]
        record,container=native_operation(output,row,definition['id'],argv,native_cwd,shared.wire.child_environment(request['environment'],'linux'))
        for channel in ('stdout','stderr'):(row/(channel+'.bin')).write_bytes(Path(record[channel+'Path']).read_bytes())
        observation=shared.wire.verify_fixture((row/'stdout.bin').read_bytes(),request,raw,record['exitCode'])
        effect=shared.effects(request,raw,before,shared.snapshot_roots(roots),network)
        facts=shared.result(request,raw,row,record,observation,effect,caller,network,container)
        shared.wire.capture_row(row,raw,facts,effect,contract)
        rows[definition['id']]=shared.wire.descriptor(request_path,output)
        shared.save(output/'reference/observations-linux.json',{'status':'CAPTURE_IN_PROGRESS','referenceRows':rows})
    for definition in fixtures['boundaryGroups']:
        if definition['platform']!='linux':continue
        group=output/Path(definition['files'][1]).parent;group.mkdir()
        observations=[]
        for mode in definition['modes']:
            if mode.startswith('sdk-'):
                captured=linux_sdk_mode(contract,fixtures,output,definition,mode,network,caller)
            else:
                captured=linux_jdk_mode(contract,fixtures,output,definition,mode,probe_inputs,network,caller)
            observations.append(captured)
            shared.persist_mode(group,captured)
        groups[definition['id']]=shared.seal_group(output,definition,observations)
    input_desc={key:shared.wire.descriptor(output/'inputs'/name,output) for key,name in
                (('contract','contract.json'),('fixtures','fixtures.json'),('sourceMap','source-map.json'))}
    return shared.write_aggregates(output,'linux',rows,groups,input_desc)


def linux_jdk_mode(contract,fixtures,output,definition,mode,inputs,network,caller):
    group=output/Path(definition['files'][1]).parent;work=group/mode;work.mkdir()
    cwd=work/fixtures['corpus']['cwd'];cwd.mkdir(parents=True)
    roots={k:work/('effects-'+k) for k in ('source','priorSDK','siblings','staging')}
    for root in roots.values():root.mkdir();(root/'sentinel.txt').write_bytes(b'OP02C preservation sentinel\n')
    selected=B/'toolchains/jdk-linux21/jdk-21.0.12.1+1/bin'/('javac' if mode=='javac-unicode' else 'java')
    native_cwd='/work/'+cwd.relative_to(output).as_posix()
    native_roots={k:'/work/'+v.relative_to(output).as_posix() for k,v in roots.items()}
    tools=[dict(shared.file_descriptor(B/'toolchains/jdk-linux21/jdk-21.0.12.1+1/bin'/n),path='/jdk/bin/'+n) for n in ('java','javac')]
    request=shared.prepare_request(contract,fixtures,definition['id'],'linux','jdk-probe',mode,
                                   {'path':'/jdk/bin/'+selected.name,'sha256':shared.wire.sha256(selected.read_bytes())},
                                   native_cwd,linux_environment(),native_roots,inputs+tools)
    raw=shared.wire.json_bytes(request);request_path=work/'prelaunch.json';request_path.write_bytes(raw)
    before=shared.snapshot_roots(roots)
    shared.save(work/'effects-before.json',before)
    argv=['/jdk/bin/java',*shared.java_flags('/work/tmp','/work/home'),'-cp','/work/probe-classes','ProcessProbe',
          '--mode',mode,'--request','/work/'+request_path.relative_to(output).as_posix(),'--',*request['argv']]
    record,container=native_operation(output,work,mode,argv,native_cwd,shared.wire.child_environment(request['environment'],'linux'))
    for channel in ('stdout','stderr'):(work/(channel+'.bin')).write_bytes(Path(record[channel+'Path']).read_bytes())
    observation=shared.wire.verify_jdk((work/'stdout.bin').read_bytes(),request,raw,record['exitCode'])
    for artifact in observation['telemetry']:
        shared.wire.require(shared.file_descriptor(cwd/artifact['path'])['sha256']==artifact['sha256'])
        (group/artifact['path']).write_bytes((cwd/artifact['path']).read_bytes())
    effect=shared.effects(request,raw,before,shared.snapshot_roots(roots),network)
    facts=shared.result(request,raw,work,record,observation,effect,caller,network,container)
    for channel in ('stdout','stderr'):
        path=group/(channel+'.bin');old=path.read_bytes() if path.exists() else b''
        data=(work/(channel+'.bin')).read_bytes();path.write_bytes(old+data)
        facts['streams'][channel]={'path':channel+'.bin','offset':len(old),'bytes':len(data),'sha256':shared.wire.sha256(data),'truncated':False}
    return mode,raw,facts,effect

def linux_sdk_mode(contract,fixtures,output,definition,mode,network,caller):
    import shlex
    group=output/Path(definition['files'][1]).parent;work=group/mode;work.mkdir()
    cwd=work/fixtures['corpus']['cwd'];cwd.mkdir(parents=True)
    native_cwd='/work/'+cwd.relative_to(output).as_posix();base='/work/'+work.relative_to(output).as_posix()
    roots={k:work/('effects-'+k) for k in ('source','priorSDK','siblings','staging')}
    for root in roots.values():root.mkdir();(root/'sentinel.txt').write_bytes(b'OP02C preservation sentinel\n')
    tool=B/'toolchains/dotnet-linux-10.0.401/dotnet'
    request=shared.prepare_request(contract,fixtures,definition['id'],'linux','sdk-command',mode,
      {'path':'/sdk/dotnet','sha256':shared.wire.sha256(tool.read_bytes())},native_cwd,linux_environment(),
      {k:'/work/'+v.relative_to(output).as_posix() for k,v in roots.items()},[dict(shared.file_descriptor(tool),path='/sdk/dotnet'),shared.source_reaper()])
    raw=shared.wire.json_bytes(request);(work/'prelaunch.json').write_bytes(raw)
    before=shared.snapshot_roots(roots);shared.save(work/'effects-before.json',before)
    env=shared.wire.child_environment(request['environment'],'linux')
    props=['-p:BaseIntermediateOutputPath=/work/fixture/obj/','-p:MSBuildProjectExtensionsPath=/work/fixture/obj/',
           '-p:OutputPath=/work/fixture/bin/','-p:UseSharedCompilation=false','-p:BuildInParallel=false']
    sdk=['/sdk/dotnet','run','--project','/work/fixture/source/Reference.csproj','--no-build',*props,
         '--','--reference-child',request['rowId'],'wait-cancel-force','--',*request['argv']]
    invocation={'executable':sdk[0],'argv':sdk[1:],'cwd':native_cwd,'environment':{'baseline':{'values':env},'set':{},'remove':[]},'inputSha256':shared.wire.sha256(raw)}
    script=work/'sdk-observer.sh';signal='TERM' if mode=='sdk-signal' else 'KILL'
    static={'schema':'dotj.owned-process.sdk-boundary-native/1','rowId':request['rowId'],'mode':mode,'requestSha256':shared.wire.sha256(raw),
            'invocation':invocation,'clockDomain':'Linux /proc/uptime monotonic nanoseconds','drainers':'SDK stdout/stderr direct owned files; shell waitpid reaped SDK parent; no pipe worker threads'}
    # All variable facts are read from actual shell wait/proc/stream observations.
    prefix=shared.wire.json_bytes(static).decode().rstrip().rstrip('}')
    lines=['set -eu','umask 077','base='+shlex.quote(base),'cd '+shlex.quote(native_cwd),
      'mono() { awk \'{printf "%.0f", $1*1000000000}\' /proc/uptime; }',
      'state() {',
      '  target=$1; output=$2; now=$(mono); terminal=true; method=proc-identity-absent;',
      '  if test -r "/proc/$target/stat"; then',
      '    cat "/proc/$target/stat" > "$output.stat";',
      '    current=$(awk \'{print $22}\' "$output.stat"); test "$current" = "$child_start";',
      '    status=$(awk \'{print $3}\' "$output.stat"); method=proc-identity-state-$status;',
      '    if test "$status" != Z && test "$status" != X; then terminal=false; fi;',
      '  fi;',
      '  printf \'{"observedTerminal":%s,"exitCode":null,"method":"%s","observedNanos":%s}\' "$terminal" "$method" "$now" > "$output";',
      '}',
      'printf \'\\000\\000\\000\\000X\' > "$base/sdk-stdin.bin"',
      shlex.join(['/usr/bin/env','-i',*[k+'='+v for k,v in env.items()],*sdk])+' < "$base/sdk-stdin.bin" > "$base/sdk-stdout.bin" 2> "$base/sdk-stderr.bin" &',
      'sdk=$!; cat /proc/$sdk/stat > "$base/sdk-initial.stat";',
      'sdk_start=$(awk \'{print $22}\' "$base/sdk-initial.stat");',
      'ready_end=$(($(mono)+14000000000)); while ! grep -q "}$" "$base/sdk-stdout.bin"; do',
      '  test "$(mono)" -lt "$ready_end"; kill -0 "$sdk"; sleep .01;',
      'done;',
      'child=$(sed -n \'s/^.*"pid":\\([0-9][0-9]*\\).*$/\\1/p\' "$base/sdk-stdout.bin");',
      'test -n "$child"; test "$child" != "$sdk";',
      'cat /proc/$child/stat > "$base/child-initial.stat"; child_start=$(awk \'{print $22}\' "$base/child-initial.stat");',
      'state "$child" "$base/pre-action.json"; grep -q \'"observedTerminal":false\' "$base/pre-action.json";',
      'current=$(awk \'{print $22}\' /proc/$sdk/stat); test "$current" = "$sdk_start";',
      'action_start=$(mono); kill -'+signal+' "$sdk"; action_end=$(mono);',
      'set +e; wait "$sdk"; sdk_exit=$?; set -e; parent_end=$(mono);',
      'state "$child" "$base/before.json"; cleanup=false; cleanup_start=null; cleanup_end=null;',
      'if grep -q \'"observedTerminal":false\' "$base/before.json"; then',
      '  current=$(awk \'{print $22}\' /proc/$child/stat); test "$current" = "$child_start";',
      '  cleanup_start=$(mono); kill -TERM "$child"; cleanup_end=$(mono); cleanup=true;',
      'fi;',
      'count=0; while :; do state "$child" "$base/after.json"; if grep -q \'"observedTerminal":true\' "$base/after.json"; then break; fi; count=$((count+1)); test "$count" -le 400; sleep .01; done;',
      'printf %s '+shlex.quote(prefix)+ ';',
      'printf \',"sdkPid":%s,"sdkStart":"%s","childPid":%s,"childStart":"%s","sdkExit":%s,"parentEndNanos":%s,"actionStartNanos":%s,"actionEndNanos":%s,"cleanupPerformed":%s,"cleanupStartNanos":%s,"cleanupEndNanos":%s,"ready":\' "$sdk" "$sdk_start" "$child" "$child_start" "$sdk_exit" "$parent_end" "$action_start" "$action_end" "$cleanup" "$cleanup_start" "$cleanup_end";',
      'head -n 1 "$base/sdk-stdout.bin";',
      'printf \',"before":\'; cat "$base/before.json"; printf \',"after":\'; cat "$base/after.json"; printf \'}\\n\';']
    script.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    record,container=native_operation(output,work,'sdk-observer',['/bin/sh','/work/'+script.relative_to(output).as_posix()],native_cwd,linux_environment())
    shared.wire.require(record['exitCode']==0,'SDK_NATIVE_OBSERVER_FAILED')
    for channel in ('stdout','stderr'):(work/(channel+'.bin')).write_bytes(Path(record[channel+'Path']).read_bytes())
    native=shared.wire.strict_json((work/'stdout.bin').read_bytes())
    parent_identity={'pid':native['sdkPid'],'startIdentity':'linux-proc-startticks:'+native['sdkStart']}
    child_identity={'pid':native['childPid'],'startIdentity':'linux-proc-startticks:'+native['childStart']}
    cleanup=[]
    if native['cleanupPerformed']:
        cleanup=[{'kind':'SIGTERM','identity':child_identity,'requestedNanos':native['cleanupStartNanos'],
                  'completedNanos':native['cleanupEndNanos'],'succeeded':True}]
    observation={'schema':'dotj.owned-process.sdk-boundary/1','rowId':request['rowId'],'mode':mode,'requestSha256':shared.wire.sha256(raw),
      'availability':{'state':'MEASURED','reason':'Actual pinned SDK process, exact verified proc-startticks, owned shell waitpid and explicit scoped signal.'},
      'platform':{'os':'linux','arch':'x64','profile':'owned-container-POSIX'},'source':shared.source_reaper(),
      'sdkParent':{'identity':parent_identity,'invocation':native['invocation'],
        'terminal':{'observedTerminal':True,'exitCode':native['sdkExit'],'method':'shell waitpid exact SDK child','observedNanos':native['parentEndNanos']}},
      'targetChild':{'identity':child_identity,'ready':native['ready'],'beforeObserverCleanup':native['before'],'afterObserverCleanup':native['after']},
      'action':{'kind':'SIGTERM' if mode=='sdk-signal' else 'SIGKILL','identity':parent_identity,'requestedNanos':native['actionStartNanos'],
                'completedNanos':native['actionEndNanos'],'succeeded':True},
      'observerCleanup':{'actions':cleanup,'terminalObserved':True,'workersJoined':True},'nativeReceipt':native,
      'targetStreams':{channel:shared.embedded((work/('sdk-'+channel+'.bin')).read_bytes()) for channel in ('stdout','stderr')},
      'qualification':'UNQUALIFIED_STRONGER_LIFECYCLE_GUARANTEES'}
    shared.wire.validate_sdk_boundary(observation,request,raw)
    effect=shared.effects(request,raw,before,shared.snapshot_roots(roots),network)
    facts=shared.result(request,raw,work,record,{'receivedPayload':native['ready']['receivedPayload']},effect,caller,network,container)
    facts.update(fixtureObservation=None,sdkBoundaryObservation=observation)
    facts['observationActors']={'outerProcess':'driver-owned-native-observer','parentEnvironment':'driver','payload':'actual-sdk-target-child',
                               'apiOperations':'SDK-parent-and-observer-actions-separately-attributed'}
    for channel in ('stdout','stderr'):
        path=group/(channel+'.bin');old=path.read_bytes() if path.exists() else b'';data=(work/(channel+'.bin')).read_bytes();path.write_bytes(old+data)
        facts['streams'][channel]={'path':channel+'.bin','offset':len(old),'bytes':len(data),'sha256':shared.wire.sha256(data),'truncated':False}
    return mode,raw,facts,effect


def prepare_reference_fixture(output,props):
    manifest_path=B/'agents/task149-op02c-native-captures-v1/linux-v8-build-reuse.json'
    shared.wire.require(shared.wire.sha256(manifest_path.read_bytes())=='2d7cd391adfe76caf29b8bc4086c4d91efeac19d42f8c14bc57e55070d03225b','LINUX_BUILD_REUSE_BINDING')
    manifest=shared.wire.strict_json(manifest_path.read_bytes())
    source=Path(manifest['fixture'])
    for relative,entry in manifest['files'].items():
        actual=shared.file_descriptor(source/relative)
        shared.wire.require(all(actual[k]==entry[k] for k in ('bytes','sha256')),'LINUX_BUILD_ARTIFACT_CHANGED')
    for name,entry in manifest['sourceFiles'].items():
        shared.wire.require(shared.file_descriptor(HERE/'reference'/name)==entry,'LINUX_BUILD_SOURCE_CHANGED')
    for entry in manifest['nativeProofs']:
        shared.wire.require(shared.file_descriptor(entry['path'])==entry,'LINUX_BUILD_PROOF_CHANGED')
    shared.shutil.copytree(source,output/'fixture')
    shared.save(output/'reused-build-provenance.json',{'manifest':shared.file_descriptor(manifest_path),'files':manifest['files'],'sourceFiles':manifest['sourceFiles'],'nativeProofs':manifest['nativeProofs']})
    slot=output/'preparation/filesystem';slot.mkdir()
    for part in ('home','tmp','cache'):(slot/part).mkdir()
    script=slot/'filesystem.sh';script.write_text('set -eu\ncd /work\ntouch CaseProbe caseprobe\ntest "$(find /work -maxdepth 1 -name "*robe" | wc -l)" -eq 2\nstat -f -c "%T" /work > /work/filesystem.txt\n',encoding='utf-8',newline='\n')
    cr=ContainerRun(slot);name='dotj-task149-'+output.name.lower()+'-filesystem'
    command=['/bin/sh','/work/preparation/filesystem/filesystem.sh']
    cr.run(name,linux_environment(),command,argv=create_argv(name,output,linux_environment(),command))
