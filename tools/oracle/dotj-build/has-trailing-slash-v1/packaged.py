"""Prepare JAR-only commands and bridge from reviewed native observations.

This module never launches a compiler/JVM. Root executes reviewed command plans
with the pinned owned guard, and retains compiler/runtime receipts separately.
"""
import argparse, base64, re, shutil
from pathlib import Path
import capture as c
import verify as pair
JDK=c.B/'toolchains/jdk-qualified/jdk-21.0.12.1+1'
MODULE='org.dotj.build.evaluation.candidate'
PACKAGE='org.dotj.internal.build.evaluation'
CONSUMER=c.W/'dotj-build/evaluation-candidate/tests/org/dotj/internal/build/evaluation/HasTrailingSlashPackagedTest.java'
BASELINE=c.B/'validation/Batch-2511-cache-product-final-green-run3/packaged94/dotj-build-evaluation-candidate.jar'
BASELINE_SHA='add631430ab15623f4ba083a9da434d607894685a3def59fc44419d29048e3fa'
def encode(value):return base64.b64encode(value.encode('utf-8')).decode('ascii')
def relative(value,root,ident):
    prefix=str(Path(root)/ident)+'\\'
    c.require(value.startswith(prefix),'native path outside case')
    return value[len(prefix):].replace('\\','/')
def bridge(receipt):
    classes=c.read(c.C/'case-classifications.json')['cases'];lines=[]
    for row,definition in zip(receipt['payload']['rows'],classes):
        ident=row['id'];c.require(ident==definition['id'],'bridge classification order')
        if definition['category']=='semantic':
            ev=row['evaluation'];c.require(ev['success'] is True,'semantic native case failed; root review required')
            imports='|'.join(relative(e['owner'],receipt['fixtureRoot'],ident)+'>'+relative(e['project'],receipt['fixtureRoot'],ident)+'@'+str(e['line'])+':'+str(e['column']) for e in ev['imports'])
            warnings=[]
            for event in row['diagnostics']:
                c.require(event['kind']=='warning' and event['code']=='MSB4130','unexpected event cannot be dropped')
                quoted=re.findall(r'"([^"]*)"',event['message'])
                c.require(len(quoted)==1,'warning condition cannot be unambiguously bridged')
                warnings.append(event['code']+':'+relative(event['file'],receipt['fixtureRoot'],ident)+'@'+str(event['line'])+':'+str(event['column'])+':'+quoted[0])
            fields=[ident,'MATCHED_EVALUATION',encode(ev['properties']['P']),encode(ev['properties']['Q']),encode(imports),encode('|'.join(warnings))]
        else:fields=[ident,definition['privateDisposition'],','.join(definition['privateErrorCodes'])]
        lines.append('CASE\t'+'\t'.join(fields))
        for key,value in row['globals'].items():lines.append('GLOBAL\t'+encode(key)+'\t'+encode(value))
        lines.append('END')
    return '\n'.join(lines)+'\n'
def commands(out,jar,bridge_path,mode):
    vm=['-Xms16m','-Xmx128m','-XX:ActiveProcessorCount=2','-XX:+UseSerialGC','-Djava.io.tmpdir='+str(out/'tmp'),'-Duser.home='+str(out/'home'),'-Duser.language=en','-Duser.country=US','-XX:ErrorFile='+str(out/'tmp/hs_err_pid%p.log'),'-XX:HeapDumpPath='+str(out/'tmp')]
    classes=out/'consumer-classes';empty=out/'empty-sourcepath';source=out/'consumer-source'/Path(*PACKAGE.split('.'))/CONSUMER.name
    return [{'label':'compile-java','timeoutSeconds':120,'argv':[str(JDK/'bin/javac.exe'),*['-J'+v for v in vm],'--release','21','-encoding','UTF-8','-implicit:none','-sourcepath',str(empty),'--module-path',str(jar),'--patch-module',MODULE+'='+str(out/'consumer-source'),'-d',str(classes),str(source)],'allowedOutputClasses':[PACKAGE.replace('.','/')+'/HasTrailingSlashPackagedTest.class'],'requireEmptySourcepath':str(empty)},
      {'label':'run-java','timeoutSeconds':120,'argv':[str(JDK/'bin/java.exe'),*vm,'--limit-modules','java.base,java.xml,'+MODULE,'--module-path',str(jar),'--patch-module',MODULE+'='+str(classes),'-m',MODULE+'/'+PACKAGE+'.HasTrailingSlashPackagedTest',str(bridge_path),str(out/('private-controls' if mode=='controls' else 'fixtures')),str(out/'results.tsv'),str(jar),mode]}]
def main():
    p=argparse.ArgumentParser();p.add_argument('--receipt',type=Path,required=True);p.add_argument('--receipt-sha256',required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--mode',choices=['red','corpus','controls'],required=True);p.add_argument('--jar',type=Path,default=BASELINE);p.add_argument('--jar-sha256',default=BASELINE_SHA)
    a=p.parse_args();out=c.confined(a.out);out.mkdir(parents=True,exist_ok=False)
    c.require(c.sha(a.jar)==a.jar_sha256,'JAR identity changed')
    native=pair.receipt(a.receipt,a.receipt_sha256)
    source=out/'consumer-source'/Path(*PACKAGE.split('.'))/CONSUMER.name;source.parent.mkdir(parents=True);shutil.copyfile(CONSUMER,source)
    shutil.copytree(c.C/'fixtures',out/'fixtures')
    for directory in ['empty-sourcepath','tmp','home','consumer-classes']:(out/directory).mkdir()
    text=bridge(native);(out/'native-bridge.tsv').write_text(text,encoding='utf-8',newline='\n')
    c.write(out/'proposed-java-commands.json',{'status':'PREPARED_NOT_EXECUTED','jar':c.descriptor(a.jar),'consumer':c.descriptor(CONSUMER),'nativeReceipt':c.descriptor(a.receipt),'bridge':c.descriptor(out/'native-bridge.tsv'),'commands':commands(out,a.jar,out/'native-bridge.tsv',a.mode),'executionRequirements':{'ownedGuardSha256':c.GUARD_SHA,'freshPhysicalBytes':512*1024**2,'availableCommitBytes':16*1024**3,'stdoutLimitBytes':2*1024**2,'stderrLimitBytes':512*1024,'compilerStderrLimitBytes':512*1024,'cleanupSeconds':5,'prelaunchResourceFreshSeconds':2,'resourceWaitSeconds':120,'noAutomaticRetry':True,'inspectCompilerOutputMembership':True},'genuineRedRequired':'HT01 NATIVE_SUPPORTED_PREDICATE_REJECTED CONDITION_PROFILE with nonzero JVM assertion exit. Compile failure, timeout, resource deferral and missing files never count as RED.'})
if __name__=='__main__':main()
