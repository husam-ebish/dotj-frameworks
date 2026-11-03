"""Replay the exact final-303 Build consumers against one explicit successor JAR."""
import argparse
import json
from pathlib import Path
import shutil
import sys
import zipfile
sys.path.insert(0,str(Path(__file__).resolve().parent))
from corpus import descriptor,sha
from owned import B,JDK,Run,container,docker_argv
PRIOR=B/'agents/batch2521-build-items-evaluation-v1'
OLD_JAR=PRIOR/'product-build-v5/dotj-build-evaluation-candidate.jar'
OLD_SHA='303dc40dbb1a5db310a06e82b73038e2649d18d72ca19b79fa7df5eaaa879fea'
WINDOWS={'items':'product-windows-v3','private':'private-windows-v3','junction':'junction-windows-v3',
         'supplement':'supplement-product-windows-v3','history':'history-windows-v5','sort':'sort-windows-v2','boundary':'boundary-windows-v1'}
LINUX={'items':('product-linux-v3','product-capture.sh','product-v13201'),
       'private':('private-linux-v3','private-linux.sh','product-v13202'),
       'sort':('sort-linux-v3','sort-linux.sh','product-v13203'),
       'boundary':('boundary-linux-v2','boundary-linux.sh','product-v13204')}

def no_product(path):
    names=zipfile.ZipFile(path).namelist() if Path(path).is_file() else [p.name for p in Path(path).rglob('*.class')]
    assert not any(n.rsplit('/',1)[-1].split('$')[0].removesuffix('.class') in
        ('ProjectEvaluationComponent','ItemEvaluator','ItemExpressions','ItemGlobs','ItemSnapshot') for n in names)

def main():
    p=argparse.ArgumentParser();p.add_argument('--group',choices=list(WINDOWS),required=True)
    p.add_argument('--platform',choices=['windows','linux'],required=True);p.add_argument('--jar',type=Path,required=True)
    p.add_argument('--attempt',type=Path,required=True);p.add_argument('--work-root',type=Path)
    a=p.parse_args();run=Run(a.attempt,a.platform=='linux');out=run.out;error=None;jar=a.jar.resolve()
    prior=PRIOR/(WINDOWS[a.group] if a.platform=='windows' else LINUX[a.group][0])
    old=json.loads((prior/'receipt.json').read_text());assert old['status']=='PASS'
    run.receipt.update(mode='inherited-'+a.group+'-'+a.platform,priorReceipt=descriptor(prior/'receipt.json'),
                       jar=descriptor(jar),inputs=[descriptor(__file__),descriptor(jar)],outputs=[])
    try:
        if a.platform=='windows':
            for name in ('consumer.jar','historical-successor.jar'):
                if (prior/name).is_file():shutil.copyfile(prior/name,out/name);no_product(out/name);run.receipt['inputs'].append(descriptor(out/name))
            if a.group in ('items','supplement'):
                source=PRIOR/('corpus-input-v1' if a.group=='items' else 'supplemental-input-v1')
                shutil.copytree(source,out/'fixtures')
                run.receipt['fixtureInputs']=[dict(relative=p.relative_to(source).as_posix(),retained=descriptor(p),actual=descriptor(out/'fixtures'/p.relative_to(source))) for p in sorted(source.rglob('*')) if p.is_file()]
            if a.group=='junction':
                for kind in ('inside','outside'):
                    root=out/'controls'/kind;root.mkdir(parents=True)
                    target=root/'target' if kind=='inside' else out/'outside-target';target.mkdir();(target/'a.cs').write_text('owned fixture')
            if a.group=='history':(out/'outputs').mkdir()
            operations=[op for op in old['operations'] if op['label'] not in ('compile-consumer','consumer-jar','compile-successor','package-successor')]
            if a.group=='history':assert len(operations)==14
            for op in operations:
                argv=[s.replace(str(OLD_JAR),str(jar)).replace(OLD_SHA,sha(jar)).replace(str(prior),str(out)) for s in op['process']['argv']]
                # Every mutable output/home/temp argument in the inherited operation is redirected.
                for s in argv:
                    if s.startswith('-Djava.io.tmpdir=') or s.startswith('-Duser.home='):assert str(out) in s
                run(op['label'],argv,min(120,op['process']['timeoutSeconds']))
            if a.group in ('items','supplement'):
                run.receipt['fixtureAfter']=[descriptor(p) for p in sorted((out/'fixtures').rglob('*')) if p.is_file()]
            run.receipt['outputs']=[descriptor(p) for p in sorted(out.rglob('*')) if p.is_file() and p.suffix in ('.stdout','.stderr','.tsv')]
        else:
            assert a.work_root and a.work_root.is_dir()
            _,script_name,slot=LINUX[a.group];work=a.work_root/slot;assert not work.exists()
            consumer=PRIOR/WINDOWS[a.group]/'consumer.jar';no_product(consumer)
            source=PRIOR/'corpus-input-v1'
            script=Path(__file__).resolve().parent.parent/'items-evaluation-v1'/script_name
            jdk=B/'toolchains/jdk-linux21/jdk-21.0.12.1+1'
            run.receipt['inputs'] += [descriptor(consumer),descriptor(script),descriptor(jdk/'bin/java'),descriptor(source/'manifest.json')]
            env=dict(HOME='/work/'+slot+'/home',TMPDIR='/work/'+slot+'/tmp',LANG='C.UTF-8',LC_ALL='C.UTF-8',
                DOTNET_EnableDiagnostics='0',DOTNET_DbgEnableMiniDump='0',DOTNET_DbgMiniDumpName='/work/'+slot+'/tmp/dotnet.dmp',
                DOTNET_CLI_TELEMETRY_OPTOUT='1',DOTNET_SKIP_FIRST_TIME_EXPERIENCE='1')
            name='dotj-task132-'+out.name
            argv=docker_argv(name,[(jar,'/product.jar',True),(consumer,'/consumer.jar',True),(jdk,'/jdk',True),
                (a.work_root,'/work',False),(source,'/corpus',True),(script,'/run.sh',True)],env,['/bin/sh','/run.sh',slot,sha(jar)])
            container(run,name,argv)
            run.receipt['work']=str(work)
            run.receipt['outputs']=[descriptor(p) for p in sorted(work.iterdir()) if p.is_file()]
        run.receipt['consumerInputs']=[descriptor(p) for p in (out/'consumer.jar',out/'historical-successor.jar') if p.is_file()]
    except BaseException as caught:error=caught;raise
    finally:run.finish(error)
    print(json.dumps(dict(status='PASS',group=a.group,platform=a.platform,receipt=str(out/'receipt.json'),sha256=sha(out/'receipt.json'))))

if __name__=='__main__':main()
