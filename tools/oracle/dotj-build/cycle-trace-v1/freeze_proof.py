"""Freeze a self-contained content-addressed proof from completed executions; never launches."""
import argparse,hashlib,json,shutil,sys,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from corpus import descriptor,sha
from read_proof import descriptors
HERE=Path(__file__).resolve().parent
B=Path('D:/AI/Implementation/dotj Frameworks')
READERS=['read_proof.py','compare.py','corpus.py','native_lock.py','inherited_models.py']
def main():
    p=argparse.ArgumentParser();p.add_argument('--artifacts',type=Path,required=True);p.add_argument('--source-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    A=a.artifacts;W=a.source_root;out=a.output;assert not out.exists();out.mkdir(parents=True);(out/'objects').mkdir();(out/'reader').mkdir()
    jar=A/'product-build-v1/dotj-build-evaluation-candidate.jar';prior=B/'agents/batch2521-build-items-evaluation-v1'
    proof=dict(schemaVersion=1,status='FROZEN_SUCCESSOR_PROOF',scope='One bounded private trace feature; no task/framework acceptance',jar=descriptor(jar),source={},classes={},executions=[],consumers=[],objects={},readerFiles={})
    proof['producer']=descriptor(__file__)
    proof['nativeFixtureAfter']={}
    additional=[]
    def document(path):
        path=Path(path);d=descriptor(path);value=json.loads(path.read_text(encoding='utf-8-sig'));additional.extend(descriptors(value));return d,value
    for path in sorted((A/'product-build-v1/src').rglob('*.java')):
        proof['source'][path.relative_to(A/'product-build-v1/src').as_posix()]=dict(retained=descriptor(path),canonicalSha256=hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest())
    with zipfile.ZipFile(jar) as z:proof['classes']={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.endswith('.class')}
    proof['contractOriginal'],_=document(W/'dotj-build/evaluation-candidate/cycle-trace-v1/contract.json')
    proof['contract'],_=document(W/'dotj-build/evaluation-candidate/cycle-trace-v1/contract-v2.json')
    proof['amendment'],_=document(A/'contract-amendment-v1.json')
    proof['nativeLock'],lock=document(A/'native-lock-v1.json')
    proof['nativeRecipes']=[document(A/name)[0] for name in ('native-recipe-v1.json','native-case-recipe-v1.json')]
    proof['gates']=[document(B/'orchestration/two-frameworks'/name)[0] for name in ('task132-root-java-gate-v1.json','task132-contract-v2-root-audit-v1.json')]
    proof['legacyProof']=descriptor(prior/'qualification-proof-final-wave-v1.json');proof['legacyResult']=descriptor(A/'baseline-proof.stdout')
    proof['baselineRed'],red=document(A/'product-baseline-red-v1/receipt.json')
    proof['failures']=[document(A/name/'receipt.json')[0] for name in ('native-linux-default-1-v1','native-retry-v1/native-linux-default-1-v1','private-windows-v1','selected-linux-v1')]
    proof['failedComparison']=descriptor(A/'selected-windows-v1/comparison-failed-v1.txt')
    for unit in lock['units']:
        _,unit_receipt=document(unit['receipt']['path']);document(unit['stdout']['path'])
        if unit['role']=='new-capture':
            root=Path(unit_receipt.get('actualFixturePath',unit_receipt['fixtureRoot']))
            proof['nativeFixtureAfter'][unit['id']]=[dict(relative=p.relative_to(root).as_posix(),file=descriptor(p)) for p in sorted(root.rglob('*')) if p.is_file()]
    native_names=['native-compile-v1']+[r['attempt'] for r in json.loads((W/'dotj-build/evaluation-candidate/cycle-trace-v1/contract.json').read_text())['nativeSchedule']['runs'] if r['platform']=='windows']
    execution_paths=[A/n/'receipt.json' for n in native_names]
    execution_paths += [Path(v)/'receipt.json' for v in lock['replacements'].values()]
    names=['product-build-v1','selected-windows-final-v1','private-windows-final-v1','selected-linux-final-v1','private-linux-final-v1','abi-v1']
    names += ['inherited-'+g+'-windows-v1' for g in ('items','private','junction','supplement','sort','boundary','history')]
    names += ['inherited-'+g+'-linux-v1' for g in ('items','private','sort','boundary')]
    execution_paths += [A/n/'receipt.json' for n in names]
    receipts={}
    for path in execution_paths:
        d,r=document(path);assert r['status']=='PASS';name=path.parent.name;receipts[name]=r
        proof['executions'].append(dict(name=name,receipt=d,expectedOperations=[dict(label=o['label'],argv=o['process']['argv'],exitCode=o['process']['exitCode']) for o in r['operations']]))
        if 'consumer' in r:proof['consumers'].append(r['consumer'])
        proof['consumers']+=r.get('consumerInputs',[])
        # Pin every retained class/fixture/bridge passed directly to a runtime outside this feature's artifact root.
        for op in r['operations']:
            argv=op['process']['argv']
            if Path(argv[0]).name.lower()!='java.exe':continue
            additional.append(descriptor(argv[0]))
            candidates=[]
            for value in argv:
                if value.startswith('org.dotj.build.evaluation.candidate='):candidates+=value.split('=',1)[1].split(';')
                else:candidates.append(value)
            for value in candidates:
                try:target=Path(value)
                except ValueError:continue
                if not target.is_absolute() or target.is_relative_to(A):continue
                if target.is_file():additional.append(descriptor(target))
                elif target.is_dir():additional.extend(descriptor(f) for f in sorted(target.rglob('*')) if f.is_file())
    proof['historyGroups']=[o['label'] for o in receipts['inherited-history-windows-v1']['operations']]
    proof['selected']=[];proof['private']=[]
    for platform in ('windows','linux'):
        for mode in ('selected','private'):
            name=f'{mode}-{platform}-final-v1';work=A/name if platform=='windows' else A/'linux-case-root-v1'/name
            entry=dict(platform=platform,receiptName=name,raw=descriptor(work/'consumer.stdout'),origin=descriptor(work/'consumer.stderr'))
            if mode=='selected':entry['fixtureRoot']=str(work/'fixtures') if platform=='windows' else '/work/'+name+'/fixtures'
            proof[mode].append(entry)
    proof['abi']=dict(pairs=[dict(baseline=descriptor(A/'abi-v1'/('baseline-'+t+'.stdout')),successor=descriptor(A/'abi-v1'/('successor-'+t+'.stdout'))) for t in ('Result','DuplicateImport','EvaluationFailure','ProfileRejected')],consumer=descriptor(A/'abi-v1/successor-legacy.stdout'))
    proof['abi']['baselineJar']=descriptor(prior/'product-build-v5/dotj-build-evaluation-candidate.jar')
    linux=A/'linux-case-root-v1';history=A/'inherited-history-windows-v1'
    oldproof=json.loads((prior/'qualification-proof-final-wave-v1.json').read_text())
    inherited=dict(nativeContract=descriptor(prior/'native-contract-v1.json'),items=[],privateRows=[descriptor(A/'inherited-private-windows-v1/controls/results.tsv'),descriptor(linux/'product-v13202/results.tsv'),descriptor(A/'inherited-junction-windows-v1/junction.stdout')],
        supplement=descriptor(A/'inherited-supplement-windows-v1/supplement.stdout'),sort=[],boundary=[],
        sortCase=descriptor(linux/'product-v13203/case-profile.tsv'),boundaryCase=descriptor(linux/'product-v13204/case-profile.tsv'),itemsCase=descriptor(linux/'product-v13201/materialized-case-profile.tsv'),
        stable=[],stableGolden=oldproof['stableGolden'],unchanged=[],ordering=descriptor(history/'runtime-ordering.stdout'),boolean=descriptor(history/'runtime-boolean.stdout'))
    for platform in ('windows','linux'):
        item=A/'inherited-items-windows-v1' if platform=='windows' else linux/'product-v13201'
        sort=A/'inherited-sort-windows-v1' if platform=='windows' else linux/'product-v13203'
        boundary=A/'inherited-boundary-windows-v1' if platform=='windows' else linux/'product-v13204'
        inherited['items'].append(dict(platform=platform,raw=descriptor(item/'capture.stdout')))
        inherited['sort'].append(dict(platform=platform,raw=descriptor(sort/'raw-sort.stdout')))
        inherited['boundary'].append(dict(platform=platform,raw=descriptor(boundary/'boundaries.stdout')))
    for entry in oldproof['stableRows']:inherited['stable'].append(dict(name=entry['name'],actual=descriptor(history/'outputs'/entry['name']),prior=entry['prior']))
    for entry in oldproof['historicalUnchanged']:inherited['unchanged'].append(dict(actual=descriptor(history/Path(entry['actual']['path']).name),prior=entry['prior']))
    proof['inherited']=inherited
    # Exact reader closure, copied physically for CC13; no import of an original-path reader.
    for name in READERS:
        shutil.copyfile(HERE/name,out/'reader'/name);proof['readerFiles'][name]=sha(HERE/name)
    all_descriptors=list(descriptors(proof))+additional
    candidates={}
    for d in all_descriptors:candidates.setdefault(d['sha256'],[]).append(d)
    # Preserved executed-source snapshots resolve historical versions whose W path later changed.
    for directory in (A/'executed-native-v1',A/'native-case-v1/executed-dependencies',A/'native-retry-v1/executed-dependencies'):
        for path in directory.iterdir():
            if path.is_file():d=descriptor(path);candidates.setdefault(d['sha256'],[]).append(d)
    for item in json.loads((W/'dotj-build/evaluation-candidate/cycle-trace-v1/contract.json').read_text())['baselineSources']:
        for path in (Path('C:/source/repos/dotj Frameworks')/item['relative'],prior/'product-build-v5/src'/Path(item['relative']).relative_to('dotj-build/evaluation-candidate/src')):
            if path.is_file():d=descriptor(path);candidates.setdefault(d['sha256'],[]).append(d)
    for digest,values in candidates.items():
        matching=[]
        for d in values:
            path=Path(d['path'])
            if path.is_file() and path.stat().st_size==d['bytes'] and sha(path)==digest:matching.append(path)
        assert matching, 'No retained matching bytes for '+str(values)
        target=out/'objects'/digest;shutil.copyfile(matching[0],target)
        proof['objects'][digest]=dict(relative='objects/'+digest,bytes=target.stat().st_size)
    proof['dependencyDescriptors']=all_descriptors
    target=out/'proof.json';target.write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(objects=len(proof['objects']),**descriptor(target))))
if __name__=='__main__':main()
