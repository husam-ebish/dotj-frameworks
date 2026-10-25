"""Verify provider-free selected UTF-8/UTF-16/UTF-16/UTF-16 lookups against pinned native observations."""
import argparse, hashlib, json, re, subprocess, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def csv(values): return ','.join(map(str,values))
def units(value): return 'null' if value is None else csv(int.from_bytes(value.encode('utf-16-le',errors='surrogatepass')[i:i+2],'little') for i in range(0,len(value.encode('utf-16-le',errors='surrogatepass')),2))
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text())['jarPath']
 path=EVIDENCE/'utf8-encoding-lookups-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-utf8-encoding-lookups-contract.ps1').read_bytes()).hexdigest();assert len(j['rows'])==j['requestCount']*26
 adjacency=EVIDENCE/'utf8-encoding-lookups-source-adjacency-v10.0.12.json';adj=json.loads(adjacency.read_text());archive=Path('D:/AI/Implementation/dotj Frameworks/toolchains/downloads/runtime-source-v10.0.12.zip');assert hashlib.sha256(archive.read_bytes()).hexdigest()==adj['sourceArchiveSha256']
 assert j['providerIsolation']['providerCountDuringCapture']==0 and j['providerIsolation']['defaultCodePage']==65001 and j['providerIsolation']['scope']=='THIS_DISPOSABLE_ORACLE_PROCESS_ONLY'
 require_names={row['request']['name'] for row in j['rows'] if row['request']['kind']=='name'};assert {'\ud800','\u0130utf-8','UTF\u20138'}.issubset(require_names)
 with zipfile.ZipFile(archive) as z:
  for item in adj['upstreamFiles']:assert hashlib.sha256(z.read(item['archiveMember'])).hexdigest()==item['sha256']
  source=z.read(next(item['archiveMember'] for item in adj['upstreamFiles'] if item['archiveMember'].endswith('/EncodingData.cs'))).decode('utf-8');section=source.split('private const string EncodingNames =',1)[1].split('private static ReadOnlySpan<int>',1)[0];aliases=re.findall(r'"([^"\n]+)"\s*[+;]\s*//\s*(\d+)',section);assert len(aliases)==42;assert set(j['utf8Aliases'])=={name for name,code in aliases if code=='65001'};assert set(j['otherCoreLibAliases'])=={name for name,code in aliases if code!='65001'}
 lines=[];groups=0;boundaries=0;differential=0;operations=0
 for row in j['rows']:
  request=row['request'];r=row['result'];base=[request['kind'],str(request['codepage']),units(request['name']),str(row['encoderProfile']),str(row['decoderProfile'])]
  utf16=request['codepage'] in [1200,1201] if request['kind']=='number' else request['name'] is not None and dict(aliases).get(''.join(chr(ord(c)+32) if 'A'<=c<='Z' else c for c in request['name'])) in ['1200','1201']
  if request['candidateScope']=='unsupported-boundary' and not utf16:lines.append('\t'.join(['B',*base]));groups+=1;boundaries+=1;continue
  differential+=1;groups+=13 if r['ok'] else 4
  meta=[str(r.get('codepage',0)),str(int(r.get('readOnly',False))),csv(r.get('preamble',[])),*[str(int(r.get(k,False))) for k in ['sameRepeated','sameUtf8','sameDefault','encoderSameInput','decoderSameInput']],r.get('encoderType',''),r.get('decoderType',''),str(r.get('encoderMax',0)),str(r.get('decoderMax',0))]
  lines.append('\t'.join(['H',*base,str(int(r['ok'])),r.get('exception',''),str(r.get('hResult',0)),r.get('paramName') or 'null',*meta]))
  if r['ok']:assert len(r['operations'])==10 and [op['kind'] for op in r['operations']]==['encode']*5+['decode']*5
  for operation in r.get('operations',[]):
   result=operation['result'];lines.append('\t'.join(['O',operation['kind'],csv(operation['input']),str(int(result['ok'])),csv(result.get('value',[])),result.get('exception',''),str(result.get('hResult',0)),result.get('paramName') or 'null']));groups+=2 if result['ok'] else 4;operations+=1
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/utf8-encoding-lookups');work.mkdir(parents=True,exist_ok=True);vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');source=work/'Utf8EncodingLookupsProbe.java';source.write_bytes(Path(__file__).with_name('utf8-encoding-lookups-probe.java').read_bytes())
 subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'Utf8EncodingLookupsProbe',str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert f'groups={groups}' in result.stdout
 record=dict(schemaVersion=1,casesPassed=groups,requestCount=j['requestCount'],differentialConfigurations=differential,operations=operations,explicitUnsupportedBoundaryControls=boundaries,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),sourceAdjacencyEvidence=adjacency.name,sourceAdjacencySha256=hashlib.sha256(adjacency.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_PROVIDER_FREE_UTF8_AND_UTF16_LOOKUPS_ONLY; OTHER_ENCODINGS_PROVIDER_REGISTRATION_UTF7_SWITCH_UNICODE_CASING_FULL_METADATA_SOURCE_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'utf8-encoding-lookups-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(f'PASS UTF-8/UTF-16 lookups: {groups} groups; {differential} differential configurations; {boundaries} explicit unsupported boundaries')
if __name__=='__main__':main()
