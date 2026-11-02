"""Java-only product qualification support; frozen producers are imported read-only."""
import hashlib, importlib.util, json, os, sys, time, zipfile
from pathlib import Path

B = Path('D:/AI/Implementation/dotj Frameworks')
ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
TOOLS = ROOT/'tools/oracle/dotj-core'
FROZEN = B/'worktrees/dotj-core-task-delay-v1/tools/oracle/dotj-core/public-task-delay-v1'
OLD = B/'worktrees/dotj-core-task-completion-v1/tools/oracle/dotj-core/public-task-v1'
H15 = B/'worktrees/dotj-core-valuetask-task-v1/tools/oracle/dotj-core/public-valuetask-task-v1'
H14 = B/'worktrees/dotj-core-cancelasync-v1/tools/oracle/dotj-core/public-worktask-cancelasync-v1'
E = ROOT/'planning/stage-2/repos/dotj-core/evidence'
A = B/'agents/batch2517-task-delay-product-implementation-v1'
O = B/'orchestration/two-frameworks'
PYTHON = B/'toolchains/python-3.13.9/python.exe'
JDK = B/'toolchains/jdk-qualified/jdk-21.0.12.1+1'
sys.path.insert(0,str(FROZEN))
import contract as c
import phase_tools as frozen_phases

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

guard=load('delay_unchanged_owned_process',OLD/'owned_process.py')
c.require(c.sha(OLD/'owned_process.py')=='a2a3701ae675fd563da61eb19ce41d79479bc1f435c1ec07af6c0ddefd67e125','unchanged guard')

def write(path,value):
    Path(path).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')

def prepare(out):
    c.confined(out);c.require(not out.exists(),'fresh output required; all failures retained')
    for name in ['','tmp','home/AppData/Roaming','home/AppData/Local','cache','classes','empty-sourcepath']:
        (out/name).mkdir(parents=True,exist_ok=True)

def resolve(pin):
    """Exact original path AND raw hash; never reinterpret a producer or its globals."""
    path=Path(pin['path'])
    if path.is_file() and path.stat().st_size==pin['sizeBytes'] and c.sha(path)==pin['sha256']:return path
    archives=c.read(FROZEN/'historical-archive-manifest.json')['entries']
    supplemental=HERE/'product-archive-manifest-v1.json'
    if supplemental.is_file():archives+=c.read(supplemental)['entries']
    matches=[x for x in archives if x['originalPath']==pin['path'] and x['durable']['sha256']==pin['sha256'] and x['durable']['sizeBytes']==pin['sizeBytes']]
    c.require(len(matches)==1,'no exact historical archive: '+pin['path'])
    c.validate_pin(matches[0]['durable']);return Path(matches[0]['durable']['path'])

def walk_pins(value):
    if type(value) is dict:
        if set(value)>={'path','sha256','sizeBytes'} and type(value['path']) is str:
            yield {key:value[key] for key in ['path','sha256','sizeBytes']}
        for child in value.values():yield from walk_pins(child)
    elif type(value) is list:
        for child in value:yield from walk_pins(child)

def historical_audit():
    manifest=c.read(FROZEN/'historical-archive-manifest.json')
    for entry in manifest['entries']:c.validate_pin(entry['durable'])
    # Audit all previously enumerated evidence, then every dependency in the
    # selected historical receipts/locks. No recursive indexing or mutation.
    seeds=[Path(x['path']) for x in manifest['inspectedJsonFiles']]
    seeds += [B/f'validation/Batch-{n}-native-observation-v1/observation-lock.json' for n in [2512,2514,2515]]
    seeds += [B/'agents/batch2515-valuetask-task-native-preparation-v1/native-input-lock-v3.json',
              B/'agents/batch2514-worktask-cancelasync-native-preparation-v1/native-input-lock-v2.json']
    inspected=set();seen={};queue=list(seeds);missing=[];missingKeys=set();nonMetadata=[]
    while queue:
        path=queue.pop()
        if str(path) in inspected:continue
        inspected.add(str(path))
        raw=path.read_bytes()
        try:value=json.loads(raw.decode('utf-8-sig'),object_pairs_hook=c.unique_pairs)
        except (ValueError,UnicodeError) as error:
            nonMetadata.append(dict(file=c.descriptor(path),reason=repr(error)));continue
        for pin in walk_pins(value):
            key=(pin['path'],pin['sha256'])
            if key in seen or key in missingKeys:continue
            try:actual=resolve(pin)
            except ValueError:
                missing.append(dict(pin,referencedBy=str(path)));missingKeys.add(key);continue
            seen[key]=dict(pin,resolvedPath=str(actual))
            if actual.suffix=='.json' and str(actual) not in inspected:queue.append(actual)
    # The expanded walk also reaches abandoned pre-native preparation and early
    # build attempts. They are preserved evidence, not inputs used by this replay.
    # Canonical dependencies must all resolve; selected current historical locks
    # are separately closed and validated by historical_replay.py.
    canonicalMissing=[x for x in missing if x['path'].replace('\\','/').lower().startswith('c:/source/repos/dotj frameworks/')]
    c.require(not canonicalMissing,'unresolved live canonical historical dependency')
    return dict(status='EXACT_READ_ONLY_ARCHIVE_RESOLUTION',jsonFiles=len(inspected),pins=len(seen),
                archives=len(manifest['entries']),resolved=list(seen.values()),nonMetadataFiles=nonMetadata,
                unconsumedSupersededDependencies=missing,additionalUnresolvedCanonicalInputs=canonicalMissing)

def prerequisites():
    lock=O/'batch2517-frozen-prerequisites-v1.json'
    c.require(c.sha(lock)=='fa953baf6466f00009ccd8798703693c8fa6b1306de2346d361777c3c8accc79','frozen prerequisites identity')
    proof=c.read(lock)
    for pin in proof['files']:c.validate_pin(pin)
    schema=c.read(FROZEN/'schema.json');manifest=c.read(FROZEN/'fixture-manifest.json')
    passes=[]
    for n in [1,2]:
        payload={}
        for partition in ['ordinary','async']:
            path=B/f'agents/batch2517-task-delay-native-preparation-v1/future/root-native-pass{n}-{partition}-v1/root-receipt.json'
            pin=next(p for p in proof['files'] if Path(p['path'])==path)
            payload.update(c.consumed_capture(path,pin['sha256'],schema,manifest))
        c.require(len(payload)==113,'complete native pass');passes.append(payload)
    c.compare(*passes,manifest)
    return manifest,schema,passes

def payload_lock():
    # Full actual used JDK distribution, not just launcher EXEs. The frozen lock
    # already inventories every payload file; select all JDK paths verbatim.
    lock=c.read(FROZEN/'toolchain-payload-lock.json')
    result=[]
    for pin in walk_pins(lock):
        if Path(pin['path']).is_relative_to(JDK):
            c.validate_pin(pin);result.append(pin)
    c.require(len(result)>100,'full JDK payload inventory')
    return result

def checked_launch(argv,out,label,timeout,deadline,update):
    c.require(time.monotonic()+timeout+5<deadline,'parent deadline before resource admission')
    sampled,samples=guard.wait_resources(min(deadline,time.monotonic()+160))
    env=frozen_phases.environment(out);env['PATH']+=r';C:\Program Files\Git\cmd'
    age=[None]
    def prelaunch():
        age[0]=time.monotonic()-sampled
        c.require(0<=age[0]<=2 and time.monotonic()+timeout+5<deadline,'fresh admission and full remaining child budget')
    prelaunch()
    record=guard.run(argv,out,env,label,timeout,on_update=update,prelaunch=prelaunch)
    record.update(resources=samples,resourceSampleAgeSeconds=age[0],environment=env,
                  streams={name:c.descriptor(record[name+'Path']) for name in ['stdout','stderr']},
                  resourcePolicy=dict(physicalFloorBytes=512*1024**2,availableCommitFloorBytes=16*1024**3,
                                      availableCommitField='ullAvailPageFile',maximumWaitSeconds=120,maximumSampleAgeSeconds=2))
    return record

def surface(jar):
    return load('delay_classfile_surface',H15/'classfile_surface.py').surface(jar)

def surface_lines(jar):
    lines=set()
    for row in surface(jar)['classes']:
        if not row['modifiers']&1:continue
        owner=row['name'];lines.add(f"{owner}|C|{row['modifiers']}")
        for m in row['publicMembers']:lines.add(f"{owner}|{m['kind']}|{m['name']}|{m['descriptor']}|{m['modifiers']}")
    return lines

ADDITIONS={
 'System/Threading/Tasks/Task|M|FromCanceled|(LSystem/Threading/CancellationToken;)LSystem/Threading/Tasks/Task;|9',
 'System/Threading/Tasks/Task|M|Delay|(I)LSystem/Threading/Tasks/Task;|9',
 'System/Threading/Tasks/Task|M|Delay|(ILSystem/Threading/CancellationToken;)LSystem/Threading/Tasks/Task;|9',
 'System/Threading/Tasks/Task|M|Delay|(LSystem/TimeSpan;)LSystem/Threading/Tasks/Task;|9',
 'System/Threading/Tasks/Task|M|Delay|(LSystem/TimeSpan;LSystem/Threading/CancellationToken;)LSystem/Threading/Tasks/Task;|9'}

def check_surface(jar):
    before=surface_lines(Path(c.read(FROZEN/'historical-preservation.json')['baseline']['jarPath']))
    after=surface_lines(jar)
    c.require(after-before==ADDITIONS and not before-after,'complete public surface exactly five additions')
    return dict(additions=sorted(after-before),removed=[],before=len(before),after=len(after))

class Session:
    def __init__(self,out,mode,jar=None):
        self.out=out;prepare(out);self.deadline=time.monotonic()+1800
        self.record=dict(status='RUNNING',mode=mode,commands=[],groups=[],nativeExecutions=0,acceptanceCredit=0)
        if jar:self.record['candidateJar']=c.descriptor(jar)
        self.record['payload']=payload_lock()
        self.record['inputs']=[];self.record['sourceSnapshots']=[]
        for source in sorted(HERE.glob('*')):
            if not source.is_file():continue
            original=c.descriptor(source);target=out/'input-snapshots'/original['sha256']/source.name
            target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(source.read_bytes())
            self.record['inputs'].append(c.descriptor(target))
            self.record['sourceSnapshots'].append(dict(original=original,durable=c.descriptor(target)))
        self.save()
    def save(self):write(self.out/'receipt.json',self.record)
    def step(self,label,argv,out=None,timeout=120):
        out=out or self.out
        ent={'label':label};self.record['commands'].append(ent);self.save()
        def update(value):ent.update(value);self.save()
        ent.update(checked_launch(argv,out,label,timeout,self.deadline,update));self.save();c.successful(ent)
        return ent
    def jdk(self,tool,*args):
        flags=frozen_phases.jvm(self.out) if tool=='java' else ['-J'+x for x in frozen_phases.jvm(self.out)]
        rec=self.step(('compile-' if tool=='javac' else 'run-')+tool+'-'+str(len(self.record['commands'])),[str(JDK/'bin'/(tool+'.exe')),*flags,*args])
        return Path(rec['stdoutPath']).read_text(encoding='utf-8')
    def java_group(self,name,fixtures,main,modes,jar,module=False):
        out=self.out/name;prepare(out)
        pathargs=['--module-path',str(jar),'--add-modules','dotj.core.foundation.v1'] if module else ['-cp',str(jar)]
        self.step('compile-'+name,[str(JDK/'bin/javac.exe'),*['-J'+x for x in frozen_phases.jvm(out)],'-parameters','-encoding','UTF-8','-implicit:none','-sourcepath',str(out/'empty-sourcepath'),*pathargs,'-d',str(out/'classes'),*map(str,fixtures)],out)
        classes=sorted((out/'classes').rglob('*.class'))
        c.require(classes and not list((out/'empty-sourcepath').iterdir()),'isolated fixture-only compilation')
        c.require(all(p.name.startswith(tuple(f.stem for f in fixtures)) for p in classes),'no product source fallback')
        records=[]
        for n,(owner,args) in enumerate(modes or [(main,[])]):
            cp=['--module-path',str(jar),'--add-modules','dotj.core.foundation.v1','-cp',str(out/'classes')] if module else ['-cp',str(out/'classes')+os.pathsep+str(jar)]
            rec=self.step('run-'+name+'-'+str(n),[str(JDK/'bin/java.exe'),*frozen_phases.jvm(out),*cp,owner,*args],out)
            c.require(Path(rec['stderrPath']).read_bytes()==b'','unexpected runtime stderr: '+name);records.append(rec)
        group=dict(name=name,fixture=[c.descriptor(p) for p in fixtures],classes=[c.descriptor(p) for p in classes],payloads=[r['streams']['stdout'] for r in records])
        self.record['groups'].append(group);self.save();return group,records
