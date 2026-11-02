"""Explicit read-only historical contract reader and same-JAR Java replay.

No frozen module globals are patched and no original native producer is retargeted.
Historical native bytes retain their original path/hash and exact archive mapping.
"""
from pathlib import Path
import product_support as p
c=p.c

def validate_closure(path,seen=None):
    seen=set() if seen is None else seen
    if str(path) in seen:return
    seen.add(str(path))
    value=c.read(path)
    for pin in p.walk_pins(value):
        resolved=p.resolve(pin)
        # Follow proof dependencies, not predecessor plans or abandoned attempts.
        # Each selected lock/receipt is independently consumed below.
    return value

def native_references():
    old=p.load('delay_old_task_reader',p.OLD/'run-comparison.py')
    # Import the pinned historical pure parsers under their own supported names.
    import sys
    sys.path.insert(0,str(p.H15))
    c15=p.load('delay_vt_pure_reader',p.H15/'capture_support.py')
    c14=p.load('delay_work_pure_reader',p.H14/'capture_support.py')
    references={}
    for n in [2512,2514,2515]:
        path=p.B/f'validation/Batch-{n}-native-observation-v1/observation-lock.json'
        lock=validate_closure(path)
        receipt=validate_closure(Path(lock['nativeReceipt']['path']))
        # Validate exact selected native locks and their bound pin inventory.
        lockpath=Path(lock['inputLock']['path']) if n==2512 else None
        if n==2514:lockpath=p.B/'agents/batch2514-worktask-cancelasync-native-preparation-v1/native-input-lock-v2.json'
        if n==2515:lockpath=p.B/'agents/batch2515-valuetask-task-native-preparation-v1/native-input-lock-v3.json'
        nativeLock=validate_closure(lockpath)
        if n==2512:
            raw=Path(receipt['commands'][-1]['streams']['stdout']['path']).read_bytes()
            actual=old.observations(raw,c.read(p.OLD/'schema.json'),True);old.invariants(actual)
            c.require(actual==lock['observations'],'Task raw frozen observation lock equality')
        else:
            raw=Path(lock['stdout']['path']).read_bytes()
            reader=c14 if n==2514 else c15
            actual=reader.observations(raw,c.read((p.H14 if n==2514 else p.H15)/'schema.json'),True);reader.invariants(actual)
        references[n]=dict(lock=c.descriptor(path),payload=actual)
    return references,old,c14,c15

def replay(s,jar,only=None):
    references,old,c14,c15=native_references()
    expected=p.HERE/'expected-public-surface-v1.txt'
    inventory=set(expected.read_text(encoding='utf-8').splitlines())
    owners={line.split('|',1)[0] for line in inventory}
    actual=set()
    for row in p.surface(jar)['classes']:
        if row['name'] not in owners:continue
        owner=row['name'];actual.add(f"{owner}|C|{row['modifiers']&0x761f}")
        for m in row['publicMembers']:actual.add(f"{owner}|{m['kind']}|{m['name']}|{m['descriptor']}|{m['modifiers']}")
    p.c.require(inventory==actual,'exact historical reflection inventory plus five additions')
    p.check_surface(jar)
    # Original old behavior assertions are byte-preserved except the explicitly
    # bounded public method guard. ValueTask controls use the corrected 2515 fixture.
    correction=p.ROOT/'tools/oracle/dotj-core/public-valuetask-task-product-v1/ValueTaskTaskBoundaryControls.java'
    plan=p.B/'orchestration/two-frameworks/batch2512-packaged-regression-plan-v2.json'
    c.require(c.sha(plan)=='1b4043fdd45066e4c867a51e019e88d8d303b9e928a5a3a1c73eb9904a6a8d62','legacy regression plan')
    prior=c.read(plan)['groups']
    groups=[
        ('valuetask-task',[p.H15/'PublicValueTaskTaskFixtures.java'],'PublicValueTaskTaskFixtures',[( 'PublicValueTaskTaskFixtures',[str(jar)])]),
        ('valuetask-boundaries',[correction],'ValueTaskTaskBoundaryControls', [('ValueTaskTaskBoundaryControls',[mode,str(jar),str(expected)]) for mode in ['controls','task-first','configured-first','conversion-first']]),
        ('task',[p.OLD/'PublicTaskFixtures.java'],'PublicTaskFixtures',[('PublicTaskFixtures',[str(jar)])]),
        ('task-boundaries',[p.HERE/'TaskBoundaryControls.java'],'System.Threading.Tasks.TaskBoundaryControls',[('System.Threading.Tasks.TaskBoundaryControls',[str(jar)])]),
        ('worktask',[p.H14/'PublicWorkTaskCancelAsyncFixtures.java'],'PublicWorkTaskCancelAsyncFixtures',[('PublicWorkTaskCancelAsyncFixtures',[str(jar)])]),
        ('worktask-boundaries',[p.HERE/'WorkTaskBoundaryControls.java',p.H14/'CancelAsyncBoundaryControls.java'],None,[('System.Threading.Tasks.WorkTaskBoundaryControls',[str(jar)]),('System.Threading.CancelAsyncBoundaryControls',[str(jar)])])]
    for entry in prior:
        for pk,hk in [('javaFixture','javaFixtureSha256'),('nativeOracle','nativeOracleSha256'),('nativeEvidence','nativeEvidenceSha256')]:c.require(c.sha(entry[pk])==entry[hk],'immutable legacy input')
        groups.append((entry['name'],[Path(entry['javaFixture'])],entry['mainClass'],None))
    for name,fixtures,main,modes in groups:
        if only is not None and name not in only.split(','):continue
        if modes is None:modes=[(main,[str(s.out/name/'observations.txt')])]
        group,records=s.java_group(name,fixtures,main,modes,jar)
        raw=[Path(r['stdoutPath']).read_bytes() for r in records]
        if name=='valuetask-task':
            actual=c15.observations(raw[0],c.read(p.H15/'schema.json'));c15.invariants(actual);c.require(actual==references[2515]['payload'],'ValueTask115/1884 actual frozen match');count=len(actual)
        elif name=='task':
            actual=old.observations(raw[0],c.read(p.OLD/'schema.json'),False);old.invariants(actual);c.require(actual==references[2512]['payload'],'Task61/697 actual frozen match');count=len(actual)
        elif name=='worktask':
            actual=c14.observations(raw[0],c.read(p.H14/'schema.json'));c14.invariants(actual);c.require(actual==references[2514]['payload'],'WorkTask66/612 actual frozen match');count=len(actual)
        elif name=='task-boundaries':c.require(raw[0].decode().strip()=='PASS Task Java boundary controls: 49','all 49 original assertions retained');count=49
        elif name=='valuetask-boundaries':
            expectedMarkers=[{'J-API-ORIGIN','J-PUBLICATION','J-INTERRUPTION','J-DETACH','J-INLINE-THROW','J-DISPATCH','J-FOREIGN-THROWABLE'},*[{f'J-CONSUMER-FIRST.{mode}'} for mode in ['task-first','configured-first','conversion-first']]]
            for data,wanted in zip(raw,expectedMarkers):c.require(set(data.decode().splitlines())=={x+'\tb\ttrue' for x in wanted},'all ValueTask boundaries')
            count=8
        elif name=='worktask-boundaries':
            for data,keys in zip(raw,[{'J01','J04.work','J05','J06','J07','J08.work'},{'J02','J03','J04.cancel','J08.cancel'}]):c.require(set(data.decode().splitlines())=={x+'\tb\ttrue' for x in keys},'eight work/cancel boundary groups')
            count=8
        else:
            file=s.out/name/'observations.txt';actual={}
            for line in file.read_text(encoding='utf-8').splitlines():
                key,value=line.split('=',1);c.require(key not in actual,'unique legacy keys');actual[key]=value
            c.require(actual==next(x['expected'] for x in prior if x['name']==name),'actual legacy raw comparison')
            group['payloads']=[c.descriptor(file)];count=len(actual)
        group['actualCount']=count;s.save()
    s.record['nativeReferences']=[v['lock'] for v in references.values()]
