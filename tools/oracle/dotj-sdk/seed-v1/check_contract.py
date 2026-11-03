"""Independent finite inventory and frozen-source preflight; no executable launch."""
import argparse,base64,copy,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from capture_native import descriptor,save

EXPECTED={
 'Q01':['--help','-h'],'Q02':['version'],'Q03':['info'],'Q04':['--help','-h'],
 'Q05':['present'],'Q06':['absent'],
 'Q07':['-getProperty;','-getProperty,','--getProperty;','--getProperty,','/getProperty;','/getProperty,','repeated-case'],
 'Q08':['--property','-property','/property','/p','-p','--p','empty-value','transport'],
 'Q09':['import'],'Q10':['cycle-duplicate'],'Q11':['malformed'],'Q12':['missing-import'],
 'Q13':['unknown'],'Q14':['-target','-t','unexecuted-task'],'Q15':['build'],'Q16':['zero','multiple']}
FILES={'harmless.proj','values.proj','conditional.proj','import.props','cycle.proj','cycle.props','malformed.proj','missing.proj','inert.proj'}
def require(ok,message):
 if not ok:raise ValueError(message)
def validate(c):
 expected={(q,v) for q,vs in EXPECTED.items() for v in vs}
 actual=[(r['id'],r['variant']) for r in c['cases']]
 require(len(actual)==34 and len(set(actual))==34 and set(actual)==expected,'Exact Q cohort/variant inventory')
 require(c['cohorts']==16 and c['invocationsPerOs']==34 and c['platforms']==['windows','linux'],'Declared cardinality')
 require(set(c['files'])==FILES,'Exact file inventory')
 for name,item in c['files'].items():
  raw=base64.b64decode(item['base64'],validate=True)
  require(len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256'],'Fixture identity '+name)
 require(c['files']['harmless.proj']['bytes']==132 and c['files']['harmless.proj']['sha256']=='cac688d3341e4c468bb43d261aaa5b0b2840b38570467304e6987d657a67a826','Harmless safety fixture')
 for r in c['cases']:
  require(all(isinstance(s,str) for s in r['argv']) and r['argv'],'Argument array')
  require(not any(s.startswith('@') for s in r['argv']),'No response files')
  if r['id']=='Q15':require(r['argv']==['build','{fixtures}/harmless.proj','--no-restore'],'No-op build guard')
  if r['id']=='Q14' and r['variant']!='unexecuted-task':require(r['argv']==['msbuild','{fixtures}/harmless.proj','-getProperty:Probe',r['variant']+':Build'],'Harmless target guard')
 return dict(cohorts=16,invocationsPerOs=34,fixtureFiles=9)

def main():
 p=argparse.ArgumentParser();p.add_argument('--contract',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 c=json.loads(a.contract.read_text(encoding='utf-8'));result=validate(c);controls=[]
 variants=[]
 v=copy.deepcopy(c);v['cases'].pop();variants.append(('omission',v))
 v=copy.deepcopy(c);v['cases'].append(copy.deepcopy(v['cases'][0]));variants.append(('duplicate',v))
 v=copy.deepcopy(c);v['cases'][0]['variant']='invented';variants.append(('wrong-binding',v))
 v=copy.deepcopy(c);v['files']['harmless.proj']['base64']=base64.b64encode(b'<Project/>').decode();variants.append(('changed-fixture',v))
 v=copy.deepcopy(c);next(r for r in v['cases'] if r['id']=='Q15')['argv'].remove('--no-restore');variants.append(('restore-guard-removal',v))
 for name,v in variants:
  try:validate(v)
  except ValueError as error:controls.append(dict(name=name,status='REJECTED',reason=str(error)))
  else:raise AssertionError('Mutation accepted '+name)
 a.out.mkdir(parents=True,exist_ok=False);save(a.out/'result.json',dict(status='PASS_FINITE_CONTRACT_ONLY',contract=descriptor(a.contract),producer=descriptor(__file__),inventory=result,controls=controls,nativeObservations=0,productPasses=0));print(json.dumps(result))
if __name__=='__main__':main()
