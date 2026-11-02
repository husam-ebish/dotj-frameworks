"""Strict corroboration of observer paths, closed binaries and actual v3 trace.

Verbosity3 does not promise absolute TPA assembly paths. The observer emits
those paths; the host emits runtime load paths, deps selection and relative TPA
assets. Neither source is relabeled as the other's evidence.
"""
import importlib.util
import re
from pathlib import Path
s=importlib.util.spec_from_file_location('ordering_runtime_binding_protocol',Path(__file__).with_name('protocol.py'))
p=importlib.util.module_from_spec(s);s.loader.exec_module(p)

def verify(value,raw,contract=None):
    contract=contract if contract is not None else p.read(p.HERE/'runtime-binding-contract.json')
    return verify_context(value,raw,contract,p.read(p.HERE/'payload-lock.json'),p.read(p.HERE/'reuse-chain.json'),p.read(p.HERE/'execution-proposal.json')['fingerprint'])

def verify_context(value,raw,contract,payload,reused,expected):
    """Same binding assertions with an explicit immutable historical context."""
    p.keys(contract,['schemaVersion','fingerprint','binaryPins','observerPins','loadedLibraries','tpaEntries','depsPath','hostVersion'],'runtime binding contract')
    p.require(type(contract['schemaVersion']) is int and contract['schemaVersion']==1,'runtime binding version')
    p.require(p.same(contract['fingerprint'],expected),'closed runtime fingerprint contract')
    libraries={name:str(p.B/'toolchains/dotnet'/folder/name) for name,folder in [('hostfxr.dll','host/fxr/10.0.12'),('hostpolicy.dll','shared/Microsoft.NETCore.App/10.0.12'),('coreclr.dll','shared/Microsoft.NETCore.App/10.0.12')]}
    p.require(p.same(contract['loadedLibraries'],libraries) and contract['depsPath']==str(p.B/'toolchains/dotnet/sdk/10.0.401/MSBuild.deps.json'),'fixed runtime directory and SDK deps context')
    for key,expected_value in expected.items():p.require(type(value.get(key)) is str and value[key]==expected_value,'observer runtime/module fingerprint '+key)
    pins=payload['files'];seen=set()
    required={expected[k] for k in ['corePath','msbuildPath','frameworkPath']}|set(contract['loadedLibraries'].values())|{contract['depsPath']}
    for d in contract['binaryPins']:
        p.check_descriptor(d);p.require(d['path'] not in seen,'unique binding binary path');seen.add(d['path'])
        p.require(any(p.same(d,x) for x in pins),'exact closed payload binary descriptor');p.pin(d)
    p.require(seen==required,'complete module/runtime/deps binary binding set')
    p.require(p.same(contract['observerPins'],[reused[k] for k in ['source','dll','runtimeconfig']]),'trusted observer source/binary/runtimeconfig chain')
    for d in contract['observerPins']:p.pin(d)
    p.require(type(raw) is bytes and len(raw)<=524288,'bounded retained host trace')
    try:text=raw.decode('utf-8')
    except UnicodeError as error:raise ValueError('host trace encoding') from error
    lines=text.splitlines();evidence=[]
    # Reject a contradictory duplicate as well as missing evidence. These are
    # actual loaded runtime libraries, not invented assembly load log entries.
    for name,expected_path in contract['loadedLibraries'].items():
        matches=[(n,line) for n,line in enumerate(lines,1) if line.startswith('Loaded library from ') and re.split(r'[\\/]',line)[-1].casefold()==name.casefold()]
        p.require(len(matches)==1 and matches[0][1]=='Loaded library from '+expected_path,'exact host loaded-library context '+name)
        evidence.append(dict(kind='LOADED_RUNTIME_LIBRARY',line=matches[0][0],text=matches[0][1]))
    deps=[(n,line) for n,line in enumerate(lines,1) if line.startswith('Deps file: ')]
    p.require(len(deps)==1 and deps[0][1]=='Deps file: '+contract['depsPath'],'exact host deps context')
    evidence.append(dict(kind='DEPS_SELECTION',line=deps[0][0],text=deps[0][1]))
    p.require(contract['hostVersion']=='10.0.12','fixed host version')
    for component in ['dotnet','hostfxr_main_startupinfo','hostpolicy']:
        rows=[(n,line) for n,line in enumerate(lines,1) if line.startswith('--- Invoked '+component+' [version: ')]
        p.require(len(rows)==1 and rows[0][1].startswith('--- Invoked '+component+' [version: '+contract['hostVersion']+' @Commit: '),'host invocation version '+component)
    actual=[]
    pattern=re.compile(r'Processing TPA for deps entry \[([^,]+), ([^,]+), ([^,]+), local_path: ([^\]]+)\] with fx level: ([0-9]+)\Z')
    for number,line in enumerate(lines,1):
        if line.startswith('Processing TPA for deps entry '):
            m=pattern.fullmatch(line);p.require(m is not None,'typed TPA context')
            package,version,asset,local,level=m.groups();actual.append((dict(package=package,version=version,asset=asset,localPath=local,fxLevel=int(level)),number,line))
    modules=[]
    for entry in contract['tpaEntries']:
        p.keys(entry,['fingerprintField','package','version','asset','localPath','fxLevel'],'TPA binding')
        field=entry['fingerprintField'];p.require(field in ['corePath','msbuildPath','frameworkPath'],'named observed module')
        filename=expected[field].rsplit('\\',1)[-1]
        relevant=[(row,n,line) for row,n,line in actual if row['asset'].rsplit('/',1)[-1].casefold()==filename.casefold() or (row['package']==entry['package'] and field!='corePath')]
        wanted={k:v for k,v in entry.items() if k!='fingerprintField'}
        p.require(len(relevant)==1 and p.same(relevant[0][0],wanted),'exact relative TPA module context '+field)
        observed=expected[field];binary=next(d for d in contract['binaryPins'] if d['path']==observed)
        modules.append(dict(fingerprintField=field,observerAbsolutePath=observed,binary=binary,traceLine=relevant[0][1],traceText=relevant[0][2],traceEvidenceKind='RELATIVE_TPA_ASSET',absoluteAssemblyPathLiterallyPrinted=observed.casefold() in text.casefold()))
    p.require({x['fingerprintField'] for x in modules}=={'corePath','msbuildPath','frameworkPath'} and len(modules)==3,'all three module bindings')
    return dict(schemaVersion=1,status='OBSERVER_PATHS_AND_CLOSED_BINARIES_CORROBORATED_BY_HOST_CONTEXT',moduleBindings=modules,hostContext=evidence,observerPins=contract['observerPins'],rawTraceSha256=__import__('hashlib').sha256(raw).hexdigest())
