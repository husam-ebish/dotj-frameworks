"""Review pinned native Unicode decoder carry; no Java decoder qualification."""
import argparse,copy,hashlib,json,zipfile
from pathlib import Path
import importlib.util
_hash_spec = importlib.util.spec_from_file_location("dotj_oracle_file_hashes", Path(__file__).with_name("oracle_file_hashes.py"))
_hash_module = importlib.util.module_from_spec(_hash_spec)
_hash_spec.loader.exec_module(_hash_module)
sha256_file = _hash_module.sha256_file
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
CORE='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';ARCHIVE='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
def validate(j,p,producer,archive):
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']==CORE and j['oracleSha256']==hashlib.sha256(producer).hexdigest()
 assert p['qualification']=='NATIVE_UNICODE_DECODER_ARRAY_STATE_REFERENCE_AND_IMPLEMENTATION_PLAN_ONLY' and not p['javaImplementationQualified'] and p['acceptedImplementationTasksCredited']==0
 assert p['task']=='DJ-001-WP-05-T2' and p['projectBatchTotal'] is None and p['projectBatchesRemaining'] is None
 assert p['sourceArchiveSha256']==ARCHIVE and sha256_file(archive)==ARCHIVE
 with zipfile.ZipFile(archive) as z:
  assert set(p['sources'])=={'UnicodeEncoding','DecoderNLS','DecoderFallback'}
  for name,pin in p['sources'].items():assert pin['entry'].endswith('/System/Text/'+name+'.cs') and hashlib.sha256(z.read(pin['entry'])).hexdigest()==pin['sha256']
 assert len(j['profiles'])==10 and len(j['textInputs'])==130 and len(j['capacityInputs'])==17
 total=0;strict=0;prior=0;capacity=0
 def outcome(r):
  nonlocal total,strict,prior,capacity
  total+=1
  if r['ok']:assert isinstance(r['count'],int) and 0<=r['count']<=20
  else:
   assert r['exception'] in {'System.ArgumentException','System.ArgumentNullException','System.ArgumentOutOfRangeException','System.Text.DecoderFallbackException'} and isinstance(r['message'],str) and r['hResult']<0
   if r['exception']=='System.Text.DecoderFallbackException':
    strict+=1;assert len(r['unknown']) in {1,2} and all(0<=v<=255 for v in r['unknown']) and isinstance(r['index'],int);prior+=int(r['index']<0)
   if r['exception']=='System.ArgumentException':capacity+=1
 def buffer(r,after,offset):
  assert all(0<=v<=65535 for v in after) and after[:offset]==[99]*offset
  if r['ok']:assert offset+r['count']<=len(after) and after[offset+r['count']:]==[99]*(len(after)-offset-r['count'])
 for profile in j['profiles']:
  assert all(profile[k] for k in ['freshInstances','initialFallbackShared','detachedAfterOwnerChange','freshUsesOwner','ownerUnchanged'])
  assert len(profile['rows'])==1164 and len(profile['capacityRows'])==2448 and len(profile['resetRows'])==36 and len(profile['guards'])==96 and len(profile['seeds'])==6
  for row in profile['rows']:
   assert len(row['steps'])==6
   for k,step in enumerate(row['steps']):
    assert step['operation']==('Count' if k%2==0 else 'Chars') and step['block']==k//2 and step['flush']==(False if k<2 else row['flushSecond'] if k<4 else True)
    outcome(step['result'])
    if k%2:assert len(step['after'])==20;buffer(step['result'],step['after'],1)
  for r in profile['capacityRows']:
   for key in ['seedResult','countResult','writeResult','tailResult']:outcome(r[key])
   assert r['seedResult']['ok'] and r['seedResult']['count']==0 and r['seedAfter']==[99]*8
   assert len(r['after'])==r['offset']+r['capacity'] and len(r['tailAfter'])==16
   buffer(r['writeResult'],r['after'],r['offset']);buffer(r['tailResult'],r['tailAfter'],0)
  for r in profile['resetRows']:
   for key in ['seedResult','countResult','writeResult']:outcome(r[key])
   assert r['seedResult']['ok'] and r['seedResult']['count']==0;buffer(r['writeResult'],r['after'],0)
   if r['reset']:assert r['countResult']==dict(ok=True,count=0) and r['writeResult']==dict(ok=True,count=0) and r['after']==[99]*16
  for g in profile['guards']:
   r=g['result'];outcome(r)
   if g['nullSource']:assert not r['ok'] and r['exception']=='System.ArgumentNullException' and r['paramName']=='bytes'
   elif g['nullDestination'] and g['operation']=='Chars':assert not r['ok'] and r['exception']=='System.ArgumentNullException' and r['paramName']=='chars'
 assert total==p['nativeCalls']==169800 and strict==15090 and prior>0 and capacity==7536
 return dict(nativeCalls=total,strictFailures=strict,priorCallIndexes=prior,capacityFailures=capacity)
def main():
 a=argparse.ArgumentParser();a.add_argument('--jar',type=Path,help='Runner compatibility only; no Java qualification');a.parse_args();native=EVIDENCE/'unicode-decoder-state-contract-v10.0.12.json';plan=EVIDENCE/'unicode-decoder-state-plan-v1.json';j=json.loads(native.read_text());p=json.loads(plan.read_text());producer=Path(__file__).with_name('capture-unicode-decoder-state-contract.ps1').read_bytes();archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');summary=validate(j,p,producer,archive)
 variants=[]
 q=copy.deepcopy(j);q['runtimeVersion']='10.0.11';variants.append((q,p,producer))
 q=copy.deepcopy(j);q['profiles'][0]['capacityRows'][0]['seedResult']['count']=1;variants.append((q,p,producer))
 q=copy.deepcopy(j);q['profiles'][0]['capacityRows'][0]['seedAfter'][0]=0;variants.append((q,p,producer))
 q=copy.deepcopy(p);q['acceptedImplementationTasksCredited']=1;variants.append((j,q,producer));variants.append((j,p,producer+b'changed'))
 for args in variants:
  try:validate(*args,archive)
  except AssertionError:continue
  raise AssertionError('Tamper control accepted')
 record=dict(schemaVersion=1,**summary,integrityControls=5,oracleEvidence=native.name,oracleSha256=hashlib.sha256(native.read_bytes()).hexdigest(),planSha256=hashlib.sha256(plan.read_bytes()).hexdigest(),qualification=p['qualification'],javaImplementationQualified=False,acceptedImplementationTasksCredited=0);(EVIDENCE/'unicode-decoder-state-reference-review-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS native Unicode decoder state review: 169800 calls and five integrity controls; Java decoder remains open')
if __name__=='__main__':main()
