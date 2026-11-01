"""Verify retained same-JAR raw observations; never launches native, Java, or a build."""
import ast
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
E = ROOT/'planning/stage-2/repos/dotj-core/evidence'
H = Path('D:/AI/Implementation/dotj Frameworks/worktrees/dotj-core-cancelasync-v1/tools/oracle/dotj-core/public-worktask-cancelasync-v1')
sys.path.insert(0, str(H))
import capture_support as c
import receipt_validation as rv

HISTORICAL_BUILDER = H.parent/'build-foundation-product-candidate.py'
HISTORICAL_SHA = '8424dc445c98b3167268259664ce365c5d0fbd9eb1403c08b733ee821295234d'
ARCHIVE = Path('D:/AI/Implementation/dotj Frameworks/orchestration/two-frameworks/batch2514-tested-builder-before-encoding-fix.py')

def historical_pin(pin, archive):
    """One explicit historical input relocation, never a generic stale-pin fallback."""
    if Path(pin['path']).resolve()==HISTORICAL_BUILDER.resolve() and pin['sha256']==HISTORICAL_SHA:
        c.require(Path(archive['path']).resolve()==ARCHIVE.resolve() and archive['sha256']==HISTORICAL_SHA
                  and archive['sizeBytes']==pin['sizeBytes']==339629,'exact archived builder identity')
        c.pin(archive)
    else:c.pin(pin)

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def command(record):
    c.successful(record)
    for flag in ['jobAssigned','resumed']:c.require(record.get(flag) is True,'owned process '+flag)
    c.require(type(record.get('exitCode')) is int and record['exitCode']==0,'typed success exit')
    c.require(record['cleanupLimitSeconds']==5 and record['cleanupSeconds']<=5 and record['outputPollSeconds']==0.1,'cleanup/output bounds')
    for name,d in record['streams'].items():
        c.pin(d);c.require(d['path']==record[name+'Path'],'raw stream path');c.bounded(d['path'],record['outputLimitsBytes'][name])
    sample=record['resources'][-1]
    c.require(sample['freePhysicalBytes']>=512*1024**2 and sample['freeVirtualBytes']>=16*1024**3,'resource readiness')

def main():
    e=c.read(E/'public-worktask-cancelasync-v1.json')
    artifact=c.read(E/'foundation-product-candidate-v1.json');jar=ROOT/artifact['jarPath']
    c.require(c.sha(jar)==artifact['jarSha256']==e['candidateJar']['sha256'],'current gate JAR differs: rerun selected groups on actual final JAR')
    for source in artifact['productSources']:c.require(c.sha(ROOT/source['path'])==source['sha256'],'current artifact source binding')
    c.pin(e['contract']);c.pin(e['nativeInputLock']);c.pin(e['observationLock']);c.pin(e['javaLock'])
    c.pin(e['baselineRed']);c.pin(e['nativeReceipt']);c.pin(e['coordinator'])
    c.pin(e['builderCorrection']);correction=c.read(e['builderCorrection']['path'])
    c.pin(correction['historical']);c.pin(correction['current'])
    def phase(path):return ast.dump(next(n for n in ast.parse(Path(path).read_text(encoding='utf-8')).body if isinstance(n,ast.FunctionDef) and n.name=='build_product'),include_attributes=False)
    c.require(phase(correction['historical']['path'])==phase(correction['current']['path']),'executed canonical artifact phase unchanged')
    c.pin(e['currentJavaLock'])
    for pin in c.read(e['currentJavaLock']['path'])['pins']:c.pin(pin)
    runner=load('retained_product_primitives',Path(e['coordinator']['path']))
    args=runner.native_args();args.java_lock=Path(e['javaLock']['path']);args.java_lock_sha256=e['javaLock']['sha256'];args.candidate_jar=Path(e['candidateJar']['path']);args.candidate_sha256=e['candidateJar']['sha256']
    new=runner.new
    for key in ['build','oldPartial','oldFollowup','auditPartial','auditFollowup']:
        d=e['receipts'][key];c.pin(d);record=c.read(d['path'])
        for pin in record['inputs']:historical_pin(pin,correction['historical'])
        expected_status={'build':'PASS_STAGED_BUILD','oldPartial':'FAILED_STOP_NO_RETRY','oldFollowup':'PASS_STAGED_OLD','auditPartial':'FAILED_STOP_NO_RETRY','auditFollowup':'PASS_STAGED_AUDITS'}[key]
        c.require(record['status']==expected_status,'exact staged receipt status '+key)
    def historical_java_inputs(request):
        c.require(c.sha(request.java_lock)==request.java_lock_sha256,'historical Java lock hash')
        lock=c.read(request.java_lock)
        for pin in lock['pins']:historical_pin(pin,correction['historical'])
        jar=c.confined(request.candidate_jar)
        c.require(c.sha(jar)==request.candidate_sha256 and lock['candidateJar']==c.descriptor(jar),'historical same-JAR identity')
        expected={'PublicWorkTaskCancelAsyncFixtures.java'} if request.mode!='boundaries' else {'WorkTaskBoundaryControls.java','CancelAsyncBoundaryControls.java'}
        for name in expected:
            c.require(any(x['kind']=='java-fixture' and Path(x['path']).resolve()==(H/name).resolve() and x['sha256']==c.sha(H/name) for x in lock['pins']),'exact historical fixture '+name)
        return jar,lock
    for mode in ['compare','boundaries']:
        d=e['receipts'][mode];c.pin(d);args.mode='verify'
        rv.validate_receipt(args,c.read(d['path']),Path(d['path']).parent,java_inputs=historical_java_inputs,native_reference=new.frozen_native)
    old=runner.old;oldlock=c.read(e['oldObservationLock']['path']);c.pin(e['oldObservationLock']);c.pin(oldlock['nativeReceipt'])
    raw=old.read(oldlock['nativeReceipt']['path'])['commands'][-1]['streams']['stdout'];c.pin(raw)
    native=old.observations(c.bounded(raw['path']),old.read(runner.OLD/'schema.json'),True)
    c.require(native==oldlock['observations'] and len(native)==697,'original old native raw/lock binding')
    failed=e['receipts']['oldPartial'];c.pin(failed);pr=c.read(failed['path'])
    c.require(pr['status']=='FAILED_STOP_NO_RETRY' and pr['candidateJar']['sha256']==e['candidateJar']['sha256'],'retained partial failure status')
    c.require([x['label'] for x in pr['commands']]==['compile-task','run-task','compile-task-boundaries','run-task-boundaries'],'partial command order')
    for x in pr['commands'][:3]:command(x)
    c.require(type(pr['commands'][3]['exitCode']) is int and pr['commands'][3]['exitCode']==1,'historical boundary failure retained')
    for d in pr['commands'][3]['streams'].values():c.pin(d)
    task=pr['groups'][0];c.pin(task['payload'])
    c.require(old.observations(c.bounded(task['payload']['path']),old.read(runner.OLD/'schema.json'),False)==native,'same-JAR old Task697')
    d=e['receipts']['oldFollowup'];c.pin(d);follow=c.read(d['path'])
    c.require(follow['status']=='PASS_STAGED_OLD' and follow['candidateJar']['sha256']==e['candidateJar']['sha256'],'old followup candidate')
    names=['task-boundaries','delegate-action-v1','public-cancellation-v1','public-valuetask-v1']
    c.require([g['name'] for g in follow['groups']]==names,'ordered old groups')
    c.require([x['label'] for x in follow['commands']]==[prefix+name for name in names for prefix in ['compile-','run-']],'ordered old commands')
    plan=c.read(runner.O/'batch2512-packaged-regression-plan-v2.json')['groups']
    for x in follow['commands']:command(x)
    for index,g in enumerate(follow['groups']):
        for d in g['fixture']+g['classes']+[g['payload']]:c.pin(d)
        raw=c.bounded(g['payload']['path'])
        if index==0:c.require(raw.decode().strip()=='PASS Task Java boundary controls: 49','original 49 controls')
        else:
            payload={}
            for line in rv.lf_lines(raw,'old retained plain payload'):
                key,value=line.split('=',1);c.require(key not in payload,'duplicate old key');payload[key]=value
            c.require(payload==plan[index-1]['expected'] and len(payload)==[34,48,135][index-1],'retained old frozen observations')
    c.require(e['qualifiedFrameworks']==0 and e['acceptanceCredit']==0,'no promoted acceptance')
    print('PASS verify-only same-JAR WorkTask/CancelAsync 66/612 +8; Task61/697 +49; delegate34/cancellation48/ValueTask135; native unchanged')

if __name__=='__main__':main()
