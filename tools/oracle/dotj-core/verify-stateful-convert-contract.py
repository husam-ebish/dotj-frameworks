"""Audit the pinned native Convert baseline without claiming Java behavior parity."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'stateful-convert-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));checks=0
 def require(value):
  nonlocal checks
  checks+=1;assert value,f'Native baseline control {checks}'
 require(j['runtimeVersion']=='10.0.12');require(j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678');require(j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-stateful-convert-contract.ps1').read_bytes()).hexdigest());require(j['candidateBehaviorQualifiedByThisBaseline'] is False);require(j['outCapture']=='DIRECT_IL_CALL_WITH_LDELEMA_INTO_SENTINEL_INITIALIZED_HEAP_ARRAYS; NO_REFLECTION_COPYBACK_DEPENDENCE');require(len(j['rows'])==5760);require(len(j['publicDeclaredConvert'])==6)
 for owner in ['System.Text.Encoder','System.Text.Decoder']:
  methods=[m for m in j['publicDeclaredConvert'] if m['owner']==owner];require(len(methods)==3)
  for method in methods:require(method['returnType']=='System.Void');require([p['type'] for p in method['parameters'] if p['isOut']]==['System.Int32&','System.Int32&','System.Boolean&'])
 converts=partials=failures=partial_failures=resets=0
 for row in j['rows']:
  require(row['direction'] in ['encoder','decoder']);require(row['runtimeStateType']==('System.Text.EncoderNLS' if row['direction']=='encoder' else 'System.Text.DecoderNLS'));require(len(row['steps'])==4+int(row['pending']));require(row['steps'][-2]['kind']=='reset');require(row['steps'][-1]['result']['ok'] and row['steps'][-1]['used']==[0,0] and row['steps'][-1]['completed']);require(row['steps'][-1]['destination']==[99]*11)
  resets+=1
  for step in row['steps']:
   if step['kind']=='reset':continue
   converts+=1;require(len(step['used'])==2 and all(type(v) is int for v in step['used']));require(type(step['completed']) is bool);require(len(step['destination'])==step['capacity']+step['offset']+3);require(step['destination'][:step['offset']]==[99]*step['offset']);require(step['destination'][step['offset']+step['capacity']:]==[99]*3)
   if step['result']['ok']:
    require(0<=step['used'][0]<=len(step['units']));require(0<=step['used'][1]<=step['capacity']);require(not step['completed'] or step['used'][0]==len(step['units']));partials+=int(not step['completed'])
   else:
    failures+=1;require(step['result']['exception'] in ['System.ArgumentException','System.Text.EncoderFallbackException','System.Text.DecoderFallbackException']);require(type(step['result']['hResult']) is int);partial_failures+=int(any(v!=99 for v in step['destination']))
 require(converts==20160);require(partials==472);require(failures==3584);require(partial_failures>0);require(resets==5760)
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/stateful-convert-contract');work.mkdir(parents=True,exist_ok=True);source=work/'StatefulConvertAvailability.java';source.write_text('''import System.Text.*;import java.lang.reflect.*;class StatefulConvertAvailability{public static void main(String[] args){Encoding e=Encoding.get_UTF8();Encoder a=e.GetEncoder();Decoder b=e.GetDecoder();if(a==null||b==null||a==e.GetEncoder()||b==e.GetDecoder())throw new AssertionError();for(Class<?> type:new Class<?>[]{Encoder.class,Decoder.class}){int count=0;for(Method m:type.getDeclaredMethods())if(Modifier.isPublic(m.getModifiers())&&m.getName().equals("Convert"))count++;java.lang.System.out.println(type.getSimpleName()+"="+count);}}}''',encoding='utf-8');subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'StatefulConvertAvailability'],capture_output=True,text=True,check=True);availability={name:int(count) for name,count in re.findall(r'(Encoder|Decoder)=(\d+)',result.stdout)};require(set(availability)=={'Encoder','Decoder'})
 adjacency=EVIDENCE/'custom-stateful-decoder-source-adjacency-v10.0.12.json';adj=json.loads(adjacency.read_text(encoding='utf-8'));require({'Encoder.cs','EncoderNLS.cs','Decoder.cs','DecoderNLS.cs','Encoding.Internal.cs'}.issubset({Path(item['archiveMember']).name for item in adj['upstreamFiles']}))
 record=dict(schemaVersion=1,casesPassed=checks,nativeSequences=5760,nativeConvertCalls=converts,nativePartialSuccesses=partials,nativeFailures=failures,nativePartialWritesBeforeFailure=partial_failures,nativeResets=resets,publicNativeConvertOverloads=6,candidateDeclaredConvertAvailability=availability,candidateBehaviorQualifiedByThisBaseline=False,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),sourceAdjacencyEvidence=adjacency.name,sourceAdjacencySha256=hashlib.sha256(adjacency.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),outputCarrierPlan=j['javaOutputCarrierPlan'],qualification='NATIVE_CONVERT_REFERENCE_AND_DECLARATION_AVAILABILITY_ONLY; NO_CANDIDATE_CONVERT_BEHAVIOR_OR_TASK_ACCEPTANCE_CREDIT');(EVIDENCE/'stateful-convert-baseline-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(f'PASS native stateful Convert baseline: {checks} integrity controls; 5760 sequences, 20160 calls, 472 partial successes; Java behavior credit=false')
if __name__=='__main__':main()
