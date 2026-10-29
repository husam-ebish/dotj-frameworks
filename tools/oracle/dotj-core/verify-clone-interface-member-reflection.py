"""Compare Clone named/flagged/typed lookup, member filtering and full selected descriptors."""
import argparse,hashlib,json,subprocess,zipfile,collections
from pathlib import Path
import importlib.util
_hash_spec = importlib.util.spec_from_file_location("dotj_oracle_file_hashes", Path(__file__).with_name("oracle_file_hashes.py"))
_hash_module = importlib.util.module_from_spec(_hash_spec)
_hash_spec.loader.exec_module(_hash_module)
sha256_file = _hash_module.sha256_file
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
MAIN=['name','declaringType','reflectedType','returnType','text','memberType','public','private','family','assembly','familyAndAssembly','familyOrAssembly','static','abstract','virtual','final','specialName','constructor','hideBySig','callingConvention','securityCritical','securitySafeCritical','securityTransparent','methodImpl','bodyNull','genericMethod','genericDefinition','constructedGeneric','containsGeneric','genericCount','parameterCount','baseName','baseOwner']
RETURN=['nameUnits','position','type','optional','hasDefault','defaultKind','rawDefaultKind','isIn','isOut','isRetval','isLcid','attributes','optionalModifiers','requiredModifiers','memberName','text']
def csv(v):return '~' if v is None else ','.join(map(str,v))
def scalar(v):return str(int(v)) if isinstance(v,bool) else str(v)
def descriptor(m):
 if m is None:return '~'
 return '|'.join([scalar(m[k]) for k in MAIN]+[csv(m['returnParameter'][k]) if k=='nameUnits' else scalar(m['returnParameter'][k]) for k in RETURN])
def result(r):
 if not r['ok']:return '|'.join(['ERR',r['exception'],csv(r['messageUnits']),str(r['hResult']),csv(None if r['paramName'] is None else [ord(c) for c in r['paramName']])])
 return 'OK|'+r['kind']+'|'+(descriptor(r['value']) if r['kind']=='method' else ';'.join(descriptor(m) for m in r['value']))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'clone-interface-member-reflection-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678' and j['culture']=='Invariant';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-clone-interface-member-reflection-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert sha256_file(archive)=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:source=z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/ICloneable.cs');assert b'object Clone();' in source
 names=[None,'','Clone','clone','CLONE','ClOnE','Missing','Clone ',' clone','Clon\u0435'];names=[None if n is None else tuple(map(ord,n)) for n in names];flags=[0,1,2,4,8,16,32,64,20,21,22,23,28,36,52,60,84,276,65556,-1];types=['empty','object','int','null','nullElement','twoObjects'];masks=[0,4,8,24,191];assert j['flags']==flags and j['typeProfiles']==types and j['memberMasks']==masks
 expected=set()
 for name in names:
  for route in ('named','member'):expected.add((route,name,20,'empty',8))
  for t in types:expected.add(('typed',name,20,t,8))
  for f in flags:
   for route in ('flagged','flaggedMember'):expected.add((route,name,f,'empty',8))
   for t in types:expected.add(('flaggedTyped',name,f,t,8))
   for mask in masks:expected.add(('filteredMember',name,f,'empty',mask))
 for route in ('members','methods','defaults'):expected.add((route,None,20,'empty',8))
 for f in flags:
  for route in ('flaggedMembers','flaggedMethods'):expected.add((route,None,f,'empty',8))
 seen=set();vectors=[];errors=0;found=0;golden=None;routes=collections.Counter()
 for row in j['rows']:
  key=(row['route'],None if row['nameUnits'] is None else tuple(row['nameUnits']),row['flags'],row['types'],row['memberMask']);assert key in expected and key not in seen;seen.add(key);routes[key[0]]+=1;r=row['result']
  if not r['ok']:assert r['exception']=='System.ArgumentNullException' and r['paramName'] in ('name','types');errors+=1
  else:
   values=([r['value']] if r['value'] is not None else []) if r['kind']=='method' else r['value'];assert len(values)<=1
   for m in values:
    assert set(m)==set(MAIN+['returnParameter']) and set(m['returnParameter'])==set(RETURN);assert m['name']==m['baseName']=='Clone' and m['declaringType']==m['reflectedType']==m['baseOwner']=='System.ICloneable' and m['returnType']=='System.Object' and m['text']=='System.Object Clone()' and m['memberType']==8 and m['parameterCount']==m['genericCount']==0 and m['callingConvention']==33 and m['methodImpl']==0
    assert all(m[k] for k in ('public','abstract','virtual','hideBySig','securityCritical','bodyNull')) and all(not m[k] for k in ('private','family','assembly','familyAndAssembly','familyOrAssembly','static','final','specialName','constructor','securitySafeCritical','securityTransparent','genericMethod','genericDefinition','constructedGeneric','containsGeneric'));ret=m['returnParameter'];assert ret['nameUnits'] is None and ret['position']==-1 and ret['type']==ret['text']=='System.Object' and ret['defaultKind']==ret['rawDefaultKind']=='DBNull' and ret['memberName']=='Clone';assert all(not ret[k] for k in ('optional','hasDefault','isIn','isOut','isRetval','isLcid','attributes','optionalModifiers','requiredModifiers'));golden=golden or m;assert m==golden;found+=1
  vectors.append('\t'.join([row['route'],csv(row['nameUnits']),str(row['flags']),row['types'],str(row['memberMask']),result(r)]))
 assert seen==expected and len(vectors)==2723 and errors==646 and found>0
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/clone-interface-member-reflection');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('clone-interface-member-reflection-probe.java');sourceFile=work/'CloneInterfaceMemberReflectionProbe.java';sourceFile.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(sourceFile)],check=True);r=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'CloneInterfaceMemberReflectionProbe',str(data)],capture_output=True,text=True,timeout=120);print(r.stdout,end='');print(r.stderr,end='');r.check_returncode();assert 'cases=2723 groups=2723' in r.stdout
 record=dict(schemaVersion=1,casesPassed=2723,nativeCases=2723,nullFailures=errors,foundDescriptors=found,routes=dict(routes),sourceSha256=hashlib.sha256(source).hexdigest(),oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_ICLONEABLE_PARAMETERLESS_CLONE_LOOKUP_AND_DESCRIPTOR_METADATA_ONLY; INVOCATION_HANDLES_TOKENS_CUSTOM_ATTRIBUTES_FULL_REFLECTION_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'clone-interface-member-reflection-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS selected Clone reflection; full reflection and task acceptance remain open')
if __name__=='__main__':main()
