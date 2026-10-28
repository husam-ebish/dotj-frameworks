from pathlib import Path
import argparse,hashlib,json,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[3];E=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args();name='exception-serialization-duplicate-field-order'
 if a.jar is None:a.jar=ROOT/json.loads((E/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=E/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));plan=Path(__file__).with_name(name+'-plan-v1.json');q=json.loads(plan.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['planSha256']==hashlib.sha256(plan.read_bytes()).hexdigest() and j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert '_source ??= Source' in z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Exception.cs').decode('utf-8')
 def csv(x):return '~' if x is None else ','.join(map(str,x))
 assert j['nullInputControls']==2106
 expected={(i,a) for i in range(2106) for a in [-1,0,1]};seen=set();vectors=[]
 for row in j['rows']:
  key=(row['index'],row['attempt']);assert key in expected and key not in seen;seen.add(key);assert row['otherCalls']==0
  values=[str(row['index']),csv(q['texts'][row['sourceIndex']]),csv(q['texts'][row['helpIndex']]),csv(q['texts'][row['messageIndex']]),row['mode'],str(row['attempt']),str(row['contextFlag']),str(row['sourceCalls']),str(row['otherCalls']),str(row['memberCount']),row['exception'],*[csv(row[k]) for k in ['sourceUnits','helpUnits','messageUnits','stackUnits']],str(row['dataNull']).lower(),row['entryNames'],csv(row['errorMessageUnits']),str(row['errorHResult']),row['collisionName']];vectors.append('\t'.join(values))
 assert seen==expected and len(seen)==6318
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/exception-serialization-duplicate-field-order');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'ExceptionSerializationDuplicateFieldOrderProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'ExceptionSerializationDuplicateFieldOrderProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'calls=6318 groups=75816' in r.stdout
 record=dict(schemaVersion=1,casesPassed=75816,nativeCalls=6318,javaFacadeCalls=6318,limitation='selected unthrown Exception getter/serialization boundaries only; formatter restoration, thrown/remote stacks and acceptance remain open',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=q['qualification']);(E/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
