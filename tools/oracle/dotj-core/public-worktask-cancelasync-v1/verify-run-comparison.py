"""MOCK_ONLY deterministic parser/composition controls. No compiler/native/JVM launch."""
import ast,base64,contextlib,copy,hashlib,importlib.util,io,json,os,sys,tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
FIXED=Path('D:/AI/Implementation/dotj Frameworks/worktrees/dotj-core-cancelasync-v1/tools/oracle/dotj-core/public-worktask-cancelasync-v1')
if Path(__file__).resolve().parent!=FIXED.resolve():raise ValueError('entrypoint path changed')
sys.path.insert(0,str(FIXED))
import capture_support as c
A=c.B/'agents/batch2514-worktask-cancelasync-native-preparation-v1'
TMP=A/'mock-temp';TMP.mkdir(exist_ok=True);tempfile.tempdir=str(TMP)
schema=c.read(FIXED/'schema.json');kinds=c.keys(schema);results=[]
def check(name,fn,reject=False):
    try:fn()
    except (ValueError,AssertionError,UnicodeError) as error:
        if not reject:raise
        results.append({'control':name,'status':'PASS_REJECTED','error':str(error)});return
    if reject:raise AssertionError('accepted negative '+name)
    results.append({'control':name,'status':'PASS'})
def raw(native=False):
    lines=[k+'\t'+kind+'\t'+('false' if kind=='b' else '0' if kind=='i' else base64.b64encode(b'MOCK_ONLY').decode()) for k,kind in kinds.items()]
    if native:lines.append('meta.runtime\ts\t'+base64.b64encode(b'10.0.12').decode())
    return ('\n'.join(lines)+'\n').encode()
good=raw();native=raw(True);lines=good.splitlines(keepends=True)
check('exact612JavaSyntheticScalars',lambda:c.require(len(c.observations(good,schema))==612,'count'))
check('exact612NativeSyntheticScalarsAndRuntime',lambda:c.require(len(c.observations(native,schema,True))==612,'count'))
check('CRLFFramingPreservesStrings',lambda:c.require(c.observations(good.replace(b'\n',b'\r\n'),schema)==c.observations(good,schema),'CRLF'))
for name,data in [('empty',b''),('missing',b''.join(lines[1:])),('duplicate',good+lines[0]),('extra',good+b'extra\tb\ttrue\n'),('wrongType',good.replace(b'\ti\t0',b'\tb\tfalse',1)),('wrongBool',good.replace(b'\tb\tfalse',b'\tb\tFalse',1)),('zeroPaddedInt',good.replace(b'\ti\t0',b'\ti\t00',1)),('plusInt',good.replace(b'\ti\t0',b'\ti\t+1',1)),('negativeZero',good.replace(b'\ti\t0',b'\ti\t-0',1)),('overflow',good.replace(b'\ti\t0',b'\ti\t2147483648',1)),('badBase64',good.replace(b'TU9DS19PTkxZ',b'***',1)),('UTF8',b'\xff\n'),('noFinalLF',good[:-1]),('standaloneCR',good.replace(b'\n',b'\r',1)),('NUL',good+b'\x00'),('unicodeLineSeparator',good.replace(b'\n',b'\xe2\x80\xa8',1)),('oversize',b'x'*(c.MAX+1))]:
    check(name,lambda data=data:c.observations(data,schema),True)
check('missingRuntime',lambda:c.observations(good,schema,True),True)
check('wrongRuntime',lambda:c.observations(native.replace(base64.b64encode(b'10.0.12'),base64.b64encode(b'10.0.11')),schema,True),True)
check('duplicateJSON',lambda:json.loads('{"x":1,"x":2}',object_pairs_hook=c.pairs),True)
check('noStringNormalization',lambda:c.require(c.observations(good.replace(b'TU9DS19PTkxZ',base64.b64encode(b'  path\\name\r\nnext  '),1),schema)['R01.type']=='  path\\name\r\nnext  ','preserve exact text'))
for field,value in [('exitCode',None),('exitCode',False),('exitCode',1),('launched',False),('timedOut',True),('cleanupError','unresolved'),('error','launch'),('outputLimitExceeded',True)]:
    check('typedExit_'+field+'_'+str(value),lambda field=field,value=value:c.successful(dict({'exitCode':0,'launched':True,'timedOut':False},**{field:value})),True)
check('typedExitZero',lambda:c.successful({'exitCode':0,'launched':True,'timedOut':False}))
def bounded_first():
    with tempfile.TemporaryDirectory(dir=TMP) as t:
        p=Path(t)/'raw';p.write_bytes(b'x'*65)
        with patch.object(Path,'open',side_effect=AssertionError('must reject before open')):
            try:c.bounded(p,64)
            except ValueError:return
        raise AssertionError('oversize accepted')
check('boundedReadBeforeOpen',bounded_first)
def incremental():
    with tempfile.TemporaryDirectory(dir=TMP) as t:
        p=Path(t)/'raw';p.write_bytes(b'hash')
        with patch.object(Path,'read_bytes',side_effect=AssertionError('whole-file hash')):c.require(c.sha(p)==hashlib.sha256(b'hash').hexdigest(),'incremental')
check('incrementalHash',incremental)
def composition(stale=False):
    events=[];clock=[0]
    class Guard:
        def wait_resources(self,deadline):events.append('wait');clock[0]=119;return (116 if stale else 119),[{'MOCK_ONLY':True}]
        def run(self,argv,out,env,label,timeout,**kw):
            events.append('run');c.require(clock[0]==119,'wait inside process clock');kw['prelaunch']();return {'MOCK_ONLY':True}
    with patch.object(c,'streams',return_value={}):c.launch(Guard(),['MOCK_ONLY'],TMP,{},'run-native',30,200,lambda r:None,now=lambda:clock[0])
    c.require(events==['wait','run'],'resource ordering')
check('119SecondWaitBeforeProcessClock',composition)
check('StaleSampleRejectedBeforeGuardClock',lambda:composition(True),True)
def commands():
    out=A/'future-native-capture-v1';jar=c.B/'validation/Batch-2512-gate2/source/dotj-core/dotj-core-public/build/foundation-v1/dotj-core-foundation-v1.jar'
    native=c.commands(out,'capture');c.require([t for _,t,_ in native]==[120,30],'native timeouts')
    argv=native[0][2];c.require(all(x in argv for x in ['-noconfig','-nostdlib','-deterministic','-langversion:14']),'native exact compiler flags')
    c.require(not any(x in ' '.join(argv) for x in [' restore',' build','download']),'no build/restore')
    for mode in ['baseline-red','compare','boundaries']:
        cmds=c.commands(out,mode,jar);c.require('-implicit:none' in cmds[0][2] and '-sourcepath' in cmds[0][2] and str(jar) in cmds[0][2],'JAR-only compile')
        c.require(all(t==120 for _,t,_ in cmds),'JDK timeout')
        if mode=='baseline-red':c.require(len(cmds)==1,'compile-only actual RED')
check('ExactProposedCommandBounds',commands)
def source_syntax():
    for p in FIXED.glob('*.py'):ast.parse(p.read_text(),filename=str(p))
check('PythonASTAllEntrypoints',source_syntax)
manifest=c.read(FIXED/'fixture-manifest.json')
check('Adopted66And612And8',lambda:c.require(len(manifest['pairedRows'])==66 and sum(len(r['stableFields']) for r in manifest['pairedRows'])==612 and len(manifest['javaPrivateRows'])==8,'adopted counts'))
check('NoInventedObservedValues',lambda:c.require(manifest['values']=='UNOBSERVED' and manifest['nativeCaptureCount']==0,'unobserved'))
# Reuse the immutable W12 69-control suite in memory, relocating only its scratch root.
# Historical code/files are read only. Every launch in that suite is an injected fake.
old=c.GUARD.parent/'verify-run-comparison.py';source=old.read_text()
c.require('subprocess.run(' not in source and 'subprocess.Popen(' not in source,'unexpected real launch in inherited pure suite')
source=source.replace("PRIVATE=Path('D:/AI/Implementation/dotj Frameworks/agents/batch2512-task-native-preparation-v1')",'PRIVATE=Path('+repr(str(A))+')')
namespace={'__file__':str(old),'__name__':'inherited_w12_mock_controls'}
with contextlib.redirect_stdout(io.StringIO()) as captured:exec(compile(source,str(old),'exec'),namespace)
inherited=json.loads(captured.getvalue());c.require(inherited['controlCount']==69 and inherited['nativeExecuted'] is False and inherited['javaExecuted'] is False and inherited['compilerExecuted'] is False,'W12 69 inherited mock controls')
report={'status':'PASS_STATIC_MOCK_ONLY','controlCount':len(results)+69,'newCompositionAndParserControlCount':len(results),'inheritedImmutableGuardControlCount':69,'controls':results,'inheritedControls':inherited['controls'],'historicalSuite':c.descriptor(old),'values':'MOCK_ONLY_NOT_NATIVE_OBSERVATIONS','nativeExecuted':False,'javaExecuted':False,'compilerExecuted':False}
c.write(A/'static-mock-controls-v1.json',report);print(json.dumps(report,indent=2))
