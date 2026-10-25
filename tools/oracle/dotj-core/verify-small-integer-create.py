import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'small-integer-create-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-small-integer-create-contract.ps1').read_bytes()).hexdigest() and len(j['sourceTypes'])==15 and len(j['sources'])==923 and len(j['rows'])==11076
 runtime=json.loads((EVIDENCE/'runtime-artifact-v10.0.12-win-x64.json').read_text(encoding='utf-8'))
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/dotnet-runtime-10.0.12-win-x64.zip');archive_hash=hashlib.sha512(archive.read_bytes()).hexdigest();assert archive_hash==runtime['releaseMetadata']['runtimeArchiveSha512']
 member='shared/Microsoft.NETCore.App/10.0.12/System.Runtime.Numerics.dll'
 with zipfile.ZipFile(archive) as bundle:numerics_hash=hashlib.sha256(bundle.read(member)).hexdigest()
 assert numerics_hash==j['numericsAssemblySha256']==hashlib.sha256((Path('D:/AI/Implementation/dotj Frameworks/toolchains/dotnet')/member).read_bytes()).hexdigest()
 expressions=[]
 for source in j['sources']:
  kind=source['type'].split('.')[-1];text=source['text']
  if kind in ['SByte','Byte','UInt16','UInt32','Int32']:expression='new '+kind+'('+text+('L' if kind=='UInt32' else '')+')'
  elif kind=='Int16':expression='Short.valueOf('+json.dumps(text)+')'
  elif kind=='Int64':expression='Long.valueOf('+json.dumps(text)+')'
  elif kind in ['UInt64','Int128','UInt128','BigInteger']:expression='new BigInteger('+json.dumps(text)+')'
  elif kind in ['Single','Half']:expression='Float.intBitsToFloat((int)Long.parseUnsignedLong('+json.dumps(source['bits'])+',16))'
  elif kind=='Double':expression='Double.longBitsToDouble(Long.parseUnsignedLong('+json.dumps(source['bits'])+',16))'
  elif kind=='Decimal':expression='Decimal.Parse('+json.dumps(text)+',(IFormatProvider)null)'
  else:raise AssertionError(kind)
  expressions.append(expression)
 total=0
 for target_index,full_name in enumerate(j['targets']):
  owner=full_name.split('.')[-1];work=Path('D:/AI/Implementation/dotj Frameworks/verification/small-integer-create')/owner;work.mkdir(parents=True,exist_ok=True);cases=[]
  for _,source_index,method,result in [r for r in j['rows'] if r[0]==target_index]:
   index=len(cases);expression=owner+'.'+method+'('+expressions[source_index]+')'
   if result[0]=='V':cases.append('{check('+expression+'.get_Value()=='+str(result[1])+'L,'+str(index)+');}')
   else:cases.append('{try{'+expression+';throw new AssertionError("missing conversion error");}catch(Exception expected){check(expected.getClass().getName().equals('+json.dumps(result[1])+') && expected.get_HResult()=='+str(result[2])+','+str(index)+');}}')
  assert len(cases)==2769;total+=len(cases);name=owner+'CreateProbe';source=work/(name+'.java');methods=['static void group'+str(i//15)+'(){\n'+'\n'.join(cases[i:i+15])+'\n}' for i in range(0,len(cases),15)]
  source.write_text('import System.SByte;import System.Byte;import System.UInt16;import System.UInt32;import System.Int32;import System.Decimal;import System.IFormatProvider;import System.Exception;import java.math.BigInteger;\nclass '+name+'{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+'\n'.join(methods)+'\npublic static void main(String[] args){'+''.join('group'+str(i)+'();' for i in range(len(methods)))+'}}',encoding='utf-8')
  subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),name],check=True)
  output=subprocess.run(['javap','-public','-classpath',str(a.jar),full_name],check=True,text=True,capture_output=True).stdout
  for method in ['CreateChecked','CreateSaturating','CreateTruncating']:assert 'public static <TOther> '+full_name+' '+method+'(TOther);' in output
  print(f'PASS {owner} numeric factories: {len(cases)} groups',flush=True)
 record=dict(schemaVersion=1,casesPassed=total,referenceRuntimeArchiveSha512=archive_hash,referenceNumericsSha256=numerics_hash,nativeSourceTypes=j['sourceTypes'],sourceAdapters='Half to Float; Int128/UInt128/UInt64/BigInteger to BigInteger; native generic constraints remain open',oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='BOUNDED_SMALL_INTEGER_FACTORIES_PASS; GENERIC_SOURCE_CONSTRAINTS_VALUE_ABI_AND_ACCEPTANCE_OPEN')
 (EVIDENCE/'small-integer-create-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
