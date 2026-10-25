"""Pin generic count/write span pointer-adapter dispatch and exceptional copy-back."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return 'null' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'generic-span-dispatch-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-generic-span-dispatch-contract.ps1').read_bytes()).hexdigest();assert len(j['rows'])==3200;lines=[];groups=writes=0
 for q in j['rows']:
  r=q['result'];groups+=2+int(q['write']);writes+=int(q['write']);lines.append('\t'.join([q['direction'],str(q['multiplier']),str(q['countMode']),str(q['writeMode']),str(q['count']),str(q['capacity']),str(q['offset']),str(int(q['flush'])),str(int(q['write'])),str(int(r['ok'])),str(r.get('value',0)),r.get('exception',''),str(r.get('hResult',0)),r.get('paramName') or 'null',csv(q['destination']),';'.join(csv(v) for v in q['trace'])]))
 assert writes==2880
 assert all(q['trace'][0][0]==2 and q['trace'][0][4]==0 for q in j['rows'] if q['direction']=='decoder' and not q['write'])
 assert all(all(v==99 for v in q['destination']) for q in j['rows'] if q['write'] and not q['result']['ok'])
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/generic-span-dispatch');work.mkdir(parents=True,exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');source=work/'GenericSpanDispatchProbe.java';source.write_bytes(Path(__file__).with_name('generic-span-dispatch-probe.java').read_bytes());shared=work/'StatefulConvertSpansProbe.java';shared.write_bytes(Path(__file__).with_name('stateful-convert-spans-probe.java').read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(shared),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'GenericSpanDispatchProbe',str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeCases=3200,countCases=320,writeCases=2880,decoderGenericCountIgnoresFlush=True,temporaryOutputClampingAndExceptionIsolation=True,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_GENERIC_COUNT_WRITE_HEAP_SPAN_ADAPTERS_ONLY; DIRECT_POINTER_OVERRIDES_REF_STRUCT_LIFETIMES_REENTRANCY_FULL_METADATA_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'generic-span-dispatch-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS generic count/write span dispatch: {groups} groups; 3200 native cases')
if __name__=='__main__':main()
