"""Compare returned stateless/stateful UTF16 decoder NUL replacement behavior."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'unicode-replacement-edge-contract-v10.0.12.json';capture=json.loads(path.read_text());assert capture['schemaVersion']==2 and capture['runtimeVersion']=='10.0.12' and capture['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert len(capture['profiles'])==18 and capture['totalCases']==40320
 for key,name in [('oracleSha256','capture-unicode-replacement-edge-contract.ps1'),('workerSha256','capture-unicode-replacement-edge-worker.ps1'),('controllerSha256','capture-unicode-replacement-edge-controller.py')]:assert capture[key]==hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
 seen=set();bounded=[];profiles=[];nativeCases=0
 for pid,profile in enumerate(capture['profiles']):
  assert len(profile['rows'])==2240;rows=[]
  for entry in profile['rows']:
   cid=entry['caseId'];assert cid not in seen and cid//2240==pid and entry['profile']==pid;seen.add(cid)
   if entry['status']=='OBSERVED_NO_RETURN_WITHIN_BOUND':
    assert entry['observationSeconds']>=entry['boundSeconds']>=3 and entry['context']['encode'] and 'row' not in entry;bounded.append(entry);continue
   assert entry['status']=='RETURNED'
   if entry['row']['encode']:rows.append(entry['row']);nativeCases+=1
  profiles.append(dict(bigEndian=profile['bigEndian'],replacement=profile['replacement'],rows=rows))
 assert seen==set(range(40320)) and len(bounded)==capture['boundedNoReturnCases'] and nativeCases+len(bounded)==14400 and nativeCases>0
 j=dict(profiles=profiles)
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/unicode-encoder-returned-replacement');work.mkdir(parents=True,exist_ok=True);specs=[];events=[];groups=0
 def action(op,source,length,offset,flush,r,after):
  nonlocal groups
  events.append('\t'.join([op,csv(source),str(length),str(offset),str(int(flush)),str(r.get('count',0)),csv(after),str(r.get('remaining','~')),r.get('exception',''),base64.b64encode(r.get('message','').encode()).decode(),str(r.get('hResult',0)),r.get('paramName') or '~',str(r.get('unknown',0)),str(r.get('index',0)),str(r.get('high',0)),str(r.get('low',0)),str(int(r.get('isPair',False)))]));groups+=1+int(op=='W')+int('remaining' in r)
 for pid,profile in enumerate(j['profiles']):
  specs.append('\t'.join([str(int(profile['bigEndian'])),csv(profile['replacement'])]))
  for r in profile['rows']:
   assert r['encode'];events.append('\t'.join(['N',str(pid),str(int(r['stateful']))]))
   if r['stateful']:action('W',r['seed'],16,0,False,r['seedResult'],r['seedAfter'])
   if r['countBefore']:action('Q',r['source'],-1,0,r['flush'],r['countResult'],None)
   action('W',r['source'],len(r['after']),r['offset'],r['flush'],r['writeResult'],r['after']);action('W',[],16,0,True,r['tailResult'],r['tailAfter'])
   for step in r['buffer']:action({'remaining':'M','next':'B','previous':'P'}[step['operation']],[],-1,0,True,step['result'],None)
 assert groups>0,groups
 states=work/'profiles.tsv';states.write_text('\n'.join(specs)+'\n',encoding='ascii');vectors=work/'events.tsv';vectors.write_text('\n'.join(events)+'\n',encoding='ascii');component=Path(__file__).with_name('unicode-encoder-returned-replacement-probe.java');source=work/'UnicodeEncoderReturnedReplacementProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeEncoderReturnedReplacementProbe',str(states),str(vectors)],capture_output=True,text=True,timeout=60);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout
 controls=[]
 for entry in bounded:
  c=entry['context'];controls.append('\t'.join([str(entry['profile']),str(int(c['stateful'])),csv(c['seed']),csv(c['source']),str(int(c['flush'])),str(int(c['countBefore'])),str(c['capacity']),str(c['offset'])]))
 controlVectors=work/'java-only-no-return-controls.tsv';controlVectors.write_text('\n'.join(controls)+'\n',encoding='ascii');controlComponent=Path(__file__).with_name('unicode-encoder-no-return-controls.java');controlSource=work/'UnicodeEncoderNoReturnControls.java';controlSource.write_bytes(controlComponent.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(controlSource)],check=True);controlResult=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeEncoderNoReturnControls',str(states),str(controlVectors)],capture_output=True,text=True,timeout=60);print(controlResult.stdout,end='');print(controlResult.stderr,end='');controlResult.check_returncode();assert f'cases={len(bounded)}' in controlResult.stdout
 record=dict(schemaVersion=1,casesPassed=groups,returnedNativeEncoderCases=nativeCases,boundedNativeRowsExcludedFromValueComparison=len(bounded),javaOnlyFiniteControls=len(bounded),javaOnlyControlsAreNativeParityEvidence=False,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),finiteControlSourceSha256=hashlib.sha256(controlComponent.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='ALL_RETURNED_ENCODER_CASES_IN_SELECTED_BOUNDED_REPLACEMENT_CORPUS_ONLY; NATIVE_NO_RETURN_VALUE_SEMANTICS_AND_PRODUCT_LIVENESS_POLICY_CUSTOM_CALLBACKS_FULL_ABI_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'unicode-encoder-returned-replacement-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS returned encoder replacement edges: {groups} comparisons, {nativeCases} returned native cases; {len(bounded)} Java-only finite controls, native no-return outcomes unqualified')
if __name__=='__main__':main()
