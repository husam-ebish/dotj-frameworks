"""Compare selected UTF-8 Encoder Convert progress and recovery to the native baseline."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'stateful-convert-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-stateful-convert-contract.ps1').read_bytes()).hexdigest();rows=[r for r in j['rows'] if r['direction']=='encoder'];assert len(rows)==2880;lines=[];groups=14;calls=0
 for row in rows:
  lines.append('R\t'+str(row['profile']))
  for step in row['steps']:
   if step['kind']=='reset':lines.append('Z');continue
   calls+=1;r=step['result'];groups+=5 if r['ok'] else 8;lines.append('\t'.join(['A',csv(step['units']),str(step['capacity']),str(step['offset']),str(int(step['flush'])),str(int(r['ok'])),r.get('exception',''),str(r.get('hResult',0)),r.get('paramName') or 'null',str(step['used'][0]),str(step['used'][1]),str(int(step['completed'])),csv(step['destination'])]))
 assert calls==10080
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/stateful-encoder-convert');work.mkdir(parents=True,exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');source=work/'StatefulEncoderConvertProbe.java';source.write_bytes(Path(__file__).with_name('stateful-encoder-convert-probe.java').read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'StatefulEncoderConvertProbe',str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeSequences=2880,nativeConvertCalls=calls,javaOutputCarrierControls=12,customProviderOrdinaryDispatchControls=2,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_UTF8_PREDEFINED_FALLBACK_ENCODER_CONVERT_ARRAYS_ONLY; BASE_PROTOCOL_DECODER_POINTER_SPAN_SOURCE_ABI_FULL_METADATA_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'stateful-encoder-convert-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS stateful Encoder Convert arrays: {groups} groups; {calls} native calls')
if __name__=='__main__':main()
