import json,subprocess,hashlib
from pathlib import Path
import argparse
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
b=Path('D:/AI/Implementation/dotj Frameworks');path=EVIDENCE/'int32-format-classification-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-int32-format-classification-contract.ps1').read_bytes()).hexdigest()
assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
assert j['typeName']=='System.Int32' and j['valueCount']==21 and len(j['cases'])==1848
cases=[]
for row in j['cases']:
 fmt='(String)null' if row['format'] is None else json.dumps(row['format']);provider='CUSTOM' if row['provider']=='Custom' else 'null'
 for expression,key in [(f'value.ToString({fmt},{provider})','direct'),(f'((IFormattable)value).ToString({fmt},{provider})','interface'),(f'value.ToString({fmt})','single')]:
  result=row[key];index=len(cases)
  if 'text' in result:check=f'check({expression}.equals({json.dumps(result["text"])}),{index});'
  else:check=f'try{{{expression};throw new AssertionError("missing format error {index}");}}catch(FormatException expected){{check(expected.get_HResult()=={result["hResult"]},{index});}}'
  cases.append('{Int32 value=new Int32('+str(row['value'])+');'+check+'}')
w=b/'verification/int32-format-classification-prototype';w.mkdir(exist_ok=True);src=w/'Int32FormatProbe.java';methods=['static void group'+str(i//15)+'(){'+''.join(cases[i:i+15])+'}' for i in range(0,len(cases),15)]
src.write_text('import System.Int32;import System.IFormattable;import System.FormatException;import System.Globalization.NumberFormatInfo;class Int32FormatProbe{static final NumberFormatInfo CUSTOM=new NumberFormatInfo();static{CUSTOM.set_NegativeSign("~");CUSTOM.set_PositiveSign("p");CUSTOM.set_NumberDecimalSeparator(":");CUSTOM.set_NumberGroupSeparator("_");CUSTOM.set_NumberDecimalDigits(3);}static void check(boolean ok,int index){if(!ok)throw new AssertionError("case "+index);}'+'\n'.join(methods)+'public static void main(String[] args){'+''.join('group'+str(i)+'();' for i in range(len(methods)))+'}}',encoding='utf-8')
subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(w),str(src)],check=True)
subprocess.run(['java','-cp',str(a.jar)+';'+str(w),'Int32FormatProbe'],check=True)
assert len(cases)==5544
record=dict(oracleEvidence=path.name,schemaVersion=1,casesPassed=len(cases),oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='BOUNDED_INT32_FORMAT_CLASSIFICATION_PASS; OTHER_FORMATS_PRECISIONS_CULTURES_AND_RELEASE_OPEN')
(EVIDENCE/'int32-format-classification-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n')
print(f'PASS Int32 format classification: {len(cases)} groups')
