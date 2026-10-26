"""Compare returned stateless/stateful UTF16 decoder NUL replacement behavior."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'unicode-encoder-returned-replacement-spans-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-unicode-encoder-returned-replacement-spans-contract.ps1').read_bytes()).hexdigest();assert len(j['profiles'])==18 and j['returnedEncoderContexts']==13680
 referencePath=EVIDENCE/'unicode-replacement-edge-contract-v10.0.12.json';reference=json.loads(referencePath.read_text());assert j['inputSha256']==hashlib.sha256(referencePath.read_bytes()).hexdigest()
 originals={entry['caseId']:(pid,entry['row']) for pid,p in enumerate(reference['profiles']) for entry in p['rows'] if entry['status']=='RETURNED' and entry['row']['encode']};assert len(originals)==13680;seen=set()
 for pid,profile in enumerate(j['profiles']):
  assert profile['bigEndian']==reference['profiles'][pid]['bigEndian'] and profile['replacement']==reference['profiles'][pid]['replacement']
  for row in profile['rows']:
   cid=row['caseId'];assert cid not in seen and cid in originals;seen.add(cid);originalPid,old=originals[cid];assert originalPid==pid
   for key in ['stateful','seed','flush','countBefore','capacity','offset']:assert row[key]==old[key]
   assert row['source']==[56320]+old['source']+[55296] and row['start']==1 and row['count']==len(old['source']);assert row['after'][:row['offset']]==[99]*row['offset'] and row['after'][row['offset']+row['capacity']:]==[99]*3
 assert seen==set(originals) and j['originalBoundedNoReturnRowsExcluded']==reference['boundedNoReturnCases']
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/unicode-encoder-returned-replacement-spans');work.mkdir(parents=True,exist_ok=True);specs=[];events=[];groups=0
 def action(op,source,length,offset,flush,r,after,start=0,count=None,capacity=None):
  nonlocal groups
  events.append('\t'.join([op,csv(source),str(length),str(offset),str(int(flush)),str(r.get('count',0)),csv(after),str(r.get('remaining','~')),r.get('exception',''),base64.b64encode(r.get('message','').encode()).decode(),str(r.get('hResult',0)),r.get('paramName') or '~',str(r.get('unknown',0)),str(r.get('index',0)),str(r.get('high',0)),str(r.get('low',0)),str(int(r.get('isPair',False))),str(start),str(len(source) if count is None else count),str(length-offset if capacity is None else capacity)]));groups+=1+int(op in {'W','SW'})+int('remaining' in r)
 for pid,profile in enumerate(j['profiles']):
  specs.append('\t'.join([str(int(profile['bigEndian'])),csv(profile['replacement'])]))
  for r in profile['rows']:
   events.append('\t'.join(['N',str(pid),str(int(r['stateful']))]))
   if r['stateful']:action('SW',r['seed'],16,0,False,r['seedResult'],r['seedAfter'])
   if r['countBefore']:action('Q',r['source'],-1,0,r['flush'],r['countResult'],None,start=r['start'],count=r['count'])
   action('W',r['source'],len(r['after']),r['offset'],r['flush'],r['writeResult'],r['after'],start=r['start'],count=r['count'],capacity=r['capacity']);action('W',[],16,0,True,r['tailResult'],r['tailAfter'])
   for step in r['buffer']:action({'remaining':'M','next':'B','previous':'P'}[step['operation']],[],-1,0,True,step['result'],None)
 assert groups==208100,groups
 states=work/'profiles.tsv';states.write_text('\n'.join(specs)+'\n',encoding='ascii');vectors=work/'events.tsv';vectors.write_text('\n'.join(events)+'\n',encoding='ascii');component=Path(__file__).with_name('unicode-encoder-returned-replacement-spans-probe.java');source=work/'UnicodeEncoderReturnedReplacementSpansProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeEncoderReturnedReplacementSpansProbe',str(states),str(vectors)],capture_output=True,text=True,timeout=60);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,returnedNativeEncoderContexts=13680,originalBoundedNoReturnRowsExcluded=j['originalBoundedNoReturnRowsExcluded'],oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),referenceSha256=j['inputSha256'],consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='ALL_HEAP_SPAN_COUNTERPARTS_OF_SELECTED_RETURNED_ENCODER_REPLACEMENT_CONTEXTS_ONLY; ORIGINAL_NO_RETURN_OUTCOMES_PRODUCT_LIVENESS_POLICY_CUSTOM_CALLBACKS_FULL_ABI_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'unicode-encoder-returned-replacement-spans-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS returned encoder replacement spans: {groups} comparisons across all 13680 returned contexts; original no-return contexts unqualified')
if __name__=='__main__':main()
