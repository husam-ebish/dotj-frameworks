"""Compare Convert heap spans, NLS state and generic pointer-backed virtual dispatch."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(v):return ','.join(map(str,v))
def vector(q):
 r=q['result'];return [csv(q['units']),str(q['capacity']),str(q['offset']),str(int(q['flush'])),str(int(q['alias'])),str(int(r['ok'])),r.get('exception',''),str(r.get('hResult',0)),r.get('paramName') or 'null',csv(q['used']),str(int(q['completed'])),csv(q['destination'])]
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'stateful-convert-spans-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-stateful-convert-spans-contract.ps1').read_bytes()).hexdigest();assert len(j['nlsRows'])==5760 and len(j['genericRows'])==11520
 assert j['baselineSha256']==hashlib.sha256((EVIDENCE/'stateful-convert-contract-v10.0.12.json').read_bytes()).hexdigest();assert j['genericInputSha256']==hashlib.sha256((EVIDENCE/'generic-convert-arrays-contract-v10.0.12.json').read_bytes()).hexdigest()
 nls=[];calls=0
 for row in j['nlsRows']:
  nls.append('\t'.join(['R',row['direction'],str(row['profile'])]))
  for step in row['steps']:
   if step['kind']=='reset':nls.append('Z');continue
   nls.append('\t'.join(['A',*vector(step)]));calls+=1
 assert calls==20160
 generic=['\t'.join([row['direction'],str(row['multiplier']),str(row['countMode']),str(row['writeMode']),str(int(row['prefill'])),*vector(row['call']),';'.join(csv(t) for t in row['trace'])]) for row in j['genericRows']]
 assert any(row['call']['result'].get('exception')=='System.IndexOutOfRangeException' for row in j['genericRows'])
 assert any(any(t[5]<17 for t in row['trace']) and len(row['call']['units'])==17 for row in j['genericRows'])
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/stateful-convert-spans');work.mkdir(parents=True,exist_ok=True);nlsPath=work/'nls.tsv';nlsPath.write_text('\n'.join(nls)+'\n',encoding='ascii');genPath=work/'generic.tsv';genPath.write_text('\n'.join(generic)+'\n',encoding='ascii');source=work/'StatefulConvertSpansProbe.java';source.write_bytes(Path(__file__).with_name('stateful-convert-spans-probe.java').read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'StatefulConvertSpansProbe',str(nlsPath),str(genPath)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();groups=calls*4+11520*5;assert f'groups={groups}' in result.stdout
 rejects=[('EncoderInput','Encoding.get_UTF8().GetEncoder().Convert(ReadOnlySpan.OfUtf8Bytes(new byte[0]),Span.OfUtf8Bytes(new byte[0]),true,new int[1],new int[1],new boolean[1]);'),('EncoderOutput','Encoding.get_UTF8().GetEncoder().Convert(ReadOnlySpan.OfChars(new char[0]),Span.OfChars(new char[0]),true,new int[1],new int[1],new boolean[1]);'),('DecoderInput','Encoding.get_UTF8().GetDecoder().Convert(ReadOnlySpan.OfChars(new char[0]),Span.OfChars(new char[0]),true,new int[1],new int[1],new boolean[1]);'),('DecoderOutput','Encoding.get_UTF8().GetDecoder().Convert(ReadOnlySpan.OfUtf8Bytes(new byte[0]),Span.OfUtf8Bytes(new byte[0]),true,new int[1],new int[1],new boolean[1]);')]
 for name,body in rejects:
  bad=work/('Bad'+name+'.java');bad.write_text('import System.Text.*;import System.ReadOnlySpan;import System.Span;class Bad'+name+'{void check(){'+body+'}}',encoding='utf-8',newline='\n');result=subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(bad)],capture_output=True,text=True);assert result.returncode!=0 and ('incompatible types' in result.stderr or 'no suitable method' in result.stderr)
 record=dict(schemaVersion=1,casesPassed=groups,nativeNlsSequences=5760,nativeNlsConvertCalls=calls,nativeGenericCases=11520,wrongCarrierCompileRejections=4,genericArrayConvertOverrideBypassed=True,callbackArrayLengthsClampingAndFailureCopyControls=True,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_HEAP_CONVERT_SPANS_ONLY; DIRECT_POINTER_OVERRIDES_REF_STRUCT_LIFETIMES_REENTRANCY_FULL_METADATA_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'stateful-convert-spans-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print(f'PASS Convert spans: {groups} groups; NLS/generic dispatch and four carrier compile rejections')
if __name__=='__main__':main()
