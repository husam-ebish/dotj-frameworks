"""Check native fallback exception construction and UTF-8 null parameters."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def literal(v):return 'null' if v is None else json.dumps(v)
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 oracle_path=EVIDENCE/'utf8-exception-boundaries-contract-v10.0.12.json';j=json.loads(oracle_path.read_text(encoding='utf-8'))
 assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'
 assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-utf8-exception-boundaries-contract.ps1').read_bytes()).hexdigest()
 assert len(j['constructors'])==18 and len(j['nullControls'])==10
 cases=[]
 for row in j['constructors']:
  r=row['result'];owner=row['direction']+'FallbackException';kind=row['kind'];setup='';expr={'default':'()','null-message':'((String)null)','empty-message':'("")','message':'("custom payload")','inner':'("custom payload",new Exception("inner payload"))'}.get(kind)
  if kind=='bytes-index':
   assert row['preservesReference'];setup='Byte[] bytes='+('null' if row['nullBytes'] else 'new Byte[]{new Byte(128),new Byte(255)}')+';';expr='("custom payload",bytes,'+str(row['index'])+')'
  checks=['Objects.equals(ex.get_Message(),'+literal(r['message'])+')','ex.get_HResult()=='+str(r['hResult']),'ex.get_ParamName()==null','Objects.equals(ex.get_InnerException()==null?null:ex.get_InnerException().get_Message(),'+literal(r['innerMessage'])+')','ex.get_Index()=='+str(r['index'])]
  if row['direction']=='Encoder':
   assert r['charUnknown']==r['charUnknownHigh']==r['charUnknownLow']==0 and not r['isUnknownSurrogate'];checks+=['ex.get_CharUnknown()==0','ex.get_CharUnknownHigh()==0','ex.get_CharUnknownLow()==0','!ex.IsUnknownSurrogate()']
  else:checks+=['ex.get_BytesUnknown()=='+('bytes' if kind=='bytes-index' else 'null')]
  cases.append('{'+setup+owner+' ex=new '+owner+expr+';check('+'&&'.join(checks)+','+str(len(cases))+');}')
 for row in j['nullControls']:
  r=row['result'];assert r['exception']=='System.ArgumentNullException';param='String' if row['method'] in ['GetBytes','GetByteCount'] else 'Byte[]'
  cases.append('{Encoding e=new UTF8Encoding(false,'+str(row['strict']).lower()+');try{e.'+row['method']+'(('+param+')null);throw new AssertionError("null accepted");}catch(ArgumentNullException ex){check(Objects.equals(ex.get_ParamName(),'+literal(r['paramName'])+')&&Objects.equals(ex.get_Message(),'+literal(r['message'])+')&&ex.get_HResult()=='+str(r['hResult'])+','+str(len(cases))+');}}')
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/utf8-exception-boundaries');work.mkdir(exist_ok=True);source=work/'Utf8ExceptionBoundaryProbe.java';source.write_text('import System.Text.*;import System.Byte;import System.Exception;import System.ArgumentNullException;import java.util.Objects;class Utf8ExceptionBoundaryProbe{static void check(boolean ok,int id){if(!ok)throw new AssertionError("case "+id);}public static void main(String[] args){\n'+'\n'.join(cases)+'}}',encoding='utf-8')
 subprocess.run(['javac','-Xmaxerrs','3','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'Utf8ExceptionBoundaryProbe'],check=True)
 record=dict(schemaVersion=1,casesPassed=len(cases),nativeConstructorControls=18,nativeNullControls=10,oracleEvidence=oracle_path.name,oracleSha256=hashlib.sha256(oracle_path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_CONSTRUCTOR_NULL_BOUNDARIES_ONLY; CONVERSION_MESSAGES_RANGE_STATEFUL_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN')
 (EVIDENCE/'utf8-exception-boundaries-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print('PASS UTF-8 exception/null boundaries: '+str(len(cases))+' controls')
if __name__=='__main__':main()
