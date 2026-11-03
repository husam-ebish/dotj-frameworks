import argparse,json,shutil,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from corpus import descriptor,sha
from owned import Run,JDK,MODULE,vm
HERE=Path(__file__).resolve().parent
TYPES=['Result','DuplicateImport','EvaluationFailure','ProfileRejected']
def main():
    p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path,required=True);p.add_argument('--jar',type=Path,required=True);p.add_argument('--attempt',type=Path,required=True);a=p.parse_args()
    run=Run(a.attempt);out=run.out;error=None
    try:
        src=out/'src';src.mkdir();shutil.copyfile(HERE/'LegacyAbiConsumer.java',src/'LegacyAbiConsumer.java')
        run.receipt['inputs']=[descriptor(a.baseline),descriptor(a.jar),descriptor(src/'LegacyAbiConsumer.java')]
        run('compile-legacy',[JDK/'javac.exe',*['-J'+v for v in vm(out)],'--release','21','-implicit:none','-sourcepath',out/'empty','--module-path',a.baseline,
            '--patch-module',MODULE+'='+str(src),'-d',out/'classes',src/'LegacyAbiConsumer.java'])
        for name,jar in [('baseline',a.baseline),('successor',a.jar)]:
            for type in TYPES:
                run(name+'-'+type,[JDK/'javap.exe',*['-J'+v for v in vm(out)],'-classpath',jar,'-p','-s','org.dotj.internal.build.evaluation.ProjectEvaluationComponent$'+type])
            run(name+'-legacy',[JDK/'java.exe',*vm(out),'--limit-modules','java.base,java.xml,'+MODULE,'--module-path',jar,
                '--patch-module',MODULE+'='+str(out/'classes'),'-m',MODULE+'/org.dotj.internal.build.evaluation.LegacyAbiConsumer',jar])
        for type in TYPES:assert (out/('baseline-'+type+'.stdout')).read_bytes()==(out/('successor-'+type+'.stdout')).read_bytes(),type
        run.receipt['outputs']=[descriptor(p) for p in sorted(out.rglob('*')) if p.is_file() and p.suffix in ('.stdout','.stderr','.class')]
    except BaseException as caught:error=caught;raise
    finally:run.finish(error)
    print(json.dumps(dict(status='PASS',receipt=str(out/'receipt.json'),sha256=sha(out/'receipt.json'))))
if __name__=='__main__':main()
