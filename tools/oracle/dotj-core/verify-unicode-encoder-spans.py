"""Compare specialized UTF16 encoder heap spans and post-call carry state."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def b64(s):return base64.b64encode(s.encode('utf-8')).decode('ascii')
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'unicode-encoder-spans-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-unicode-encoder-spans-contract.ps1').read_bytes()).hexdigest();assert len(j['profiles'])==10 and len(j['inputs'])==17 and all(len(p['rows'])==2064 for p in j['profiles']);assert {x['exception'] for p in j['profiles'] for r in p['rows'] for key in ['countResult','writeResult','tailResult'] if not (x:=r[key])['ok']}=={'System.ArgumentException','System.Text.EncoderFallbackException'}
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/unicode-encoder-spans');work.mkdir(parents=True,exist_ok=True);specs=[];events=[];groups=0
 def action(op,source,index,count,length,offset,flush,result,after,capacity):
  nonlocal groups
  events.append('\t'.join([op,csv(source),str(index),str(count),str(length),str(offset),str(int(flush)),str(result.get('count',0)),csv(after),result.get('exception',''),b64(result.get('message','')),str(result.get('hResult',0)),result.get('paramName') or '~',str(result.get('unknown','~')),str(result.get('index','~')),str(result.get('high','~')),str(result.get('low','~')),str(int(result['isPair'])) if 'isPair' in result else '~',str(capacity)]));groups+=1 if op=='SC' else 2
 for pid,p in enumerate(j['profiles']):
  c=p['config'];specs.append('\t'.join([str(int(c['bigEndian'])),str(int(c['strict'])),csv(c['replacement'])]))
  for r in p['rows']:
   events.append('N\t'+str(pid))
   if r['pending']:action('W',[55296],0,1,0,0,False,dict(ok=True,count=0),[],0)
   source=[56320]+j['inputs'][r['sourceId']]+[55296];action('SC',source,r['start'],r['count'],0,0,r['flush'],r['countResult'],None,0);action('SW',source,r['start'],r['count'],len(r['after']),r['offset'],r['flush'],r['writeResult'],r['after'],r['capacity']);action('W',[],0,0,16,0,True,r['tailResult'],r['tailAfter'],16)
 assert groups==123840
 states=work/'profiles.tsv';states.write_text('\n'.join(specs)+'\n',encoding='ascii');vectors=work/'events.tsv';vectors.write_text('\n'.join(events)+'\n',encoding='ascii');component=Path(__file__).with_name('unicode-encoder-spans-probe.java');source=work/'UnicodeEncoderSpansProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeEncoderSpansProbe',str(states),str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeCases=20640,nativeProfiles=10,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_UNICODE_ENCODER_HEAP_SPANS_AND_CARRY_TAILS_ONLY; ARBITRARY_FALLBACK_BUFFERS_CONVERT_POINTER_BYREF_SOURCE_ABI_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'unicode-encoder-spans-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS Unicode encoder spans: {groups} groups, 20640 native cases')
if __name__=='__main__':main()
