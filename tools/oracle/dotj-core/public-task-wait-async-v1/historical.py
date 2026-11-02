"""Frozen historical behaviors on the selected final JAR; exact surface successors."""
from pathlib import Path
import batch2520_qualify as q
p=q.p
c=p.c

def replay(s,jar,only=None):
    import historical_replay as old_replay
    references,old,c14,c15=old_replay.native_references()
    expected=q.HERE/'expected-public-surface-v1.txt'
    inventory=set(expected.read_text().splitlines());owners={line.split('|',1)[0] for line in inventory};actual=set()
    for row in p.surface(jar)['classes']:
        if row['name'] not in owners:continue
        owner=row['name'];actual.add(f"{owner}|C|{row['modifiers']&0x761f}")
        for m in row['publicMembers']:actual.add(f"{owner}|{m['kind']}|{m['name']}|{m['descriptor']}|{m['modifiers']}")
    c.require(actual==inventory,'complete reflection surface exact one overload successor');q.surface(jar)
    correction=p.ROOT/'tools/oracle/dotj-core/public-valuetask-task-product-v1/ValueTaskTaskBoundaryControls.java'
    groups=[
        ('valuetask-task',[p.H15/'PublicValueTaskTaskFixtures.java'],[('PublicValueTaskTaskFixtures',[str(jar)])]),
        ('valuetask-boundaries',[correction],[('ValueTaskTaskBoundaryControls',[mode,str(jar),str(expected)]) for mode in ['controls','task-first','configured-first','conversion-first']]),
        ('task',[p.OLD/'PublicTaskFixtures.java'],[('PublicTaskFixtures',[str(jar)])]),
        ('task-boundaries',[q.HERE/'TaskBoundaryControls.java'],[('System.Threading.Tasks.TaskBoundaryControls',[str(jar)])]),
        ('worktask',[p.H14/'PublicWorkTaskCancelAsyncFixtures.java'],[('PublicWorkTaskCancelAsyncFixtures',[str(jar)])]),
        ('worktask-boundaries',[q.HERE/'WorkTaskBoundaryControls.java',p.H14/'CancelAsyncBoundaryControls.java'],[('System.Threading.Tasks.WorkTaskBoundaryControls',[str(jar)]),('System.Threading.CancelAsyncBoundaryControls',[str(jar)])])]
    plan=p.B/'orchestration/two-frameworks/batch2512-packaged-regression-plan-v2.json'
    c.require(c.sha(plan)=='1b4043fdd45066e4c867a51e019e88d8d303b9e928a5a3a1c73eb9904a6a8d62','immutable historical plan')
    prior=c.read(plan)['groups']
    for entry in prior:
        for pk,hk in [('javaFixture','javaFixtureSha256'),('nativeOracle','nativeOracleSha256'),('nativeEvidence','nativeEvidenceSha256')]:c.require(c.sha(entry[pk])==entry[hk],'immutable legacy input')
        groups.append((entry['name'],[Path(entry['javaFixture'])],[(entry['mainClass'],[str(s.out/entry['name']/'observations.txt')])]))
    for name,fixtures,modes in groups:
        if only is not None and name not in only.split(','):continue
        group,records=s.java_group(name,fixtures,None,modes,jar);raw=[Path(x['stdoutPath']).read_bytes() for x in records]
        if name in ['task','worktask','valuetask-task']:
            n={'task':2512,'worktask':2514,'valuetask-task':2515}[name]
            reader=old if n==2512 else c14 if n==2514 else c15
            schema=c.read((p.OLD if n==2512 else p.H14 if n==2514 else p.H15)/'schema.json')
            actual=reader.observations(raw[0],schema,False) if n==2512 else reader.observations(raw[0],schema)
            c.require(actual==references[n]['payload'],'historical native match '+name);count=len(actual)
        elif name=='task-boundaries':c.require(raw[0].decode().strip()=='PASS Task Java boundary controls: 49','old 49 assertions');count=49
        elif name=='valuetask-boundaries':
            keys=[{'J-API-ORIGIN','J-PUBLICATION','J-INTERRUPTION','J-DETACH','J-INLINE-THROW','J-DISPATCH','J-FOREIGN-THROWABLE'},*[{f'J-CONSUMER-FIRST.{mode}'} for mode in ['task-first','configured-first','conversion-first']]]
            for data,wanted in zip(raw,keys):c.require(set(data.decode().splitlines())=={x+'\tb\ttrue' for x in wanted},'ValueTask private controls')
            count=8
        elif name=='worktask-boundaries':
            for data,wanted in zip(raw,[{'J01','J04.work','J05','J06','J07','J08.work'},{'J02','J03','J04.cancel','J08.cancel'}]):c.require(set(data.decode().splitlines())=={x+'\tb\ttrue' for x in wanted},'work/cancel private groups')
            count=8
        else:
            file=s.out/name/'observations.txt';actual=dict(line.split('=',1) for line in file.read_text().splitlines())
            c.require(actual==next(x['expected'] for x in prior if x['name']==name),'legacy exact observed values');group['payloads']=[c.descriptor(file)];count=len(actual)
        group['actualCount']=count;s.save()
    if only is not None and 'delay' not in only.split(','):return
    # The prior qualified delay payload was compared to both frozen native passes.
    # Consume its actual immutable raw bytes, avoiding old SDK/launcher replay.
    delay_evidence=c.read(p.E/'public-task-delay-v1.json');paired=c.read(p.resolve(delay_evidence['paired']));old_group=paired['groups'][0]
    manifest=c.read(p.FROZEN/'fixture-manifest.json');schema=c.read(p.FROZEN/'schema.json')
    group,records=s.java_group('delay',[p.HERE/'PublicTaskDelayProductFixtures.java'],None,[('PublicTaskDelayProductFixtures',[str(p.FROZEN/'fixture-manifest.json'),str(p.HERE/'case-inputs.tsv'),part,str(jar)]) for part in ['ordinary','async']],jar,module=True)
    actual={};prior_actual={}
    for rec,pin,part in zip(records,old_group['payloads'],['ordinary','async']):
        actual.update(c.wire(Path(rec['stdoutPath']).read_bytes(),schema,manifest,part));prior_actual.update(c.wire(p.resolve(pin).read_bytes(),schema,manifest,part))
    c.compare(actual,prior_actual,manifest);group.update(actualCases=len(actual),actualFields=sum(len(x) for x in actual.values()));s.data['retainedDelayPaired']=delay_evidence['paired'];s.save()
    group,records=s.java_group('delay-private',[p.HERE/'TaskDelayProductControls.java'],None,[('System.Threading.Tasks.TaskDelayProductControls',[str(jar),str(n)]) for n in range(1,10)],jar)
    markers=[line for rec in records for line in Path(rec['stdoutPath']).read_text().splitlines()]
    c.require(len(markers)==30 and set(markers)=={f'J{n:02}\tb\ttrue' for n in range(1,31)},'all delay private controls');group.update(actualControls=len(markers),actualGroups=len(records))
    s.data['nativeReferences']=[x['lock'] for x in references.values()]
