import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding="utf-8"))['jarPath']
 oracle_path=EVIDENCE/'integer-string-parsing-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding="utf-8"));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-integer-string-parsing-contract.ps1').read_bytes()).hexdigest() and j['textCount']==398 and [v['fullName'] for v in j['types']]==['System.SByte','System.Byte','System.UInt16','System.UInt32']
 cases=[]
 for profile in j['types']:
  owner=profile['fullName'].split('.')[-1];assert len(profile['cases'])==796
  for row in profile['cases']:
   text='(String)null' if row['text'] is None else json.dumps(row['text']);provider='CUSTOM' if row['provider']=='Custom' else 'null'
   routes=[('parse',owner+'.Parse('+text+','+provider+')',False),('tryParse',owner+'.TryParse('+text+','+provider+',result)',True)]
   if 'parseDefault' in row:routes+=[('parseDefault',owner+'.Parse('+text+')',False),('tryDefault',owner+'.TryParse('+text+',result)',True)]
   for key,expression,is_try in routes:
    index=len(cases);result=row[key];setup=owner+'[] result={new '+owner+'(99)};' if is_try else ''
    if 'exception' in result:
     setup+='try{'+expression+';throw new AssertionError("missing parse error");}catch(Exception expected){check(expected.getClass().getName().equals('+json.dumps(result['exception'])+') && expected.get_HResult()=='+str(result['hResult'])+' && java.util.Objects.equals(expected instanceof ArgumentException argument ? argument.get_ParamName() : null,'+json.dumps(result['paramName'])+'),'+str(index)+');}'
     if is_try:setup+='check(result[0].get_Value()=='+str(result['value'])+'L,'+str(index)+');'
    elif is_try:setup+='check('+expression+'=='+str(result['boolean']).lower()+' && result[0].get_Value()=='+str(result['value'])+'L,'+str(index)+');'
    else:setup+='check('+expression+'.get_Value()=='+str(result['value'])+'L,'+str(index)+');'
    cases.append('{'+setup+'}')
  output=subprocess.run(['javap','-public','-classpath',str(a.jar),profile['fullName']],check=True,text=True,capture_output=True).stdout
  for signature in ['public static '+profile['fullName']+' Parse(java.lang.String);','public static '+profile['fullName']+' Parse(java.lang.String, System.IFormatProvider);','public static boolean TryParse(java.lang.String, '+profile['fullName']+'[]);','public static boolean TryParse(java.lang.String, System.IFormatProvider, '+profile['fullName']+'[]);']:assert signature in output
 assert len(j['providerQueries'])==120
 for row in j['providerQueries']:
  owner=row['fullName'].split('.')[-1];index=len(cases);result=row['result'];text='(String)null' if row['text'] is None else json.dumps(row['text']);is_try=row['operation']=='TryParse'
  expression=owner+'.'+row['operation']+'('+text+',provider'+(',result)' if is_try else ')')
  setup='ProbeProvider provider=new ProbeProvider('+json.dumps(row['kind'])+');'+(owner+'[] result={new '+owner+'(99)};' if is_try else '')
  if 'exception' in result:
   setup+='try{'+expression+';throw new AssertionError("missing provider error");}catch(Exception expected){check(expected.getClass().getName().equals('+json.dumps(result['exception'])+') && expected.get_HResult()=='+str(result['hResult'])+' && java.util.Objects.equals(expected instanceof ArgumentException argument ? argument.get_ParamName() : null,'+json.dumps(result['paramName'])+'),'+str(index)+');}'
   if is_try:setup+='check(result[0].get_Value()=='+str(result['value'])+'L,'+str(index)+');'
  elif is_try:setup+='check('+expression+'=='+str(result['boolean']).lower()+' && result[0].get_Value()=='+str(result['value'])+'L,'+str(index)+');'
  else:setup+='check('+expression+'.get_Value()=='+str(result['value'])+'L,'+str(index)+');'
  requested='null' if row['requestedType'] is None else 'Type.GetType('+json.dumps(row['requestedType'])+')'
  setup+='check(provider.calls=='+str(row['calls'])+' && provider.requested=='+requested+','+str(index)+');';cases.append('{'+setup+'}')
 assert len(cases)==9672
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/integer-string-parsing');work.mkdir(exist_ok=True);source=work/'IntegerStringParseProbe.java';methods=['static void group'+str(i//15)+'(){\n'+'\n'.join(cases[i:i+15])+'\n}' for i in range(0,len(cases),15)]
 source.write_text('import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.Exception;import System.ArgumentException;import System.FormatException;import System.OverflowException;import System.IFormatProvider;import System.Type;import System.Globalization.NumberFormatInfo;\nclass IntegerStringParseProbe{static final class ProbeProvider implements IFormatProvider{final String kind;int calls;Type requested;ProbeProvider(String kind){this.kind=kind;}public Object GetFormat(Type type){calls++;requested=type;if(kind.equals("Format"))throw new FormatException("provider failure");if(kind.equals("Overflow"))throw new OverflowException("provider failure");return null;}}static final NumberFormatInfo CUSTOM=new NumberFormatInfo();static{CUSTOM.set_NegativeSign("~");CUSTOM.set_PositiveSign("p");}static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+''.join('group'+str(i)+'();' for i in range(len(methods)))+'}}')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'IntegerStringParseProbe'],check=True)
 record=dict(schemaVersion=1,casesPassed=len(cases),nativeTextCount=j['textCount'],providerQueryControls=len(j['providerQueries']),oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='BOUNDED_INTEGER_STRING_PARSE_PASS; OTHER_STYLES_SPANS_PROVIDERS_GENERIC_INTERFACES_CLR_ABI_AND_ACCEPTANCE_OPEN')
 (EVIDENCE/'integer-string-parsing-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n');print('PASS integer String parsing: 9672 groups across four carriers, including 120 provider controls')
if __name__=='__main__':main()
