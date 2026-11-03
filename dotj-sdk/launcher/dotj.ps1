$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$utf8 = [Text.UTF8Encoding]::new($false,$true)
if (-not $env:JAVA_HOME) { [Console]::Error.WriteLine('dotj: JAVA_HOME_REQUIRED'); exit 1 }
if ($env:JAVA_HOME -match '[^\x20-\x7E]') { [Console]::Error.WriteLine('dotj: JDK_INSTALL_PATH_PROFILE: Windows JAVA_HOME must use printable ASCII characters'); exit 1 }
if (-not [IO.File]::Exists([IO.Path]::Combine($env:JAVA_HOME,'bin/java.exe'))) { [Console]::Error.WriteLine('dotj: JDK_JAVA_MISSING'); exit 1 }
$selection = [IO.File]::ReadAllLines([IO.Path]::Combine($PSScriptRoot,'current'))
if ($selection.Length -ne 2 -or $selection[0] -notmatch '^[a-f0-9]{64}-[a-f0-9]{64}$' -or $selection[1] -notmatch '^[a-f0-9]{64}$') { [Console]::Error.WriteLine('dotj: INVALID_SELECTION'); exit 1 }
$tokens = @('-Xms16m','-Xmx128m','-XX:ActiveProcessorCount=2','-XX:+UseSerialGC','-XX:ReservedCodeCacheSize=32m','-XX:-UsePerfData','-Djava.io.tmpdir=.','-Duser.home=.','-XX:ErrorFile=hs_err_pid%p.log','-XX:HeapDumpPath=.',('-Ddotj.cwd.b64='+[Convert]::ToBase64String($utf8.GetBytes($PWD.ProviderPath))),('-Ddotj.launcher.b64='+[Convert]::ToBase64String($utf8.GetBytes($PSCommandPath))),('-Ddotj.jar.sha256='+$selection[1]),('-Ddotj.arg.count='+$args.Count))
for ($i=0; $i -lt $args.Count; $i++) { $tokens += '-Ddotj.arg.'+$i+'='+[Convert]::ToBase64String($utf8.GetBytes([string]$args[$i])) }
$tokens += @('--class-path','current','--add-modules','jdk.compiler,jdk.jartool','--module-path',('versions/'+$selection[0]+'/dotj.jar'),'-m','org.dotj.build.evaluation.candidate/org.dotj.internal.build.evaluation.SdkMain')
function Quote-Native([string]$value) {
    '"' + [regex]::Replace([regex]::Replace($value,'(\\*)"','$1$1\"'),'(\\+)$','$1$1') + '"'
}
$start = [Diagnostics.ProcessStartInfo]::new()
$start.FileName = [IO.Path]::Combine($env:JAVA_HOME,'bin/java.exe')
$start.UseShellExecute = $false
$start.WorkingDirectory = $PSScriptRoot
$start.Arguments = (($tokens | ForEach-Object { Quote-Native $_ }) -join ' ')
if ($start.Arguments.Length + $start.FileName.Length + 4 -gt 30000) { [Console]::Error.WriteLine('dotj: WINDOWS_TRANSPORT_BOUND: encoded command exceeds 30000 UTF16 units'); exit 1 }
$process = [Diagnostics.Process]::Start($start)
$process.WaitForExit()
exit $process.ExitCode
