from pathlib import Path
import argparse,hashlib,json,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[3];E=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args();name='type-generic-construction-validation'
 if a.jar is None:a.jar=ROOT/json.loads((E/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=E/(name+'-contract-v10.0.12.json');j=json.loads(path.read_text(encoding='utf-8'));plan=Path(__file__).with_name(name+'-plan-v1.json');q=json.loads(plan.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['planSha256']==hashlib.sha256(plan.read_bytes()).hexdigest() and j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-'+name+'-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert 'where T : struct' in z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Nullable.cs').decode('utf-8')
 with zipfile.ZipFile(archive) as z:assert 'genericParameters.Length != typeArguments.Length' in z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/coreclr/System.Private.CoreLib/src/System/RuntimeType.CoreCLR.cs').decode('utf-8')
 expected={x['key']:x for x in q['cases']};seen=set();vectors=[];assert j['nullInputControls']==95
 def token(value):return '~' if value is None else str(value).lower() if isinstance(value,bool) else str(value)
 def units(value):return '~' if value is None else ','.join(map(str,value))
 for row in j['rows']:
  key=row['key'];assert key in expected and key not in seen;seen.add(key);args=expected[key]['arguments'];argument='#' if args is None else args if isinstance(args,str) else ';'.join('~' if a is None else a for a in args);values=[units(row[f]) if f.endswith('Units') else token(row[f]) for f in q['fields']];vectors.append('\t'.join([key,expected[key]['receiver'],argument,*values]));assert row['inputUnchanged']
 assert seen==set(expected) and len(seen)==380
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/type-generic-construction-validation');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name(name+'-probe.java');source=work/'TypeGenericConstructionValidationProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'TypeGenericConstructionValidationProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'calls=380 groups=6840' in r.stdout
 record=dict(schemaVersion=1,casesPassed=6840,nativeCalls=380,javaFacadeCalls=380,limitation='selected runtime MakeGenericType validation and construction metadata only; inner exceptions, non-runtime tokens, arbitrary constraints and acceptance remain open',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=q['qualification']);(E/(name+'-differential-v1.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':main()
