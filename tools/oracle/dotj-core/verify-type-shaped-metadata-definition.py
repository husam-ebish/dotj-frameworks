from pathlib import Path
import argparse,hashlib,json,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[3];E=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args();name='type-shaped-metadata-definition'
 if a.jar is None:a.jar=ROOT/json.loads((E/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=E/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));plan=Path(__file__).with_name(name+'-plan-v1.json');q=json.loads(plan.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['planSha256']==hashlib.sha256(plan.read_bytes()).hexdigest() and j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:
  s=z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/coreclr/System.Private.CoreLib/src/System/Reflection/MemberInfo.Internal.cs').decode('utf-8');assert 'MetadataToken != other.MetadataToken' in s and 'Module.Equals(other.Module)' in s
 def csv(x):return '~' if x is None else ','.join(map(str,x))
 assert j['typeCount']==154 and len(j['diagnostics'])==154;diagnostics=j['diagnostics'];assert {d['index'] for d in diagnostics}==set(range(154));vectors=[]
 for base in q['bases']:
  for shape in q['shapes']:vectors.append('\t'.join(['T',base,shape]))
 for d in diagnostics:
  if d['hasElement']:assert d['token']==0x02000000 and d['module']=='System.Private.CoreLib.dll'
 expected={(l,r) for l in range(154) for r in range(155)};seen=set()
 for row in j['rows']:
  key=(row['left'],row['right']);assert key in expected and key not in seen;seen.add(key)
  if row['right']<154:assert row['same']==(diagnostics[row['left']]['token']==diagnostics[row['right']]['token'] and diagnostics[row['left']]['module']==diagnostics[row['right']]['module'])
  vectors.append('\t'.join(['E',str(row['left']),str(row['right']),'~' if row['same'] is None else str(row['same']).lower(),row['exception'],csv(row['messageUnits']),str(row['hResult']),csv(row['paramUnits']),str(row['equal']).lower()]))
 assert seen==expected and len(seen)==23870
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/type-shaped-metadata-definition');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'TypeShapedMetadataDefinitionProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'TypeShapedMetadataDefinitionProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'calls=47740 groups=143220' in r.stdout
 record=dict(schemaVersion=1,casesPassed=143220,nativeCalls=47740,javaFacadeCalls=47740,limitation='selected CoreLib named/generic/array/pointer/byref definition relations only; public module/token APIs, non-CoreLib loader policy and acceptance remain open',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=q['qualification']);(E/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
