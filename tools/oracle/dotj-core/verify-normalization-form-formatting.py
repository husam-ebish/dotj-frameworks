"""Verify selected normalization-form enum formatting against native observations."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];EVIDENCE=ROOT/'planning/stage-2/repos/dotj-core/evidence'
def main():
 p=argparse.ArgumentParser();p.add_argument('--jar',type=Path);a=p.parse_args()
 if a.jar is None:a.jar=ROOT/json.loads((EVIDENCE/'foundation-product-candidate-v1.json').read_text(encoding='utf-8'))['jarPath']
 path=EVIDENCE/'normalization-form-formatting-contract-v10.0.12.json';j=json.loads(path.read_text(encoding='utf-8'));assert j['runtimeVersion']=='10.0.12' and j['coreLibSha256']=='1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678';assert j['oracleSha256']==hashlib.sha256(Path(__file__).with_name('capture-normalization-form-formatting-contract.ps1').read_bytes()).hexdigest();assert len(j['rows'])==546 and j['providerTrapResult']=='FormC, FormD';assert {r['failure']['type'] for r in j['rows'] if r['failure']}=={'System.FormatException'}
 work=Path('D:/AI/Implementation/dotj Frameworks/verification/normalization-form-formatting');work.mkdir(parents=True,exist_ok=True);lines=[]
 for r in j['rows']:
  f=r['failure'] or {};lines.append('\t'.join([str(r['value']),r['format'] if r['format'] is not None else '~',r['culture'],r['result'] or '',f.get('type',''),str(f.get('hResult',0)),f.get('message',''),r['default']]))
 vectors=work/'vectors.tsv';vectors.write_text('\n'.join(lines)+'\n',encoding='ascii');component=Path(__file__).with_name('normalization-form-formatting-probe.java');source=work/'NormalizationFormFormattingProbe.java';source.write_bytes(component.read_bytes());subprocess.run(['javac','--release','21','-cp',str(a.jar),'-d',str(work),str(source)],check=True);result=subprocess.run(['java','-cp',str(a.jar)+';'+str(work),'NormalizationFormFormattingProbe',str(vectors)],capture_output=True,text=True);print(result.stdout,end='');print(result.stderr,end='');result.check_returncode();assert 'groups=1638' in result.stdout
 record=dict(schemaVersion=1,casesPassed=1638,nativeCases=546,oracleEvidence=path.name,oracleSha256=hashlib.sha256(path.read_bytes()).hexdigest(),consumerSourceSha256=hashlib.sha256(component.read_bytes()).hexdigest(),candidateJarSha256=hashlib.sha256(a.jar.read_bytes()).hexdigest(),qualification='SELECTED_NORMALIZATION_FORM_FORMATTING_ONLY; CONVERSIONS_SPANS_FULL_ENUM_ABI_AND_TASK_ACCEPTANCE_OPEN');(EVIDENCE/'normalization-form-formatting-differential-v1.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS normalization form formatting: 546 native cases, 1638 groups')
if __name__=='__main__':main()
