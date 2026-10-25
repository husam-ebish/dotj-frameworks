"""Pin selected UTF-8 metadata properties under invariant UI culture."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'utf8-metadata-properties-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-utf8-metadata-properties-contract.ps1').read_bytes()).hexdigest();assert len(j['metadata'])==11 and j['uiCulture']=='';lines=[];b=lambda v:str(v).lower()
 for row in j['metadata']:
  profile=row['profile'];kind=profile['kind'];expr='new '+('DerivedUtf8' if kind=='derived' else 'CodePageOverride' if kind=='CodePageOverride' else 'UTF8Encoding')+'('+b(profile['emit'])+','+b(profile['strict'])+')'
  if kind=='default':expr='Encoding.get_UTF8()'
  elif kind=='defaultClone':expr='(Encoding)Encoding.get_UTF8().Clone()'
  lines.append('{Encoding e='+expr+';')
  assert len(row['properties'])==12
  for name,value in row['properties'].items():
   call='e.get_'+name+'()';expected=b(value) if isinstance(value,bool) else json.dumps(value);lines.append('check('+ (call+'.equals('+expected+')' if isinstance(value,str) else call+'=='+expected)+',id++);')
  lines.append('check(Arrays.equals(bytes(e.GetPreamble()),new int[]{'+','.join(map(str,row['preamble']))+'}),id++);check(((Encoding)e.Clone()).get_IsReadOnly()=='+b(row['cloneReadOnly'])+',id++);}')
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/utf8-metadata-properties');work.mkdir(exist_ok=True);source=work/'Utf8MetadataPropertiesProbe.java';source.write_text('''import System.Text.*;import System.Byte;import java.util.*;
class DerivedUtf8 extends UTF8Encoding{DerivedUtf8(boolean e,boolean s){super(e,s);}}
class CodePageOverride extends UTF8Encoding{CodePageOverride(boolean e,boolean s){super(e,s);}public int get_CodePage(){return 90000;}}
class Utf8MetadataPropertiesProbe{static int[] bytes(Byte[] b){int[] r=new int[b.length];for(int i=0;i<b.length;i++)r[i]=b[i].get_Value();return r;}static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}public static void main(String[] args){int id=0;
'''+ '\n'.join(lines)+'''java.lang.System.out.println("PASS UTF-8 metadata groups="+id);}}''',encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'Utf8MetadataPropertiesProbe'],check=True)
 record=dict(schemaVersion=1,casesPassed=154,nativeProfiles=11,nativeProperties=12,uiCulture='',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_UTF8_METADATA_PROPERTIES_ONLY; OTHER_ENCODINGS_CULTURES_FULL_METADATA_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'utf8-metadata-properties-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS selected UTF-8 metadata: 154 groups; invariant UI culture and CodePage override controls')
if __name__=='__main__':main()
