"""Stream pinned String/Char/UTF-8 style results through external Java consumers."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def b64(value):return '!' if value is None else base64.b64encode(value.encode('utf-8')).decode('ascii')
def outcome(value):
 if value is None:return '!'
 assert value[0] in ['V','T','E'],value
 if value[0]=='V':return 'V:'+str(value[1])
 if value[0]=='T':return 'T:'+str(value[1]).lower()+':'+str(value[2])
 return 'E:'+value[1]+':'+str(value[2])+':'+b64(value[3])+(':'+str(value[4]) if len(value)==5 else '')
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'integer-style-parsing-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-integer-style-parsing-contract.ps1').read_bytes()).hexdigest()
 assert j['inputEvidence']=='integer-string-parsing-contract-v10.0.12.json' and j['inputSha256']==hashlib.sha256((EVIDENCE/j['inputEvidence']).read_bytes()).hexdigest()
 assert j['types']==['System.SByte','System.Byte','System.UInt16','System.UInt32'] and len(j['providers'])==3 and len(j['rows'])>100000 and len(j['spanRows'])>20000 and len(j['providerQueries'])==612 and None in j['texts']
 provider_code=''
 for index,provider in enumerate(j['providers']):
  setters=[('NegativeSign','negativeSign'),('PositiveSign','positiveSign'),('NumberDecimalSeparator','numberDecimal'),('NumberGroupSeparator','numberGroup'),('CurrencySymbol','currencySymbol'),('CurrencyDecimalSeparator','currencyDecimal'),('CurrencyGroupSeparator','currencyGroup')]
  provider_code+='PROVIDERS['+str(index)+']=new NumberFormatInfo();'+''.join('PROVIDERS['+str(index)+'].set_'+name+'('+json.dumps(provider[key])+');' for name,key in setters)+'PROVIDERS['+str(index)+'].set_NumberNegativePattern('+str(provider['numberNegativePattern'])+');'
 total=0
 for type_index,full_name in enumerate(j['types']):
  owner=full_name.split('.')[-1];work=Path('D:/AI/Implementation/dotj Frameworks/verification/integer-style-parsing')/owner;work.mkdir(parents=True,exist_ok=True);tsv=work/'cases.tsv';rows=[];groups=0
  for index,row in enumerate(j['rows']):
   if row[0]!=type_index:continue
   rows.append('\t'.join([str(index),str(row[2]),str(row[3]),b64(j['texts'][row[1]]),outcome(row[4]),outcome(row[5]),outcome(row[6]),'S','','','','','']));groups+=2+(row[6] is not None)
  for index,row in enumerate(j['spanRows']):
   if row[0]!=type_index:continue
   rows.append('\t'.join(['P'+str(index),str(row[2]),str(row[3]),b64(j['texts'][row[1]]),outcome(row[5]),outcome(row[6]),'!','C' if row[4]==0 else 'B','','','','','']));groups+=2
  for index,row in enumerate(j['providerQueries']):
   if row[0]!=type_index:continue
   kind='S' if len(row)==10 else ('C' if row[10]==0 else 'B')
   rows.append('\t'.join(['Q'+str(index),str(row[2]),'0',b64(row[1]),outcome(row[4]),outcome(row[5]),'!',kind,str(row[6]),b64(row[7]),str(row[8]),b64(row[9]),row[3]]));groups+=2
  tsv.write_text('\n'.join(rows)+'\n',encoding='ascii');assert len(rows)>25000
  name=owner+'StyleParseProbe';source=work/(name+'.java')
  source.write_text(JAVA.replace('CLASSNAME',name).replace('PROVIDERSOURCE',provider_code).replace('OWNER',owner),encoding='utf-8')
  subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),name,str(tsv)],check=True);total+=groups
 record=dict(schemaVersion=1,casesPassed=total,nativeStringRows=len(j['rows']),nativeSpanRows=len(j['spanRows']),providerControls=len(j['providerQueries']),oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='BOUNDED_INTEGER_STYLE_PARSE_PASS; ADDITIONAL_CULTURES_GENERIC_INTERFACES_CLR_ABI_AND_ACCEPTANCE_OPEN')
 (EVIDENCE/'integer-style-parsing-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(f'PASS integer String/Char/UTF-8 styles: {total} groups')
JAVA='''import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.ReadOnlySpan;import System.Exception;import System.ArgumentException;import System.FormatException;import System.OverflowException;import System.Type;import System.IFormatProvider;import System.Globalization.NumberStyles;import System.Globalization.NumberFormatInfo;
import java.nio.file.Files;import java.nio.file.Path;import java.nio.charset.StandardCharsets;import java.util.Base64;
class CLASSNAME {
static final NumberFormatInfo[] PROVIDERS=new NumberFormatInfo[3];static{PROVIDERSOURCE}
static final class ProbeProvider implements IFormatProvider{final String kind;int calls;Type requested;ProbeProvider(String kind){this.kind=kind;}public Object GetFormat(Type type){calls++;requested=type;if(kind.equals("Format"))throw new FormatException("provider failure");if(kind.equals("Overflow"))throw new OverflowException("provider failure");return null;}}
static String decode(String value){return value.equals("!")?null:new String(Base64.getDecoder().decode(value),StandardCharsets.UTF_8);}
static String encode(String value){return value==null?"!":Base64.getEncoder().encodeToString(value.getBytes(StandardCharsets.UTF_8));}
static String run(int operation,String text,NumberStyles style,IFormatProvider provider,String kind){OWNER[] result={new OWNER(99)};
try{
if(kind.equals("C")){char[] core=(text==null?"":text).toCharArray();char[] buffer=new char[core.length+5];java.util.Arrays.fill(buffer,'#');java.lang.System.arraycopy(core,0,buffer,3,core.length);ReadOnlySpan<Character> span=ReadOnlySpan.OfChars(buffer,3,core.length);if(operation==0)return "V:"+OWNER.Parse(span,style,provider).get_Value();boolean ok=OWNER.TryParse(span,style,provider,result);return "T:"+ok+":"+result[0].get_Value();}
if(kind.equals("B")){byte[] core=(text==null?"":text).getBytes(StandardCharsets.UTF_8);byte[] buffer=new byte[core.length+5];java.util.Arrays.fill(buffer,(byte)35);java.lang.System.arraycopy(core,0,buffer,3,core.length);ReadOnlySpan<Byte> span=ReadOnlySpan.OfUtf8Bytes(buffer,3,core.length);if(operation==0)return "V:"+OWNER.Parse(span,style,provider).get_Value();boolean ok=OWNER.TryParse(span,style,provider,result);return "T:"+ok+":"+result[0].get_Value();}
if(operation==0)return "V:"+OWNER.Parse(text,style,provider).get_Value();
if(operation==1){boolean ok=OWNER.TryParse(text,style,provider,result);return "T:"+ok+":"+result[0].get_Value();}
return "V:"+OWNER.Parse(text,style).get_Value();}
catch(Exception error){return "E:"+error.getClass().getName()+":"+error.get_HResult()+":"+encode(error instanceof ArgumentException argument?argument.get_ParamName():null)+(operation==1?":"+result[0].get_Value():"");}}
public static void main(String[] args)throws java.lang.Exception{
int cases=0,failures=0;
try(java.io.BufferedReader reader=Files.newBufferedReader(Path.of(args[0]),StandardCharsets.US_ASCII)){
String line;while((line=reader.readLine())!=null){String[] row=line.split("\\t",-1);NumberStyles style=NumberStyles.FromInt32(Integer.parseInt(row[1]));String text=decode(row[3]);boolean query=!row[12].isEmpty();ProbeProvider probe=query?new ProbeProvider(row[12]):null;IFormatProvider provider=query?probe:PROVIDERS[Integer.parseInt(row[2])];
for(int operation=0;operation<3;operation++){String expected=row[operation+4];if(expected.equals("!"))continue;cases++;if(query){probe.calls=0;probe.requested=null;}String actual=run(operation,text,style,provider,row[7]);boolean matches=actual.equals(expected);
if(query){int field=operation==0?8:10;String requested=decode(row[field+1]);matches=matches&&probe.calls==Integer.parseInt(row[field])&&probe.requested==(requested==null?null:Type.GetType(requested));}
if(!matches){failures++;if(failures<=20)java.lang.System.out.println("MISMATCH id="+row[0]+" style="+row[1]+" provider="+row[2]+" text="+row[3]+" kind="+row[7]+" op="+operation+" expected="+expected+" actual="+actual+(query?" calls="+probe.calls:"")+" probe="+row[12]);}
}
}
}
java.lang.System.out.println("RESULT OWNER cases="+cases+" failures="+failures);if(failures!=0)throw new AssertionError(failures+" native mismatches");
}
}
'''
if __name__=='__main__':main()
