"""Compare selected stateless encoder allocations with known returned reference counts."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'unicode-encoder-returned-replacement-allocations-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-unicode-encoder-returned-replacement-allocations-contract.ps1').read_bytes()).hexdigest();assert len(j['profiles'])==18 and j['selectedKnownReturnedStatelessCountContexts']==138 and j['unselectedStatelessSourceContexts']==6
 refPath=EVIDENCE/'unicode-replacement-edge-contract-v10.0.12.json';ref=json.loads(refPath.read_text());assert j['inputSha256']==hashlib.sha256(refPath.read_bytes()).hexdigest();originals={};ids={}
 for pid,profile in enumerate(ref['profiles']):
  for entry in profile['rows']:
   if entry['status']=='RETURNED':
    old=entry['row']
    if old['encode'] and not old['stateful'] and old['countBefore']:
     key=(pid,tuple(old['source']))
     if key not in originals:originals[key]=(entry['caseId'],old)
     ids[entry['caseId']]=(pid,old)
 assert len(originals)==138;seen=set();work=Path('D:/AI/Implementation/dotj Frameworks/verification/unicode-encoder-returned-replacement-allocations');work.mkdir(parents=True,exist_ok=True);specs=[];events=[];groups=failures=allocated=0
 for pid,profile in enumerate(j['profiles']):
  assert profile['bigEndian']==ref['profiles'][pid]['bigEndian'] and profile['replacement']==ref['profiles'][pid]['replacement'];specs.append('\t'.join([str(int(profile['bigEndian'])),csv(profile['replacement'])]))
  for row in profile['rows']:
   assert row['basisCaseId'] in ids;oldPid,old=ids[row['basisCaseId']];key=(pid,tuple(old['source']));assert oldPid==pid and key not in seen and row['basisCaseId']==originals[key][0];seen.add(key);assert row['source']==[56320]+old['source']+[55296] and row['start']==1 and row['count']==len(old['source']) and row['referenceCountResult']==old['countResult'];expected=dict(old['countResult'])
   if expected['ok']:expected['value']=expected.pop('count')
   assert row['results']['CountArray']==expected and set(row['results'])==set(j['operations'])=={'CountArray','CountString','BytesArrayRange','BytesArrayWhole','BytesStringRange','BytesStringWhole'};events.append('N\t'+str(pid))
   for op,result in row['results'].items():
    isCount=op.startswith('Count');expectedValue=str(result.get('value',0)) if isCount else csv(result.get('value'));events.append('\t'.join([op,csv(row['source']),str(row['start']),str(row['count']),expectedValue,'','','','',result.get('exception',''),base64.b64encode(result.get('message','').encode()).decode(),str(result.get('hResult',0)),result.get('paramName') or '~',str(result.get('unknown',0)),str(result.get('index',0)),str(result.get('high',0)),str(result.get('low',0)),str(int(result.get('isPair',False)))]));groups+=1 if isCount or not result['ok'] else 2;failures+=int(not result['ok']);allocated+=int(not isCount and result['ok'])
 assert seen==set(originals) and groups==1364,groups
 states=work/'profiles.tsv';states.write_text('\n'.join(specs)+'\n',encoding='ascii');vectors=work/'events.tsv';vectors.write_text('\n'.join(events)+'\n',encoding='ascii');component=Path(__file__).with_name('unicode-encoder-returned-replacement-allocations-probe.java');source=work/'UnicodeEncoderReturnedReplacementAllocationsProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeEncoderReturnedReplacementAllocationsProbe',str(states),str(vectors)],capture_output=True,text=True,timeout=60);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeCalls=828,selectedKnownReturnedCountContexts=138,unselectedStatelessSourceContexts=6,returnedAllocatedValues=allocated,exceptionOutcomes=failures,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),referenceSha256=j['inputSha256'],consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='STATELESS_ENCODER_ALLOCATIONS_FOR_ALL_SELECTED_KNOWN_RETURNED_COUNT_CONTEXTS_ONLY; UNSELECTED_NO_RETURN_OUTCOMES_PRODUCT_LIVENESS_POLICY_CUSTOM_CALLBACKS_FULL_ABI_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'unicode-encoder-returned-replacement-allocations-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS returned encoder allocations: {groups} groups, 138 count contexts, 828 native calls')
if __name__=='__main__':main()
