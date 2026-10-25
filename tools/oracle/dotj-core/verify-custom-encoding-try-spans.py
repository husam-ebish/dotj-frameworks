"""Compare custom UTF8 Try span callbacks and exceptional output ordering."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'custom-encoding-try-spans-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-custom-encoding-try-spans-contract.ps1').read_bytes()).hexdigest();assert len(j['rows'])==14112
 lines=[]
 for row in j['rows']:
  r=row['result'];lines.append('\t'.join([row['direction'],csv(row['replacementUnits']),str(row['mode']),csv(row['units']),str(row['capacity']),str(row['offset']),str(int(r['ok'])),str(int(r.get('success',False))),r.get('exception',''),str(r.get('hResult',0)),r.get('paramName') or '~',str(r.get('unknown',0)),str(r.get('index',0)),csv(r.get('unknownBytes',[])),str(row['written']),csv(row['destination']),str(row['factoryCalls']),csv(row['bufferCalls'])]))
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/custom-encoding-try-spans');work.mkdir(parents=True,exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');component=Path(__file__).with_name('custom-encoding-try-spans-probe.java');source=work/'CustomEncodingTrySpansProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'CustomEncodingTrySpansProbe',str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert 'groups=70560' in result.stdout
 record=dict(schemaVersion=1,casesPassed=70560,nativeCases=14112,providerModes=14,capacityLikeCallbackExceptionControls=True,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_CUSTOM_UTF8_TRY_SPANS_ONLY; ARBITRARY_REENTRANCY_POINTER_LIFETIME_FULL_METADATA_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'custom-encoding-try-spans-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS custom Encoding Try spans: 14112 cases, 70560 groups')
if __name__=='__main__':main()
