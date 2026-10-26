"""Compare existing ICloneable registration, selected Type relationships and typed dispatch."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'numberformatinfo-clone-interface-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-numberformatinfo-clone-interface-contract.ps1').read_bytes()).hexdigest();planPath=Path(__file__).with_name('numberformatinfo-clone-interface-plan-v1.json');assert j['planSha256']==hashlib.sha256(planPath.read_bytes()).hexdigest();plan=json.loads(planPath.read_text());props=plan['properties'];assert len(props)==22 and len(plan['queries'])==24 and len(plan['types'])==7
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Globalization/NumberFormatInfo.cs')).hexdigest()=='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a'
 interfaces=['System.IFormatProvider','System.ICloneable'];assert j['interfaces']==j['interfacesAfterMutation']==interfaces and j['distinctInterfaces'];vectors=['I\t'+','.join(interfaces)+'\t1\t'+','.join(interfaces)];seen=set()
 for row in j['lookups']:
  key=(row['query'],row['ignoreCase']);assert 0<=key[0]<24 and key not in seen;seen.add(key);name=plan['queries'][key[0]];r=row['result']
  if name is None:assert not r['ok'] and r['exception']=='System.ArgumentNullException' and r['paramName']=='fullname';result='|'.join(['ERR',r['exception'],csv(r['messageUnits']),str(r['hResult']),csv([ord(c) for c in r['paramName']]),'~'])
  else:
   assert r['ok'];namespace,_,short=name.rpartition('.');expected=None
   if not namespace or namespace=='System':
    for value in interfaces:
     target=value.rsplit('.',1)[-1]
     if short==target or key[1] and name.isascii() and short.lower()==target.lower():expected=value
   assert r['name']==expected;result='OK|'+(expected or '~')
  vectors.append('\t'.join(['L',csv(None if name is None else [ord(c) for c in name]),str(int(key[1])),result]))
 assert seen=={(q,i) for q in range(24) for i in (False,True)};seen=set();parents={'System.Globalization.NumberFormatInfo':{'System.IFormatProvider','System.ICloneable','System.Object'},'System.ICloneable':{'System.Object'},'System.IFormatProvider':{'System.Object'},'System.Object':set(),'System.Int32':{'System.Object'},'System.Text.Encoding':{'System.Object','System.ICloneable'},'System.Text.UTF8Encoding':{'System.Object','System.Text.Encoding','System.ICloneable'}};matches=0
 for row in j['assignments']:
  key=(row['target'],row['source']);assert key[0] in plan['types'] and key[1] in plan['types'] and key not in seen;seen.add(key);assert row['assignable']==(key[0]==key[1] or key[0] in parents[key[1]]);matches+=int(row['assignable']);vectors.append('\t'.join(['A',key[0],key[1],str(int(row['assignable']))]))
 assert len(seen)==49 and matches==18;seed={s['name']:s['seed'] for s in props};modes=set()
 def snapshot(value):return str(int(value['readOnly']))+'|'+'|'.join(str(value['values'][s['name']]) if s['kind']=='int' else csv(value['values'][s['name']]) for s in props)
 for row in j['clones']:
  mode=row['mode'];assert mode in ('mutable','readonly','clone') and mode not in modes;modes.add(mode);assert row['before']==dict(readOnly=mode=='readonly',values=seed) and row['clone']==dict(readOnly=False,values=seed) and row['distinct'] and row['isInstance'] and row['cloneIsInstance'] and row['cloneType']=='System.Globalization.NumberFormatInfo';vectors.append('\t'.join(['C',mode,snapshot(row['before']),snapshot(row['clone']),'1','1','1',row['cloneType']]))
 assert len(modes)==3 and len(vectors)==101
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/numberformatinfo-clone-interface');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('numberformatinfo-clone-interface-probe.java');source=work/'NumberFormatInfoCloneInterfaceProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'NumberFormatInfoCloneInterfaceProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'lookups=48 assignments=49 clones=3 groups=118' in r.stdout
 record=dict(schemaVersion=1,casesPassed=118,nativeCases=101,interfaceLookups=48,assignments=49,typedClones=3,sourceSha256='fd3c0ea9e8a880122bde525501a81e31db55e8a060cbbf9717cf51cbb17fb57a',planSha256=j['planSha256'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_NUMBERFORMATINFO_ICLONEABLE_DISPATCH_AND_TYPE_RELATIONSHIPS_ONLY; OTHER_IMPLEMENTORS_ARRAY_STRING_BOXING_FULL_METADATA_CULTURE_SERIALIZATION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'numberformatinfo-clone-interface-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS represented NumberFormatInfo clone interface; task acceptance remains open')
if __name__=='__main__':main()
