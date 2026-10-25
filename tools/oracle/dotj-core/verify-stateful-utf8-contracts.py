"""Audit the pinned stateful contract baseline without claiming Java behavior qualification."""
import argparse,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'stateful-utf8-contracts-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-stateful-utf8-contracts-contract.ps1').read_bytes()).hexdigest()
 assert len(j['types'])==2 and len(j['profiles'])==8
 methods=0
 for t,count in zip(j['types'],[13,15]):
  assert t['fullName'] in ['System.Text.Encoder','System.Text.Decoder'] and t['isAbstract'] and t['baseType']=='System.Object';assert len(t['methods'])==count and len(t['constructors'])==1 and t['constructors'][0]['isFamily'];methods+=count
  names={m['name'] for m in t['methods']};assert {'get_Fallback','set_Fallback','get_FallbackBuffer','Reset','Convert'}.issubset(names)
 actions=0;sequences=0
 for profile in j['profiles']:
  assert profile['freshInstances'] and profile['fallbackSharedWithEncoding'];assert len(profile['sequences'])==10
  kind='Exception' if profile['strict'] else 'Replacement';assert profile['fallbackType']=='System.Text.'+profile['direction']+kind+'Fallback'
  first=profile['sequences'][0]['rows'];expected=[0,4,0,1] if profile['direction']=='Encoder' else [0,0,0,2,0];assert [r['result']['count'] for r in first]==expected
  for sequence in profile['sequences']:
   sequences+=1
   for row in sequence['rows']:
    actions+=1;r=row['result'];assert isinstance(r['ok'],bool)
    if row['after'] is not None:assert len(row['after'])==64 and row['after'][0]==99
    if not r['ok']:assert r['exception'] in ['System.Text.EncoderFallbackException','System.Text.DecoderFallbackException'] and r['hResult']==-2147024809
 assert sequences==80 and actions==236 and methods==28
 with zipfile.ZipFile(a.jar) as z:classes=set(z.namelist())
 assert {'System/Text/Encoding.class','System/Text/UTF8Encoding.class'}.issubset(classes)
 coverage=[dict(nativeType=t['fullName'],candidateClassPresent=t['fullName'].replace('.','/')+'.class' in classes,nativeDeclaredMethods=len(t['methods']),candidateBehaviorQualifiedByThisBaseline=False) for t in j['types']]
 record=dict(schemaVersion=1,nativeTypes=2,nativeDeclaredMethods=28,nativeProfiles=8,nativeSequences=80,nativeTransitions=236,typeCoverage=coverage,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),nextImplementation='Selected UTF-8 Encoder array count/write with pending surrogate, flush, Reset and fallback property semantics; then Decoder pending byte prefixes',qualification='NATIVE_CONTRACT_BASELINE_ONLY; NO_CANDIDATE_STATEFUL_BEHAVIOR_OR_TASK_ACCEPTANCE');(EVIDENCE/'stateful-utf8-contracts-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS stateful UTF-8 baseline: 28 declarations, 80 sequences, 236 native transitions; candidate stateful behavior not qualified')
if __name__=='__main__':main()
