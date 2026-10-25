"""Compare generic Encoding Try span virtual dispatch and output assignment order."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'generic-encoding-try-spans-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-generic-encoding-try-spans-contract.ps1').read_bytes()).hexdigest();assert len(j['rows'])==3584
 lines=[]
 for row in j['rows']:
  r=row['result'];lines.append('\t'.join([row['direction'],*[str(row[k]) for k in ['multiplier','countMode','writeMode','length','capacity','offset']],str(int(r['ok'])),str(int(r.get('success',False))),r.get('exception',''),str(r.get('hResult',0)),r.get('paramName') or '~',str(row['written']),csv(row['destination']),';'.join(csv(t) for t in row['trace'])]))
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/generic-encoding-try-spans');work.mkdir(parents=True,exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');source=work/'GenericEncodingTrySpansProbe.java';component=Path(__file__).with_name('generic-encoding-try-spans-probe.java');source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'GenericEncodingTrySpansProbe',str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert 'groups=14336' in result.stdout
 record=dict(schemaVersion=1,casesPassed=14336,nativeCases=3584,virtualSpanOverrides=True,arrayOverridesMustNotBeCalled=True,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_GENERIC_ENCODING_TRY_SPAN_DISPATCH_ONLY; CUSTOM_UTF8_PROVIDERS_POINTER_LIFETIME_FULL_METADATA_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'generic-encoding-try-spans-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS generic Encoding Try spans: 3584 native cases, 14336 groups')
if __name__=='__main__':main()
