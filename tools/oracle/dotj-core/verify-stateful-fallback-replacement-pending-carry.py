"""Bound selected UTF16 replacement maximum-count arithmetic by native and pinned source evidence."""
import argparse,base64,hashlib,json,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
REPLACEMENTS=[[],[0],[65,0],[0,66],[65,0,66],[55296,56320],[65,0,55296,56320],[55296,56320,0,65],[0,55296,56320,0]]
def inputs(method,m):
 bound=2147483647//(2*m)-1 if method=='GetMaxByteCount' else 2*(2147483647//m-1)
 return set([-2147483648,-1,0,1,2,3,4,7,8,15,16,31,32,255,256,65535,65536,1073741822,1073741823,1073741824,2147483646,2147483647]+[bound+d for d in range(-3,4) if 0<=bound+d<=2147483647])
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'stateful-fallback-replacement-pending-carry-contract-v10.0.12.json';j=json.loads(path.read_text());assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-stateful-fallback-replacement-pending-carry-contract.ps1').read_bytes()).hexdigest()
 archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()=='ae0460937c3d6ca394d8240a8e34eb61b80bb34951ec47efab1ba302b04ce115'
 entry='runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Text/UTF8Encoding.cs'
 with zipfile.ZipFile(archive) as z:source=z.read(entry)
 assert hashlib.sha256(source).hexdigest()=='47f5e4c98751367a86329ab1e0a76d86b39fd076a5b019284694f39d40fd9011'
 with zipfile.ZipFile(archive) as z:assert hashlib.sha256(z.read('runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/System/Text/UnicodeEncoding.cs')).hexdigest()=='b5a717988edb22bae8688fb5cf9d8efe9d503dfe2918cdb5a9c95578a5768828'
 sourcePins={'System/Text/Encoder.cs': '803a635510c36435b6cfa82a92720bc590673abae7a502506ac8c68eaa7b39f0', 'System/Text/Encoding.Internal.cs': 'a427a1e8fa18546aac0743018e0b40a9e798564951492dcf303caf169a9715b4', 'System/Text/EncoderNLS.cs': '79a6e4501f5da67690194d5c31da8c92b44271941422d5a5bf49113c43601b15', 'System/Text/EncoderFallback.cs': 'fecaa8e71992f9d568254202327662e6de473b3d73ad5b6fa83a79417cc98715', 'System/NullReferenceException.cs': '6cff73e54975e9cbaa01dc0f8f5148358d92291660dd529044ef90b06aae7b58'}
 with zipfile.ZipFile(archive) as z:
  for name,digest in sourcePins.items():assert hashlib.sha256(z.read("runtime-4271d88e0aebf3d04f188f1334c2220d80555ef6/src/libraries/System.Private.CoreLib/src/"+name)).hexdigest()==digest
 replacements=[[],[63],[65,66],[55296,56320]];expected={(kind,tuple(old),tuple(next)) for kind in ['UTF8','UTF16LE','UTF16BE'] for old in replacements for next in replacements};seen=set();vectors=[];calls=0;groups=0;sequences=0
 operations=['seedEncoder','seedDecoder','flushExistingEncoder','flushExistingDecoder','reuseExistingEncoder','reuseExistingDecoder','ownerEncoder','ownerDecoder']
 identityNames={'encoderAssigned','decoderAssigned','ownerEncoderUnchanged','ownerDecoderUnchanged','encoderBufferChanged','decoderBufferChanged','newEncoderRemaining','newDecoderRemaining'}
 def csv(v):return ','.join(map(str,v))
 for profile in j['profiles']:
  kind,old,next=profile['kind'],profile['oldReplacement'],profile['nextReplacement'];key=(kind,tuple(old),tuple(next));assert key in expected and key not in seen;seen.add(key);modes=set()
  for row in profile['rows']:
   mode=row['seedMode'];assert mode in (0,1,2) and (mode,row['precreate'],row['sameProvider']) not in modes;modes.add((mode,row['precreate'],row['sameProvider']));seedChars=[] if mode==0 else [55296];seedBytes=[] if mode==0 else ([226] if mode==1 else [240,144]) if kind=='UTF8' else [0] if mode==1 else [0,216] if kind=='UTF16LE' else [216,0];assert row['seedChars']==seedChars and row['seedBytes']==seedBytes;assert set(row['identity'])==identityNames and all(value is True for key,value in row['identity'].items() if not key.endswith('Remaining')) and row['identity']['newEncoderRemaining']==row['identity']['newDecoderRemaining']==0;assert set(row['events'])==set(operations)
   vectors.append('\t'.join(['N',kind,csv(old),csv(next),str(int(row['precreate'])),str(int(row['sameProvider']))]));sequences+=1
   for op in operations:
    if op=='flushExistingEncoder':
     vectors.append('M');groups+=8
     assert len(row['oldBufferProbes'])==2
     for direction,probe in zip(['E','D'],row['oldBufferProbes']):
      assert set(probe)=={'remainingBefore','next','remainingAfterNext','previous','remainingAfterPrevious'}
      vectors.append('\t'.join(['V',direction,str(probe['remainingBefore']),str(probe['next']),str(probe['remainingAfterNext']),str(int(probe['previous'])),str(probe['remainingAfterPrevious'])]));groups+=5
    event=row['events'][op];r=event['result'];assert (r['ok'] is True and r['count']>=0) or (r['exception']=='System.NullReferenceException' and kind=='UTF8' and op in ('flushExistingEncoder','reuseExistingEncoder'));assert len(event['after'])==35 and event['after'][0]==event['after'][-1]==99
    source=seedChars if op=='seedEncoder' else seedBytes if op=='seedDecoder' else [] if op.startswith('flush') else [56320] if op.endswith('Encoder') else [255]
    vectors.append('\t'.join(['W',op,csv(source),str(r.get('count',0)),r.get('exception',''),base64.b64encode(r.get('message','').encode()).decode(),str(r.get('hResult',0)),r.get('paramName') or '~',csv(event['after'])]));calls+=1;groups+=2
  assert modes=={(mode,pre,same) for mode in (0,1,2) for pre in (False,True) for same in (False,True)}
 nativeNullReferenceCases=sum(not e['result']['ok'] for profile in j['profiles'] for row in profile['rows'] for e in row['events'].values());assert nativeNullReferenceCases==128
 assert seen==expected and calls==j['nativeCalls']==4608 and sequences==576 and groups==19584
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/stateful-fallback-replacement-pending-carry');work.mkdir(parents=True,exist_ok=True);data=work/'vectors.tsv';data.write_text('\n'.join(vectors)+'\n',encoding='ascii');component=Path(__file__).with_name('stateful-fallback-replacement-pending-carry-probe.java');probe=work/'StatefulFallbackReplacementPendingCarryProbe.java';probe.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(probe)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'StatefulFallbackReplacementPendingCarryProbe',str(data)],capture_output=True,text=True,timeout=60);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert 'calls=4608 groups=19584' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,nativeCalls=calls,sequences=sequences,profiles=48,nativeNullReferenceCases=nativeNullReferenceCases,sourcePins=sourcePins,identityComparisons=4608,abandonedBufferComparisons=5760,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_STATEFUL_FALLBACK_REPLACEMENT_PENDING_CARRY_AND_BUFFER_IDENTITY_ONLY; ARBITRARY_CALLBACKS_FULL_PARITY_E01_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'stateful-fallback-replacement-pending-carry-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS owner fallback state snapshots: 19584 comparisons; no task acceptance credited')
if __name__=='__main__':main()
