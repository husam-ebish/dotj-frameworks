"""Compare owned UTF16 arrays against pinned core and range/capacity native packets."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
CORE='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
def csv(v):return '~' if v is None else ','.join(map(str,v))
def b64(s):return base64.b64encode(s.encode('utf-8')).decode('ascii')
def error(f):
 f=f or {};return [f.get('type',''),b64(f.get('message','')),str(f.get('hResult',0)),f.get('paramName') or '~',str(f.get('index','~')),str(f.get('charUnknown','~')),str(f.get('high','~')),str(f.get('low','~')),str(int(f['isPair'])) if 'isPair' in f else '~',csv(f.get('bytes')),str(int('actualValue' in f)),str(f['actualValue']) if f.get('actualValue') is not None else '~']
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 paths=[EVIDENCE/'unicode-encoding-plan-contract-v10.0.12.json',EVIDENCE/'unicode-encoding-arrays-contract-v10.0.12.json'];j,k=[json.loads(p.read_text(encoding='utf-8')) for p in paths]
 for v,name in [(j,'plan'),(k,'arrays')]:
  assert v['runtimeVersion']=='10.0.12' and v['coreLibSha256']==CORE;assert v['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-unicode-encoding-'+name+'-contract.ps1').read_bytes()).hexdigest()
 assert k['factoryIdentities']==dict(little=True,big=True,littleCodePage=1200,bigCodePage=1201);assert [len(j[x]) for x in ['specs','rows','maximums','equalities']]==[18,1224,360,324] and len(k['rows'])==5616
 for x,y in zip(j['specs'],k['specs']):assert {v:z for v,z in x.items() if v not in ['hash','encoderHash','decoderHash']}=={v:z for v,z in y.items() if v not in ['hash','encoderHash','decoderHash']}
 assert {r['failure']['type'] for r in k['rows'] if r['failure']}=={'System.ArgumentException','System.ArgumentNullException','System.ArgumentOutOfRangeException','System.Text.EncoderFallbackException','System.Text.DecoderFallbackException'}
 assert not any(r['failure'] and any(x in r['failure']['message'] for x in ['Object of type','Parameter count mismatch']) for r in k['rows'])
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/unicode-encoding-arrays');work.mkdir(parents=True,exist_ok=True);specs=[]
 for s in j['specs']:specs.append('\t'.join([str(s['constructor']),str(int(s['bigEndian'])),str(int(s['bom'])),str(int(s['strict'])),str(int(s['custom'])),str(s['codePage']),str(int(s['readOnly'])),s['webName'],b64(s['encodingName']),str(int(s['singleByte'])),s['encoderFallback'],s['decoderFallback'],str(s['encoderMax']),str(s['decoderMax']),csv(s['preamble']),str(int(s['preambleIdentity']))]))
 states=work/'specs.tsv';states.write_text('\n'.join(specs)+'\n',encoding='ascii');lines=[]
 def row(op,state,units,index,count,offset,buffer,result,failure):
  kind='n' if isinstance(result,int) else 'a';lines.append('\t'.join([op,str(state),csv(units),str(index),str(count),str(offset),csv(buffer),kind,str(result) if kind=='n' else csv(result),*error(failure)]))
 for r in j['rows']:row('P_'+('E' if r['direction']=='encode' else 'D')+('C' if r['countOnly'] else 'B'),r['state'],r['input'],0,len(r['input']),0,None,r['result'],r['failure'])
 for r in j['maximums']:row('MB' if r['encode'] else 'MC',r['state'],None,0,r['count'],0,None,r['result'],r['failure'])
 for r in k['rows']:row(r['operation'],r['state'],r['input'],r['index'],r['count'],r['outputIndex'],r['buffer'],r['result'],r['failure'])
 vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');pairs=work/'pairs.tsv';pairs.write_text('\n'.join('\t'.join(str(int(r[v])) for v in ['left','right','equal']) for r in j['equalities'])+'\n',encoding='ascii');component=Path(__file__).with_name('unicode-encoding-arrays-probe.java');source=work/'UnicodeEncodingArraysProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'UnicodeEncodingArraysProbe',str(states),str(vectors),str(pairs)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert 'groups=12587' in result.stdout
 record=dict(schemaVersion=1,casesPassed=12587,nativeCoreRows=1908,nativeBoundaryRows=5616,nativeStates=18,oracleEvidence=paths[1].name,oracleSha256=hashlib.sha256(paths[1].read_bytes()).hexdigest(),coreOracleEvidence=paths[0].name,coreOracleSha256=hashlib.sha256(paths[0].read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_UNICODEENCODING_STATELESS_ARRAYS_ONLY; ARBITRARY_CUSTOM_FALLBACK_PROTOCOLS_SPANS_SPECIALIZED_STATEFUL_POINTER_ABI_SOURCE_ABI_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'unicode-encoding-arrays-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS UnicodeEncoding arrays: 1908 core rows, 5616 range/capacity rows, 18 states; 12587 groups')
if __name__=='__main__':main()
