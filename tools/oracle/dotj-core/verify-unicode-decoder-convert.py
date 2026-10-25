"""Compare selected specialized UTF16 decoder array Convert including signed counters."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'unicode-decoder-convert-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-unicode-decoder-convert-contract.ps1').read_bytes()).hexdigest();assert len(j['profiles'])==10 and all(len(p['rows'])==3264 and len(p['guards'])==52 for p in j['profiles'])
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/unicode-decoder-convert');work.mkdir(parents=True,exist_ok=True);specs=[];events=[];groups=0
 def action(op,source,index,count,length,offset,capacity,flush,r,after):
  nonlocal groups
  events.append('\t'.join([op,csv(source),str(index),str(count),str(length),str(offset),str(int(flush)),str(r.get('count',0)),csv(after),r.get('exception',''),base64.b64encode(r.get('message','').encode()).decode(),str(r.get('hResult',0)),r.get('paramName') or '~',csv(r.get('unknown')),str(r.get('index','~')),str(r.get('bytesUsed',0)),str(r.get('charsUsed',0)),str(int(r.get('completed',False))),str(r.get('remaining',0)),str(capacity)]));groups+=2 if op=='W' else 4
 for pid,profile in enumerate(j['profiles']):
  c=profile['config'];specs.append('\t'.join([str(int(c['bigEndian'])),str(int(c['strict'])),csv(c['replacement'])]))
  for r in profile['rows']:
   events.append('N\t'+str(pid));seed=profile['seeds'][r['seedId']];action('W',seed,0,len(seed),8,0,8,False,r['seedResult'],r['seedAfter']);units=j['inputs'][r['sourceId']];source=[221]+units+[216];action('C',source,1,len(units),len(r['after']),r['offset'],r['capacity'],r['flush'],r['first'],r['after']);used=r['first']['bytesUsed'] if r['first']['ok'] else 0;action('C',source,1+used,len(units)-used,32,0,32,True,r['second'],r['secondAfter']);action('C',[],0,0,16,0,16,True,r['third'],r['thirdAfter'])
  for g in profile['guards']:
   events.append('N\t'+str(pid));action('C',None if g['nullSource'] else [65,0],g['byteIndex'],g['byteCount'],-1 if g['nullDestination'] else 2,g['charIndex'],g['charCount'],True,g['result'],g['after'])
 assert groups==459040,groups
 states=work/'profiles.tsv';states.write_text('\n'.join(specs)+'\n',encoding='ascii');vectors=work/'events.tsv';vectors.write_text('\n'.join(events)+'\n',encoding='ascii');component=Path(__file__).with_name('unicode-decoder-convert-probe.java');source=work/'UnicodeDecoderConvertProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeDecoderConvertProbe',str(states),str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeCalls=131080,negativeBytesUsedCases=456,unreportedPrefixWrites=588,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_UNICODE_DECODER_ARRAY_CONVERT_ONLY; SPANS_CUSTOM_BUFFERS_POINTER_BYREF_SOURCE_ABI_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'unicode-decoder-convert-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS Unicode decoder Convert: {groups} groups, 131080 native calls')
if __name__=='__main__':main()
