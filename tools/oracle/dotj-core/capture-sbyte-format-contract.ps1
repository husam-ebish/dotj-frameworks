param([Parameter(Mandatory)][string]$OutputPath)
$ErrorActionPreference='Stop';Set-StrictMode -Version Latest
$coreHash=(Get-FileHash -LiteralPath ([object].Assembly.Location) -Algorithm SHA256).Hash.ToLowerInvariant()
if([Environment]::Version.ToString() -ne '10.0.12' -or $coreHash -ne '1125acc8106c43fc8bad2d203c4c4485df6182d292846c2fff415c1040c54678'){throw 'Pinned CoreLib required'}
[Globalization.CultureInfo]::CurrentCulture=[Globalization.CultureInfo]::InvariantCulture
function Failure($record){$e=$record.Exception.GetBaseException();[ordered]@{exception=$e.GetType().FullName;hResult=$e.HResult;paramName=$(if($e -is [ArgumentException]){$e.ParamName}else{$null})}}
$custom=[Globalization.NumberFormatInfo]::InvariantInfo.Clone();$custom.NegativeSign='~';$custom.PositiveSign='p';$custom.NumberDecimalSeparator=':';$custom.NumberGroupSeparator='_';$custom.NumberDecimalDigits=3
$providers=@([ordered]@{name='Invariant';value=[Globalization.NumberFormatInfo]::InvariantInfo},[ordered]@{name='Custom';value=$custom})
$anchors=[int[]]@(-128,-127,-100,-42,-1,0,1,9,10,42,99,100,126,127)
$wide=@($null,'','G','g','G0','G2','D','d','D0','D2','D4','X','x','X0','X2','X4','B','b','B0','B4','B8','B12','R','F0','F2','N0','N2','E2','e2','Q')
$bitFormats=@('X','X4','x2','B','B12');$type=[sbyte];$single=$type.GetMethod('ToString',[type[]]@([string]));$both=$type.GetMethod('ToString',[type[]]@([string],[IFormatProvider]));$iface=[IFormattable].GetMethod('ToString');$defaultProvider=$type.GetMethod('ToString',[type[]]@([IFormatProvider]));$defaultPlain=$type.GetMethod('ToString',[type[]]@());$defaultConvertible=[IConvertible].GetMethod('ToString');$defaults=@();$rows=@()
foreach($number in -128..127){foreach($formatProfile in $providers){
 $boxed=[sbyte]$number;$oneProvider=[object[]]@($formatProfile.value)
 try{$providerDefault=[ordered]@{text=$defaultProvider.Invoke($boxed,$oneProvider)}}catch{$providerDefault=Failure $_}
 try{$plainDefault=[ordered]@{text=$defaultPlain.Invoke($boxed,[object[]]@())}}catch{$plainDefault=Failure $_}
 try{$convertibleDefault=[ordered]@{text=$defaultConvertible.Invoke($boxed,$oneProvider)}}catch{$convertibleDefault=Failure $_}
 $defaults+=[ordered]@{value=$number;provider=$formatProfile.name;plain=$plainDefault;providerText=$providerDefault;convertible=$convertibleDefault}
 $formats=if($anchors -contains $number){@($wide)+@('x2')}else{$bitFormats}
 foreach($format in $formats){
  $boxed=[sbyte]$number;$args2=[object[]]::new(2);$args2[0]=$format;$args2[1]=$formatProfile.value;$args1=[object[]]::new(1);$args1[0]=$format
  try{$direct=[ordered]@{text=$both.Invoke($boxed,$args2)}}catch{$direct=Failure $_}
  try{$interface=[ordered]@{text=$iface.Invoke($boxed,$args2)}}catch{$interface=Failure $_}
  try{$plain=[ordered]@{text=$single.Invoke($boxed,$args1)}}catch{$plain=Failure $_}
  $rows+=[ordered]@{value=$number;provider=$formatProfile.name;format=$format;direct=$direct;interface=$interface;single=$plain}
 }
}}
$record=[ordered]@{schemaVersion=1;runtimeVersion=[Environment]::Version.ToString();coreLibSha256=$coreHash;oracleSha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();typeName=$type.FullName;interfaces=@($type.GetInterfaces()|ForEach-Object FullName);defaults=$defaults;valueCount=256;anchorCount=$anchors.Count;providerCount=$providers.Count;cases=$rows;qualification='BOUNDED_SBYTE_STANDARD_FORMAT_REFERENCE; OTHER_FORMATS_CULTURES_FULL_NUMERIC_API_AND_RELEASE_OPEN'}
[IO.File]::WriteAllText($OutputPath,($record|ConvertTo-Json -Depth 15)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output "PASS pinned SByte standard formatting: $($rows.Count) rows; exhaustive signed-byte bit formats"
