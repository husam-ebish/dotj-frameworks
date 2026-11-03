"""Explicit-source, explicit-artifact owned product build and packaged consumers."""
import argparse
import json
from pathlib import Path
import shutil
import sys
import zipfile
sys.path.insert(0,str(Path(__file__).resolve().parent))
from corpus import descriptor,sha,read_contract,materialize,verify_fixtures
from owned import Run,JDK,MODULE,vm
HERE=Path(__file__).resolve().parent

def consumer(run,jar):
    out=run.out;src=out/'consumer-source';src.mkdir()
    for p in [HERE/'CycleTraceProductTest.java',HERE.parent/'items-evaluation-v1/ItemsJson.java']:
        shutil.copyfile(p,src/p.name);run.receipt['inputs'].append(descriptor(src/p.name))
    run('compile-consumer',[JDK/'javac.exe',*['-J'+v for v in vm(out)],'--release','21','-implicit:none','-sourcepath',out/'empty',
        '--module-path',jar,'--patch-module',MODULE+'='+str(src),'-d',out/'classes',*sorted(src.glob('*.java'))])
    packaged=out/'consumer.jar'
    run('consumer-jar',[JDK/'jar.exe',*['-J'+v for v in vm(out)],'--create','--file',packaged,'--date=2020-01-01T00:00:00Z','-C',out/'classes','.'])
    with zipfile.ZipFile(packaged) as z:
        assert not any(n.rsplit('/',1)[-1].startswith(('ProjectEvaluationComponent','ItemEvaluator','ItemExpressions','ItemGlobs','ItemSnapshot')) for n in z.namelist())
    run.receipt['consumer']=descriptor(packaged)
    return packaged

def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['build','selected','red','private'])
    p.add_argument('--source-root',type=Path);p.add_argument('--jar',type=Path)
    p.add_argument('--contract',type=Path);p.add_argument('--attempt',type=Path,required=True)
    a=p.parse_args();run=Run(a.attempt);out=run.out;error=None
    run.receipt['inputs']=[descriptor(__file__),descriptor(HERE/'owned.py'),descriptor(HERE/'corpus.py')]
    try:
        if a.mode=='build':
            source=a.source_root/'dotj-build/evaluation-candidate/src';frozen=out/'src'
            shutil.copytree(source,frozen)
            run.receipt['sourceRoot']=str(a.source_root.resolve())
            run.receipt['sources']=[dict(relative=p.relative_to(source).as_posix(),origin=descriptor(p),retained=descriptor(frozen/p.relative_to(source))) for p in sorted(source.rglob('*.java'))]
            run('compile-product',[JDK/'javac.exe',*['-J'+v for v in vm(out)],'--release','21','-implicit:none','-classpath',out/'empty','-sourcepath',frozen,'-d',out/'classes',*sorted(frozen.rglob('*.java'))])
            jar=out/'dotj-build-evaluation-candidate.jar'
            run('product-jar',[JDK/'jar.exe',*['-J'+v for v in vm(out)],'--create','--file',jar,'--date=2020-01-01T00:00:00Z','-C',out/'classes','.'])
            run.receipt['outputs']=[descriptor(jar),*[descriptor(p) for p in sorted((out/'classes').rglob('*.class'))]]
        else:
            jar=a.jar.resolve();run.receipt['inputs'] += [descriptor(jar),descriptor(a.contract)]
            contract=read_contract(a.contract);materialize(contract,out/'fixtures')
            run.receipt['fixtureInputs']=[descriptor(p) for p in sorted((out/'fixtures').rglob('*')) if p.is_file()]
            packaged=consumer(run,jar)
            if a.mode=='private':
                for kind in ('inside','outside'):
                    root=out/'controls/links'/kind;root.mkdir(parents=True)
                    target=root/'target' if kind=='inside' else out/'outside-link-target';target.mkdir()
                    (target/'one.props').write_text('<Project/>')
                    quote=lambda p:"'"+str(p).replace("'","''")+"'"
                    command="$ErrorActionPreference='Stop'; New-Item -ItemType Junction -Path "+quote(root/'alias')+' -Target '+quote(target)+' | Select-Object FullName,LinkType,Target | ConvertTo-Json'
                    run('junction-'+kind,['C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe','-NoProfile','-NonInteractive','-Command',command],15)
                tail=['private',out/'controls',out/'fixtures','windows']
            else:tail=['selected',out/'fixtures']
            run('consumer',[JDK/'java.exe',*vm(out),'--limit-modules','java.base,java.xml,'+MODULE,'--module-path',jar,
                '--patch-module',MODULE+'='+str(packaged),'-m',MODULE+'/org.dotj.internal.build.evaluation.CycleTraceProductTest',*tail,jar,sha(jar)],120,a.mode!='red')
            op=run.receipt['operations'][-1]
            if a.mode=='red':
                assert op['process']['exitCode']!=0 and 'FEATURE_RED: required trace-aware sidecar absent' in (out/'consumer.stderr').read_text()
                run.receipt['expectedFeatureRed']=True
            else:
                raw=json.loads((out/'consumer.stdout').read_text());assert raw['status']=='PASS'
                (out/'parsed.json').write_text(json.dumps(raw,indent=2)+'\n',encoding='utf-8')
                run.receipt['outputs'].append(descriptor(out/'parsed.json'))
            verify_fixtures(contract,out/'fixtures',[c['id'] for c in contract['cases']])
            run.receipt['outputs'] += [descriptor(packaged),descriptor(out/'consumer.stdout'),descriptor(out/'consumer.stderr')]
    except BaseException as caught:error=caught;raise
    finally:run.finish(error)
    print(json.dumps(dict(status='PASS',mode=a.mode,receipt=str(out/'receipt.json'),sha256=sha(out/'receipt.json'))))

if __name__=='__main__':main()
