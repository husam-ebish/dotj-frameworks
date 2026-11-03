"""Behavioral seed acceptance; missing seed is the initial expected feature RED."""
import argparse,json,os,sys,shutil,base64,hashlib,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from capture_native import descriptor,save

def ps_command(script,args):
    quote=lambda s:"'"+str(s).replace("'","''")+"'"
    code='$dotjArgs=@('+','.join(quote(s) for s in args)+'); & '+quote(script)+' @dotjArgs'
    return ['C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe','-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-EncodedCommand',base64.b64encode(code.encode('utf-16-le')).decode()]

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source-root',type=Path,required=True)
    p.add_argument('--attempt',type=Path,required=True)
    p.add_argument('--expect-red',action='store_true')
    args=p.parse_args()
    entry=args.source_root/'dotj-sdk/seed/build.ps1'
    # A missing source seed cannot produce the requested runnable SDK.
    result=dict(test='S01-source-only-build-and-query',producer=descriptor(__file__),entry=str(entry),status='RUNNING')
    if not entry.is_file():
        args.attempt.mkdir(parents=True,exist_ok=False)
        result.update(status='FEATURE_RED',reason='source-only SDK seed entrypoint absent',actualProductLaunches=0)
        save(args.attempt/'result.json',result)
        print(json.dumps(result));return 0 if args.expect_red else 1
    if args.expect_red:raise AssertionError('Expected source absence RED no longer applies')
    from owned import Run,B
    run=Run(args.attempt);error=None
    try:
        source=run.out/'source-root';source.mkdir()
        lock=args.source_root/'dotj-sdk/seed/sources.properties'
        relatives=[line.split('=',1)[0][7:] for line in lock.read_text().splitlines() if line.startswith('sha256.')]
        relatives += ['dotj-sdk/seed/sources.properties','dotj-sdk/seed/build.ps1','dotj-sdk/seed/build.sh']
        for relative in relatives:
            target=source/relative;target.parent.mkdir(parents=True,exist_ok=True)
            raw=(args.source_root/relative).read_bytes()
            if relative.endswith('.java'):raw=raw.replace(b'\r\n',b'\n')
            target.write_bytes(raw)
        run.receipt['sourceInputs']=[dict(relative=r,file=descriptor(source/r)) for r in relatives]
        run.env['JAVA_HOME']=str(B/'toolchains/jdk-qualified/jdk-21.0.12.1+1')
        run.env['PATH']='C:/Windows/System32'
        output=run.out/'sdk';shell='C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe'
        run('seed-build',[shell,'-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',source/'dotj-sdk/seed/build.ps1','-Output',output],120)
        pointer=(output/'current').read_text().splitlines();jar=output/'versions'/pointer[0]/'dotj.jar'
        assert descriptor(jar)['sha256']==pointer[1]
        run.receipt['jar']=descriptor(jar);run.receipt['sdkRoot']=str(output)
        run.receipt['environmentOverrides'].update(JAVA_HOME=run.env['JAVA_HOME'],PATH=run.env['PATH'])
        project=run.out/'probe.proj';project.write_text('<Project><PropertyGroup><Probe>seed-baseline</Probe></PropertyGroup></Project>\n')
        for label,tail,want in [('help',['--help'],'Usage: dotj'),('query',['msbuild',str(project),'-getProperty:Probe'],'seed-baseline')]:
            run(label,ps_command(output/'dotj.ps1',tail),20)
            assert want in (run.out/(label+'.stdout')).read_text(encoding='utf-8-sig')
            assert (run.out/(label+'.stderr')).read_bytes()==b''
        run.receipt['classes']={name:hashlib.sha256(raw).hexdigest() for name,raw in ((n,zipfile.ZipFile(jar).read(n)) for n in zipfile.ZipFile(jar).namelist() if n.endswith('.class'))}
        run.receipt['scope']='One actual source-only fresh Windows build + help/query; offline isolation not qualified'
    except BaseException as caught:error=caught
    run.finish(error)
    if error:raise error
    print(json.dumps(dict(status='PASS_SOURCE_ONLY_BUILD_HELP_QUERY',jar=descriptor(jar))))
    return 0

if __name__=='__main__':sys.exit(main())
