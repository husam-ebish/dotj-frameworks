"""Pin Decoder Convert validation, output aliases, strict payloads and cross-API state."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return 'null' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'decoder-convert-boundaries-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-decoder-convert-boundaries-contract.ps1').read_bytes()).hexdigest();assert j['forms']==110 and len(j['rows'])==1356;lines=[];groups=calls=aliases=payloads=0
 for row in j['rows']:
  lines.append('R\t'+str(row['profile']))
  for step in row['steps']:
   q=step['request'];r=step['result'];payload=r.get('exception')=='System.Text.DecoderFallbackException';groups+=(6 if r['ok'] else 8)+2*int(payload);calls+=1;aliases+=int(q['alias']);payloads+=int(payload);lines.append('\t'.join(['Q',q['kind'],csv(q['units']),str(int(q['srcNull'])),str(int(q['destNull'])),str(q['destLength']),str(q['byteIndex']),str(q['byteCount']),str(q['charIndex']),str(q['charCount']),str(int(q['flush'])),str(int(q['alias'])),str(int(r['ok'])),str(r.get('value',0)),r.get('exception',''),str(r.get('hResult',0)),r.get('paramName') or 'null',str(step['used'][0]),str(step['used'][1]),str(int(step['completed'])),csv(step['destination']),str(step['remaining']),csv(r.get('bytesUnknown',[])),str(r.get('index',0))]))
 assert aliases==72 and sum(row['family']=='cross-api' for row in j['rows'])==36
 assert any(s['request']['alias'] and s['result']['ok'] and s['used']==[3,-8] and s['destination'][:1]==[8364] for row in j['rows'] for s in row['steps'])
 assert any(s['result'].get('index',0)<0 and s['result'].get('bytesUnknown')==[226] for row in j['rows'] for s in row['steps'])
 assert all(s['remaining']==0 for row in j['rows'] for s in row['steps'])
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/decoder-convert-boundaries');work.mkdir(parents=True,exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');source=work/'DecoderConvertBoundariesProbe.java';source.write_bytes(Path(__file__).with_name('decoder-convert-boundaries-probe.java').read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'DecoderConvertBoundariesProbe',str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeForms=110,nativeSequences=1356,nativeActions=calls,aliasControls=aliases,crossApiSequences=36,strictExceptionPayloads=payloads,pendingPrefixAndNegativeIndexControls=True,nativeAliasAssignmentOrder=True,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_PREDEFINED_UTF8_DECODER_ARRAY_BOUNDARIES_ONLY; CUSTOM_PROVIDERS_BASE_POINTER_SPAN_SOURCE_ABI_FULL_METADATA_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'decoder-convert-boundaries-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS Decoder Convert boundaries: {groups} groups; {calls} native actions; {payloads} strict payloads')
if __name__=='__main__':main()
