"""Pin Encoding.Convert arrays, validation order and virtual array dispatch."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return 'null' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'encoding-convert-arrays-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-encoding-convert-arrays-contract.ps1').read_bytes()).hexdigest();assert len(j['rows'])==3786
 lines=[]
 for row in j['rows']:
  q=row['request'];r=row['result'];lines.append('\t'.join([str(q['src']),str(q['dst']),str(int(q['whole'])),csv(q['units']),str(q['index']),str(q['count']),str(q['sourceMode']),str(q['destMode']),str(int(r['ok'])),csv(r.get('value')),r.get('exception',''),str(r.get('hResult',0)),r.get('paramName') or 'null',str(int(r.get('sameInput',False))),str(int(r.get('sameDestinationReturn',False))),','.join(row['events']),str(int(row['sourceSeenInput'])),str(row['seenIndex']),str(row['seenCount']),str(int(row['destinationSeenSourceReturn']))]))
 assert sum(row['request']['sourceMode']>=0 or row['request']['destMode']>=0 for row in j['rows'])==120
 assert any(row['request']['units'] is None and row['request']['src']==-1 and row['request']['whole'] and row['result'].get('paramName')=='bytes' for row in j['rows'])
 assert any(row['request']['units'] is None and row['request']['src']==-1 and not row['request']['whole'] and row['result'].get('paramName')=='srcEncoding' for row in j['rows'])
 assert any(row['request']['sourceMode']==0 and row['request']['index']<0 and row['result']['ok'] for row in j['rows'])
 assert any(row['result'].get('sameDestinationReturn') for row in j['rows'])
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/encoding-convert-arrays');work.mkdir(parents=True,exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');source=work/'EncodingConvertArraysProbe.java';source.write_bytes(Path(__file__).with_name('encoding-convert-arrays-probe.java').read_bytes())
 subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'EncodingConvertArraysProbe',str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();groups=len(j['rows'])*9;assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeScenarios=len(j['rows']),derivedDispatchScenarios=120,nativeNullOrderingAndDerivedRangeBypass=True,sourceAndDestinationReferenceControls=True,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_ENCODING_CONVERT_ARRAYS_ONLY; OTHER_ENCODINGS_PROVIDER_POINTER_FULL_METADATA_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'encoding-convert-arrays-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(f'PASS Encoding.Convert arrays: {groups} groups; 120 derived dispatch scenarios')
if __name__=='__main__':main()
