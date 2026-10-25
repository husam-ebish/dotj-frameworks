<# Run a selected reference oracle against shared pinned CoreLib, never bundled CoreLib. #>
[CmdletBinding()]
param([Parameter(Mandatory)][ValidateSet('timespan', 'exception', 'datetime', 'temporal-type', 'temporal-span', 'temporal-span-parsing', 'temporal-span-exact', 'timespan-custom-exact', 'timespan-general-exact', 'timespan-general-format', 'timespan-array-exact', 'datetime-clock', 'datetime-dst', 'datetime-filetime', 'datetime-binary', 'datetime-saturation', 'stopwatch', 'clock-envelope', 'stopwatch-type', 'array-shape', 'element-modifier', 'timespan-style', 'timespan-style-type', 'enum-query', 'enum-receiver', 'shape-lookup', 'array-rank-lookup', 'datetime-oadate', 'datetime-convertible', 'int32-target-conversion', 'small-integer-target-conversion', 'decimal-target-conversion', 'dbnull', 'type-value-flags', 'exception-type', 'interface-lookup', 'collection-interface', 'boxed-value-instance', 'array-collection', 'datetime-standard', 'datetime-roundtrip-format', 'datetime-format-lists', 'datetime-style', 'datetime-exact-style', 'datetime-array-exact', 'datetime-custom-format', 'datetime-custom-buffer', 'datetime-custom-unicode', 'datetime-timeonly-offset', 'datetime-style-format', 'datetime-style-comparison', 'datetime-style-conversion', 'span-copy', 'datetime-style-span', 'datetime-style-hasflag', 'timespan-style-format', 'timespan-style-comparison', 'timespan-style-conversion', 'timespan-style-span', 'timespan-style-hasflag', 'number-style-format', 'number-style-comparison', 'number-style-conversion', 'number-style-span', 'number-style-hasflag', 'binding-flags-format', 'binding-flags-comparison', 'binding-flags-conversion', 'binding-flags-span', 'binding-flags-hasflag', 'span-slice', 'span-mutation', 'member-types-format', 'member-types-comparison', 'member-types-conversion', 'member-types-span', 'member-types-hasflag', 'calling-conventions-format', 'calling-conventions-comparison', 'calling-conventions-conversion', 'calling-conventions-span', 'calling-conventions-hasflag', 'method-impl-attributes-format', 'method-impl-attributes-comparison', 'method-impl-attributes-conversion', 'method-impl-attributes-span', 'method-impl-attributes-hasflag', 'streaming-context-states-format', 'streaming-context-states-comparison', 'streaming-context-states-conversion', 'streaming-context-states-span', 'streaming-context-states-hasflag', 'sbyte-format', 'int32-format-classification', 'generic-parameter-attributes-format', 'generic-parameter-attributes-comparison', 'generic-parameter-attributes-conversion', 'generic-parameter-attributes-span', 'generic-parameter-attributes-hasflag', 'byte-format', 'byte-comparison', 'sbyte-comparison', 'uint16-format', 'uint16-comparison', 'uint32-format', 'uint32-comparison', 'sbyte-span', 'sbyte-utf8', 'byte-span', 'byte-utf8', 'uint16-span', 'uint16-utf8', 'uint32-span', 'uint32-utf8', 'small-integer-signatures', 'small-integer-constants', 'small-integer-min-max-clamp', 'small-integer-bit-operations', 'sbyte-signed-magnitude', 'unsigned-integer-log2', 'integer-sign-log-boundaries', 'integer-string-parsing', 'integer-span-parsing', 'integer-style-parsing', 'sbyte-sign-predicates', 'small-integer-divrem', 'uint32-bigmul', 'small-integer-create', 'integer-generic-boundaries', 'utf8-contract-inventory', 'utf8-replacement', 'utf8-strict', 'utf8-exception-boundaries', 'utf8-array-ranges', 'utf8-destination', 'utf8-array-capacity', 'utf8-type', 'encoding-clone', 'icloneable-type', 'encoding-fallback-contracts', 'encoder-fallback-buffers', 'decoder-fallback-buffers', 'encoding-fallback-customization', 'fallback-type-metadata', 'fallback-hash-contracts', 'custom-fallback-dispatch', 'custom-fallback-boundaries', 'custom-buffer-protocol', 'custom-buffer-capacity', 'fallback-allocation-passes', 'utf8-equality-hash', 'fallback-equality-dispatch', 'custom-fallback-slices', 'utf8-metadata-properties', 'stateful-utf8-contracts', 'stateful-utf8-encoder', 'encoder-boundaries', 'stateful-utf8-decoder', 'decoder-boundaries', 'stateful-encoding-type-metadata', 'custom-stateful-encoder', 'custom-stateful-decoder', 'stateful-encoding-spans', 'encoding-span-conversion', 'utf8-preamble-span', 'utf8-encoding-lookups', 'encoding-convert-arrays', 'stateful-convert', 'encoder-convert-boundaries', 'custom-encoder-convert', 'decoder-convert-boundaries', 'custom-decoder-convert', 'generic-convert-arrays')][string]$Contract,
      [string]$StorageRoot = 'D:\AI\Implementation\dotj Frameworks',
      [string]$JarPath, [string]$ConsumerClassPath)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$storage = [IO.Path]::GetFullPath($StorageRoot)
if ([IO.Path]::GetPathRoot($storage) -ine 'D:\') { throw 'Oracle storage must be on D:.' }
$root = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$dotnet = Join-Path $storage 'toolchains/dotnet/dotnet.exe'
$pwsh = Join-Path $storage 'toolchains/powershell-7.6.0-fxdependent/pwsh.dll'
$config = Join-Path $storage 'toolchains/powershell-oracle.runtimeconfig.json'
$settings = '{"runtimeOptions":{"tfm":"net10.0","framework":{"name":"Microsoft.NETCore.App","version":"10.0.12"},"rollForward":"Disable"}}'
[IO.File]::WriteAllText($config, $settings, (New-Object Text.UTF8Encoding($false)))
$variables = @('DOTNET_ROOT', 'DOTNET_CLI_HOME', 'DOTNET_CLI_TELEMETRY_OPTOUT', 'TEMP', 'TMP', 'PSModuleAnalysisCachePath')
$saved = @{}
foreach ($name in $variables) { $saved[$name] = [Environment]::GetEnvironmentVariable($name, 'Process') }
try {
    $env:DOTNET_ROOT = Split-Path $dotnet
    $env:DOTNET_CLI_HOME = Join-Path $storage 'cache/dotnet-home'
    $env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'
    $env:TEMP = Join-Path $storage 'tmp'; $env:TMP = $env:TEMP
    $env:PSModuleAnalysisCachePath = Join-Path $storage 'cache/powershell-analysis'
    New-Item -ItemType Directory -Force -Path $env:TEMP, $env:DOTNET_CLI_HOME | Out-Null
    $outputPath = Join-Path $root "planning/stage-2/repos/dotj-core/evidence/$Contract-contract-v10.0.12.json"
    $captureArguments=@('-OutputPath',$outputPath)
    if($Contract -in @('datetime-clock','stopwatch','datetime-timeonly-offset')){
        if(!$JarPath -or !$ConsumerClassPath){throw 'Clock capture requires an explicit product JAR and consumer class path.'}
        $captureArguments+=@('-JarPath',$JarPath,'-ConsumerClassPath',$ConsumerClassPath)
    }
    & $dotnet exec --runtimeconfig $config $pwsh -NoLogo -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "capture-$Contract-contract.ps1") @captureArguments
    if ($LASTEXITCODE -ne 0) { throw 'Pinned reference oracle failed.' }
    # Preserve a stable byte representation across PowerShell/checkout line endings.
    $canonical = [IO.File]::ReadAllText($outputPath).Replace("`r`n", "`n")
    [IO.File]::WriteAllText($outputPath, $canonical, (New-Object Text.UTF8Encoding($false)))
} finally {
    foreach ($name in $variables) { [Environment]::SetEnvironmentVariable($name, $saved[$name], 'Process') }
}
