"""Compare generic Encoding protected constructors, provider properties, clones and empty preambles."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return ','.join(map(str,v))
def outcome(r):return [str(int(r['ok'])),r.get('exception',''),str(r.get('hResult',0)),r.get('paramName') or '~',str(r['actualValue']) if r.get('actualValue') is not None else '~',base64.b64encode(r.get('message','').encode('utf-8')).decode('ascii')]
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'generic-encoding-default-properties-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-generic-encoding-default-properties-contract.ps1').read_bytes()).hexdigest();assert len(j['rows'])==65;lines=[];states=steps=0
 def snapshots(case,values):
  nonlocal states
  for owner,r in enumerate(values):
   states+=1;assert len(r['identity'])==9;lines.append('\t'.join(['S',str(case),str(owner),str(int(r['readOnly'])),str(r['codePage']),str(int(r['singleByte'])),r['encoderType'],r['decoderType'],str(r['encoderMax']),str(r['decoderMax']),str(int(r['encoderUnits'] is not None)),csv(r['encoderUnits'] or []),str(int(r['decoderUnits'] is not None)),csv(r['decoderUnits'] or []),''.join(str(int(v)) for v in r['identity']),str(r['preambleLength'])]))
 for case,row in enumerate(j['rows']):
  lines.append('\t'.join(['C',str(case),str(row['kind']),str(row['codePage']),str(row['profile']),*outcome(row['result'])]))
  if row['result']['ok']:
   assert len(row['steps'])==16;snapshots(case,row['initial'])
   for step in row['steps']:
    steps+=1;lines.append('\t'.join(['A',str(case),step['operation'],str(step['target']),*outcome(step['result'])]));snapshots(case,step['states'])
  else:assert row['result']['exception']=='System.ArgumentOutOfRangeException' and row['result']['paramName']=='codePage' and row['result']['actualValue']==row['codePage']<0
 assert states==1666 and steps==784
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/generic-encoding-default-properties');work.mkdir(parents=True,exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');component=Path(__file__).with_name('generic-encoding-default-properties-probe.java');source=work/'GenericEncodingDefaultPropertiesProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'GenericEncodingDefaultPropertiesProbe',str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert 'groups=12511' in result.stdout
 record=dict(schemaVersion=1,casesPassed=12511,nativeConstructorProfiles=65,nativePropertySteps=steps,nativeStateSnapshots=states,readOnlyBeforeNullSetterControls=True,negativeActualValueAndMessageControls=True,sharedUtf8EmptyPreambleIdentity=True,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_GENERIC_ENCODING_CONSTRUCTORS_FALLBACK_CLONE_CODEPAGE_PREAMBLE_ONLY; METADATA_TABLES_CUSTOM_CALLBACKS_FULL_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'generic-encoding-default-properties-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS generic Encoding defaults: 65 constructors, 784 steps, 1666 snapshots, 12511 groups')
if __name__=='__main__':main()
