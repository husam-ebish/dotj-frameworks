"""Compare decoder buffer transitions, null normalization and byte payload identity."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def b(v):return str(v).lower()
def q(v):return 'null' if v is None else json.dumps(v)
def array(v):return 'null' if v is None else 'bytes(new int[]{'+','.join(map(str,v))+'})'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'decoder-fallback-buffers-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'))
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-decoder-fallback-buffers-contract.ps1').read_bytes()).hexdigest()
 assert len(j['profiles'])==8 and all(len(p['steps'])==44 for p in j['profiles']);methods=[];group=0
 for profile in j['profiles']:
  assert profile['factoryDistinct'];n=profile['profile'];factory='new DecoderExceptionFallback()' if n==7 else 'new DecoderReplacementFallback(new String(new char[]{'+','.join('(char)'+str(v) for v in profile['replacementUnits'])+'}))';body=['DecoderFallback fallback='+factory+';DecoderFallbackBuffer buffer=fallback.CreateFallbackBuffer();check(buffer!=fallback.CreateFallbackBuffer(),'+str(group)+');'];group+=1
  for step in profile['steps']:
   action=step['action'];r=step['result'];unknown=j['byteInputs'][action[1]] if action[0]=='fallback' and action[1]>=0 else None;body.append('{Byte[] unknown='+array(unknown)+';check(buffer.get_Remaining()=='+str(step['remainingBefore'])+','+str(group)+');');group+=1
   call='buffer.Fallback(unknown,'+str(action[2])+')' if action[0]=='fallback' else {'remaining':'buffer.get_Remaining()','previous':'buffer.MovePrevious()','next':'buffer.GetNextChar()','reset':'buffer.Reset()'}[action[0]]
   if r['ok']:
    if action[0]=='reset':body.append(call+';check(true,'+str(group)+');')
    else:body.append('check('+call+'=='+(b(r['value']) if isinstance(r['value'],bool) else str(r['value']))+','+str(group)+');')
   else:
    checks=['ex.getClass().getName().equals('+q(r['exception'])+')','ex.get_HResult()=='+str(r['hResult']),'Objects.equals(ex.get_ParamName(),'+q(r['paramName'])+')']
    if 'index' in r:checks+=['((DecoderFallbackException)ex).get_Index()=='+str(r['index']),'Arrays.equals(values(((DecoderFallbackException)ex).get_BytesUnknown()),values('+array(r['bytesUnknown'])+'))','((((DecoderFallbackException)ex).get_BytesUnknown()==unknown)=='+b(r['bytesReferenceSame'])+')']
    body.append('try{'+call+';throw new AssertionError("expected fallback failure");}catch(ArgumentException ex){check('+'&&'.join(checks)+','+str(group)+');}')
   group+=1;body.append('check(buffer.get_Remaining()=='+str(step['remainingAfter'])+','+str(group)+');');group+=1;body.append('check(Arrays.equals(values(unknown),values('+array(step['bytesAfter'])+')),'+str(group)+');}');group+=1
  methods.append('static void run'+str(n)+'(){\n'+'\n'.join(body)+'\n}')
 assert group==1416
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/decoder-fallback-buffers');work.mkdir(exist_ok=True);source=work/'DecoderFallbackBufferProbe.java';source.write_text('import System.Text.*;import System.Byte;import System.ArgumentException;import java.util.Objects;import java.util.Arrays;class DecoderFallbackBufferProbe{static Byte[] bytes(int[] v){Byte[] r=new Byte[v.length];for(int i=0;i<v.length;i++)r[i]=new Byte(v[i]);return r;}static int[] values(Byte[] v){if(v==null)return null;int[] r=new int[v.length];for(int i=0;i<v.length;i++)r[i]=v[i].get_Value();return r;}static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}\n'+'\n'.join(methods)+'public static void main(String[] args){'+''.join('run'+str(i)+'();' for i in range(8))+'}}',encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'DecoderFallbackBufferProbe'],check=True)
 record=dict(schemaVersion=1,casesPassed=group,nativeProfiles=8,transitionsPerProfile=44,nativeInternalBufferTypes=[p['nativeBufferType'] for p in j['profiles']],nativeInternalRuntimeTypeQualified=False,oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_DECODER_BUFFER_STATE_AND_PAYLOADS_ONLY; MESSAGES_CUSTOMIZATION_FULL_METADATA_INTERNAL_RUNTIME_TYPE_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN')
 (EVIDENCE/'decoder-fallback-buffers-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS selected decoder fallback buffers: '+str(group)+' groups; 352 native transitions')
if __name__=='__main__':main()
