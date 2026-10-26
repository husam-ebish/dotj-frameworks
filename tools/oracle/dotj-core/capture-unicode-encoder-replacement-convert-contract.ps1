param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop'
$hash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $hash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned runtime required'}
& 'D:/AI/Implementation/dotj Frameworks/toolchains/python-3.13.9/python.exe' (Join-Path $PSScriptRoot 'capture-unicode-encoder-replacement-convert-controller.py') --output $OutputPath
if($LASTEXITCODE -ne 0){throw 'Bounded replacement edge capture failed'}
