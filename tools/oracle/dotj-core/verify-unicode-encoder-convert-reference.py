"""Review pinned native Unicode encoder Convert arrays; does not qualify Java Convert."""
import argparse,copy,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
CORE='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
ARCHIVE='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
def validate(j,p,producer,archive):
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']==CORE
 assert j['oracleSha256']==hashlib.sha256(producer).hexdigest()
 assert p['qualification']=='NATIVE_ARRAY_CONVERT_REFERENCE_AND_IMPLEMENTATION_PLAN_ONLY' and p['acceptedImplementationTasksCredited']==0 and p['javaImplementationQualified'] is False
 assert p['task']=='DJ-001-WP-05-T2' and p['projectBatchTotal'] is None and p['projectBatchesRemaining'] is None
 assert p['sourceArchiveSha256']==ARCHIVE and hashlib.sha256(archive.read_bytes()).hexdigest()==ARCHIVE
 with zipfile.ZipFile(archive) as z:
  assert set(p['sources'])=={'UnicodeEncoding','EncoderNLS','EncoderFallback'}
  for pin in p['sources'].values():assert hashlib.sha256(z.read(pin['entry'])).hexdigest()==pin['sha256']
 assert len(j['profiles'])==10 and len(j['inputs'])==17
 total=0;partial=0;deferred=0;empty=0;fallback=0
 for profile in j['profiles']:
  assert len(profile['rows'])==1088 and len(profile['guards'])==52
  for r in profile['rows']:
   capacity=r['capacity'];offset=r['offset'];after=r['after'];assert len(after)==capacity+offset+3 and after[:offset]==[99]*offset and after[offset+capacity:]==[99]*3
   count=len(j['inputs'][r['sourceId']]);previous=0
   for key,dest,cap in [('first',after,capacity),('second',r['secondAfter'],32),('third',r['thirdAfter'],16)]:
    a=r[key];total+=1;assert a['remaining']>=0
    if a['ok']:
     n=a['bytesUsed'];assert 0<=n<=cap and n%2==0 and 0<=a['charsUsed']<=(count if key=='first' else count-previous if key=='second' else 0)
     start=offset if key=='first' else 0;assert dest[start+n:]==[99]*(len(dest)-start-n)
     if key=='first':
      previous=a['charsUsed'];partial+=int(0<previous<count);deferred+=int(a['remaining']>0);empty+=int(count==0 and not r['pending'] and n==0 and a['completed'])
    else:
     assert a['exception'] in {'System.ArgumentException','System.Text.EncoderFallbackException'} and isinstance(a['message'],str) and a['hResult']<0
     if a['exception']=='System.Text.EncoderFallbackException':assert not a['isPair'];fallback+=1
   assert len(r['secondAfter'])==32 and len(r['thirdAfter'])==16
  for g in profile['guards']:
   a=g['result'];total+=1
   if g['nullSource'] or g['nullDestination']:
    assert not a['ok'] and a['exception']=='System.ArgumentNullException' and a['paramName']==('chars' if g['nullSource'] else 'bytes')
   elif (g['charIndex'],g['charCount'],g['byteIndex'],g['byteCount'])==(0,1,0,8):assert a['ok'] and a['charsUsed']==1 and a['bytesUsed']==2 and a['completed']
   else:assert not a['ok'] and a['exception']=='System.ArgumentOutOfRangeException'
 assert total==33160 and partial>0 and deferred>0 and empty>0 and fallback>0
 return dict(nativeCalls=total,partialInputCases=partial,deferredFallbackCases=deferred,emptyCompletedCases=empty,strictFailures=fallback)
def main():
 a=argparse.ArgumentParser();a.add_argument('--jar',type=Path,help='Accepted for runner compatibility; no Java Convert qualification');a.parse_args()
 native=EVIDENCE/'unicode-encoder-convert-contract-v10.0.12.json';plan=EVIDENCE/'unicode-encoder-convert-plan-v1.json';producer=Path(__file__).with_name('capture-unicode-encoder-convert-contract.ps1').read_bytes();archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');j=json.loads(native.read_text());p=json.loads(plan.read_text());summary=validate(j,p,producer,archive)
 variants=[]
 q=copy.deepcopy(j);q['runtimeVersion']='10.0.11';variants.append((q,p,producer))
 q=copy.deepcopy(j);q['profiles'][0]['rows'][0]['after'][0]=0;variants.append((q,p,producer))
 q=copy.deepcopy(j);q['profiles'][0]['rows'][0]['first']['bytesUsed']=1;variants.append((q,p,producer))
 q=copy.deepcopy(p);q['acceptedImplementationTasksCredited']=1;variants.append((j,q,producer))
 variants.append((j,p,producer+b'changed'))
 for args in variants:
  try:validate(*args,archive)
  except AssertionError:continue
  raise AssertionError('Tamper control accepted')
 record=dict(schemaVersion=1,**summary,integrityControls=5,oracleEvidence=native.name,oracleSha256=hashlib.sha256(native.read_bytes()).hexdigest(),planSha256=hashlib.sha256(plan.read_bytes()).hexdigest(),qualification=p['qualification'],javaImplementationQualified=False,acceptedImplementationTasksCredited=0)
 (EVIDENCE/'unicode-encoder-convert-reference-review-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS native Unicode encoder Convert review: 33160 calls and five integrity controls; Java Convert remains open')
if __name__=='__main__':main()
