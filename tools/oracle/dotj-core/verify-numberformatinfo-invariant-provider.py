"""Compare represented InvariantInfo cache, immutable defaults, clones and numeric provider use."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
import importlib.util
_hash_spec = importlib.util.spec_from_file_location("dotj_oracle_file_hashes", Path(__file__).with_name("oracle_file_hashes.py"))
_hash_module = importlib.util.module_from_spec(_hash_spec)
_hash_spec.loader.exec_module(_hash_module)
sha256_file = _hash_module.sha256_file
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def encoded(spec,value):return str(value) if spec['kind']=='int' else csv(value)
def outcome(r):
 if r['ok']:return 'OK'
 return '|'.join(['ERR',r['exception'],csv(r['messageUnits']),str(r['hResult']),csv(None if r['paramName'] is None else [ord(c) for c in r['paramName']]),str(r['actualValue']) if r['actualValue'] is not None else '~'])
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'numberformatinfo-invariant-provider-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-numberformatinfo-invariant-provider-contract.ps1').read_bytes()).hexdigest();planPath=Path(__file__).with_name('numberformatinfo-invariant-provider-plan-v1.json');assert j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();plan=json.loads(planPath.read_text());props=plan['properties'];names=[s['name'] for s in props];assert len(props)==len(set(names))==22 and len(plan['formats'])==16 and len(plan['values'])==8
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Globalization/NumberFormatInfo.cs')).hexdigest()=='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a'
 def snapshot(v):assert set(v['values'])==set(names);return str(int(v['readOnly']))+'|'+'|'.join(encoded(s,v['values'][s['name']]) for s in props)
 original=j['snapshot'];assert original['readOnly'] and not j['fresh']['readOnly'] and j['fresh']['values']==original['values'] and len(j['identity'])==64 and all(j['identity']) and j['sameReadOnly'] and j['providerSelf'];assert j['finalSnapshot']==original;vectors=['\t'.join(['I',snapshot(original),snapshot(j['fresh']),'1','1',','.join('1' for _ in range(64))])];seen=set()
 for row in j['clones']:
  name=row['property'];assert name in names and name not in seen;seen.add(name);i=names.index(name);spec=props[i];r=row['readonlyMutation'];assert not r['ok'] and r['exception']=='System.InvalidOperationException' and r['paramName'] is None and r['actualValue'] is None;assert row['before']==dict(readOnly=False,values=original['values']);values=original['values'].copy();values[name]=spec['invariantMutation'];assert row['after']==dict(readOnly=False,values=values) and row['invariantAfter']==original and row['distinct'] and row['providerSelf'];vectors.append('\t'.join(['C',str(i),encoded(spec,spec['invariantMutation']),outcome(r),snapshot(row['before']),snapshot(row['after']),snapshot(row['invariantAfter']),'1','1']))
 assert seen==set(names);seen=set()
 for row in j['formats']:
  key=(row['value'],None if row['formatUnits'] is None else tuple(row['formatUnits']));assert key not in seen;seen.add(key);assert row['result']['ok'];vectors.append('\t'.join(['F',str(row['value']),csv(row['formatUnits']),csv(row['result']['textUnits'])]))
 expected={(v,None if f is None else tuple(map(ord,f))) for v in plan['values'] for f in plan['formats']};assert seen==expected and len(seen)==128;vectors.append('S\t'+snapshot(j['finalSnapshot']));assert len(vectors)==152
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/numberformatinfo-invariant-provider');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('numberformatinfo-invariant-provider-probe.java');source=work/'NumberFormatInfoInvariantProviderProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'NumberFormatInfoInvariantProviderProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'identities=64 clones=22 formats=128 groups=329' in r.stdout
 record=dict(schemaVersion=1,casesPassed=329,nativeCases=152,sequentialIdentities=64,cloneCases=22,formatCases=128,sourceSha256='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='REPRESENTED_INVARIANTINFO_SEQUENTIAL_CACHE_IMMUTABILITY_CLONES_AND_INT32_PROVIDER_ONLY; FIRST_ACCESS_RACES_CURRENT_CULTURE_OTHER_FIELDS_FULL_METADATA_SERIALIZATION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'numberformatinfo-invariant-provider-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS represented InvariantInfo; full culture and task acceptance remain open')
if __name__=='__main__':main()
