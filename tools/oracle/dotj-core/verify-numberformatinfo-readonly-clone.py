"""Compare represented read-only/clone API, validation precedence and snapshot isolation."""
import argparse,hashlib,json,subprocess,zipfile,collections,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def encoded(spec,value):return '~' if value is None else str(value) if spec['kind']=='int' else csv(value)
def outcome(r):
 if r['ok']:return 'OK'
 return '|'.join(['ERR',r['exception'],csv(r['messageUnits']),str(r['hResult']),csv(None if r['paramName'] is None else [ord(c) for c in r['paramName']]),str(r['actualValue']) if r['actualValue'] is not None else '~'])
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'numberformatinfo-readonly-clone-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-numberformatinfo-readonly-clone-contract.ps1').read_bytes()).hexdigest();planPath=Path(__file__).with_name('numberformatinfo-readonly-clone-plan-v1.json');assert j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();plan=json.loads(planPath.read_text());props=plan['properties'];names=[s['name'] for s in props];assert len(props)==len(set(names))==22 and plan['setterCases']==870 and plan['cloneCases']==22
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115';root='runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/'
 with zipfile.ZipFile(archive) as z:
  assert hashlib.sha256(z.read(root+'System/Globalization/NumberFormatInfo.cs')).hexdigest()=='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a';resource=z.read(root+'Resources/Strings.resx');resources={x.attrib['name']:x.findtext('value') for x in ET.fromstring(resource).findall('data')};assert resources['InvalidOperation_ReadOnly']=='Instance is read-only.'
 seed={s['name']:s['seed'] for s in props}
 def snapshot(value):assert set(value)=={'readOnly','values'} and set(value['values'])==set(names);return str(int(value['readOnly']))+'|'+'|'.join(encoded(s,value['values'][s['name']]) for s in props)
 def state(values,readonly=False):return dict(readOnly=readonly,values=values)
 expected={(s['name'],i,m) for s in props for i in range(len(s['inputs'])) for m in ('mutable','readonly','clone')};seen=set();vectors=[];counts=collections.Counter()
 nullFirst={'NegativeSign','PositiveSign','CurrencySymbol','PercentSymbol','PerMilleSymbol'}
 for row in j['rows']:
  key=(row['property'],row['profile'],row['mode']);assert key in expected and key not in seen;seen.add(key);index=names.index(key[0]);spec=props[index];value=spec['inputs'][key[1]];ro=key[2]=='readonly';assert row['before']==state(seed,ro);r=row['result'];error=None
  if spec['kind']=='int':error='System.ArgumentOutOfRangeException' if not 0<=value<=spec['maximum'] else 'System.InvalidOperationException' if ro else None
  elif spec['kind']=='array':error='System.ArgumentNullException' if value is None else 'System.InvalidOperationException' if ro else 'System.ArgumentException' if any(v<0 or v>9 or (v==0 and i!=len(value)-1) for i,v in enumerate(value)) else None
  else:error='System.ArgumentNullException' if value is None and (not ro or key[0] in nullFirst) else 'System.InvalidOperationException' if ro else 'System.ArgumentException' if not value and key[0].endswith('DecimalSeparator') else None
  assert r['ok']==(error is None);counts[error or 'OK']+=1;after=seed.copy()
  if error is None:after[key[0]]=value
  else:
   assert r['exception']==error and r['paramName']==(None if error=='System.InvalidOperationException' else 'value')
   assert r['actualValue']==(value if error=='System.ArgumentOutOfRangeException' else None)
  assert row['after']==state(after,ro) and row['originalAfter']==state(after if key[2]=='mutable' else seed);assert row['targetIsOriginal']==(key[2]=='mutable') and row['providerSelf'] and row['providerNull'] and row['providerOther']
  vectors.append('\t'.join(['S',str(index),encoded(spec,value),key[2],snapshot(row['before']),outcome(r),snapshot(row['after']),snapshot(row['originalAfter']),str(int(row['targetIsOriginal'])),str(int(row['providerSelf'])),str(int(row['providerNull'])),str(int(row['providerOther']))]))
 assert seen==expected and len(seen)==870 and dict(counts)=={'OK':332,'System.ArgumentOutOfRangeException':258,'System.InvalidOperationException':196,'System.ArgumentException':48,'System.ArgumentNullException':36}
 cloneNames=set()
 for row in j['clones']:
  name=row['property'];assert name in names and name not in cloneNames;cloneNames.add(name);index=names.index(name);spec=props[index];before=[state(seed),state(seed,True),state(seed),state(seed)];assert row['before']==before and row['identity']==[True]*5 and row['cloneType']=='System.Globalization.NumberFormatInfo';original=seed.copy();original[name]=spec['originalMutation'];afterOriginal=[state(original),state(seed,True),state(seed),state(seed)];assert row['afterOriginal']==afterOriginal;clone=seed.copy();clone[name]=spec['cloneMutation'];assert row['afterClone']==[state(original),state(seed,True),state(seed),state(clone)]
  vectors.append('\t'.join(['C',str(index),','.join(str(int(v)) for v in row['identity']),*[snapshot(x) for x in row['before']],*[snapshot(x) for x in row['afterOriginal']],*[snapshot(x) for x in row['afterClone']],row['cloneType'],encoded(spec,spec['originalMutation']),encoded(spec,spec['cloneMutation'])]))
 assert cloneNames==set(names);assert not j['nullFactory']['ok'] and j['nullFactory']['exception']=='System.ArgumentNullException' and j['nullFactory']['paramName']=='nfi';vectors.append('F\t'+outcome(j['nullFactory']));assert len(vectors)==893
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/numberformatinfo-readonly-clone');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('numberformatinfo-readonly-clone-probe.java');source=work/'NumberFormatInfoReadonlyCloneProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-Xmaxerrs','3','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'NumberFormatInfoReadonlyCloneProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'setters=870 clones=22 factories=1 groups=7269' in r.stdout
 record=dict(schemaVersion=1,casesPassed=7269,nativeCases=893,setterCases=870,cloneCases=22,representedProperties=22,sourceSha256='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a',resourceSha256=hashlib.sha256(resource).hexdigest(),planSha256=j['planSha256'],outcomes=dict(counts),oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='REPRESENTED_NUMBERFORMATINFO_READONLY_CLONE_PUBLIC_BEHAVIOR_ONLY; ICLONEABLE_INTERFACE_FULL_METADATA_OTHER_FIELDS_CULTURE_SERIALIZATION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'numberformatinfo-readonly-clone-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS represented NumberFormatInfo readonly/clone; interface and task acceptance remain open')
if __name__=='__main__':main()
