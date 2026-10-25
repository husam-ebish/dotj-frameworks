"""Compare custom public span override routing with native pointer-backed encoding operations."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'encoding-span-override-dispatch-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-encoding-span-override-dispatch-contract.ps1').read_bytes()).hexdigest();assert len(j['rows'])==1368
 for row in j['rows']:
  if row['operation'].startswith(('SpanCount','SpanWrite','Try')):
   assert row['result'].get('exception')=='System.InvalidOperationException' and len(row['trace'])==1 and row['trace'][0][0]>=10
  else:assert row['trace'] and row['trace'][0][0]<10
 lines=[]
 for row in j['rows']:
  r=row['result'];lines.append('\t'.join([*[str(row[k]) for k in ['multiplier','countMode','writeMode','length']],row['operation'],str(row['capacity']),str(int(r['ok'])),str(r.get('count',int(r.get('boolean',False)))),csv(r.get('units',[])),r.get('exception',''),str(r.get('hResult',0)),r.get('paramName') or '~',str(row['written']),csv(row['destination']),';'.join(csv(t) for t in row['trace'])]))
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/encoding-span-override-dispatch');work.mkdir(parents=True,exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');component=Path(__file__).with_name('encoding-span-override-dispatch-probe.java');source=work/'EncodingSpanOverrideDispatchProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'EncodingSpanOverrideDispatchProbe',str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert 'groups=5472' in result.stdout
 record=dict(schemaVersion=1,casesPassed=5472,nativeCases=1368,publicSpanOverrideBypassControls=True,directSpanAndTryVirtualControls=True,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_CUSTOM_ENCODING_PUBLIC_SPAN_OVERRIDE_DISPATCH_ONLY; DIRECT_POINTER_OVERRIDES_CLR_LIFETIME_REENTRANCY_FULL_METADATA_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'encoding-span-override-dispatch-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS Encoding span override dispatch: 1368 native cases, 5472 groups')
if __name__=='__main__':main()
