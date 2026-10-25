"""Validate a pinned UTF-16 reference packet and explicit implementation plan.

This check does not qualify a Java UnicodeEncoding implementation.
"""
import argparse,copy,hashlib,json,os,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
CORE='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
ARCHIVE='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
SOURCE='b5a717988edb22bae8688fb5cf9d8efe9d503dfe2918cdb5a9c95578a5768828'
ENTRY='runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Text/UnicodeEncoding.cs'

def encode(units,big,replacement):
 out=[];invalid=[];i=0
 while i<len(units):
  c=units[i]
  if 0xd800<=c<=0xdbff and i+1<len(units) and 0xdc00<=units[i+1]<=0xdfff:out.extend(units[i:i+2]);i+=2;continue
  if 0xd800<=c<=0xdfff:invalid.append(i);out.extend(replacement)
  else:out.append(c)
  i+=1
 result=[]
 for c in out:result.extend([c>>8,c&255] if big else [c&255,c>>8])
 return result,invalid

def decode(data,big,replacement):
 out=[];invalid=[];i=0
 def unit(k):return (data[k]<<8|data[k+1]) if big else (data[k]|data[k+1]<<8)
 while i<len(data):
  if i+1==len(data):invalid.append((i,data[i:i+1]));out.extend(replacement);i+=1;continue
  c=unit(i)
  if 0xd800<=c<=0xdbff and i+3<len(data) and 0xdc00<=unit(i+2)<=0xdfff:out.extend([c,unit(i+2)]);i+=4;continue
  if 0xd800<=c<=0xdfff:
   index=min(i+4,len(data))-2 if c<=0xdbff else i
   invalid.append((index,data[i:i+2]));out.extend(replacement)
  else:out.append(c)
  i+=2
 return out,invalid

def validate(j,plan,producer,source):
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']==CORE
 assert j['oracleSha256']==hashlib.sha256(producer).hexdigest()
 assert hashlib.sha256(source).hexdigest()==SOURCE
 assert plan['sourceArchiveSha256']==ARCHIVE and plan['sourceSha256']==SOURCE and plan['sourceEntry']==ENTRY
 assert plan['task']=='DJ-001-WP-05-T2' and plan['qualification']=='NATIVE_REFERENCE_AND_IMPLEMENTATION_PLAN_ONLY'
 assert plan['acceptedImplementationTasksCredited']==0 and not plan['javaImplementationQualified']
 assert plan['projectBatchTotal'] is None and plan['projectBatchesRemaining'] is None
 assert j['nativeType']=='System.Text.UnicodeEncoding' and j['charSize']==2
 assert [len(j[k]) for k in ['specs','methods','rows','maximums','equalities']]==[18,19,1224,360,324]
 assert [[p['type'] for p in c] for c in j['constructors']]==[[],['System.Boolean']*2,['System.Boolean']*3]
 assert [x['native'] for x in plan['methodProjection']]==j['methods']
 assert sum(x['status']=='OPEN_POINTER_ABI' for x in plan['methodProjection'])==4
 assert sum(x['status']=='OPEN_STATEFUL_CONTRACT' for x in plan['methodProjection'])==2
 assert all(x['status'] in {'OPEN_POINTER_ABI','OPEN_STATEFUL_CONTRACT','PLANNED_HEAP_SPAN_ADAPTER','PLANNED_STATELESS_ADAPTER'} for x in plan['methodProjection'])
 assert {'stateful encoder/decoder carry','inherited span override dispatch','slice validation and partial writes','pointer ABI and byref lifetimes','full N01/E01/E02/E03 closure','culture comparisons and normalization transforms'}<=set(plan['openWork'])
 for s in j['specs']:
  assert s['codePage']==(1201 if s['bigEndian'] else 1200)
  assert s['readOnly'] is (not s['custom']) and not s['singleByte']
  assert s['preamble']==(([254,255] if s['bigEndian'] else [255,254]) if s['bom'] else [])
  assert s['preambleIdentity'] is (not s['bom'])
  expected=(s['codePage']+s['encoderHash']+s['decoderHash']+(4 if s['bom'] else 0)+(8 if s['bigEndian'] else 0)+2**31)%2**32-2**31
  assert s['hash']==expected
  for side in ['encoder','decoder']:
   strict=s['strict'] and not s['custom'];assert s[side+'Max']==(2 if s['custom'] else 0 if strict else 1)
   assert s[side+'Fallback']=='System.Text.'+side.title()+('ExceptionFallback' if strict else 'ReplacementFallback')
 for row in j['rows']:
  s=j['specs'][row['state']];encoding=row['direction']=='encode';replacement=([65,66] if encoding else [67,68]) if s['custom'] else [0xfffd]
  result,invalid=(encode if encoding else decode)(row['input'],s['bigEndian'],replacement)
  strict=s['strict'] and not s['custom'];f=row['failure']
  if invalid and strict:
   assert f and f['type']=='System.Text.'+('Encoder' if encoding else 'Decoder')+'FallbackException'
   index=f['index'];assert 0<=index<len(row['input'])
   if encoding:assert not f['isPair'] and f['charUnknown']==row['input'][index]
   else:assert (index,f['bytes'])==invalid[0]
  else:assert f is None and row['result']==(len(result) if row['countOnly'] else result),row
 for row in j['maximums']:
  s=j['specs'][row['state']];count=row['count'];expected=((count+1)*2*max(1,s['encoderMax'])) if row['encode'] else ((count>>1)+(count&1)+1)*max(1,s['decoderMax'])
  if count<0 or expected>0x7fffffff:assert row['failure'] and row['failure']['type']=='System.ArgumentOutOfRangeException' and row['failure']['paramName']==('charCount' if row['encode'] else 'byteCount')
  else:assert row['failure'] is None and row['result']==expected
 for row in j['equalities']:
  a,b=(j['specs'][row[k]] for k in ['left','right'])
  key=lambda s:(s['codePage'],s['bom'],s['bigEndian'],s['custom'],False if s['custom'] else s['strict'])
  assert row['equal']==(key(a)==key(b))
 return 1908

def controls(j,plan,producer,source):
 mutations=[]
 bad=copy.deepcopy(j);bad['runtimeVersion']='10.0.11';mutations.append((bad,plan,producer,source))
 bad=copy.deepcopy(j);bad['oracleSha256']='0'*64;mutations.append((bad,plan,producer,source))
 bad=copy.deepcopy(j);r=next(r for r in bad['rows'] if r['failure'] is None and r['countOnly']);r['result']+=1;mutations.append((bad,plan,producer,source))
 mutations.append((j,plan,producer,source+b'changed'))
 bad=copy.deepcopy(plan);bad['acceptedImplementationTasksCredited']=1;mutations.append((j,bad,producer,source))
 for args in mutations:
  try:validate(*args)
  except AssertionError:continue
  raise AssertionError('Invalid reference/qualification control accepted')
 return len(mutations)

def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);p.add_argument('--source-archive',type=Path,default=Path(os.environ.get('DOTJ_RUNTIME_SOURCE_ARCHIVE','D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip')));a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 fixture=EVIDENCE/'unicode-encoding-plan-contract-v10.0.12.json';plan_path=EVIDENCE/'unicode-encoding-implementation-plan-v1.json';j=json.loads(fixture.read_text(encoding='utf-8'));plan=json.loads(plan_path.read_text(encoding='utf-8'))
 archive_manifest=json.loads((EVIDENCE/'source-archive-v10.0.12.json').read_text(encoding='utf-8'));assert archive_manifest['archive']['sha256']==ARCHIVE
 assert hashlib.sha256(a.source_archive.read_bytes()).hexdigest()==ARCHIVE
 with zipfile.ZipFile(a.source_archive) as z:source=z.read(ENTRY)
 producer=Path(__file__).with_name('capture-unicode-encoding-plan-contract.ps1').read_bytes();count=validate(j,plan,producer,source);negative=controls(j,plan,producer,source)
 with zipfile.ZipFile(a.jar) as z:present='System/Text/UnicodeEncoding.class' in z.namelist()
 record=dict(schemaVersion=1,nativeRowsValidated=count,nativeStatesValidated=18,nativeDeclaredMethods=19,negativeControlsPassed=negative,oracleEvidence=fixture.name,oracleSha256=hashlib.sha256(fixture.read_bytes()).hexdigest(),planSha256=hashlib.sha256(plan_path.read_bytes()).hexdigest(),validatorSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),sourceArchiveSha256=ARCHIVE,sourceSha256=SOURCE,candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),candidateUnicodeClassPresent=present,javaImplementationQualifiedByThisCheck=False,acceptedImplementationTasksCredited=0,qualification='NATIVE_UTF16_REFERENCE_AND_PLAN_ONLY; JAVA_IMPLEMENTATION_STATEFUL_POINTER_ABI_SOURCE_ABI_E01_AND_TASK_ACCEPTANCE_OPEN')
 (EVIDENCE/'unicode-encoding-plan-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(f'PASS UTF16 reference and plan: {count} native rows, 18 states, 19 methods, {negative} integrity controls; Java implementation qualification OPEN')
if __name__=='__main__':main()
