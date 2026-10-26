"""Compare every returned selected encoder Convert replacement case; classify bounded observations separately."""
import argparse,base64,copy,hashlib,json,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
CORE='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
def validate(capture,plan):
 assert capture['schemaVersion']==2 and capture['runtimeVersion']=='10.0.12' and capture['coreLibSha256']==CORE and capture['totalCases']==9216 and capture['boundSeconds']>=3
 assert capture['qualification']=='NATIVE_ENCODER_REPLACEMENT_CONVERT_REFERENCE_WITH_EXPLICIT_BOUNDED_NO_RETURN_OBSERVATIONS_ONLY; NO_JAVA_OR_FULL_NONTERMINATION_QUALIFICATION'
 assert plan['qualification']=='SELECTED_ENCODER_REPLACEMENT_CONVERT_RETURNED_CASES_ONLY; NATIVE_NO_RETURN_OUTCOMES_AND_FINAL_PRODUCT_LIVENESS_POLICY_OPEN'
 assert plan['task']=='DJ-001-WP-05-T2' and plan['profiles']==18 and plan['casesPerProfile']==512 and plan['totalCases']==9216 and plan['acceptedImplementationTasksCredited']==0 and plan['projectBatchTotal'] is None and plan['projectBatchesRemaining'] is None and plan['nativeNoReturnRowsHaveReturnedValues'] is False and plan['javaOnlyFiniteControlsAreNativeParityEvidence'] is False
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()==plan['sourceArchiveSha256']=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 with zipfile.ZipFile(archive) as z:
  assert set(plan['sources'])=={'UnicodeEncoding','EncoderNLS','EncoderFallback','EncoderReplacementFallback'}
  for name,pin in plan['sources'].items():assert pin['entry'].endswith('/System/Text/'+name+'.cs') and hashlib.sha256(z.read(pin['entry'])).hexdigest()==pin['sha256']
 for key,name in [('oracleSha256','capture-unicode-encoder-replacement-convert-contract.ps1'),('workerSha256','capture-unicode-encoder-replacement-convert-worker.ps1'),('controllerSha256','capture-unicode-encoder-replacement-convert-controller.py')]:assert capture[key]==hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
 replacements=[[],[0],[65,0],[0,66],[65,0,66],[55296,56320],[65,0,55296,56320],[55296,56320,0,65],[0,55296,56320,0]];inputs=[[],[65],[55296],[56320],[55296,65],[55296,56320],[65,55296],[56320,55296]];capacities=[0,1,2,3,4,5,6,8];seen=set();bounded=[];profiles=[];returned=0
 assert len(capture['profiles'])==18
 def outcome(value):
  assert isinstance(value['ok'],bool)
  if not value['ok']:assert value['exception'] in {'System.ArgumentException','System.ArgumentOutOfRangeException','System.Text.EncoderFallbackException'} and value['hResult']<0 and isinstance(value['message'],str)
 for pid,profile in enumerate(capture['profiles']):
  assert profile['bigEndian']==(pid>=9) and profile['replacement']==replacements[pid%9] and len(profile['rows'])==512;rows=[]
  for entry in profile['rows']:
   cid=entry['caseId'];assert cid not in seen and cid//512==pid and entry['profile']==pid and entry['bigEndian']==profile['bigEndian'] and entry['replacement']==profile['replacement'];seen.add(cid);local=cid%512;seed=[] if local//256==0 else [55296];source=inputs[(local//32)%8];flush=bool((local//16)%2);capacity=capacities[(local//2)%8];offset=[0,2][local%2]
   if entry['status']=='OBSERVED_NO_RETURN_WITHIN_BOUND':
    assert 'row' not in entry and entry['observationSeconds']>=entry['boundSeconds']>=capture['boundSeconds'] and entry['context']==entry['lastCall']['context'] and entry['lastCall']['phase'] in {'seed','first','second','third'}
    assert entry['qualification']=='BOUNDED_OBSERVATION_ONLY; NOT_A_RETURN_VALUE_OR_PROOF_OF_INFINITE_EXECUTION'
    context=entry['context'];assert context['profile']==pid and context['bigEndian']==profile['bigEndian'] and context['replacement']==profile['replacement'] and context['encode'] is True and context['stateful'] is True;assert context['caseId']==cid and context['seed']==seed and context['source']==source and context['flush']==flush and context['capacity']==capacity and context['offset']==offset;bounded.append(entry);continue
   assert entry['status']=='RETURNED';row=entry['row'];assert row['seed']==seed and row['source']==[56320]+source+[55296] and row['start']==1 and row['count']==len(source) and row['flush']==flush and row['capacity']==capacity and row['offset']==offset;assert row['seedResult']==dict(ok=True,count=0) and row['seedAfter']==[99]*16
   for key,after,start,cap in [('first',row['after'],offset,capacity),('second',row['secondAfter'],0,32),('third',row['thirdAfter'],0,16)]:
    value=row[key];outcome(value);assert len(after)==start+cap+(3 if key=='first' else 0) and all(0<=n<=255 for n in after) and after[:start]==[99]*start
    if key=='first':assert after[start+cap:]==[99]*3
    assert value['remaining']>=0 and isinstance(value['completed'],bool)
    if value['ok']:assert -2147483648<=value['charsUsed']<=2147483647 and 0<=value['bytesUsed']<=cap and after[start+value['bytesUsed']:start+cap]==[99]*(cap-value['bytesUsed'])
   assert [x['operation'] for x in row['buffer']]==['remaining','next','remaining','previous']
   for probe in row['buffer']:outcome(probe['result']);assert probe['result']['remaining']>=0
   rows.append(row);returned+=1
  profiles.append(dict(bigEndian=profile['bigEndian'],replacement=profile['replacement'],rows=rows))
 assert seen==set(range(9216)) and returned==capture['returnedCases'] and len(bounded)==capture['boundedNoReturnCases'] and returned+len(bounded)==9216
 return dict(profiles=profiles),bounded,returned

def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'unicode-encoder-replacement-convert-contract-v10.0.12.json';planPath=EVIDENCE/'unicode-encoder-replacement-convert-plan-v1.json';capture=json.loads(path.read_text());plan=json.loads(planPath.read_text());j,bounded,returned=validate(capture,plan)
 def reject(value,proposal):
  try:validate(value,proposal)
  except AssertionError:return
  raise AssertionError('Tamper control accepted')
 q=copy.deepcopy(capture);q['runtimeVersion']='10.0.11';reject(q,plan);del q
 q=copy.deepcopy(capture);q['profiles'][0]['rows'].pop();reject(q,plan);del q
 q=copy.deepcopy(capture);q['workerSha256']='0'*64;reject(q,plan);del q
 if bounded:
  q=copy.deepcopy(capture);next(e for p in q['profiles'] for e in p['rows'] if e['status']=='OBSERVED_NO_RETURN_WITHIN_BOUND')['observationSeconds']=0;reject(q,plan);del q
 else:raise AssertionError('Expected bounded observations in selected native corpus')
 reject(capture,dict(plan,acceptedImplementationTasksCredited=1))
 reject(capture,dict(plan,qualification='FULL_NATIVE_PARITY'))
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/unicode-encoder-replacement-convert');work.mkdir(parents=True,exist_ok=True);specs=[];events=[];groups=0
 def action(op,source,index,count,length,offset,capacity,flush,r,after):
  nonlocal groups
  events.append('\t'.join([op,csv(source),str(index),str(count),str(length),str(offset),str(int(flush)),str(r.get('count',0)),csv(after),r.get('exception',''),base64.b64encode(r.get('message','').encode()).decode(),str(r.get('hResult',0)),r.get('paramName') or '~',str(r.get('unknown',0)),str(r.get('index',0)),str(r.get('high',0)),str(r.get('low',0)),str(int(r.get('isPair',False))),str(r.get('charsUsed',0)),str(r.get('bytesUsed',0)),str(int(r.get('completed',False))),str(r.get('remaining','~')),str(capacity)]));groups+=1+int(op in {'W','C'})+int(op=='C')+int('remaining' in r)
 for pid,profile in enumerate(j['profiles']):
  specs.append('\t'.join([str(int(profile['bigEndian'])),csv(profile['replacement'])]))
  for row in profile['rows']:
   events.append('N\t'+str(pid));action('W',row['seed'],0,len(row['seed']),16,0,16,False,row['seedResult'],row['seedAfter']);action('C',row['source'],row['start'],row['count'],len(row['after']),row['offset'],row['capacity'],row['flush'],row['first'],row['after']);used=row['first']['charsUsed'] if row['first']['ok'] else 0;action('C',row['source'],row['start']+used,row['count']-used,32,0,32,True,row['second'],row['secondAfter']);action('C',[56320,55296],1,0,16,0,16,True,row['third'],row['thirdAfter'])
   for probe in row['buffer']:action({'remaining':'M','next':'B','previous':'P'}[probe['operation']],[],0,0,-1,0,0,True,probe['result'],None)
 states=work/'profiles.tsv';states.write_text('\n'.join(specs)+'\n',encoding='ascii');vectors=work/'events.tsv';vectors.write_text('\n'.join(events)+'\n',encoding='ascii');component=Path(__file__).with_name('unicode-encoder-replacement-convert-probe.java');source=work/'UnicodeEncoderReplacementConvertProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeEncoderReplacementConvertProbe',str(states),str(vectors)],capture_output=True,text=True,timeout=60);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout;print(f'PASS returned encoder Convert value comparisons: {groups} groups across {returned} returned cases')

 controls=[]
 for entry in bounded:
  c=entry['context'];controls.append('\t'.join([str(entry['profile']),csv(c['seed']),csv(c['source']),str(int(c['flush'])),str(c['capacity']),str(c['offset'])]))
 controlVectors=work/'finite-controls.tsv';controlVectors.write_text('\n'.join(controls)+'\n',encoding='ascii');controlComponent=Path(__file__).with_name('unicode-encoder-convert-no-return-controls.java');controlSource=work/'UnicodeEncoderConvertNoReturnControls.java';controlSource.write_bytes(controlComponent.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(controlSource)],check=True);control=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeEncoderConvertNoReturnControls',str(states),str(controlVectors)],capture_output=True,text=True,timeout=60);print(control.stdout,end='');print(control.stderr,end='');control.check_returncode();assert f'cases={len(bounded)}' in control.stdout
 record=dict(schemaVersion=1,casesPassed=groups,returnedNativeCases=returned,boundedNativeRowsExcludedFromValueComparison=len(bounded),javaOnlyFiniteControls=len(bounded),javaOnlyControlsAreNativeParityEvidence=False,integrityControls=6,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),planSha256=hashlib.sha256(planPath.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),finiteControlSourceSha256=hashlib.sha256(controlComponent.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification=plan['qualification'],acceptedImplementationTasksCredited=0);(EVIDENCE/'unicode-encoder-replacement-convert-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS encoder replacement Convert: {groups} comparisons, {returned} returned native cases, {len(bounded)} separate Java-only finite controls; six integrity controls')

if __name__=='__main__':main()
