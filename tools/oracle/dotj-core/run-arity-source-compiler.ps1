$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$source = Join-Path $root 'dotj-core/dotj-core-01/src'
$output = Join-Path ([System.IO.Path]::GetTempPath()) ('dotj-arity-source-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $output | Out-Null
try {
    $files = @(
        'main/java/org/dotj/internal/types/ArityNameMap.java',
        'main/java/org/dotj/internal/types/ArityTypeReferenceBinder.java',
        'main/java/org/dotj/internal/types/ArityMethodSignatureBinder.java',
        'main/java/org/dotj/internal/types/ArityJavaSourceRenderer.java',
        'main/java/org/dotj/internal/types/AritySourceCompiler.java',
        'test/java/org/dotj/internal/types/AritySourceCompilerTest.java'
    ) | ForEach-Object { Join-Path $source $_ }
    & javac --release 21 -d $output @files
    if ($LASTEXITCODE -ne 0) { throw 'javac failed' }
    & java -cp $output org.dotj.internal.types.AritySourceCompilerTest
    if ($LASTEXITCODE -ne 0) { throw 'Task source compiler fixture failed' }
} finally {
    Remove-Item -LiteralPath $output -Recurse -Force
}
