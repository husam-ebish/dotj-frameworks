"""Compare selected UTF16 encoder cross-method and fallback-ownership state."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'unicode-encoder-interleaving-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-unicode-encoder-interleaving-contract.ps1').read_bytes()).hexdigest();assert len(j['profiles'])==10 and all(len(p['rows'])==1536 for p in j['profiles'])
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/unicode-encoder-interleaving');work.mkdir(parents=True,exist_ok=True);specs=[];events=[];groups=0
 def action(op,source,index,count,length,offset,capacity,flush,r,after,state=None):
  nonlocal groups
  stateFields=['~']*5 if state is None else [state['fallbackType'],csv(state['replacement']),state['ownerType'],csv(state['ownerReplacement']),str(int(state['sharedOwner']))]
  events.append('\t'.join([op,csv(source),str(index),str(count),str(length),str(offset),str(int(flush)),str(r.get('count',0)),csv(after),r.get('exception',''),base64.b64encode(r.get('message','').encode()).decode(),str(r.get('hResult',0)),r.get('paramName') or '~',str(r.get('unknown','~')),str(r.get('index','~')),str(r.get('high','~')),str(r.get('low','~')),str(int(r['isPair'])) if 'isPair' in r else '~',str(r.get('charsUsed',0)),str(r.get('bytesUsed',0)),str(int(r.get('completed',False))),str(r.get('remaining','~')),str(capacity)]+stateFields));groups+=1+int(op in {'W','V'})+int(op=='V')+int('remaining' in r)+int(state is not None)
 operations={'Count':'Q','CountEmpty':'Q','Bytes':'W','BytesEmpty':'W','Reset':'R','SetEmpty':'FE','SetAB':'FA','SetStrict':'FX','OwnerStrict':'OX','BufferNext':'BN','BufferPrevious':'BP','BufferReset':'BR'}
 for pid,profile in enumerate(j['profiles']):
  c=profile['config'];specs.append('\t'.join([str(int(c['bigEndian'])),str(int(c['strict'])),csv(c['replacement'])]))
  for r in profile['rows']:
   events.append('N\t'+str(pid))
   if r['pending']:action('W',[55296],0,1,0,0,0,False,dict(ok=True,count=0),[])
   units=j['inputs'][r['sourceId']];action('V',units,0,len(units),len(r['after']),1,r['capacity'],r['flush'],r['first'],r['after'])
   name=r['operation'];op=operations[name];source=[65,55296] if name in {'Count','Bytes'} else [];action(op,source,0,len(source),18,1,17,True,r['operationResult'],r['operationAfter'],r['state'])
   action('Q',[],0,0,-1,0,0,True,r['countResult'],None);action('W',[],0,0,18,1,17,True,r['writeResult'],r['writeAfter'])
   for probe in r['bufferResults']:action(operations[probe['operation']],[],0,0,-1,0,0,True,probe['result'],None)
   action('V',[56320,65],0,2,20,1,16,True,r['lastResult'],r['lastAfter'])
 assert groups==448000,groups
 states=work/'profiles.tsv';states.write_text('\n'.join(specs)+'\n',encoding='ascii');vectors=work/'events.tsv';vectors.write_text('\n'.join(events)+'\n',encoding='ascii');component=Path(__file__).with_name('unicode-encoder-interleaving-probe.java');source=work/'UnicodeEncoderInterleavingProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeEncoderInterleavingProbe',str(states),str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,sequences=15360,nativeCalls=168960,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_UNICODE_ENCODER_ARRAY_INTERLEAVING_AND_REPLACEMENT_BUFFER_OWNERSHIP_ONLY; ARBITRARY_CUSTOM_FALLBACK_SPAN_INTERLEAVING_POINTER_BYREF_SOURCE_ABI_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'unicode-encoder-interleaving-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS Unicode encoder interleaving: {groups} groups, 168960 native calls')
if __name__=='__main__':main()
