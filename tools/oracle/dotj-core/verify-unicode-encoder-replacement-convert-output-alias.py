"""Compare all output carrier counterparts of returned selected encoder replacement Convert contexts."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'unicode-encoder-replacement-convert-output-alias-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-unicode-encoder-replacement-convert-output-alias-contract.ps1').read_bytes()).hexdigest();assert len(j['profiles'])==18 and j['basisReturnedContexts']==8960 and j['nativeCases']==35840 and j['sharedOutputCases']==17920 and j['originalBoundedNoReturnRowsExcluded']==256
 refPath=EVIDENCE/'unicode-encoder-replacement-convert-contract-v10.0.12.json';reference=json.loads(refPath.read_text());assert j['inputSha256']==hashlib.sha256(refPath.read_bytes()).hexdigest();originals={entry['caseId']:(pid,entry['row']) for pid,p in enumerate(reference['profiles']) for entry in p['rows'] if entry['status']=='RETURNED'};assert len(originals)==8960;seen=set()
 for pid,profile in enumerate(j['profiles']):
  assert profile['bigEndian']==reference['profiles'][pid]['bigEndian'] and profile['replacement']==reference['profiles'][pid]['replacement']
  for row in profile['rows']:
   cid=row['basisCaseId'];key=(cid,row['span'],row['alias']);assert cid in originals and key not in seen;seen.add(key);oldPid,old=originals[cid];assert oldPid==pid
   for key in ['seed','source','start','count','flush','capacity','offset']:assert row[key]==old[key]
   assert row['after'][:row['offset']]==[99]*row['offset'] and row['after'][row['offset']+row['capacity']:]==[99]*3
 assert seen=={(cid,span,alias) for cid in originals for span in (False,True) for alias in (False,True)}
 distinctions=0
 for profile in j['profiles']:
  controls={(row['basisCaseId'],row['span']):row for row in profile['rows'] if not row['alias']}
  for row in profile['rows']:
   if not row['alias']:continue
   control=controls[row['basisCaseId'],row['span']]
   for field in ['seedResult','seedAfter','after','secondAfter','thirdAfter','buffer']:assert row[field]==control[field]
   for field in ['first','second','third']:
    actual=row[field];expected=control[field];assert actual['first']==expected['first'] and actual['second']==expected['first']
    for key in set(expected)-{'first','second'}:assert actual[key]==expected[key]
    distinctions+=int(expected['ok'] and expected['first']!=expected['second'])
 assert distinctions>0
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/unicode-encoder-replacement-convert-output-alias');work.mkdir(parents=True,exist_ok=True);specs=[];events=[];groups=0
 def action(op,source,index,count,length,offset,capacity,flush,r,after):
  nonlocal groups
  events.append('\t'.join([op,csv(source),str(index),str(count),str(length),str(offset),str(int(flush)),str(r.get('count',0)),csv(after),r.get('exception',''),base64.b64encode(r.get('message','').encode()).decode(),str(r.get('hResult',0)),r.get('paramName') or '~',str(r.get('unknown',0)),str(r.get('index',0)),str(r.get('high',0)),str(r.get('low',0)),str(int(r.get('isPair',False))),str(r.get('first',0)),str(r.get('second',0)),str(int(r.get('completed',False))),str(r.get('remaining','~')),str(capacity)]));groups+=1+int(op in {'W','C'})+int(op=='C')+int('remaining' in r)
 for pid,profile in enumerate(j['profiles']):
  specs.append('\t'.join([str(int(profile['bigEndian'])),csv(profile['replacement'])]))
  for row in profile['rows']:
   events.append('N\t'+str(pid)+'\t'+str(int(row['span']))+'\t'+str(int(row['alias'])));action('W',row['seed'],0,len(row['seed']),16,0,16,False,row['seedResult'],row['seedAfter']);action('C',row['source'],row['start'],row['count'],len(row['after']),row['offset'],row['capacity'],row['flush'],row['first'],row['after']);used=row['first']['first'] if row['first']['ok'] else 0;action('C',row['source'],row['start']+used,row['count']-used,32,0,32,True,row['second'],row['secondAfter']);action('C',[56320,55296],1,0,16,0,16,True,row['third'],row['thirdAfter'])
   for probe in row['buffer']:action({'remaining':'M','next':'B','previous':'P'}[probe['operation']],[],0,0,-1,0,0,True,probe['result'],None)
 states=work/'profiles.tsv';states.write_text('\n'.join(specs)+'\n',encoding='ascii');vectors=work/'events.tsv';vectors.write_text('\n'.join(events)+'\n',encoding='ascii');component=Path(__file__).with_name('unicode-encoder-replacement-convert-output-alias-probe.java');source=work/'UnicodeEncoderReplacementConvertOutputAliasProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeEncoderReplacementConvertOutputAliasProbe',str(states),str(vectors)],capture_output=True,text=True,timeout=60);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout;assert groups==788480,groups;print(f'PASS all returned encoder Convert span comparisons: {groups}')
 record=dict(schemaVersion=1,casesPassed=groups,returnedArrayContexts=8960,nativeCases=35840,sharedOutputCases=17920,counterDistinctions=distinctions,originalBoundedNoReturnRowsExcluded=256,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),referenceSha256=j['inputSha256'],consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='ALL_ARRAY_AND_HEAP_SPAN_SHARED_DISTINCT_OUTPUT_CELLS_OF_SELECTED_RETURNED_ENCODER_REPLACEMENT_CONVERT_CONTEXTS_ONLY; ORIGINAL_NO_RETURN_OUTCOMES_PRODUCT_LIVENESS_POLICY_CUSTOM_CALLBACKS_FULL_ABI_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'unicode-encoder-replacement-convert-output-alias-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS replacement Convert spans: {groups} groups across all 8960 returned contexts; original no-return contexts unqualified')

if __name__=='__main__':main()
