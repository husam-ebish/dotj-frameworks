"""Compare writable cloning and selected interface dispatch, without full reflection credit."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'encoding-clone-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'))
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-encoding-clone-contract.ps1').read_bytes()).hexdigest()
 assert j['interfaceName']=='System.ICloneable' and j['interfaceMethods']==['System.Object Clone()'] and len(j['profiles'])==6;cases=[]
 for row in j['profiles']:
  assert row['distinct'] and row['distinctClone2'] and row['sourceReadOnly'] and not row['cloneReadOnly'] and not row['clone2ReadOnly'] and row['isCloneable']
  assert row['sourceEncode']==row['cloneEncode'] and row['sourceDecode']==row['cloneDecode']
  profile=row['profile'];checks=['clone!=source','clone2!=clone','source.get_IsReadOnly()','!clone.get_IsReadOnly()','!clone2.get_IsReadOnly()','clone instanceof ICloneable','clone.get_CodePage()==65001','Arrays.equals(values(clone.GetPreamble()),new int[]{'+','.join(map(str,row['preamble']))+'})','clone.getClass().getName().equals('+json.dumps(row['cloneType'])+')','clone2.getClass()==clone.getClass()']
  if profile==5:assert row['marker']==42;checks+=['((Utf8CloneSubclass)clone).Marker==42']
  cases.append('{Encoding source=sources['+str(profile)+'];Encoding clone=(Encoding)source.Clone(),clone2=(Encoding)((ICloneable)clone).Clone();check('+'&&'.join(checks)+','+str(len(cases))+');}')
  for direction in ['Encode','Decode']:
   r=row['clone'+direction];call='e.GetBytes(new String(new char[]{65,(char)0xd800,66}))' if direction=='Encode' else 'e.GetChars(new Byte[]{new Byte(65),new Byte(255),new Byte(66)})'
   if r['ok']:expression='Arrays.equals(values('+call+'),new int[]{'+','.join(map(str,r['units']))+'})' if direction=='Encode' else 'Arrays.equals('+call+',new char[]{'+','.join('(char)'+str(v) for v in r['units'])+'})';body='check('+expression+','+str(len(cases))+');'
   else:body='try{'+call+';throw new AssertionError("invalid input accepted");}catch(ArgumentException ex){check(ex.getClass().getName().equals('+json.dumps(r['exception'])+')&&ex.get_HResult()=='+str(r['hResult'])+'&&'+('((EncoderFallbackException)ex)' if direction=='Encode' else '((DecoderFallbackException)ex)')+'.get_Index()=='+str(r['index'])+','+str(len(cases))+');}'
   cases.append('{Encoding original=sources['+str(profile)+'];for(Encoding e:new Encoding[]{original,(Encoding)original.Clone(),(Encoding)((ICloneable)original).Clone()}){'+body+'}}')
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/encoding-clone');work.mkdir(exist_ok=True);source=work/'EncodingCloneProbe.java';source.write_text('import System.Text.*;import System.ICloneable;import System.Byte;import System.ArgumentException;import java.util.Arrays;class Utf8CloneSubclass extends UTF8Encoding{public int Marker=42;}class EncodingCloneProbe{static int[] values(Byte[] bytes){int[] r=new int[bytes.length];for(int i=0;i<r.length;i++)r[i]=bytes[i].get_Value();return r;}static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}public static void main(String[] args){Encoding[] sources={new UTF8Encoding(),new UTF8Encoding(true),new UTF8Encoding(false,true),new UTF8Encoding(true,true),Encoding.get_UTF8(),new Utf8CloneSubclass()};\n'+'\n'.join(cases)+'}}',encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'EncodingCloneProbe'],check=True)
 record=dict(schemaVersion=1,casesPassed=42,nativeProfiles=6,selectedInterface='System.ICloneable.Clone()',nativeDefaultRuntimeType=j['profiles'][4]['sourceType'],nativeInternalDefaultRuntimeTypeQualified=False,nativeFallbackReferenceSharingRecordedButNotQualified=True,oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_CLONE_INTERFACE_DISPATCH_ONLY; INTERFACE_REFLECTION_FALLBACK_CUSTOMIZATION_INTERNAL_RUNTIME_TYPE_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN')
 (EVIDENCE/'encoding-clone-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS selected Encoding Clone: 42 groups across six profiles; selected ICloneable metadata is recorded separately; runtime internals remain open')
if __name__=='__main__':main()
