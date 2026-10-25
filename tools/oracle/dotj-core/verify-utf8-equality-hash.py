"""Compare selected UTF-8 equality and process-local hash formulas with pinned native evidence."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'utf8-equality-hash-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-utf8-equality-hash-contract.ps1').read_bytes()).hexdigest();assert len(j['profiles'])==82 and len(j['rows'])==6724
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/utf8-equality-hash');work.mkdir(exist_ok=True);b=lambda v:str(v).lower();definitions=[]
 for index,profile in enumerate(j['profiles']):
  assert profile['hashFormulaMatches'] and profile['hashStable'] and profile['equalsClone'] and profile['cloneHashMatches'];assert not any(profile[k] for k in ['equalsNull','equalsString','equalsObject'])
  kind=profile['kind'];expression='new '+('DerivedUtf8' if kind=='derived' else 'UTF8Encoding')+'('+b(profile['emit'])+','+b(profile['strict'])+')'
  if kind=='default':expression='Encoding.get_UTF8()'
  elif kind=='defaultClone':expression='(Encoding)Encoding.get_UTF8().Clone()'
  elif kind=='customized':expression='(Encoding)('+expression+').Clone()'
  definitions.append(f'values[{index}]={expression};')
  if kind=='customized':
   for direction,key in [('Encoder','encoder'),('Decoder','decoder')]:
    number=profile[key];expression='new '+direction+'ExceptionFallback()' if number==5 else 'new '+direction+'ReplacementFallback(new String(new char[]{'+','.join('(char)'+str(v) for v in j['replacementTemplates'][number])+'}))';definitions.append(f'values[{index}].set_{direction}Fallback({expression});')
 checks=[]
 for index,profile in enumerate(j['profiles']):
  checks.append('{Encoding e=values['+str(index)+'];int hash=e.GetHashCode();check(hash==e.get_EncoderFallback().GetHashCode()+e.get_DecoderFallback().GetHashCode()+65001+'+('1' if profile['emit'] else '0')+',id++);check(hash==e.GetHashCode(),id++);check(e.Equals(e.Clone()),id++);check(hash==((Encoding)e.Clone()).GetHashCode(),id++);check(!e.Equals(null),id++);check(!e.Equals("UTF-8"),id++);check(!e.Equals(new Object()),id++);}')
 vectors=work/'pairs.tsv';vectors.write_text('\n'.join(f"{row['left']}\t{row['right']}\t{int(row['equals'])}" for row in j['rows'])+'\n',encoding='ascii')
 source=work/'Utf8EqualityHashProbe.java';source.write_text('''import System.Text.*;import java.nio.file.*;
class DerivedUtf8 extends UTF8Encoding{DerivedUtf8(boolean emit,boolean strict){super(emit,strict);}}
class Utf8EqualityHashProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}public static void main(String[] args)throws java.lang.Exception{int id=0;Encoding[] values=new Encoding[82];
'''+ '\n'.join(definitions+checks)+'''
for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\\t");Encoding left=values[Integer.parseInt(p[0])],right=values[Integer.parseInt(p[1])];boolean expected=p[2].equals("1");check(left.Equals(right)==expected&&(!expected||left.GetHashCode()==right.GetHashCode()),id++);}java.lang.System.out.println("PASS UTF-8 equality/hash groups="+id);}}
''',encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'Utf8EqualityHashProbe',str(vectors)],check=True)
 record=dict(schemaVersion=1,casesPassed=7298,nativeProfiles=82,nativeOrderedPairs=6724,hashScope='Candidate process-local formula, stability and equal-object invariant; native raw hash values are not compared across processes',oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_UTF8_EQUALITY_HASH_ONLY; CUSTOM_OVERRIDES_FULL_METADATA_HOST_OBJECT_INTEROP_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'utf8-equality-hash-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS selected UTF-8 equality/hash: 7298 groups; process-local hash scope')
if __name__=='__main__':main()
