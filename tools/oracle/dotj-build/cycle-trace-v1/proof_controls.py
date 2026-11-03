"""Execute CC12 corruption controls and CC13 physical relocation against the actual pure reader."""
import argparse,copy,hashlib,io,json,os,shutil,sys,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from corpus import descriptor,sha
from owned import B,Run
PYTHON=B/'toolchains/python-3.13.9/python.exe'
def main():
    p=argparse.ArgumentParser()
    for field in ('proof','jar','source-root','attempt'):p.add_argument('--'+field,type=Path,required=True)
    a=p.parse_args();run=Run(a.attempt);out=run.out;error=None;original=json.loads(a.proof.read_text());results=[]
    run.receipt['inputs']=[descriptor(__file__),descriptor(a.proof),descriptor(a.jar)]
    def execute(label,root,proof,jar,source,expected=None):
        path=root/'proof.json';path.write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
        argv=[PYTHON,'-B',root/'reader/read_proof.py','--proof',path,'--sha256',sha(path),'--jar',jar,'--source-root',source]
        run(label,argv,120,False);op=run.receipt['operations'][-1]
        code=op['process']['exitCode'];stderr=(out/(label+'.stderr')).read_text()
        if expected is None:assert code==0,(label,stderr)
        else:assert code!=0 and expected in stderr,(label,code,stderr)
        results.append(dict(id=label,expected='PASS' if expected is None else 'REJECT',exitCode=code,reason=expected,argv=list(map(str,argv)),stdout=op['stdout'],stderr=op['stderr']))
    def variant(name):
        root=out/name;root.mkdir();(root/'objects').mkdir();shutil.copytree(a.proof.parent/'reader',root/'reader')
        for source in (a.proof.parent/'objects').iterdir():os.link(source,root/'objects'/source.name)
        return root,copy.deepcopy(original)
    def blob(root,proof,d,raw):
        digest=hashlib.sha256(raw).hexdigest();(root/'objects'/digest).write_bytes(raw)
        proof['objects'][digest]=dict(relative='objects/'+digest,bytes=len(raw))
        return dict(path=d['path'],sha256=digest,bytes=len(raw))
    def obj(root,proof,d,value):return blob(root,proof,d,(json.dumps(value,indent=2)+'\n').encode())
    def read(d):return json.loads((a.proof.parent/'objects'/d['sha256']).read_text())
    def mutate_execution(root,proof,name,change):
        entry=next(e for e in proof['executions'] if e['name']==name);receipt=read(entry['receipt']);change(receipt)
        entry['receipt']=obj(root,proof,entry['receipt'],receipt)
    def mutate_selected(root,proof,change,origin=False):
        entry=next(e for e in proof['selected'] if e['platform']=='windows');old=copy.deepcopy(entry['origin' if origin else 'raw'])
        if origin:new=blob(root,proof,old,b'PRODUCT_ORIGIN\t/wrong.jar\twrong\n')
        else:
            value=read(old);change(value);new=obj(root,proof,old,value)
        entry['origin' if origin else 'raw']=new
        def replacement(receipt):
            for field in ('outputs',):
                for i,d in enumerate(receipt[field]):
                    if d['sha256']==old['sha256']:receipt[field][i]=dict(new,path=d['path'])
                    elif not origin and d['path'].endswith('parsed.json'):receipt[field][i]=dict(new,path=d['path'])
            for operation in receipt['operations']:
                stream='stderr' if origin else 'stdout'
                if operation[stream]['sha256']==old['sha256']:operation[stream]=dict(new,path=operation[stream]['path'])
        mutate_execution(root,proof,entry['receiptName'],replacement)
    try:
        root,proof=variant('baseline');execute('baseline-reader',root,proof,a.jar,a.source_root)
        for name,jar in [('missing-jar',out/'absent.jar'),('wrong-jar',Path(original['abi']['baselineJar']['path']))]:
            root,proof=variant(name);execute(name,root,proof,jar,a.source_root,'Qualified explicit JAR required')
        root,proof=variant('stale-source');source=root/'source';shutil.copytree(a.source_root/'dotj-build/evaluation-candidate/src',source/'dotj-build/evaluation-candidate/src')
        target=source/'dotj-build/evaluation-candidate/src/org/dotj/internal/build/evaluation/ProjectEvaluationComponent.java'
        with target.open('ab') as f:f.write(b'\n// intentional stale-source negative\n')
        execute('stale-source',root,proof,a.jar,source,'Current source bytes')
        root,proof=variant('embedded-product');d=proof['consumers'][0];buffer=io.BytesIO((a.proof.parent/'objects'/d['sha256']).read_bytes())
        with zipfile.ZipFile(buffer,'a') as z,zipfile.ZipFile(a.jar) as product:
            name='org/dotj/internal/build/evaluation/ProjectEvaluationComponent.class';z.writestr(name,product.read(name))
        proof['consumers'][0]=blob(root,proof,d,buffer.getvalue());execute('embedded-product',root,proof,a.jar,a.source_root,'Consumer embeds product class')
        root,proof=variant('wrong-argv')
        def wrongargv(r):r['operations'][-1]['process']['argv'][-1]='wrong-final-hash'
        mutate_execution(root,proof,'selected-windows-final-v1',wrongargv)
        execute('wrong-argv',root,proof,a.jar,a.source_root,'Actual argv/exit differs')
        root,proof=variant('wrong-origin');mutate_selected(root,proof,None,True);execute('wrong-origin',root,proof,a.jar,a.source_root,'Selected actual loaded origin')
        def trace(value):return next(r for r in value['rows'] if r['id']=='CT04-long-nonroot' and r['profile']=='DEFAULT')['observation']['traces'][0]
        mutations={
            'reordered-edge':lambda v:trace(v)['edges'].reverse(),
            'omitted-edge':lambda v:trace(v)['edges'].pop(),
            'bad-cycle-index':lambda v:trace(v).__setitem__('cycleStartIndex',0),
            'colluding-native-projection':lambda v:next(r for r in v['rows'] if r['id']=='CT04-long-nonroot' and r['profile']=='DEFAULT')['observation']['evaluation']['properties'].__setitem__('P','forged')}
        for name,change in mutations.items():
            root,proof=variant(name);mutate_selected(root,proof,change);execute(name,root,proof,a.jar,a.source_root,'Selected native projection' if name=='colluding-native-projection' else 'Selected trace')
        root,proof=variant('changed-raw');entry=proof['selected'][0];value=read(entry['raw']);value['rows']=[];entry['raw']=obj(root,proof,entry['raw'],value)
        execute('changed-raw',root,proof,a.jar,a.source_root,'Selected execution binding')
        root,proof=variant('forged-cleanup');mutate_execution(root,proof,'selected-linux-final-v1',lambda r:r['container'].__setitem__('absenceVerified',False))
        execute('forged-cleanup',root,proof,a.jar,a.source_root,'Container absence')
        root,proof=variant('omitted-obligation');proof['executions']=[e for e in proof['executions'] if e['name']!='inherited-items-linux-v1']
        execute('omitted-obligation',root,proof,a.jar,a.source_root,'Complete executed obligation inventory')
        root,proof=variant('forged-child-status');lock=read(proof['nativeLock']);unit=next(u for u in lock['units'] if u['aggregateStatus']=='FAILED')
        receipt=read(unit['receipt']);receipt['status']='PASS';unit['receipt']=obj(root,proof,unit['receipt'],receipt);proof['nativeLock']=obj(root,proof,proof['nativeLock'],lock)
        execute('forged-child-status',root,proof,a.jar,a.source_root,'Completed native child raw/parsed/status')
        # Physical copies, not links: complete executed reader closure, evidence objects, source and JAR.
        relocated=out/'physical-relocation';shutil.copytree(a.proof.parent,relocated)
        shutil.copytree(a.source_root/'dotj-build/evaluation-candidate/src',relocated/'source/dotj-build/evaluation-candidate/src')
        shutil.copyfile(a.jar,relocated/'product.jar');proof=copy.deepcopy(original)
        execute('physical-relocation',relocated,proof,relocated/'product.jar',relocated/'source')
        selected=proof['selected'][0]['raw'];missing=relocated/'objects'/selected['sha256'];withheld=relocated/'withheld-object';missing.rename(withheld)
        execute('relocation-no-original-fallback',relocated,proof,relocated/'product.jar',relocated/'source','FileNotFoundError')
        withheld.rename(missing)
        result=dict(status='PASS',groups=['CC12-proof-binding','CC13-relocation'],controls=results,
                    physicalRelocation=dict(path=str(relocated),readerDependencies=proof['readerFiles'],objectCount=len(proof['objects']),noOriginalFallback=True))
        path=out/'controls.json';path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');run.receipt['outputs']=[descriptor(path)]
    except BaseException as caught:error=caught;raise
    finally:run.finish(error)
    print(json.dumps(dict(status='PASS',negativeControls=sum(r['expected']=='REJECT' for r in results),receipt=str(out/'receipt.json'),sha256=sha(out/'receipt.json'))))
if __name__=='__main__':main()
