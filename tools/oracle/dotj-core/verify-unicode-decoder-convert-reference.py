"""Review pinned native decoder Convert quirks; no Java Convert qualification."""
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
 assert p['qualification']=='NATIVE_UNICODE_DECODER_ARRAY_CONVERT_REFERENCE_AND_IMPLEMENTATION_PLAN_ONLY' and p['javaImplementationQualified'] is False and p['acceptedImplementationTasksCredited']==0
 assert p['task']=='DJ-001-WP-05-T2' and p['projectBatchTotal'] is None and p['projectBatchesRemaining'] is None
 assert p['sourceArchiveSha256']==ARCHIVE and sha256_file(archive)==ARCHIVE
 with zipfile.ZipFile(archive) as z:
  assert set(p['sources'])=={'UnicodeEncoding','DecoderNLS','DecoderFallback'}
  for name,pin in p['sources'].items():assert pin['entry'].endswith('/System/Text/'+name+'.cs') and hashlib.sha256(z.read(pin['entry'])).hexdigest()==pin['sha256']
 assert len(j['profiles'])==10 and len(j['inputs'])==17
 total=negative=unreported=partial=0
 def outcome(r,capacity,count):
  nonlocal total
  total+=1;assert r['remaining']>=0
  if r['ok']:assert -1<=r['bytesUsed']<=count and 0<=r['charsUsed']<=capacity
  else:
   assert r['exception'] in {'System.ArgumentException','System.ArgumentNullException','System.ArgumentOutOfRangeException','System.Text.DecoderFallbackException'} and isinstance(r['message'],str) and r['hResult']<0
   if r['exception']=='System.Text.DecoderFallbackException':assert len(r['unknown']) in {1,2} and all(0<=b<=255 for b in r['unknown']) and isinstance(r['index'],int)
 for profile in j['profiles']:
  assert len(profile['rows'])==3264 and len(profile['guards'])==52 and len(profile['seeds'])==6
  for r in profile['rows']:
   total+=1;assert r['seedResult']==dict(ok=True,count=0) and r['seedAfter']==[99]*8
   count=len(j['inputs'][r['sourceId']]);cap=r['capacity'];offset=r['offset'];after=r['after'];assert len(after)==offset+cap+3 and after[:offset]==[99]*offset and after[offset+cap:]==[99]*3 and all(0<=c<=65535 for c in after)
   a=r['first'];outcome(a,cap,count)
   if a['ok']:
    negative+=int(a['bytesUsed']<0);unreported+=int(any(v!=99 for v in after[offset+a['charsUsed']:offset+cap]));partial+=int(0<=a['bytesUsed']<count)
   used=a['bytesUsed'] if a['ok'] else 0;outcome(r['second'],32,count-used);outcome(r['third'],16,0);assert len(r['secondAfter'])==32 and len(r['thirdAfter'])==16
   if r['second']['ok'] and r['second']['completed']:assert r['third']==dict(ok=True,bytesUsed=0,charsUsed=0,completed=True,remaining=0) and r['thirdAfter']==[99]*16
  for g in profile['guards']:
   a=g['result'];outcome(a,max(0,g['charCount']),max(0,g['byteCount']))
   if g['nullSource']:assert not a['ok'] and a['exception']=='System.ArgumentNullException' and a['paramName']=='bytes'
   elif g['nullDestination']:assert not a['ok'] and a['exception']=='System.ArgumentNullException' and a['paramName']=='chars'
   elif (g['byteIndex'],g['byteCount'],g['charIndex'],g['charCount'])==(0,2,0,2):assert a['ok'] and a['bytesUsed']==2 and a['charsUsed']==1 and a['completed']
   else:assert not a['ok'] and a['exception']=='System.ArgumentOutOfRangeException'
 assert total==p['nativeCalls']==131080 and negative==p['negativeBytesUsedCases']==456 and unreported==p['unreportedPrefixWrites']==588 and partial>0
 return dict(nativeCalls=total,negativeBytesUsedCases=negative,unreportedPrefixWrites=unreported,partialInputCases=partial)
def main():
 a=argparse.ArgumentParser();a.add_argument('--jar',type=Path,help='Runner compatibility only; no Java qualification');a.parse_args();native=EVIDENCE/'unicode-decoder-convert-contract-v10.0.12.json';plan=EVIDENCE/'unicode-decoder-convert-plan-v1.json';j=json.loads(native.read_text());p=json.loads(plan.read_text());producer=Path(__file__).with_name('capture-unicode-decoder-convert-contract.ps1').read_bytes();archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');summary=validate(j,p,producer,archive)
 def reject(a,b,c):
  try:validate(a,b,c,archive)
  except AssertionError:return
  raise AssertionError('Tamper control accepted')
 q=copy.deepcopy(j);q['runtimeVersion']='10.0.11';reject(q,p,producer);del q
 q=copy.deepcopy(j);r=next(r for profile in q['profiles'] for r in profile['rows'] if r['first']['ok'] and r['first']['bytesUsed']<0);r['first']['bytesUsed']=0;reject(q,p,producer);del q
 q=copy.deepcopy(j);q['profiles'][0]['rows'][0]['after'][0]=0;reject(q,p,producer);del q
 q=dict(p,acceptedImplementationTasksCredited=1);reject(j,q,producer);reject(j,p,producer+b'changed')
 record=dict(schemaVersion=1,**summary,integrityControls=5,oracleEvidence=native.name,oracleSha256=hashlib.sha256(native.read_bytes()).hexdigest(),planSha256=hashlib.sha256(plan.read_bytes()).hexdigest(),qualification=p['qualification'],javaImplementationQualified=False,acceptedImplementationTasksCredited=0);(EVIDENCE/'unicode-decoder-convert-reference-review-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS native Unicode decoder Convert review: 131080 calls, 456 signed counter cases, 588 unreported writes and five integrity controls; Java Convert remains open')
if __name__=='__main__':main()
