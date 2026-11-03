import argparse,json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from corpus import descriptor,sha,read_contract,materialize,verify_fixtures
from owned import B,Run,container,docker_argv
from history import no_product
HERE=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['selected','private'],required=True)
    for field in ('jar','consumer','contract','attempt','work-root'):p.add_argument('--'+field,type=Path,required=True)
    a=p.parse_args();run=Run(a.attempt,True);out=run.out;slot=out.name;error=None
    assert re.fullmatch('[a-z0-9-]+',slot) and a.work_root.is_dir() and not (a.work_root/slot).exists()
    try:
        contract=read_contract(a.contract);materialize(contract,out/'fixtures');no_product(a.consumer)
        jdk=B/'toolchains/jdk-linux21/jdk-21.0.12.1+1';script=HERE/'product-linux.sh'
        run.receipt['inputs']=[descriptor(p) for p in (Path(__file__),HERE/'owned.py',HERE/'corpus.py',a.jar,a.consumer,a.contract,script,jdk/'bin/java')]
        run.receipt['jar']=descriptor(a.jar);run.receipt['consumer']=descriptor(a.consumer)
        env=dict(HOME='/work/'+slot+'/home',TMPDIR='/work/'+slot+'/tmp',LANG='C.UTF-8',LC_ALL='C.UTF-8')
        name='dotj-task132-'+out.name
        args=docker_argv(name,[(a.jar,'/product.jar',True),(a.consumer,'/consumer.jar',True),(jdk,'/jdk',True),
            (a.work_root,'/work',False),(out/'fixtures','/corpus',True),(script,'/run.sh',True)],env,['/bin/sh','/run.sh',slot,a.mode,sha(a.jar)])
        container(run,name,args);work=a.work_root/slot
        verify_fixtures(contract,out/'fixtures',[c['id'] for c in contract['cases']]);verify_fixtures(contract,work/'fixtures',[c['id'] for c in contract['cases']])
        assert (work/'case-profile.tsv').read_text().splitlines()==[c['id']+'\tfalse\tfalse' for c in contract['cases']]
        raw=json.loads((work/'consumer.stdout').read_text());assert raw['status']=='PASS'
        run.receipt['work']=str(work);run.receipt['fixtureRoot']='/work/'+slot+'/fixtures'
        run.receipt['outputs']=[descriptor(p) for p in sorted(work.iterdir()) if p.is_file()]
    except BaseException as caught:error=caught;raise
    finally:run.finish(error)
    print(json.dumps(dict(status='PASS',mode=a.mode,receipt=str(out/'receipt.json'),sha256=sha(out/'receipt.json'))))
if __name__=='__main__':main()
