"""Read-only verification of the retained sole-JAR qualification; launches no compiler/JVM/native process."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import contract as c
import argparse,zipfile
LABELS=['compile-consumers','packaged-boolean','packaged-current-base','packaged-current-locations','packaged-current-cycles','packaged-current-profiles','packaged-current-paths','packaged-current-whitespace','packaged-condition','packaged-cache','packaged-and','packaged-cache-controls','packaged-predicate','packaged-predicate-controls']
def success(process):
    c.require(type(process['processId'])is int and process['processId']>0 and type(process['exitCode'])is int and process['exitCode']==0,'typed process identity/exit')
    for k in ['launched','jobAssigned','resumed']:c.require(process[k]is True,'ownership '+k)
    for k in ['timedOut','outputLimitExceeded']:c.require(process[k]is False,'process bound '+k)
    c.require('cleanupError'not in process and 'error'not in process and process['cleanupLimitSeconds']==5 and process['cleanupSeconds']<=5 and process['timeoutSeconds'] in [120,600],'cleanup/timeout')
    c.require(process['outputPollSeconds']==0.1 and process['outputLimitsBytes']=={'stdout':2097152,'stderr':524288},'raw stream limits')
def main():
    p=argparse.ArgumentParser();p.add_argument('--receipt',type=Path,required=True);p.add_argument('--receipt-sha256',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    c.require(c.sha(a.receipt)==a.receipt_sha256,'external success receipt pin');r=c.read(a.receipt);root=a.receipt.parent
    c.require(r['status']=='PASS_PRIVATE_BOOLEAN_PRODUCT_CANDIDATE','qualification status')
    native=c.frozen();contract=c.read(c.HERE/'CONTRACT.json');c.validate_contract(contract,native)
    for field in ['inputPins','fixtureInputs','bridges','stagedSources','sourceInputs','historicalValidators','resultFiles']:
        for d in r[field]:c.pin(d)
    for field in ['candidateJar','consumerJar','sourceCoordinator','ownedGuard','baselineRed','nativeLock','oneBuildReceipt']:c.pin(r[field])
    c.require([x['label'] for x in r['commands']]==LABELS,'full command coverage')
    for command in r['commands']:
        process=command['process'];success(process);c.pin(command['stdout']);c.pin(command['stderr']);c.require(Path(command['stderr']['path']).read_bytes()==b'','unexpected stderr')
        sample=command['resources'][-1];c.require(type(sample['prelaunch']['freePhysicalBytes'])is int and sample['prelaunch']['freePhysicalBytes']>=512*1024**2 and type(sample['prelaunch']['freeVirtualBytes'])is int and sample['prelaunch']['freeVirtualBytes']>=16*1024**3 and 0<=sample['durationSeconds']<=2,'fresh physical/available-commit sample')
        argv=process['argv'];c.require('--module-path'in argv and argv[argv.index('--module-path')+1]==r['candidateJar']['path'],'exact sole JAR')
        if command['label']!='compile-consumers':c.require(argv[argv.index('--patch-module')+1]==c.MODULE+'='+r['consumerJar']['path'],'explicit consumer-only patch')
    built=c.read(r['oneBuildReceipt']['path']);c.require(built['sourceInputs']==r['sourceInputs'] and built['candidateJar']==r['candidateJar'],'single product source/JAR lineage')
    success(built['commands'][0]['process'])
    with zipfile.ZipFile(r['candidateJar']['path'])as z:
        cls=Path(r['productClasses']);actual={p.relative_to(cls).as_posix():p.read_bytes()for p in cls.rglob('*.class')};c.require(set(z.namelist())==set(actual)and all(z.read(k)==v for k,v in actual.items()),'product class/JAR bytes')
    with zipfile.ZipFile(r['consumerJar']['path'])as z:c.require(set(z.namelist())==set(r['consumerOutputClasses'])and not any(Path(n).name.startswith('ProjectEvaluationComponent$')or Path(n).name in ['ProjectEvaluationComponent.class','module-info.class']for n in z.namelist()),'consumer-only class membership')
    lines=(root/'boolean-results.tsv').read_text(encoding='utf-8').splitlines();expected=['\t'.join([x['id'],x['disposition'],*x['expectedFields']])for x in contract['nativeRecords']+contract['privateRecords']]
    expected += [x['id']+'\tPRIVATE_CONTROL\tPASS'for x in contract['groups']];c.require(lines==expected and len(lines)==327,'297+16+14 ordered exact fields')
    c.require(len(r['transitions'])==18 and [(x['id'],x['nativeCase'])for x in r['transitions']]==[(x['id'],x['nativeCase'])for x in contract['transitions']],'18 exact successor IDs')
    c.require([len(x['diagnostics'])for x in c.read(c.B/'validation/Batch-2511-cache-native-pair-v1/observation-lock.json')['normalizedPayload']['rows']]==[1,0,0,1,1,1,0,1],'retained cache vector')
    exports=c.read(c.HERE/'export-lock.json')['exports'];c.require(len({x['repositoryRelativePath']for x in exports})==len(exports),'export bijection')
    for x in exports:
        c.pin(x['original']);c.pin(x['export']);c.require(x['original']['sha256']==x['export']['sha256']and x['original']['sizeBytes']==x['export']['sizeBytes'],'raw export bytes')
    c.require(not list(root.rglob('must-not-exist.txt')),'task marker')
    result={'status':'PASS_READ_ONLY_SOLE_JAR_AUDIT','receipt':c.descriptor(a.receipt),'counts':r['counts'],'exportedFiles':len(exports),'historicalArchive':c.descriptor(c.ARCHIVE),'nativeLaunches':0,'jdkLaunches':0,'acceptedTasksAdded':0}
    c.write(a.out,result);print(result['status'],len(lines),'rows',len(exports),'raw exports')
if __name__=='__main__':main()
