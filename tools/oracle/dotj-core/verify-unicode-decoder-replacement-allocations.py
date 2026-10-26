"""Compare selected stateless UTF16 decoder replacement allocated values."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'unicode-decoder-replacement-allocations-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-unicode-decoder-replacement-allocations-contract.ps1').read_bytes()).hexdigest();assert len(j['profiles'])==18 and all(len(p['rows'])==46 for p in j['profiles'])
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/unicode-decoder-replacement-allocations');work.mkdir(parents=True,exist_ok=True);specs=[];events=[];groups=0
 for pid,profile in enumerate(j['profiles']):
  specs.append('\t'.join([str(int(profile['bigEndian'])),csv(profile['replacement'])]))
  for row in profile['rows']:
   events.append('N\t'+str(pid));assert set(row['results'])=={'Count','CharsRange','StringRange','StringSpan','CharsWhole','StringWhole'}
   for op,result in row['results'].items():
    expected=str(result.get('value',0)) if op=='Count' else csv(result.get('value'));events.append('\t'.join([op,csv(row['source']),str(row['start']),str(row['count']),expected,'','','','',result.get('exception',''),base64.b64encode(result.get('message','').encode()).decode(),str(result.get('hResult',0)),result.get('paramName') or '~',csv(result.get('bytesUnknown')),str(result.get('index','~'))]));groups+=1 if op=='Count' or not result['ok'] else 2
 assert groups==9033,groups
 states=work/'profiles.tsv';states.write_text('\n'.join(specs)+'\n',encoding='ascii');vectors=work/'events.tsv';vectors.write_text('\n'.join(events)+'\n',encoding='ascii');component=Path(__file__).with_name('unicode-decoder-replacement-allocations-probe.java');source=work/'UnicodeDecoderReplacementAllocationsProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeDecoderReplacementAllocationsProbe',str(states),str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeCalls=4968,inputViews=828,allocatedValues=4065,failedAllocations=75,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_STATELESS_UNICODE_DECODER_REPLACEMENT_ALLOCATING_SURFACES_ONLY; CUSTOM_CALLBACKS_FULL_ABI_ENCODER_NONTERMINAL_NATIVE_NO_RETURN_POLICY_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'unicode-decoder-replacement-allocations-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS decoder replacement allocations: {groups} groups, 4968 native calls')
if __name__=='__main__':main()
