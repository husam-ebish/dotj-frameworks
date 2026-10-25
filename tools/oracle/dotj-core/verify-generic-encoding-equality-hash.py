"""Verify selected generic Encoding equality/hash against the pinned native ordered matrix."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'generic-encoding-equality-hash-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-generic-encoding-equality-hash-contract.ps1').read_bytes()).hexdigest();assert len(j['specs'])==120 and len(j['rows'])==14400
 for s in j['specs']:
  expected=(s['codePage']+s['encoderHash']+s['decoderHash']+(1 if s['kind'] in [3,5] else 0)+2**31)%2**32-2**31;assert s['hash']==expected
 assert any(j['rows'][x*120+y]['equal']!=j['rows'][y*120+x]['equal'] for x in range(120) for y in range(120))
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/generic-encoding-equality-hash');work.mkdir(parents=True,exist_ok=True)
 specs=work/'specs.tsv';specs.write_text('\n'.join('\t'.join(str(int(s[k])) for k in ['kind','codePage','profile','cloned','readOnly','reportedCodePage','hash','equalsNull','equalsString']) for s in j['specs'])+'\n',encoding='ascii');pairs=work/'pairs.tsv';pairs.write_text('\n'.join('\t'.join(str(int(s[k])) for k in ['left','right','equal']) for s in j['rows'])+'\n',encoding='ascii')
 component=Path(__file__).with_name('generic-encoding-equality-hash-probe.java');source=work/'GenericEncodingEqualityHashProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'GenericEncodingEqualityHashProbe',str(specs),str(pairs)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert 'groups=14880' in result.stdout
 record=dict(schemaVersion=1,casesPassed=14880,nativeStates=120,orderedComparisons=14400,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_GENERIC_ENCODING_EQUALITY_HASH_AND_UTF8_INTERACTIONS_ONLY; ARBITRARY_PROVIDER_OVERRIDES_FULL_METADATA_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'generic-encoding-equality-hash-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS generic Encoding equality/hash: 120 states, 14400 ordered comparisons, 14880 groups')
if __name__=='__main__':main()
