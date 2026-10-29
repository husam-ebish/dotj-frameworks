"""Exercise the real proposed wrapper guard in an owned tiny D: Git fixture."""
from pathlib import Path
import argparse,json,subprocess,time,os,hashlib
p=argparse.ArgumentParser()
p.add_argument('--wrapper',type=Path,required=True)
p.add_argument('--original-wrapper',type=Path)
p.add_argument('--storage-root',type=Path,required=True)
a=p.parse_args()
base=Path(r'D:\AI\Implementation\dotj Frameworks').resolve()
out=a.storage_root.resolve()
assert out.is_relative_to(base) and out!=base
out.mkdir(parents=True,exist_ok=True)
fixture=out/('fixture-'+time.strftime('%Y%m%d-%H%M%S',time.gmtime()))
fixture.mkdir(exist_ok=False)
assert fixture.resolve().is_relative_to(out)
env=os.environ.copy()
env.update(TEMP=str(out/'tmp'),TMP=str(out/'tmp'),PYTHONPYCACHEPREFIX=str(out/'cache/python'),GIT_OPTIONAL_LOCKS='0')
(out/'tmp').mkdir(exist_ok=True)
def git(*args):
    return subprocess.run(['git','-C',str(fixture),*args],env=env,capture_output=True,text=True,encoding='utf-8',check=True)
git('init','-b','feature/export-guard-fixture')
git('config','user.email','validation-fixture@example.invalid')
git('config','user.name','Owned validation fixture')
git('config','core.autocrlf','false')
prefix='planning/stage-2/repos/dotj-core/evidence/'
paths=[prefix+f'clean-{i:02}.json' for i in range(24)]+[prefix+'name with space.json',prefix+'naïve-ß.json',prefix+'brackets[1].json']
baseline='{"baseline":true}\n'
for name in paths+['outside.txt']:
    f=fixture/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(baseline,encoding='utf-8')
git('add','.')
git('commit','--quiet','-m','Owned export guard fixture')
probe=Path(__file__).with_name('probe-export-guard.ps1')
results=[]
def run(name,selected,expected,route='batched',repository=None):
    cases=out/(name+'-cases.json');output=out/(name+'-result.json')
    cases.write_text(json.dumps([dict(name=name,route=route,paths=selected)],ensure_ascii=False),encoding='utf-8')
    command=['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(probe),'-Repository',str(repository or fixture),'-CasesPath',str(cases),'-OutputPath',str(output),'-WrapperPath',str(a.wrapper.resolve())]
    if a.original_wrapper:command+=['-OriginalWrapperPath',str(a.original_wrapper.resolve())]
    r=subprocess.run(command,env=env,capture_output=True,text=True)
    assert r.returncode==0,(name,r.stdout,r.stderr)
    row=json.loads(output.read_text(encoding='utf-8-sig'))[0]
    assert row['blocked']==expected,(name,row)
    results.append(row)
def restore(name):
    (fixture/name).write_text(baseline,encoding='utf-8');git('add','--',name)
if a.original_wrapper:run('benchmark_original_clean8',paths[:8],False,'original')
run('benchmark_batched_clean8',paths[:8],False)
run('clean_two_chunks',paths,False)
(fixture/paths[23]).write_text('changed\n',encoding='utf-8')
run('dirty_second_chunk',paths,True);restore(paths[23])
(fixture/paths[0]).write_text('staged\n',encoding='utf-8');git('add','--',paths[0])
run('staged_selected',paths,True);restore(paths[0])
extra=prefix+'new untracked.json';(fixture/extra).write_text('untracked\n',encoding='utf-8')
run('untracked_selected',paths+[extra],True)
f=fixture/extra;assert f.resolve().is_relative_to(fixture);f.unlink()
(fixture/'outside.txt').write_text('outside edit\n',encoding='utf-8')
run('dirty_outside_selection',paths,False);restore('outside.txt')
for name in paths[24:26]:(fixture/name).write_text('changed\n',encoding='utf-8')
run('unicode_and_space',paths[24:26],True)
for name in paths[24:26]:restore(name)
(fixture/paths[26]).write_text('changed\n',encoding='utf-8')
run('literal_bracket_batched',[paths[26]],True)
if a.original_wrapper:run('literal_bracket_original_control',[paths[26]],True,'original')
restore(paths[26])
renamed=prefix+'renamed with space.json'
assert (fixture/paths[0]).resolve().is_relative_to(fixture) and (fixture/renamed).resolve().is_relative_to(fixture)
git('mv','--',paths[0],renamed)
run('renamed_destination',[renamed],True)
git('mv','--',renamed,paths[0])
run('git_failure_closed',paths,True,repository=fixture/'absent')
run('empty_selection',[],False)
timings={r['name']:r['seconds'] for r in results}
record=dict(status='PASS',cases=len(results),fixture=str(fixture),wrapper=str(a.wrapper.resolve()),wrapperSha256=hashlib.sha256(a.wrapper.read_bytes()).hexdigest(),originalWrapperSha256=hashlib.sha256(a.original_wrapper.read_bytes()).hexdigest() if a.original_wrapper else None,results=results,
 benchmark=dict(originalEightPathSeconds=timings.get('benchmark_original_clean8'),batchedEightPathSeconds=timings['benchmark_batched_clean8'],qualification='One light fixture sample per route; not a full-gate speedup measurement'),
 limitations=['No full gate run','Literal path interpretation is explicit; bracket-name refusal was equivalent in the tested Git version','Caller checks and destination copying remain in the wrapper; the tested block is the actual extracted status guard'])
(out/'export-guard-fixture-results.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in record.items() if k not in ['results','limitations']},indent=2))
