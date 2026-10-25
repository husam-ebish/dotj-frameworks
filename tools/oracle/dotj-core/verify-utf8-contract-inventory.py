"""Audit pinned UTF-8 declarations and report candidate coverage without acceptance credit."""
import argparse, hashlib, json, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'utf8-contract-inventory-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'))
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-utf8-contract-inventory-contract.ps1').read_bytes()).hexdigest()
 types=j['types'];assert len(types)==14 and len({t['fullName'] for t in types})==14
 by_name={t['fullName']:t for t in types};assert by_name['System.Text.Encoding']['isAbstract']
 assert by_name['System.Text.UTF8Encoding']['baseType']=='System.Text.Encoding'
 for name in ['EncoderFallbackException','DecoderFallbackException']:assert by_name['System.Text.'+name]['baseType']=='System.ArgumentException'
 utf8=by_name['System.Text.UTF8Encoding'];assert len(utf8['constructors'])==3
 assert {'GetBytes','GetByteCount','GetChars','GetCharCount','GetString','GetPreamble','GetEncoder','GetDecoder'}.issubset({m['name'] for m in utf8['methods']})
 assert len(j['constructorProfiles'])==4
 for row in j['constructorProfiles']:
  assert row['codePage']==65001 and row['isReadOnly']
  assert row['preamble']==([239,187,191] if row['emitIdentifier'] else [])
  kind='Exception' if row['throwOnInvalidBytes'] else 'Replacement'
  for direction in ['encoder','decoder']:
   assert row[direction+'Fallback']=='System.Text.'+direction.title()+kind+'Fallback'
   assert row[direction+'Replacement']==(None if kind=='Exception' else '\ufffd')
 assert j['defaultUtf8']['isReadOnly'] and j['defaultUtf8']['preamble']==[239,187,191]
 with zipfile.ZipFile(a.jar) as z:present=set(z.namelist())
 coverage=[dict(nativeType=t['fullName'],candidateClassPresent=t['fullName'].replace('.','/')+'.class' in present,declaredNativeMethods=len(t['methods']),declaredNativeConstructors=len(t['constructors'])) for t in types]
 assert not any('EncodingProfile.class' in v or 'CultureProfile.class' in v for v in present)
 record=dict(schemaVersion=1,nativeTypes=14,constructorProfiles=4,typeCoverage=coverage,nativeMethodCount=sum(len(t['methods']) for t in types),oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='CONTRACT_INVENTORY_ONLY; CLASS_PRESENCE_IS_NOT_BEHAVIOR_OR_TASK_ACCEPTANCE',openCriteria=['UTF-8 invalid-input replacement and strict modes','stateful Encoder/Decoder behavior','span and pointer overloads','normalization and culture comparison','source identity and CLR ABI','E01/E02/E03/N01 and implementation-task acceptance'])
 (EVIDENCE/'utf8-contract-inventory-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS UTF-8 contract inventory: 14 native types, four constructor profiles; qualification remains open')
if __name__=='__main__':main()
