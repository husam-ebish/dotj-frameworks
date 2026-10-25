"""Compare selected typed Char/UTF-8 parsing bridges with real pinned CoreLib spans."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding="utf-8"))['jarPath']
 oracle_path=EVIDENCE/'integer-span-parsing-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding="utf-8"));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-integer-span-parsing-contract.ps1').read_bytes()).hexdigest()
 assert j['inputEvidence']=='integer-string-parsing-contract-v10.0.12.json' and j['inputSha256']==hashlib.sha256((EVIDENCE/j['inputEvidence']).read_bytes()).hexdigest()
 assert j['sourceCount']==868 and len(j['providerQueries'])==144 and [v['fullName'] for v in j['types']]==['System.SByte','System.Byte','System.UInt16','System.UInt32']
 assert len(j['providers'])==14
 provider_ids={row['name']:'PROVIDER_'+str(i) for i,row in enumerate(j['providers'])}
 provider_source=''.join('static final NumberFormatInfo '+provider_ids[row['name']]+'=makeProvider('+json.dumps(row['negativeSign'])+','+json.dumps(row['positiveSign'])+');' for row in j['providers'])
 total=0;rejected=[]
 for profile in j['types']:
  owner=profile['fullName'].split('.')[-1];assert len(profile['cases'])==2516;cases=[]
  def setup(row,offset,control):
   char=row['encoding']=='Char';element='char' if char else 'byte';carrier='Character' if char else 'Byte';factory='OfChars' if char else 'OfUtf8Bytes';units='new '+element+'[]{'+','.join('('+element+')'+str(v) for v in row['units'])+'}'
   text=element+'[] core='+units+';'+element+'[] backing=new '+element+'[core.length+'+str(offset+2)+'];java.util.Arrays.fill(backing,('+element+')35);java.lang.System.arraycopy(core,0,backing,'+str(offset)+',core.length);'+element+'[] before=backing.clone();ReadOnlySpan<'+carrier+'> text=ReadOnlySpan.'+factory+'(backing,'+str(offset)+',core.length);'
   if control:text+='ProbeProvider provider=new ProbeProvider('+json.dumps(row['kind'])+');'
   else:text+='IFormatProvider provider='+provider_ids[row['provider']]+';'
   return text
  def add(row,offset,key,control=False):
   index=len(cases);result=row['result'] if control else row[key];is_try=(row['operation']=='TryParse') if control else key!='parse'
   text=setup(row,offset,control)+(owner+'[] result={new '+owner+'(99)};' if is_try else '')
   expression=owner+'.'+('TryParse' if is_try else 'Parse')+'(text'+(',result)' if key=='tryDefault' else ',provider'+(',result)' if is_try else ')'))
   if 'exception' in result:
    text+='try{'+expression+';throw new AssertionError("missing span parse error");}catch(Exception expected){check(expected.getClass().getName().equals('+json.dumps(result['exception'])+') && expected.get_HResult()=='+str(result['hResult'])+' && java.util.Objects.equals(expected instanceof ArgumentException argument ? argument.get_ParamName() : null,'+json.dumps(result['paramName'])+'),'+str(index)+');}'
    if is_try:text+='check(result[0].get_Value()=='+str(result['value'])+'L,'+str(index)+');'
   elif is_try:text+='check('+expression+'=='+str(result['boolean']).lower()+' && result[0].get_Value()=='+str(result['value'])+'L,'+str(index)+');'
   else:text+='check('+expression+'.get_Value()=='+str(result['value'])+'L,'+str(index)+');'
   if control:
    requested='null' if row['requestedType'] is None else 'Type.GetType('+json.dumps(row['requestedType'])+')'
    text+='check(provider.calls=='+str(row['calls'])+' && provider.requested=='+requested+','+str(index)+');'
   text+='check(java.util.Arrays.equals(backing,before),'+str(index)+');';cases.append('{'+text+'}')
  for row in profile['cases']:
   for offset in [0,3]:
    for key in ['parse','tryParse']+(['tryDefault'] if 'tryDefault' in row else []):add(row,offset,key)
  controls=[v for v in j['providerQueries'] if v['fullName']==profile['fullName']];assert len(controls)==36
  for row in controls:
   for offset in [0,3]:add(row,offset,'control',True)
  assert len(cases)==11784,(owner,len(cases));total+=len(cases)
  work=Path('D:/AI/Implementation/dotj Frameworks/verification/integer-span-parsing')/owner;work.mkdir(parents=True,exist_ok=True);class_name=owner+'SpanParseProbe';source=work/(class_name+'.java');methods=['static void group'+str(i//10)+'(){\n'+'\n'.join(cases[i:i+10])+'\n}' for i in range(0,len(cases),10)]
  source.write_text('import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.ReadOnlySpan;import System.Exception;import System.ArgumentException;import System.FormatException;import System.OverflowException;import System.IFormatProvider;import System.Type;import System.Globalization.NumberFormatInfo;\nclass '+class_name+'{'+provider_source+'static NumberFormatInfo makeProvider(String negative,String positive){NumberFormatInfo value=new NumberFormatInfo();value.set_NegativeSign(negative);value.set_PositiveSign(positive);return value;}static final class ProbeProvider implements IFormatProvider{final String kind;int calls;Type requested;ProbeProvider(String kind){this.kind=kind;}public Object GetFormat(Type type){calls++;requested=type;if(kind.equals("Format"))throw new FormatException("provider failure");if(kind.equals("Overflow"))throw new OverflowException("provider failure");return null;}}static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+''.join('group'+str(i)+'();' for i in range(len(methods)))+'}}')
  subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),class_name],check=True)
  output=subprocess.run(['javap','-public','-classpath',str(a.jar),profile['fullName']],check=True,text=True,capture_output=True).stdout
  for signature in ['public static <T> '+profile['fullName']+' Parse(System.ReadOnlySpan<T>, System.IFormatProvider);','public static <T> boolean TryParse(System.ReadOnlySpan<T>, '+profile['fullName']+'[]);','public static <T> boolean TryParse(System.ReadOnlySpan<T>, System.IFormatProvider, '+profile['fullName']+'[]);']:assert signature in output
  bad=work/('Bad'+owner+'SpanOut.java');bad.write_text('import System.'+owner+';import System.ReadOnlySpan;import System.Int32;class Bad'+owner+'SpanOut{void test(){'+owner+'.TryParse(ReadOnlySpan.OfUtf8Bytes(new byte[0]),new Int32[1]);}}')
  result=subprocess.run(['javac','-Xmaxerrs','1','--release','21','-cp',str(a.jar),'-d',str(work),str(bad)],text=True,capture_output=True);assert result.returncode!=0 and any(v in result.stderr for v in ['no suitable method','incompatible types','inference variable']),result.stderr;rejected.append(owner)
  print(f'PASS {owner} typed span parsing: {len(cases)} groups',flush=True)
 assert total==47136 and len(rejected)==4
 record=dict(schemaVersion=1,casesPassed=total,providerControls=144,providerProfiles=len(j['providers']),compileRejections=rejected,nativeParsingOverloads=24,typedJavaParsingBridges=12,oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),inputEvidence=j['inputEvidence'],inputSha256=j['inputSha256'],candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='BOUNDED_INTEGER_CHAR_UTF8_PARSE_PASS; ERASED_TYPED_BRIDGES_BYREF_LIFETIMES_GENERIC_INTERFACES_STYLES_PROVIDERS_CULTURES_AND_ACCEPTANCE_OPEN')
 (EVIDENCE/'integer-span-parsing-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n');print('PASS integer typed span parsing: 47136 groups and four compile rejections')
if __name__=='__main__':main()
