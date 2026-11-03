param([Parameter(Mandatory=$true)][string]$Output)
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$utf8 = [Text.UTF8Encoding]::new($false,$true)
if (-not $env:JAVA_HOME) { [Console]::Error.WriteLine('dotj seed: JAVA_HOME_REQUIRED'); exit 1 }
if ($env:JAVA_HOME -match '[^\x20-\x7E]') { [Console]::Error.WriteLine('dotj seed: JDK_INSTALL_PATH_PROFILE: Windows JAVA_HOME must use printable ASCII characters'); exit 1 }
if (-not [IO.File]::Exists([IO.Path]::Combine($env:JAVA_HOME,'bin/java.exe'))) { [Console]::Error.WriteLine('dotj seed: JDK_JAVA_MISSING'); exit 1 }
$root = [IO.Path]::GetFullPath([IO.Path]::Combine($PSScriptRoot,'../..'))
$scratch = [IO.Path]::GetDirectoryName([IO.Path]::GetFullPath($Output))
$encoded = @($root,[IO.Path]::GetFullPath($Output),'414e04c987d4c6a928a71d8bb78e61448ef0f453146fa4ade3ef67f9aaa4ab0e') | ForEach-Object { [Convert]::ToBase64String($utf8.GetBytes($_)) }
$tokens = @('-Xms16m','-Xmx128m','-XX:ActiveProcessorCount=2','-XX:+UseSerialGC','-XX:ReservedCodeCacheSize=32m','-XX:-UsePerfData','-Duser.home=.','-XX:ErrorFile=hs_err_pid%p.log','-XX:HeapDumpPath=.',('-Ddotj.cwd.b64='+[Convert]::ToBase64String($utf8.GetBytes($PWD.ProviderPath))),('-Ddotj.seed.script.b64='+[Convert]::ToBase64String($utf8.GetBytes($PSCommandPath))),'-Ddotj.seed.encoded=1',('-Ddotj.seed.arg.0='+$encoded[0]),('-Ddotj.seed.arg.1='+$encoded[1]),('-Ddotj.seed.arg.2='+$encoded[2]),'--class-path','sources.properties','--add-modules','jdk.compiler,jdk.jartool','--source','21','Bootstrap.java')
function Quote-Native([string]$value) {
    '"' + [regex]::Replace([regex]::Replace($value,'(\\*)"','$1$1\"'),'(\\+)$','$1$1') + '"'
}
$start = [Diagnostics.ProcessStartInfo]::new()
$start.FileName = [IO.Path]::Combine($env:JAVA_HOME,'bin/java.exe')
$start.UseShellExecute = $false
$start.WorkingDirectory = $PSScriptRoot
$start.EnvironmentVariables['TEMP'] = $scratch
$start.EnvironmentVariables['TMP'] = $scratch
$start.Arguments = (($tokens | ForEach-Object { Quote-Native $_ }) -join ' ')
if ($start.Arguments.Length + $start.FileName.Length + 4 -gt 30000) { [Console]::Error.WriteLine('dotj: WINDOWS_TRANSPORT_BOUND: encoded command exceeds 30000 UTF16 units'); exit 1 }
$process = [Diagnostics.Process]::Start($start)
$process.WaitForExit()
exit $process.ExitCode
