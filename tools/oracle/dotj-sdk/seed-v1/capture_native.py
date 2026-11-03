"""Finite SDK-host observations. Qualification tooling, never a product dependency."""
import argparse,base64,hashlib,json,os,shlex,stat,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))

def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def descriptor(path):
    path=Path(path);return dict(path=str(path),bytes=path.stat().st_size,sha256=sha(path))
def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def inventory(root):
    return {p.relative_to(root).as_posix():descriptor(p) for p in Path(root).rglob('*') if p.is_file()}
def tree_inventory(root):
    return [dict(relative=p.relative_to(root).as_posix(),kind='directory' if p.is_dir() else 'file' if p.is_file() else 'special',**(descriptor(p) if p.is_file() else {})) for p in sorted(Path(root).rglob('*'))]
def fixtures(contract,dest):
    dest.mkdir(parents=True,exist_ok=False)
    for name,v in contract['files'].items():
        raw=base64.b64decode(v['base64'],validate=True)
        assert len(raw)==v['bytes'] and hashlib.sha256(raw).hexdigest()==v['sha256']
        (dest/name).write_bytes(raw)
    return inventory(dest)

def capture(args):
    from owned import Run,container,docker_argv,DOCKER,B
    own=Path(__file__).parent
    contract=json.loads((own/'contract.json').read_text(encoding='utf-8'))
    lock=json.loads((own/'baseline-lock.json').read_text(encoding='utf-8'))
    recipe=json.loads(args.recipe.read_text(encoding='utf-8'))
    assert recipe['status']=='ROOT_TECHNICAL_GATE_APPROVED', 'Native gate not approved'
    for entry in recipe['frozenInputs']:
        assert descriptor(entry['path'])==entry, 'Frozen producer/input differs'
    assert len(contract['cases'])==contract['invocationsPerOs']
    assert {c['id'] for c in contract['cases']}=={f'Q{i:02}' for i in range(1,17)}
    ids=[args.cohort] if args.cohort else [f'Q{i:02}' for i in range(1,17)]
    nativeRoot=B/('toolchains/dotnet' if args.platform=='windows' else 'toolchains/dotnet-linux-10.0.401')
    for entry in lock['tools'][args.platform]['nativeSdk'].values():assert descriptor(entry['path'])==entry
    results=[]
    for q in ids:
        selected=[c for c in contract['cases'] if c['id']==q]
        run=Run(args.out/q,linux=args.platform=='linux')
        error=None
        try:
            run.receipt.update(platform=args.platform,cohort=q,contract=descriptor(own/'contract.json'),lock=descriptor(own/'baseline-lock.json'),producer=[descriptor(own/x) for x in ['capture_native.py','owned.py']],nativeRole='ACTUAL_NATIVE_SDK_HOST',invocations=[])
            frozen=fixtures(contract,run.out/'fixtures')
            run.receipt['fixturesBefore']=frozen
            common=dict(recipe['environment'])
            # Do not force an out-of-process node. This is one bounded host evaluation.
            common.pop('MSBUILDNOINPROCNODE',None)
            if args.platform=='windows':
                run.env.update(common)
                run.env.pop('DOTNET_NOLOGO',None);run.env.pop('MSBUILD_EXE_PATH',None)
                run.env['PATH']=str(Path(os.environ['SystemRoot'])/'System32')
                run.receipt['network']=recipe['windowsNetwork']
                run.receipt['environmentOverrides'].update(common)
                for p in (run.out/'fixtures').iterdir():p.chmod(stat.S_IREAD)
                for index,case in enumerate(selected):
                    argv=[str(nativeRoot/'dotnet.exe')]+[a.replace('{fixtures}',str(run.out/'fixtures')) for a in case['argv']]
                    if case['argv'][0] in ('msbuild','build'):argv.append('-noAutoResponse')
                    label=f'native-{index:02}'
                    before=inventory(run.out/'home')
                    run(label,argv,20,False)
                    op=run.receipt['operations'][-1]
                    assert not any(op['process'].get(k) for k in ['timedOut','error','cleanupError','outputLimitExceeded'])
                    run.receipt['invocations'].append(dict(case=case,argv=argv,operation=label,exitCode=op['process']['exitCode'],stdout=op['stdout'],stderr=op['stderr'],homeBefore=before,homeAfter=inventory(run.out/'home')))
                    run.save()
            else:
                slot=args.linux_root/q
                # This parent was empty and case-enabled by the separately retained preparation receipt.
                assert args.linux_root.is_dir() and not slot.exists()
                require_tmp=args.linux_tmp_root/q
                assert args.linux_tmp_root.is_dir() and not require_tmp.exists()
                require_tmp.mkdir()
                run.receipt['systemTmpBefore']=tree_inventory(require_tmp)
                assert not run.receipt['systemTmpBefore']
                env=dict(common,HOME='/work/home',TMPDIR='/work/tmp',DOTNET_CLI_HOME='/work/home',NUGET_PACKAGES='/work/cache',LANG='C.UTF-8',LC_ALL='C.UTF-8',DOTNET_ROOT='/sdk',DOTNET_MULTILEVEL_LOOKUP='0',MSBUILDUSEREXTENSIONSPATH='/work/home/msbuild')
                env={k:v.replace('/work','/parent/'+q) for k,v in env.items()}
                shell=['set -eu','mkdir -p /work/home /work/tmp /work/cache /work/empty','cd /work/empty','stat -f -c "%T" /work > /work/filesystem.txt','touch /work/CaseProbe /work/caseprobe','test "$(find /work -maxdepth 1 -name "*robe" | wc -l)" -eq 2']
                for index,case in enumerate(selected):
                    argv=['/sdk/dotnet']+[a.replace('{fixtures}','/fixtures') for a in case['argv']]
                    if case['argv'][0] in ('msbuild','build'):argv.append('-noAutoResponse')
                    label=f'native-{index:02}'
                    shell += ['set +e',shlex.join(['/usr/bin/timeout','-s','KILL','20',*argv])+f' > /work/{label}.stdout 2> /work/{label}.stderr',f'printf "%s\\n" "$?" > /work/{label}.exit','set -e']
                    run.receipt['invocations'].append(dict(case=case,argv=argv,operation=label))
                # Docker creates the empty slot; every content entry is Linux-created.
                argv=docker_argv('dotj-task136-native-'+args.out.name.lower()+'-'+q.lower(),[(nativeRoot,'/sdk',True),(run.out/'fixtures','/fixtures',True),(args.linux_root,'/parent',False),(require_tmp,'/tmp',False)],env,['/bin/sh','-c','mkdir /parent/'+q+'; '+ '\n'.join(shell).replace('/work','/parent/'+q)])
                # Working directory exists at creation; no writable source/repository mount.
                argv[argv.index('--workdir')+1]='/parent'
                container(run,'dotj-task136-native-'+args.out.name.lower()+'-'+q.lower(),argv)
                run.receipt['systemTmpAfter']=tree_inventory(require_tmp)
                for inv in run.receipt['invocations']:
                    label=inv['operation'];inv['exitCode']=int((slot/(label+'.exit')).read_text())
                    assert inv['exitCode'] not in (124,137),'Inner timeout'
                    inv['stdout']=descriptor(slot/(label+'.stdout'));inv['stderr']=descriptor(slot/(label+'.stderr'))
                run.receipt['network']={'isolation':'Docker NetworkMode none','capture':'Container config inspected; network access impossible in selected namespace, no packet capture claimed'}
                run.receipt['filesystem']=dict(type=(slot/'filesystem.txt').read_text().strip(),caseDistinct=(slot/'CaseProbe').exists() and (slot/'caseprobe').exists(),inventory=inventory(slot))
            assert inventory(run.out/'fixtures')==frozen,'Native fixture mutation'
            run.receipt['fixturesAfter']=inventory(run.out/'fixtures')
            run.receipt['privateDelta']=inventory(run.out/'home')
            for entry in lock['tools'][args.platform]['nativeSdk'].values():assert descriptor(entry['path'])==entry
            run.receipt['nativeInputsUnchanged']=True
        except BaseException as exc:
            error=exc
            if args.platform=='linux' and args.linux_tmp_root and (args.linux_tmp_root/q).is_dir():
                run.receipt['systemTmpAfter']=tree_inventory(args.linux_tmp_root/q)
        run.finish(error)
        results.append(descriptor(run.out/'receipt.json'))
        save(args.out/'manifest.json',dict(status='FAILED' if error else 'CAPTURED_NOT_QUALIFIED',platform=args.platform,receipts=results))
        if error:raise error

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--platform',choices=['windows','linux'],required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--recipe',type=Path,required=True)
    parser.add_argument('--linux-root',type=Path)
    parser.add_argument('--linux-tmp-root',type=Path)
    parser.add_argument('--cohort',choices=[f'Q{i:02}' for i in range(1,17)])
    capture(parser.parse_args())
