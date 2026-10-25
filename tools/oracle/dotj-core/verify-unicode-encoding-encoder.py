"""Compare selected UTF16 encoder carry, counts, writes, reset and fallback ownership."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def b64(s):return base64.b64encode(s.encode('utf-8')).decode('ascii')
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'unicode-encoding-encoder-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-unicode-encoding-encoder-contract.ps1').read_bytes()).hexdigest();assert len(j['profiles'])==10 and len(j['textInputs'])==130;assert sum(len(p['rows']) for p in j['profiles'])==11440;assert all(len(p['capacityRows'])==1040 and len(p['resetRows'])==36 for p in j['profiles'])
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/unicode-encoding-encoder');work.mkdir(parents=True,exist_ok=True);states=[];events=[];groups=20
 def begin(pid):events.append('N\t'+str(pid))
 def action(op,source,index,count,length,offset,flush,result,after):
  nonlocal groups
  events.append('\t'.join([op,csv(source),str(index),str(count),str(length),str(offset),str(int(flush)),str(result.get('count',0)),csv(after),result.get('exception',''),b64(result.get('message','')),str(result.get('hResult',0)),result.get('paramName') or '~',str(result.get('unknown','~')),str(result.get('index','~')),str(result.get('high','~')),str(result.get('low','~')),str(int(result['isPair'])) if 'isPair' in result else '~']));groups+=2 if op=='W' else 1
 def seed():action('W',[55296],0,1,0,0,False,dict(ok=True,count=0),[])
 for pid,p in enumerate(j['profiles']):
  c=p['config'];f=p['factoryOwnership'];assert f['result']['ok'];states.append('\t'.join([str(int(c['bigEndian'])),str(int(c['strict'])),csv(c['replacement']),str(int(p['freshInstances'])),str(int(p['fallbackSharedWithEncoding'])),str(int(f['encoderDetachedAfterOwnerChange'])),str(int(f['newEncoderUsesCurrentOwner'])),str(int(f['ownerUnchangedAfterEncoderChange'])),str(f['result']['count']),csv(f['after'])]))
  for r in p['rows']:
   begin(pid);text=j['textInputs'][r['sourceId']];blocks=[text[:r['split']],text[r['split']:],[]]
   for step in r['steps']:
    source=blocks[step['block']];op='C' if step['operation']=='Count' else 'W';action(op,source,0,len(source),24 if op=='W' else 0,1 if op=='W' else 0,step['flush'],step['result'],step['after'])
  for r in p['capacityRows']:
   begin(pid)
   if r['pending']:seed()
   source=p['capacityInputs'][r['sourceId']];full=[33]+source+[35];action('C',full,1,len(source),0,0,r['flush'],r['countResult'],None);action('W',full,1,len(source),r['offset']+r['capacity'],r['offset'],r['flush'],r['writeResult'],r['after']);action('W',[],0,0,16,0,True,r['tailResult'],r['tailAfter'])
  for r in p['resetRows']:
   begin(pid)
   if r['pending']:seed()
   if r['fallback']:events.append('S\t'+str(r['fallback']));groups+=1
   if r['reset']:assert r['resetResult']['ok'];events.append('R');groups+=1
   source=p['capacityInputs'][r['sourceId']];action('C',source,0,len(source),0,0,True,r['countResult'],None);action('W',source,0,len(source),16,0,True,r['writeResult'],r['after']);action('W',[],0,0,16,0,True,r['tailResult'],r['tailAfter'])
 specs=work/'profiles.tsv';specs.write_text('\n'.join(states)+'\n',encoding='ascii');vectors=work/'events.tsv';vectors.write_text('\n'.join(events)+'\n',encoding='ascii');component=Path(__file__).with_name('unicode-encoding-encoder-probe.java');source=work/'UnicodeEncodingEncoderProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeEncodingEncoderProbe',str(specs),str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativePartitionSequences=11440,nativePartitionSteps=68640,nativeCapacityCases=10400,nativeResetFallbackCases=360,nativeProfiles=10,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_UNICODEENCODING_ENCODER_ARRAY_CARRY_COUNTS_WRITES_RESET_CAPACITY_AND_FALLBACK_OWNERSHIP_ONLY; ARBITRARY_CUSTOM_BUFFERS_CONVERT_SPANS_POINTER_SOURCE_ABI_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'unicode-encoding-encoder-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS UnicodeEncoding encoder: {groups} groups; 11440 sequences, 10400 capacity cases, 360 reset/fallback cases')
if __name__=='__main__':main()
