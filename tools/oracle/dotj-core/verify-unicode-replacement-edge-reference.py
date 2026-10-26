"""Review finite native replacement results and explicit bounded no-return observations."""
import argparse,copy,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence';CORE='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';ARCHIVE='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
def validate(j,p,tools,archive):
 assert j['schemaVersion']==2 and j['runtimeVersion']=='10.0.12' and j['coreLibSha256']==CORE
 for key,name in [('oracleSha256','capture-unicode-replacement-edge-contract.ps1'),('workerSha256','capture-unicode-replacement-edge-worker.ps1'),('controllerSha256','capture-unicode-replacement-edge-controller.py')]:assert j[key]==hashlib.sha256((tools/name).read_bytes()).hexdigest()
 assert j['qualification']=='NATIVE_REPLACEMENT_EDGE_REFERENCE_WITH_EXPLICIT_BOUNDED_NO_RETURN_OBSERVATIONS_ONLY; NO_JAVA_OR_FULL_NONTERMINATION_QUALIFICATION'
 assert p['qualification']=='NATIVE_REPLACEMENT_EDGE_REFERENCE_AND_BOUNDED_NO_RETURN_PLAN_ONLY' and p['javaImplementationQualified'] is False and p['acceptedImplementationTasksCredited']==0 and p['projectBatchTotal'] is None and p['projectBatchesRemaining'] is None and p['task']=='DJ-001-WP-05-T2'
 assert p['sourceArchiveSha256']==ARCHIVE and hashlib.sha256(archive.read_bytes()).hexdigest()==ARCHIVE
 with zipfile.ZipFile(archive) as z:
  assert set(p['sources'])=={'UnicodeEncoding','EncoderNLS','DecoderNLS','EncoderFallback','DecoderFallback','EncoderReplacementFallback','DecoderReplacementFallback'}
  for name,pin in p['sources'].items():assert pin['entry'].endswith('/System/Text/'+name+'.cs') and hashlib.sha256(z.read(pin['entry'])).hexdigest()==pin['sha256']
 assert len(j['profiles'])==p['profiles']==18 and j['totalCases']==p['totalCases']==40320 and j['boundSeconds']>=3
 seen=set();returned=bounded=calls=0;families=set()
 def outcome(r):
  nonlocal calls
  calls+=1
  if r['ok']:assert isinstance(r['count'],int) and r['count']>=0
  else:families.add(r['exception']);assert r['exception'] in {'System.ArgumentException','System.ArgumentOutOfRangeException','System.Text.EncoderFallbackException','System.Text.DecoderFallbackException'} and isinstance(r['message'],str) and r['hResult']<0
  if 'remaining' in r:assert r['remaining']>=0
 def buffer(result,after,offset,capacity):
  assert len(after)==offset+capacity and all(0<=v<=65535 for v in after) and after[:offset]==[99]*offset
  if result['ok']:assert 0<=result['count']<=capacity and after[offset+result['count']:]==[99]*(capacity-result['count'])
 for pid,profile in enumerate(j['profiles']):
  assert len(profile['rows'])==p['casesPerProfile']==2240
  for entry in profile['rows']:
   cid=entry['caseId'];assert cid not in seen and cid//2240==pid and entry['profile']==pid and entry['bigEndian']==profile['bigEndian'] and entry['replacement']==profile['replacement'];seen.add(cid)
   if entry['status']=='OBSERVED_NO_RETURN_WITHIN_BOUND':
    bounded+=1;assert entry['qualification']=='BOUNDED_OBSERVATION_ONLY; NOT_A_RETURN_VALUE_OR_PROOF_OF_INFINITE_EXECUTION';assert entry['observationSeconds']>=entry['boundSeconds']>=j['boundSeconds'] and entry['context']==entry['lastCall']['context'] and entry['context']['caseId']==cid and 'row' not in entry
    continue
   assert entry['status']=='RETURNED';returned+=1;r=entry['row'];assert len(r['source'])<=8 and r['capacity'] in {0,1,2,4,8} and r['offset'] in {0,2}
   if r['stateful']:assert r['seedResult']==dict(ok=True,count=0,remaining=0) and r['seedAfter']==[99]*16;outcome(r['seedResult'])
   else:assert r['seedResult'] is None
   if r['countBefore']:assert r['countResult'] is not None;outcome(r['countResult'])
   else:assert r['countResult'] is None
   outcome(r['writeResult']);buffer(r['writeResult'],r['after'],r['offset'],r['capacity']);outcome(r['tailResult']);buffer(r['tailResult'],r['tailAfter'],0,16)
   if not r['stateful']:assert r['tailResult']==dict(ok=True,count=0) and not r['buffer']
   else:
    assert [x['operation'] for x in r['buffer']]==['remaining','next','remaining','previous']
    for probe in r['buffer']:outcome(probe['result'])
 assert seen==set(range(40320)) and returned==j['returnedCases']>0 and bounded==j['boundedNoReturnCases']>0 and returned+bounded==40320
 return dict(totalCases=40320,returnedCases=returned,boundedNoReturnCases=bounded,returnedNativeCalls=calls,errorFamilies=sorted(families))
def main():
 a=argparse.ArgumentParser();a.add_argument('--jar',type=Path,help='Runner compatibility; no Java qualification');a.parse_args();native=EVIDENCE/'unicode-replacement-edge-contract-v10.0.12.json';plan=EVIDENCE/'unicode-replacement-edge-plan-v1.json';j=json.loads(native.read_text());p=json.loads(plan.read_text());tools=Path(__file__).parent;archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');summary=validate(j,p,tools,archive)
 def reject(q,r):
  try:validate(q,r,tools,archive)
  except AssertionError:return
  raise AssertionError('Tamper control accepted')
 q=copy.deepcopy(j);q['runtimeVersion']='10.0.11';reject(q,p);del q
 q=copy.deepcopy(j);entry=next(e for profile in q['profiles'] for e in profile['rows'] if e['status']=='OBSERVED_NO_RETURN_WITHIN_BOUND');entry['observationSeconds']=0;reject(q,p);del q
 q=copy.deepcopy(j);q['profiles'][0]['rows'].pop();reject(q,p);del q
 q=copy.deepcopy(j);q['workerSha256']='0'*64;reject(q,p);del q
 reject(j,dict(p,acceptedImplementationTasksCredited=1))
 record=dict(schemaVersion=1,**summary,integrityControls=5,oracleEvidence=native.name,oracleSha256=hashlib.sha256(native.read_bytes()).hexdigest(),planSha256=hashlib.sha256(plan.read_bytes()).hexdigest(),qualification=p['qualification'],javaImplementationQualified=False,acceptedImplementationTasksCredited=0);(EVIDENCE/'unicode-replacement-edge-reference-review-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f"PASS replacement edge reference: {summary['returnedCases']} returned, {summary['boundedNoReturnCases']} bounded no-return cases; five integrity controls; Java semantics/liveness remain open")
if __name__=='__main__':main()
