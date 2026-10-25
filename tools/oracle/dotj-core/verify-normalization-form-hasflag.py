"""Compare selected HasFlag pairs and null/unrelated enum controls."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'normalization-form-hasflag-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-normalization-form-hasflag-contract.ps1').read_bytes()).hexdigest();assert len(j['rows'])==484 and len(j['controls'])==66 and not j['isFlagsEnum'];assert len({(r['value'],r['flag']) for r in j['rows']})==484;assert {r['failure']['type'] for r in j['controls']}=={'System.ArgumentNullException','System.ArgumentException'}
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/normalization-form-hasflag');work.mkdir(parents=True,exist_ok=True);lines=[]
 for mode,key,rows in [('P','flag',j['rows']),('C','kind',j['controls'])]:
  for r in rows:
   f=r.get('failure') or {};lines.append('\t'.join([mode,str(r['value']),str(r[key]),str(int(bool(r['result']))),f.get('type',''),str(f.get('hResult',0)),f.get('paramName') or '~',f.get('message','')]))
 vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');component=Path(__file__).with_name('normalization-form-hasflag-probe.java');source=work/'NormalizationFormHasFlagProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'NormalizationFormHasFlagProbe',str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert 'groups=550' in result.stdout
 record=dict(schemaVersion=1,casesPassed=550,nativePairs=484,nativeControls=66,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_NORMALIZATION_FORM_HASFLAG_ONLY; PARSING_FULL_ENUM_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'normalization-form-hasflag-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS normalization HasFlag: 484 native pairs, 66 controls, 550 groups')
if __name__=='__main__':main()
