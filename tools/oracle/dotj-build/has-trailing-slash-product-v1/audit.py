"""Read-only external receipt audit; launches no processes."""
import argparse, importlib.util, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('predicate_audited_successor',HERE/'verify.py')
v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
c=v.c

def check_descriptor(d):
    c.require(c.descriptor(d['path'])==d,'artifact descriptor changed: '+d['path'])

def audit(path,pin,lockpin):
    c.require(c.sha(path)==pin,'externally pinned GREEN receipt changed')
    r=c.read(path);out=path.parent
    c.require(r['status']=='PASS_HAS_TRAILING_SLASH_PRODUCT_V1','GREEN status missing')
    c.require(r['acceptedTasksAdded']==r['nativeLaunches']==r['numberedBatchCredit']==0,'credit/native launch changed')
    lockpath=out/'artifact-lock.json';c.require(c.sha(lockpath)==lockpin,'externally pinned artifact lock changed')
    lock=c.read(lockpath);check_descriptor(lock['receipt'])
    for d in lock['artifacts']:check_descriptor(d)
    for d in r['sourceInputs']+r['toolchain']+[r['candidateJar'],r['coordinator'],r['oneBuildReceipt'],r['oneBuildCoordinatorSnapshot'],r['canonical94Receipt'],r['ownedGuard']]:check_descriptor(d)
    c.require(r['frozenInputsAfter']==r['frozenInputsBefore']==v.frozen_inputs(),'frozen native evidence changed')
    expected=['compile-candidate','compile-tests','packaged-contract','packaged-locations','packaged-default-cycles','packaged-import-profiles','packaged-import-paths','packaged-import-path-whitespace','compile-successor-consumers','packaged-cache','packaged-condition','packaged-and','packaged-cache-controls','packaged-predicate','packaged-predicate-controls']
    commands=r['oneBuildCommands']+r['commands'];c.require([x['label'] for x in commands]==expected,'actual JDK command coverage differs')
    jar=r['candidateJar']['path']
    for command in commands:
        c.successful(command)
        c.require(command['jobAssigned'] is True and command['resumed'] is True,'unowned/unresumed child')
        c.require(command['timeoutSeconds']==120 and command['cleanupLimitSeconds']==5 and command['outputPollSeconds']==0.1,'guard bounds differ')
        c.require(command['outputLimitsBytes']=={'stdout':2097152,'stderr':524288},'raw output limits differ')
        c.require(Path(command['argv'][0]) in [v.JDK/'bin/java.exe',v.JDK/'bin/javac.exe'],'unapproved JDK executable')
        for stream in ['stdout','stderr']:check_descriptor(command[stream])
        c.require(Path(command['stderrPath']).read_bytes()==b'','JDK stderr nonempty')
        args=command['argv'];vm_prefix='-J' if Path(args[0]).name=='javac.exe' else ''
        c.require(vm_prefix+'-Xmx128m' in args and vm_prefix+'-XX:ActiveProcessorCount=2' in args,'JDK heap/CPU bounds differ')
        if command['label']!='compile-candidate':c.require(args[args.index('--module-path')+1]==jar,'dataset did not use exact one-build JAR')
        if command['label'].startswith('compile-') and command['label']!='compile-candidate':
            c.require('-implicit:none' in args and '-sourcepath' in args and not list(Path(args[args.index('-sourcepath')+1]).iterdir()),'compiler source fallback permitted')
    samples=r['oneBuildResourceSamples']+r['resourceSamples']
    immediate=[x for x in samples if 'prelaunch' in x]
    c.require(len(immediate)==len(commands),'fresh prelaunch resource coverage differs')
    for x in immediate:
        sample=x['prelaunch'];c.require(type(sample['freePhysicalBytes']) is int and sample['freePhysicalBytes']>=512*1024**2 and type(sample['freeVirtualBytes']) is int and sample['freeVirtualBytes']>=16*1024**3 and 0<=x['durationSeconds']<=2,'fresh resource bounds differ')
    for d in [out/'controller-receipt.json',Path(r['oneBuildReceipt']['path']).parent/'controller-receipt.json']:
        controller=c.read(d)['process']
        c.require(controller['jobAssigned'] is True and controller['resumed'] is True and controller['timeoutSeconds']==600,'outer ownership/bound changed')
    c.successful(c.read(out/'controller-receipt.json')['process'])
    v.validate_classes([p.relative_to(out/'consumer-classes').as_posix() for p in (out/'consumer-classes').rglob('*') if p.is_file()],r['consumerOutputClasses'])
    v.v3.and_product.verify94(Path(r['canonical94Receipt']['path']).parent/'outputs/all-comparisons.tsv',v.v3.GOLDEN94)
    v.v3.and_product.verify_probe_results(out/'and-results.tsv',v.v3.native_sets()[0])
    v.validate_lines((out/'cache-controls.tsv').read_text().splitlines(),v.cache.control_rows())
    c.require(len((out/'predicate-results.tsv').read_text().splitlines())==38,'predicate result coverage missing')
    c.require(not list(out.rglob('must-not-exist.txt')),'task marker created')
    return r,{'status':'PASS_EXTERNAL_RECEIPT_AUDIT','receipt':c.descriptor(path),'artifactLock':c.descriptor(lockpath),'verifiedArtifacts':len(lock['artifacts']),'jdkCommands':len(commands),'productBuilds':sum(x['label']=='compile-candidate' for x in commands),'candidateJar':r['candidateJar'],'counts':r['counts'],'acceptedTasksAdded':0}

def main():
    p=argparse.ArgumentParser();p.add_argument('--receipt',type=Path,required=True);p.add_argument('--receipt-sha256',required=True);p.add_argument('--artifact-lock-sha256',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    out=c.confined(a.out);c.require(not out.exists(),'new audit directory required');out.mkdir()
    r,result=audit(a.receipt,a.receipt_sha256,a.artifact_lock_sha256)
    result.update(auditor=c.descriptor(HERE/'audit.py'),processesLaunched=0)
    c.write(out/'audit.json',result);print(json.dumps({'status':result['status'],'audit':c.descriptor(out/'audit.json')}))

if __name__=='__main__':main()
