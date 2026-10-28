from pathlib import Path
import argparse,hashlib,json,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[3];E=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args();name='default-member-info-equality'
 if a.jar is None:a.jar=ROOT/json.loads((E/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=E/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));plan=Path(__file__).with_name(name+'-plan-v1.json');q=json.loads(plan.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['planSha256']==hashlib.sha256(plan.read_bytes()).hexdigest() and j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert 'override bool Equals' in z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/coreclr/System.Private.CoreLib/src/System/Reflection/RuntimePropertyInfo.cs').decode('utf-8')
 assert j['memberCount']==8 and j['apiCalls']==172;assert len(j['arrays'])==12 and {r['owner'] for r in j['arrays']}==set(q['owners']);vectors=[]
 for row in j['arrays']:vectors.append('\t'.join(['A',row['owner'],str(row['count']),str(row['sameArray']).lower(),str(row['defensive']).lower()]))
 assert len(j['metadata'])==8 and {r['index'] for r in j['metadata']}==set(range(8))
 for row in j['metadata']:vectors.append('\t'.join(['M',str(row['index']),row['name'],str(row['memberType']),row['declaringType'],row['reflectedType']]))
 expected={(l,r) for l in range(8) for r in range(11)};seen=set()
 for row in j['rows']:
  key=(row['left'],row['right']);assert key in expected and key not in seen;seen.add(key);vectors.append('\t'.join(['E',str(row['left']),str(row['right']),str(row['equal']).lower(),str(row['reference']).lower(),str(row['equalHash']).lower()]))
 assert seen==expected and len(j['hashes'])==8 and {r['left'] for r in j['hashes']}==set(range(8))
 for row in j['hashes']:vectors.append('\t'.join(['H',str(row['left']),str(row['stable']).lower()]))
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/default-member-info-equality');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'DefaultMemberInfoEqualityProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'DefaultMemberInfoEqualityProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'calls=172 groups=340' in r.stdout
 record=dict(schemaVersion=1,casesPassed=340,nativeCalls=172,javaFacadeCalls=172,limitation='selected String/List default property and empty-default descriptors only; PropertyInfo APIs, other members, numeric hash parity and acceptance remain open',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=q['qualification']);(E/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
