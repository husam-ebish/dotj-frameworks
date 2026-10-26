"""Compare selected stateless terminal UTF16 encoder replacement behavior."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'unicode-encoder-terminal-replacement-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-unicode-encoder-terminal-replacement-contract.ps1').read_bytes()).hexdigest();assert len(j['profiles'])==18 and all(len(p['rows'])==160 for p in j['profiles'])
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/unicode-encoder-terminal-replacement-edge');work.mkdir(parents=True,exist_ok=True);specs=[];events=[];groups=0
 def action(op,source,length,offset,flush,r,after):
  nonlocal groups
  events.append('\t'.join([op,csv(source),str(length),str(offset),str(int(flush)),str(r.get('count',0)),csv(after),str(r.get('remaining','~')),r.get('exception',''),base64.b64encode(r.get('message','').encode()).decode(),str(r.get('hResult',0)),r.get('paramName') or '~',str(r.get('unknown',0)),str(r.get('index',0)),str(r.get('high',0)),str(r.get('low',0)),str(int(r.get('isPair',False)))]));groups+=1+int(op=='W')+int('remaining' in r)
 for pid,profile in enumerate(j['profiles']):
  specs.append('\t'.join([str(int(profile['bigEndian'])),csv(profile['replacement'])]))
  for r in profile['rows']:
   assert r['encode'] and not r['stateful'];events.append('\t'.join(['N',str(pid),str(int(r['stateful']))]))
   if r['stateful']:action('W',r['seed'],16,0,False,r['seedResult'],r['seedAfter'])
   if r['countBefore']:action('Q',r['source'],-1,0,r['flush'],r['countResult'],None)
   action('W',r['source'],len(r['after']),r['offset'],r['flush'],r['writeResult'],r['after']);action('W',[],16,0,True,r['tailResult'],r['tailAfter'])
   for step in r['buffer']:action({'remaining':'M','next':'B','previous':'P'}[step['operation']],[],-1,0,True,step['result'],None)
 assert groups==12960,groups
 states=work/'profiles.tsv';states.write_text('\n'.join(specs)+'\n',encoding='ascii');vectors=work/'events.tsv';vectors.write_text('\n'.join(events)+'\n',encoding='ascii');component=Path(__file__).with_name('unicode-encoder-replacement-edge-probe.java');source=work/'UnicodeEncoderReplacementEdgeProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeEncoderReplacementEdgeProbe',str(states),str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeCases=2880,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_STATELESS_ENCODER_TERMINAL_STANDARD_REPLACEMENT_ARRAY_EDGES_ONLY; NONTERMINAL_INTERLEAVINGS_OWNED_STATE_SPANS_CONVERT_NATIVE_NO_RETURN_POLICY_ABI_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'unicode-encoder-terminal-replacement-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS encoder terminal replacement edges: {groups} groups, 2880 native cases')
if __name__=='__main__':main()
