"""Compare selected stateless terminal UTF16 encoder replacement heap spans."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'unicode-encoder-terminal-replacement-spans-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-unicode-encoder-terminal-replacement-spans-contract.ps1').read_bytes()).hexdigest();assert len(j['profiles'])==18 and all(len(p['rows'])==380 for p in j['profiles'])
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/unicode-encoder-terminal-replacement-spans');work.mkdir(parents=True,exist_ok=True);specs=[];events=[];groups=0
 def action(op,row,result):
  nonlocal groups
  events.append('\t'.join([op,csv(row['source']),str(row['start']),str(row['count']),str(len(row['after']) if op=='W' else -1),str(row['offset']),'1',str(result.get('count',0)),csv(row['after'] if op=='W' else None),result.get('exception',''),base64.b64encode(result.get('message','').encode()).decode(),str(result.get('hResult',0)),result.get('paramName') or '~',str(result.get('unknown',0)),str(result.get('index',0)),str(result.get('high',0)),str(result.get('low',0)),str(int(result.get('isPair',False))),str(row['capacity'])]));groups+=1+int(op=='W')
 for pid,profile in enumerate(j['profiles']):
  specs.append('\t'.join([str(int(profile['bigEndian'])),csv(profile['replacement'])]))
  for row in profile['rows']:
   assert len(row['after'])==row['offset']+row['capacity']+3 and row['after'][:row['offset']]==[99]*row['offset'] and row['after'][row['offset']+row['capacity']:]==[99]*3
   events.append('N\t'+str(pid))
   if row['countBefore']:action('Q',row,row['countResult'])
   action('W',row,row['writeResult'])
 assert groups==17100,groups
 states=work/'profiles.tsv';states.write_text('\n'.join(specs)+'\n',encoding='ascii');vectors=work/'events.tsv';vectors.write_text('\n'.join(events)+'\n',encoding='ascii');component=Path(__file__).with_name('unicode-encoder-terminal-replacement-spans-probe.java');source=work/'UnicodeEncoderTerminalReplacementSpansProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeEncoderTerminalReplacementSpansProbe',str(states),str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeCases=6840,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_STATELESS_ENCODER_TERMINAL_REPLACEMENT_HEAP_SPANS_ONLY; NONTERMINAL_INTERLEAVINGS_OWNED_STATE_CONVERT_NATIVE_NO_RETURN_POLICY_ABI_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'unicode-encoder-terminal-replacement-spans-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS encoder terminal replacement spans: {groups} groups, 6840 native cases')
if __name__=='__main__':main()
