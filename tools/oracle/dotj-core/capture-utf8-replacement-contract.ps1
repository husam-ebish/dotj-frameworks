param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant();if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
$encoding=[Text.UTF8Encoding]::new($false,$false)
$texts=[Collections.Generic.List[string]]::new();$texts.Add('')
foreach($unit in @(0,1,9,10,13,32,65,127,128,255,256,0x7ff,0x800,0xd7ff,0xd800,0xdbff,0xdc00,0xdfff,0xe000,0xfffd,0xffff)){
 $texts.Add([string][char]$unit);$texts.Add('a'+[char]$unit+'z')
}
foreach($unit in 0..255){$texts.Add([string][char]$unit)}
foreach($high in @(0xd7ff,0xd800,0xda00,0xdbff,0xdc00,0xdfff)){foreach($low in @(0xd800,0xdbff,0xdc00,0xde00,0xdfff,65)){$texts.Add(([string][char]$high)+[char]$low)}}
[uint32]$seed=123456789
foreach($iteration in 0..511){$chars=[char[]]::new(5);foreach($i in 0..4){$seed=[uint32](([uint64]$seed*1664525+1013904223)-band 4294967295L);$chars[$i]=[char]($seed -band 0xffff)};$texts.Add([string]::new($chars))}
$textRows=@(foreach($text in $texts){[ordered]@{units=[int[]][char[]]$text;bytes=[int[]]$encoding.GetBytes($text);byteCount=$encoding.GetByteCount($text)}})
$inputs=[Collections.Generic.List[byte[]]]::new();$inputs.Add([byte[]]@())
foreach($value in 0..255){$inputs.Add([byte[]]@($value))}
foreach($lead in 0xc0..0xff){foreach($tail in @(0,0x7f,0x80,0x9f,0xa0,0xbf,0xc0,0xff)){$inputs.Add([byte[]]@($lead,$tail));$inputs.Add([byte[]]@(65,$lead,$tail,90))}}
foreach($lead in @(0xe0,0xed,0xef,0xf0,0xf4,0xf5)){foreach($b1 in @(0x80,0x8f,0x90,0x9f,0xa0,0xaf,0xbf)){foreach($b2 in @(0,0x80,0xbf,0xc0)){$inputs.Add([byte[]]@($lead,$b1,$b2));$inputs.Add([byte[]]@($lead,$b1,$b2,0x80))}}}
foreach($row in $textRows){$inputs.Add([byte[]]$row.bytes)}
$byteRows=@(foreach($bytes in $inputs){[ordered]@{bytes=[int[]]$bytes;units=[int[]]$encoding.GetChars($bytes);charCount=$encoding.GetCharCount($bytes)}})
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();textRows=$textRows;byteRows=$byteRows;qualification='SELECTED_STATELESS_UTF8_REPLACEMENT_ONLY; STRICT_STATEFUL_POINTER_AND_TASK_ACCEPTANCE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 9)+"`n",[Text.UTF8Encoding]::new($false));Write-Output "PASS pinned replacement UTF-8: $($textRows.Count) text and $($byteRows.Count) byte vectors"
