"""Compare legal shared and distinct output cells for specialized Unicode Convert."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'unicode-convert-output-alias-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-unicode-convert-output-alias-contract.ps1').read_bytes()).hexdigest();assert len(j['profiles'])==10 and all(len(p['rows'])==4224 for p in j['profiles'])
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/unicode-convert-output-alias');work.mkdir(parents=True,exist_ok=True);specs=[];events=[];groups=0
 def action(op,source,length,offset,capacity,flush,r,after):
  nonlocal groups
  events.append('\t'.join([op,csv(source),str(len(source)),str(length),str(offset),str(capacity),str(int(flush)),str(r.get('count',0)),csv(after),r.get('exception',''),base64.b64encode(r.get('message','').encode()).decode(),str(r.get('hResult',0)),r.get('paramName') or '~',str(r.get('unknown','~')),str(r.get('index','~')),str(r.get('high','~')),str(r.get('low','~')),str(int(r['isPair'])) if 'isPair' in r else '~',csv(r.get('bytesUnknown')),str(r.get('first',0)),str(r.get('second',0)),str(int(r.get('completed',False))),str(r.get('remaining',0))]));groups+=2 if op=='W' else 4
 for pid,profile in enumerate(j['profiles']):
  c=profile['config'];specs.append('\t'.join([str(int(c['bigEndian'])),str(int(c['strict'])),csv(c['replacement'])]))
  for r in profile['rows']:
   events.append('\t'.join(['N',str(pid),str(int(r['encode'])),str(int(r['span'])),str(int(r['alias']))]));action('W',r['seed'],16,0,16,False,r['seedResult'],r['seedAfter']);action('C',r['source'],len(r['after']),r['offset'],r['capacity'],r['flush'],r['first'],r['after']);action('C',[],32,0,32,True,r['tailResult'],r['tailAfter']);events.append('R');groups+=1;action('C',r['source'],32,0,32,True,r['lastResult'],r['lastAfter'])
 assert groups==633600,groups
 states=work/'profiles.tsv';states.write_text('\n'.join(specs)+'\n',encoding='ascii');vectors=work/'events.tsv';vectors.write_text('\n'.join(events)+'\n',encoding='ascii');component=Path(__file__).with_name('unicode-convert-output-alias-probe.java');source=work/'UnicodeConvertOutputAliasProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeConvertOutputAliasProbe',str(states),str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeCases=42240,sharedCases=21120,counterDistinctions=29208,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_SPECIALIZED_UNICODE_CONVERT_OUTPUT_CELL_ALIASING_ONLY; UNSAFE_POINTER_LIFETIMES_FULL_BYREF_SOURCE_ABI_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'unicode-convert-output-alias-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS Unicode Convert output aliases: {groups} groups, 42240 native cases')
if __name__=='__main__':main()
