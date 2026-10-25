"""Selected fallback defaults, construction, equality and UTF-8 reference sharing."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def chars(v):return 'new String(new char[]{'+','.join('(char)'+str(x) for x in v)+'})'
def b(v):return str(v).lower()
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'encoding-fallback-contracts-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'))
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-encoding-fallback-contracts-contract.ps1').read_bytes()).hexdigest()
 assert len(j['constructors'])==34 and len(j['singletons'])==len(j['utf8Profiles'])==4;cases=[]
 for row in j['constructors']:
  direction=row['direction'];owner=direction+'ReplacementFallback';opposite=('Decoder' if direction=='Encoder' else 'Encoder')+'ReplacementFallback';r=row['result'];input_id=row['inputId'];argument='' if input_id==-2 else '(String)null' if input_id==-1 else chars(j['inputs'][input_id]);construct='new '+owner+'('+argument+')'
  if not r['ok']:cases.append('{try{'+construct+';throw new AssertionError("invalid replacement accepted");}catch(ArgumentException ex){check(ex.getClass().getName().equals('+json.dumps(r['exception'])+')&&ex.get_HResult()=='+str(r['hResult'])+'&&Objects.equals(ex.get_ParamName(),'+json.dumps(r['paramName'])+'),'+str(len(cases))+');}}');continue
  assert r['equalHashInvariant'];setup=owner+' value='+construct+';';checks=['value.get_DefaultString().equals('+chars(r['defaultUnits'])+')','value.get_MaxCharCount()=='+str(r['maxCharCount'])];cases.append('{'+setup+'check('+'&&'.join(checks)+','+str(len(cases))+');}')
  for expression,expected in [('value.Equals(value)',r['equalsSelf']),('value.Equals(new '+owner+'(value.get_DefaultString()))',r['equalsEquivalent']),('value.Equals(new '+owner+'("different replacement"))',r['equalsDifferent']),('value.Equals(new '+opposite+'(value.get_DefaultString()))',r['equalsOpposite']),('value.Equals(null)',r['equalsNull'])]:cases.append('{'+setup+'check('+expression+'=='+b(expected)+','+str(len(cases))+');}')
 for row in j['singletons']:
  base=row['direction']+'Fallback';owner=row['direction']+row['kind']+'Fallback';call=base+'.get_'+row['kind']+'Fallback()';assert row['singleton'] and row['equalHashInvariant'];checks=['value=='+call,'value.getClass().getName().equals('+json.dumps(row['type'])+')','value.get_MaxCharCount()=='+str(row['maxCharCount']),'value.Equals(new '+owner+'())=='+b(row['equalsNew']),'value.Equals(null)=='+b(row['equalsNull'])]
  if row['kind']=='Replacement':checks+=['(('+owner+')value).get_DefaultString().equals('+chars(row['defaultUnits'])+')']
  cases.append('{'+base+' value='+call+';check('+'&&'.join(checks)+','+str(len(cases))+');}')
 for row in j['utf8Profiles']:
  setup='Encoding value=new UTF8Encoding('+b(row['emit'])+','+b(row['strict'])+'),other=new UTF8Encoding('+b(row['emit'])+','+b(row['strict'])+'),clone=(Encoding)value.Clone();';checks=['value.get_EncoderFallback().getClass().getName().equals('+json.dumps(row['encoderType'])+')','value.get_DecoderFallback().getClass().getName().equals('+json.dumps(row['decoderType'])+')','value.get_EncoderFallback().get_MaxCharCount()=='+str(row['encoderMax']),'value.get_DecoderFallback().get_MaxCharCount()=='+str(row['decoderMax']),'(value.get_EncoderFallback()==other.get_EncoderFallback())=='+b(row['encoderShared']),'(value.get_DecoderFallback()==other.get_DecoderFallback())=='+b(row['decoderShared']),'(value.get_EncoderFallback()==clone.get_EncoderFallback())=='+b(row['encoderCloneShared']),'(value.get_DecoderFallback()==clone.get_DecoderFallback())=='+b(row['decoderCloneShared'])]
  if not row['strict']:checks+=['((EncoderReplacementFallback)value.get_EncoderFallback()).get_DefaultString().equals('+chars(row['encoderUnits'])+')','((DecoderReplacementFallback)value.get_DecoderFallback()).get_DefaultString().equals('+chars(row['decoderUnits'])+')']
  cases.append('{'+setup+'check('+'&&'.join(checks)+','+str(len(cases))+');}')
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/encoding-fallback-contracts');work.mkdir(exist_ok=True);source=work/'EncodingFallbackObjectProbe.java';source.write_text('import System.Text.*;import System.ArgumentException;import java.util.Objects;class EncodingFallbackObjectProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}public static void main(String[] args){\n'+'\n'.join(cases)+'}}',encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'EncodingFallbackObjectProbe'],check=True)
 record=dict(schemaVersion=1,casesPassed=len(cases),nativeConstructors=34,nativeSingletons=4,nativeUtf8Profiles=4,nativeHashEqualityInvariantRecorded=True,nativeGetHashCodeAlgorithmQualified=False,nativeBufferCreationQualified=False,oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_DEFAULT_OBJECTS_CONSTRUCTION_EQUALITY_AND_REFERENCE_SHARING_ONLY; BUFFER_CUSTOMIZATION_HASH_ALGORITHM_FULL_METADATA_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN')
 (EVIDENCE/'encoding-fallback-contracts-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS selected encoding fallback objects: '+str(len(cases))+' groups; buffers, customization and native hashing remain open')
if __name__=='__main__':main()
