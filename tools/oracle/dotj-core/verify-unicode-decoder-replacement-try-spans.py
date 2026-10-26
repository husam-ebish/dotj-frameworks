"""Compare selected stateless UTF16 decoder replacement TryGetChars heap spans."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'unicode-decoder-replacement-try-spans-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-unicode-decoder-replacement-try-spans-contract.ps1').read_bytes()).hexdigest();assert len(j['profiles'])==18 and all(len(p['rows'])==552 for p in j['profiles'])
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/unicode-decoder-replacement-try-spans');work.mkdir(parents=True,exist_ok=True);specs=[];events=[];groups=failures=small=0
 for pid,profile in enumerate(j['profiles']):
  specs.append('\t'.join([str(int(profile['bigEndian'])),csv(profile['replacement'])]));events.append('N\t'+str(pid))
  for row in profile['rows']:
   result=row['result'];assert len(row['after'])==row['offset']+row['capacity']+3 and row['after'][:row['offset']]==[99]*row['offset'] and row['after'][row['offset']+row['capacity']:]==[99]*3
   if result['ok']:
    assert result['success']==(row['required']<=row['capacity'])
    if not result['success']:assert row['written']==0 and row['after']==[99]*len(row['after']);small+=1
   else:failures+=1
   events.append('\t'.join([csv(row['source']),str(row['start']),str(row['count']),str(len(row['after'])),str(row['offset']),str(row['capacity']),str(int(result.get('success',False))),str(row['written']),csv(row['after']),result.get('exception',''),base64.b64encode(result.get('message','').encode()).decode(),str(result.get('hResult',0)),result.get('paramName') or '~',csv(result.get('bytesUnknown')),str(result.get('index','~'))]));groups+=3
 assert groups==29808,groups
 states=work/'profiles.tsv';states.write_text('\n'.join(specs)+'\n',encoding='ascii');vectors=work/'events.tsv';vectors.write_text('\n'.join(events)+'\n',encoding='ascii');component=Path(__file__).with_name('unicode-decoder-replacement-try-spans-probe.java');source=work/'UnicodeDecoderReplacementTrySpansProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeDecoderReplacementTrySpansProbe',str(states),str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeCalls=9936,tooSmallReturns=small,recursiveFailures=failures,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_STATELESS_UNICODE_DECODER_REPLACEMENT_TRY_HEAP_SPANS_ONLY; CUSTOM_CALLBACKS_FULL_ABI_ENCODER_NONTERMINAL_NATIVE_NO_RETURN_POLICY_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'unicode-decoder-replacement-try-spans-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS decoder replacement Try spans: {groups} groups, 9936 native calls')
if __name__=='__main__':main()
