"""Capture only the immutable explicit-import matrix through pinned typed native APIs."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(r'D:\AI\Implementation\dotj Frameworks')
REPO = Path(__file__).resolve().parents[3]
BASE = REPO/'dotj-build/evaluation-candidate'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    if os.name != 'nt' or out.exists() or not out.is_relative_to(ROOT) or out == ROOT:
        raise RuntimeError('New private D: output required')
    out.mkdir(parents=True)
    record = {'schemaVersion':1, 'status':'VERIFYING', 'commands':[], 'resources':[],
              'producerSha256':sha(Path(__file__)), 'csharpProducerSha256':sha(Path(__file__).with_name('CaptureImportLocationsV1.cs')), 'productQualification':False, 'acceptedTasksAdded':0,
              'limits':{'nativeHeapHardLimitMiB':128, 'processors':2, 'timeoutSeconds':30,
                        'minFreeVirtualKiB':16777216, 'minFreePhysicalKiB':524288}}
    def save():
        (out/'verification.json').write_text(json.dumps(record, indent=2)+'\n')
    save()
    try:
        lockpath = BASE/'evidence/import-lock-v1.json'
        lock = json.loads(lockpath.read_text())
        record['lockSha256'] = sha(lockpath)
        def verify():
            for item in lock['inputs']:
                base = ROOT if item['base']=='root' else REPO
                p = (base/item['path']).resolve(strict=True)
                if not p.is_relative_to(base) or sha(p) != item['sha256']:
                    raise RuntimeError('Pinned input mismatch: '+item['path'])
        verify()
        plan = json.loads((BASE/'evidence/profile-plan-v1.json').read_text())
        location_lock = json.loads((BASE/'evidence/profile-input-lock-v1.json').read_text())
        def verify_locations():
            for item in location_lock['inputs']:
                anchor = ROOT if item['base']=='root' else REPO
                if sha(anchor/item['path']) != item['sha256']:raise RuntimeError('Profile input mismatch: '+item['path'])
        verify_locations()
        original_plan = json.loads((BASE/'evidence/import-plan-v1.json').read_text())
        if {p.relative_to(BASE/'import-fixtures').as_posix() for p in (BASE/'import-fixtures').rglob('*') if p.is_file()} != {i['path'] for i in original_plan['fixtures']}:
            raise RuntimeError('Unexpected fixture inventory')
        for item in original_plan['fixtures']:
            if sha(BASE/'import-fixtures'/item['path']) != item['sha256']:
                raise RuntimeError('Fixture mismatch: '+item['path'])
        shutil.copytree(BASE/'import-fixtures', out/'fixtures')
        for source in [Path(__file__),Path(__file__).with_name('CaptureImportLocationsV1.cs'),BASE/'evidence/profile-plan-v1.json',BASE/'evidence/profile-input-lock-v1.json']:
            shutil.copyfile(source,out/source.name)
        for name in ['tmp','home','logs','cache']:
            (out/name).mkdir()
        env = os.environ.copy()
        for key in list(env):
            if key.upper().startswith(('MSBUILD','DOTNET_','COMPLUS_','CORECLR_','COR_')) or key in ['JAVA_TOOL_OPTIONS','_JAVA_OPTIONS']:
                env.pop(key)
        env.update(TEMP=str(out/'tmp'), TMP=str(out/'tmp'), USERPROFILE=str(out/'home'), HOME=str(out/'home'),
                   APPDATA=str(out/'home/AppData/Roaming'), LOCALAPPDATA=str(out/'home/AppData/Local'),
                   DOTNET_ROOT=str(ROOT/'toolchains/dotnet'), DOTNET_CLI_HOME=str(out/'home'),
                   NUGET_PACKAGES=str(out/'cache'), DOTNET_CLI_TELEMETRY_OPTOUT='1',
                   DOTNET_SKIP_FIRST_TIME_EXPERIENCE='1', DOTNET_NOLOGO='1', DOTNET_MULTILEVEL_LOOKUP='0',
                   DOTNET_ROLL_FORWARD='Disable', DOTNET_CLI_UI_LANGUAGE='en-US', VSLANG='1033',
                   MSBUILD_EXE_PATH=str(ROOT/'toolchains/dotnet/sdk/10.0.401/MSBuild.dll'),
                   MSBUILDDISABLENODEREUSE='1', MSBUILDUSEREXTENSIONSPATH=str(out/'home/msbuild-user'),
                   DOTNET_GCHeapHardLimit='8000000', DOTNET_gcServer='0', DOTNET_PROCESSOR_COUNT='2')
        def run(label, argv):
            result = subprocess.run(['powershell','-NoLogo','-NoProfile','-Command',
                '$m=Get-CimInstance Win32_OperatingSystem;[pscustomobject]@{freeVirtualKiB=[uint64]$m.FreeVirtualMemory;freePhysicalKiB=[uint64]$m.FreePhysicalMemory}|ConvertTo-Json -Compress'],
                cwd=out, env=env, capture_output=True, text=True, timeout=20, check=True)
            memory = json.loads(result.stdout)
            memory.update(before=label, utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
            record['resources'].append(memory)
            if memory['freeVirtualKiB']<16777216 or memory['freePhysicalKiB']<524288:
                raise RuntimeError('Existing resource floor not met; command not launched')
            child = env.copy()
            trace = out/'logs'/(label+'.host-trace.txt')
            child.update(DOTNET_HOST_TRACE='1', DOTNET_HOST_TRACEFILE=str(trace))
            command = {'label':label,'argv':list(map(str,argv)),'cwd':str(out),'environmentOverrides':{}}
            # Retain only our explicit non-secret overrides, never the inherited process environment.
            command['environmentOverrides'] = {k:env[k] for k in ['TEMP','TMP','USERPROFILE','HOME','APPDATA','LOCALAPPDATA','NUGET_PACKAGES'] if k in env} | {k:v for k,v in env.items() if k.startswith(('DOTNET_','MSBUILD'))}
            record['commands'].append(command); save()
            result = subprocess.run(argv, cwd=out, env=child, capture_output=True, timeout=30)
            command['exitCode'] = result.returncode
            for suffix,data in [('stdout',result.stdout),('stderr',result.stderr)]:
                p=out/'logs'/(label+'.'+suffix);p.write_bytes(data)
                command[suffix]={'path':str(p),'sha256':sha(p)}
            command['hostTrace']={'path':str(trace),'sha256':sha(trace)}
            save()
            if result.returncode or result.stderr:
                raise RuntimeError(label+' failed; inspect retained output')
            return result.stdout
        sdk = ROOT/'toolchains/dotnet/sdk/10.0.401'
        dotnet = ROOT/'toolchains/dotnet/dotnet.exe'
        references = sorted((ROOT/'toolchains/dotnet/packs/Microsoft.NETCore.App.Ref/10.0.12/ref/net10.0').glob('*.dll'))
        references += [sdk/'Microsoft.Build.dll', sdk/'Microsoft.Build.Framework.dll']
        binary = out/'CaptureImports.dll'
        run('compile-probe', [str(dotnet),'exec',str(sdk/'Roslyn/bincore/csc.dll'),'/nologo','/noconfig','/nostdlib+',
            '/target:exe','/nullable:enable','/deterministic+', '/out:'+str(binary),
            *['/reference:'+str(p) for p in references], str(Path(__file__).with_name('CaptureImportLocationsV1.cs'))])
        config=out/'CaptureImports.runtimeconfig.json';config.write_text(json.dumps(lock['runtimeConfig'],indent=2)+'\n')
        record['binary']={'path':str(binary),'sha256':sha(binary)}
        record['runtimeConfig']={'path':str(config),'sha256':sha(config)}
        record['captures']=[]
        for profile in plan['profiles']:
            data=run(profile,[str(dotnet),'exec','--runtimeconfig',str(config),'--depsfile',str(sdk/'MSBuild.deps.json'),str(binary),str(out/'fixtures'),profile])
            raw=json.loads(data)
            if raw['runtime']!='.NET 10.0.12' or len(raw['rows'])!=len(plan['cases']):
                raise RuntimeError('Unexpected runtime/case profile')
            for key in ['msbuildPath','frameworkPath','corePath']:
                path=Path(raw[key]);expected=next(x['sha256'] for x in lock['inputs'] if x['base']=='root' and ROOT/x['path']==path)
                if sha(path)!=expected:raise RuntimeError('Resolved assembly mismatch')
            if [r['id'] for r in raw['rows']] != plan['cases'] or raw['profile'] != profile:
                raise RuntimeError('Unexpected case/profile order')
            if any(r['cleanup']['afterUnload'] != 0 or not r['cleanup']['disposed'] or not r['taskMarkerAbsent'] for r in raw['rows']):
                raise RuntimeError('Cleanup/marker observation failed')
            record['captures'].append(raw)
        if list(out.rglob('must-not-exist.txt')):raise RuntimeError('Task marker unexpectedly exists')
        for item in original_plan['fixtures']:
            if sha(out/'fixtures'/item['path'])!=item['sha256'] or sha(BASE/'import-fixtures'/item['path'])!=item['sha256']:
                raise RuntimeError('Fixture changed')
        verify()
        verify_locations()
        record.update(status='PASS_NATIVE_PROFILE_OBSERVATIONS',fixturesUnchanged=True,taskMarkersAbsent=True)
    except Exception as error:
        record.update(status='FAILED',error=str(error))
        raise
    finally:
        save()
    print(json.dumps({'status':record['status'],'observations':sum(len(x['rows']) for x in record['captures']),'report':str(out/'verification.json')}))


if __name__=='__main__':
    main()
