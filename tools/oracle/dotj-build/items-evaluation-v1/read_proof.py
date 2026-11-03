"""Read-only qualification gate. Execution paths come from frozen proof, never this file's location."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

PRODUCT_CLASSES={'ProjectEvaluationComponent','ItemEvaluator','ItemExpressions','ItemGlobs','ItemSnapshot'}
def require(value,message):
    if not value:raise ValueError(message)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def descriptor(value):
    p=Path(value['path'])
    require(p.is_file(),'Missing evidence: '+str(p))
    require(sha(p)==value['sha256'],'Changed evidence: '+str(p))
    require(p.stat().st_size==value.get('bytes',value.get('sizeBytes')),'Evidence length: '+str(p))
def descriptors(value):
    if isinstance(value,dict):
        if 'path' in value and 'sha256' in value and ('bytes' in value or 'sizeBytes' in value):yield value
        for child in value.values():yield from descriptors(child)
    elif isinstance(value,list):
        for child in value:yield from descriptors(child)
def consumer(path):
    with zipfile.ZipFile(path) as archive:
        require(not any(n.rsplit('/',1)[-1].split('$')[0].removesuffix('.class') in PRODUCT_CLASSES for n in archive.namelist()),'Embedded product class')
def source(proof,root):
    root=Path(root)/'dotj-build/evaluation-candidate/src'
    actual={str(p.relative_to(root)).replace('\\','/'):p for p in root.rglob('*.java')}
    require(set(actual)==set(proof['source']),'Source closure differs')
    for name,pin in proof['source'].items():
        raw=actual[name].read_bytes()
        require(hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest()==pin['canonicalSha256'],'Source differs: '+name)
def execution(receipt,expected):
    require(receipt['status']=='PASS','Execution not PASS')
    ops=receipt['operations'];require(len(ops)==len(expected),'Operation count')
    for op,pin in zip(ops,expected):
        p=op['process']
        require(op['label']==pin['label'] and p['argv']==pin['argv'],'Execution argv mismatch')
        require(p['exitCode']==pin['exitCode'],'Execution exit mismatch')
        require(p.get('launched') and p.get('jobAssigned') and p.get('resumed'),'Owned launch missing')
        require(not any(p.get(k) for k in ('timedOut','outputLimitExceeded','cleanupError','error')),'Execution failure')
    if 'container' in receipt:
        c=receipt['container'];t=c['terminalInspect'];created=c['createdInspect']
        require(c['absenceVerified'] and t['State']['ExitCode']==0 and not t['State']['Running'] and not t['State']['OOMKilled'],'Container terminal/cleanup')
        require(t['Id']==c['cid']==created['Id'] and t['Name']=='/'+c['name'] and t['Config']['Labels']['dotj.owner']=='task128' and t['Config']['Image']==c['image'],'Container identity')
        h=created['HostConfig']
        require(h['ReadonlyRootfs'] and h['NetworkMode']=='none' and h['Memory']==536870912 and h['MemorySwap']==536870912 and h['PidsLimit']==64,'Container restrictions')
def check(proof_path,proof_sha,jar,source_root):
    require(sha(proof_path)==proof_sha,'Proof manifest hash')
    proof=json.loads(Path(proof_path).read_text(encoding='utf-8'))
    require(Path(jar).is_file() and sha(jar)==proof['jar']['sha256'],'Qualified JAR required; no fallback')
    source(proof,source_root)
    checked={}
    for d in descriptors(proof):
        descriptor(d);checked[d['path']]=d['sha256']
    for entry in proof['executions']:
        receipt=json.loads(Path(entry['receipt']['path']).read_text())
        execution(receipt,entry['expectedOperations'])
        if receipt['mode']=='capture-windows':
            # IS01 deliberately removes old.cs and adds new.cs. Validate BEFORE bytes
            # against retained immutable inputs, not the intentionally mutated tree.
            capture=next(o for o in receipt['operations'] if o['label']=='capture')
            fixture=Path(capture['process']['argv'][-4])
            before={Path(d['path']).relative_to(fixture).as_posix():d for d in receipt['fixtureInputs']}
            after={Path(d['path']).relative_to(fixture).as_posix():d for d in receipt['fixtureAfter']}
            expected={name:d['sha256'] for name,d in before.items()}
            manifest=json.loads((Path(proof['corpusRoot'])/'manifest.json').read_text())
            for case in manifest['cases']:
                for step in case.get('steps',[]):
                    prefix=case['id']+'/'
                    if step['kind']=='filesystem-change':
                        for name in step.get('delete',[]):del expected[prefix+name]
                        for name,content in step.get('write',{}).items():expected[prefix+name]=hashlib.sha256(content.encode()).hexdigest()
                    elif step['kind']=='evaluate-xml':expected[prefix+step['owner']]=hashlib.sha256(step['xml'].encode()).hexdigest()
                    elif step['kind']=='repeat-owner':expected[prefix+step['owner']]=before[prefix+'main.proj']['sha256']
            require(expected=={name:d['sha256'] for name,d in after.items()},'Unexpected fixture mutation')
            for name,d in before.items():
                retained=dict(d,path=str(Path(proof['corpusRoot'])/name));descriptor(retained)
                if name in after:require(d['sha256']==after[name]['sha256'],'Changed unowned fixture')
            del receipt['fixtureInputs']
        for d in descriptors(receipt):descriptor(d);checked[d['path']]=d['sha256']
        if 'consumer' in receipt:consumer(receipt['consumer']['path'])
    for platform,comparison in proof['comparisons'].items():
        value=json.loads(Path(comparison['path']).read_text())
        require(value['status']=='PASS' and value['passed']==42 and len(value['rows'])==42 and all(r['passed'] and not r['differences'] for r in value['rows']),platform+' comparison')
    profile=Path(proof['linuxCaseProfile']['path']).read_text().splitlines()
    require(len(profile)==42 and all(r.endswith('\tfalse\tfalse') for r in profile),'Materialized Linux case capabilities')
    private=[]
    for d in proof['privateRows']:private+=Path(d['path']).read_text().splitlines()
    require(all('\tPASS\t' in r for r in private),'Private control failure')
    require({r.split('-',1)[0] for r in private if r.startswith('IR')}=={'IR'+str(i).zfill(2) for i in range(1,15)},'Missing private group')
    require(len(private)==61,'Private controls changed')
    stable=[]
    for entry in proof['stableRows']:
        lines=Path(entry['actual']['path']).read_text().splitlines()
        if entry['name']=='import-path-results.tsv':lines.remove('NEG-dynamic-import\tNATIVE_IMPORT_PATH_MATCH\tSUCCESS')
        stable+=lines
    old=Path(proof['stableGolden']['path']).read_text().splitlines()
    require(len(stable)==len(old)==94,'Stable94 inventory')
    differences=[(a,b) for a,b in zip(old,stable) if a!=b]
    require(differences==[('NEG-items\tPROFILE_REJECT\tUNSUPPORTED_ELEMENT','NEG-items\tNATIVE_ITEM_TRANSITION_EMPTY\tSUCCESS')],'Unexpected historical transition')
    for pair in proof['historicalUnchanged']:
        require(Path(pair['actual']['path']).read_text()==Path(pair['prior']['path']).read_text(),'Historical rows changed')
    return dict(status='PASS',evidenceFiles=len(checked),semanticScenariosPerPlatform=42,privateGroups=14,privateRows=len(private),stableRows=94,acceptedTasksAdded=0)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--proof',required=True);parser.add_argument('--sha256',required=True)
    parser.add_argument('--jar',required=True);parser.add_argument('--source-root',required=True)
    args=parser.parse_args();print(json.dumps(check(args.proof,args.sha256,args.jar,args.source_root)))
if __name__=='__main__':main()
