"""Pin generic Encoder/Decoder Convert halving, virtual calls, aliases and failure outputs."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'generic-convert-arrays-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-generic-convert-arrays-contract.ps1').read_bytes()).hexdigest();assert len(j['rows'])==11520;lines=[]
 for row in j['rows']:
  q=row;r=q['result'];lines.append('\t'.join([q['direction'],str(q['multiplier']),str(q['count']),str(q['capacity']),str(int(q['flush'])),str(q['offset']),str(int(q['alias'])),str(int(q['prefill'])),str(q['countMode']),str(q['writeMode']),str(int(r['ok'])),r.get('exception',''),str(r.get('hResult',0)),r.get('paramName') or 'null',csv(q['used']),str(int(q['completed'])),csv(q['destination']),';'.join(csv(t) for t in q['trace'])]))
 assert any(not q['result']['ok'] and q['used'][0]==0 and q['count']==0 for q in j['rows'])
 assert any(q['result'].get('exception')=='System.InvalidOperationException' and q['used'][0]>0 and any(v!=99 for v in q['destination']) for q in j['rows'])
 assert any(q['count']==17 and q['result']['ok'] and q['trace'][:2]==[[0,0,17,0,1],[0,0,8,0,0]] for q in j['rows'])
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/generic-convert-arrays');work.mkdir(parents=True,exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');source=work/'GenericConvertArraysProbe.java';source.write_bytes(Path(__file__).with_name('generic-convert-arrays-probe.java').read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'GenericConvertArraysProbe',str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();groups=len(j['rows'])*5;assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeCases=11520,halvingFlushAndVirtualCallbackTraceControls=True,failureOutputAndDestinationControls=True,aliasedOutputAndPrefilledFallbackControls=True,contractViolatingCallbacks='BOUNDED_NATIVE_OBSERVATIONS_ONLY; NOT_ENDORSED_PROVIDER_CONTRACTS',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_GENERIC_BASE_CONVERT_ARRAYS_ONLY; COMPLETE_BOUNDARY_MATRIX_POINTER_SPAN_REENTRANCY_FULL_METADATA_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'generic-convert-arrays-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS generic Convert arrays: {groups} groups; 11520 native cases and exact callback traces')
if __name__=='__main__':main()
