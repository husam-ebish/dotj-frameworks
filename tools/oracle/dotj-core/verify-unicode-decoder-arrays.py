"""Compare selected owned UTF16 decoder array carry, counts/writes, reset and guards."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'unicode-decoder-state-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-unicode-decoder-state-contract.ps1').read_bytes()).hexdigest();assert len(j['profiles'])==10 and all((len(p['rows']),len(p['capacityRows']),len(p['resetRows']),len(p['guards']))==(1164,2448,36,96) for p in j['profiles'])
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/unicode-decoder-arrays');work.mkdir(parents=True,exist_ok=True);specs=[];events=[];groups=50
 def action(op,source,index,count,length,offset,flush,r,after,skip=False):
  nonlocal groups
  events.append('\t'.join([op,csv(source),str(index),str(count),str(length),str(offset),str(int(flush)),str(r.get('count',0)),csv(after),r.get('exception',''),base64.b64encode(r.get('message','').encode()).decode(),str(r.get('hResult',0)),r.get('paramName') or '~',csv(r.get('unknown')),str(r.get('index','~')),str(int(skip))]));groups+=1+int(op=='W' and not skip)
 for pid,profile in enumerate(j['profiles']):
  c=profile['config'];specs.append('\t'.join([str(int(c['bigEndian'])),str(int(c['strict'])),csv(c['replacement'])]+[str(int(profile[k])) for k in ['freshInstances','initialFallbackShared','detachedAfterOwnerChange','freshUsesOwner','ownerUnchanged']]))
  for row in profile['rows']:
   events.append('N\t'+str(pid));source=j['textInputs'][row['sourceId']];split=row['split'];blocks=[source[:split],source[split:],[]]
   for step in row['steps']:
    data=blocks[step['block']];action('Q' if step['operation']=='Count' else 'W',data,0,len(data),20,1,step['flush'],step['result'],step['after'])
  for row in profile['capacityRows']:
   events.append('N\t'+str(pid));seed=profile['seeds'][row['seedId']];action('W',seed,0,len(seed),8,0,False,row['seedResult'],row['seedAfter']);data=j['capacityInputs'][row['sourceId']];source=[33]+data+[35];action('Q',source,1,len(data),-1,0,row['flush'],row['countResult'],None);action('W',source,1,len(data),len(row['after']),row['offset'],row['flush'],row['writeResult'],row['after']);action('W',[],0,0,16,0,True,row['tailResult'],row['tailAfter'])
  for row in profile['resetRows']:
   events.append('N\t'+str(pid));seed=profile['seeds'][row['seedId']];action('W',seed,0,len(seed),8,0,False,row['seedResult'],None,True)
   if row['fallback']:events.append('F\t'+str(row['fallback']));groups+=1
   if row['reset']:events.append('R');groups+=1
   action('Q',[],0,0,-1,0,True,row['countResult'],None);action('W',[],0,0,16,0,True,row['writeResult'],row['after'])
  for g in profile['guards']:
   events.append('N\t'+str(pid));action('Q' if g['operation']=='Count' else 'W',None if g['nullSource'] else [65,0],g['index'],g['count'],-1 if g['nullDestination'] else 2,g['charIndex'],True,g['result'],g['after'])
 assert groups==279470,groups
 states=work/'profiles.tsv';states.write_text('\n'.join(specs)+'\n',encoding='ascii');vectors=work/'events.tsv';vectors.write_text('\n'.join(events)+'\n',encoding='ascii');component=Path(__file__).with_name('unicode-decoder-arrays-probe.java');source=work/'UnicodeDecoderArraysProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeDecoderArraysProbe',str(states),str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeCalls=169800,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_UNICODE_DECODER_ARRAY_STATE_ONLY; CONVERT_SPANS_CUSTOM_BUFFERS_POINTER_BYREF_SOURCE_ABI_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'unicode-decoder-arrays-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS Unicode decoder arrays: {groups} groups, 169800 native calls')
if __name__=='__main__':main()
