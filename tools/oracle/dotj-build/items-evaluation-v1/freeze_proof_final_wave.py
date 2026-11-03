"""Freeze actual completed execution identities after qualification, without replaying producers."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from product import A,B,W,descriptor

def main():
    target=A/sys.argv[1]
    if target.parent!=A:raise ValueError('Immediate proof path required')
    if target.exists():raise ValueError('Proof already frozen')
    names=['product-build-v5','product-windows-v3','product-linux-v3','private-windows-v3','private-linux-v3',
        'junction-windows-v3','supplement-product-windows-v3','history-windows-v5','sort-windows-v2','sort-linux-v3','boundary-windows-v1','boundary-linux-v2']
    proof=dict(schemaVersion=1,scope='One selected bounded private candidate; no public API or task acceptance',
        jar=descriptor(A/'product-build-v5/dotj-build-evaluation-candidate.jar'),source={},executions=[],corpusRoot=str(A/'corpus-input-v1'),
        nativeContract=descriptor(A/'native-contract-v1.json'),rootPreimplementationGate=descriptor(B/'orchestration/two-frameworks/task128-root-java-gate-v1.json'),
        sourcePolicy='Exact source closure and LF-canonical bytes; only CRLF/LF difference admitted for Git checkout relocation')
    for p in sorted((A/'product-build-v5/src').rglob('*.java')):
        proof['source'][p.relative_to(A/'product-build-v5/src').as_posix()]=dict(retained=descriptor(p),canonicalSha256=hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest())
    for name in names:
        p=A/name/'receipt.json';r=json.loads(p.read_text());assert r['status']=='PASS'
        proof['executions'].append(dict(name=name,receipt=descriptor(p),expectedOperations=[dict(label=o['label'],argv=o['process']['argv'],exitCode=o['process']['exitCode']) for o in r['operations']]))
    proof['comparisons']={'windows':descriptor(A/'product-windows-v3/comparison.json'),'linux':descriptor(A/'product-linux-v3/comparison.json')}
    proof['linuxCaseProfile']=descriptor(A/'product-linux-v3/retained-output/materialized-case-profile.tsv')
    proof['privateRows']=[descriptor(A/p) for p in ('private-windows-v3/controls/results.tsv','private-linux-v3/retained-output/results.tsv','junction-windows-v3/junction.stdout')]
    prior=B/'agents/batch2518-build-ordering-preparation-v1'
    history=A/'history-windows-v5';old=prior/'task106-historical-finaljar-attempt02'
    stable=['case-results.tsv','location-results.tsv','cycle-results.tsv','profile-results.tsv','import-path-results.tsv','whitespace-results.tsv']
    proof['stableRows']=[dict(name=name,actual=descriptor(history/'outputs'/name),prior=descriptor(old/'outputs'/name)) for name in stable]
    proof['stableGolden']=descriptor(prior/'root-task108-historical-finaljar-attempt02/typed94-v2.tsv')
    proof['historicalUnchanged']=[dict(actual=descriptor(history/name),prior=descriptor(old/name)) for name in
        ('and-results.tsv','cache-controls.tsv','cache-results.tsv','condition-results.tsv','predicate-controls.tsv','predicate-results.tsv')]
    proof['historicalUnchanged'] += [dict(actual=descriptor(history/name),prior=descriptor(prior/'task106-product-dev-attempt02'/name)) for name in ('ordering-results.tsv','boolean-results.tsv')]
    proof['supplementalInputs']=descriptor(A/'supplemental-input-v1/manifest.json')
    proof['reader']=descriptor(Path(__file__).with_name('read_proof_final_wave.py'))
    proof['readerBase']=descriptor(Path(__file__).with_name('read_proof.py'))
    proof['rawSortRegression']={'windows':descriptor(A/'sort-windows-v2/raw-sort.stdout'),'linux':descriptor(A/'sort-linux-v3/retained-output/raw-sort.stdout')}
    proof['rawSortLinuxCaseProfile']=descriptor(A/'sort-linux-v3/retained-output/case-profile.tsv')
    proof['retainedRed']=descriptor(B/'orchestration/two-frameworks/task129-focused-v3/focused-jvm-receipt.json')
    proof['readerPrevious']=descriptor(Path(__file__).with_name('read_proof_fix1.py'))
    proof['finalWaveRegression']={'windows':descriptor(A/'boundary-windows-v1/boundaries.stdout'),'linux':descriptor(A/'boundary-linux-v2/retained-output/boundaries.stdout')}
    proof['finalWaveLinuxCaseProfile']=descriptor(A/'boundary-linux-v2/retained-output/case-profile.tsv')
    proof['finalWaveRetainedRed']=descriptor(B/'orchestration/two-frameworks/task130-focused-v1/focused-jvm-receipt.json')
    target.write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(descriptor(target)))
if __name__=='__main__':main()
