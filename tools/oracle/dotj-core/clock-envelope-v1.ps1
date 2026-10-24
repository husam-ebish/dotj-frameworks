function Test-SelectedClockEnvelope {
    param([string]$Property,[long]$BeforeUtcTicks,[long]$AfterUtcTicks,[long]$BeforePropertyTicks,[long]$AfterPropertyTicks,
          [long]$BeforeOffsetTicks,[long]$AfterOffsetTicks,[long]$Ticks,[string]$Kind,[long]$DateTicks,[long]$TimeTicks,[long]$UtcTicks)
    if($AfterUtcTicks -lt $BeforeUtcTicks){return [ordered]@{status='ReferenceClockReversed';reason='Native UTC frame moved backwards.'}}
    $expectedKind=if($Property -eq 'UtcNow'){'Utc'}else{'Local'}
    if($Property -notin @('UtcNow','Now','Today') -or $Kind -ne $expectedKind){return [ordered]@{status='Fail';reason='Clock property or Kind mismatch.'}}
    if($Ticks -lt 0 -or $Ticks -gt 3155378975999999999 -or $TimeTicks -lt 0 -or $TimeTicks -ge 864000000000 -or $DateTicks+$TimeTicks -ne $Ticks -or $DateTicks%864000000000 -ne 0){return [ordered]@{status='Fail';reason='Invalid date/time decomposition.'}}
    if($Property -eq 'Today'){
        if($TimeTicks -ne 0 -or $Ticks -lt [Math]::Min($BeforePropertyTicks,$AfterPropertyTicks) -or $Ticks -gt [Math]::Max($BeforePropertyTicks,$AfterPropertyTicks)){return [ordered]@{status='Fail';reason='Today is outside native midnight boundaries.'}}
    }else{
        if($UtcTicks -lt $BeforeUtcTicks -or $UtcTicks -gt $AfterUtcTicks){return [ordered]@{status='Fail';reason='Clock is outside native UTC envelope.'}}
        if($Property -eq 'UtcNow' -and $Ticks -ne $UtcTicks){return [ordered]@{status='Fail';reason='UtcNow normalization changed ticks.'}}
        if($Property -eq 'Now' -and $Ticks-$UtcTicks -notin @($BeforeOffsetTicks,$AfterOffsetTicks)){return [ordered]@{status='Fail';reason='Local offset is outside native frame offsets.'}}
    }
    return [ordered]@{status='Pass';reason='Selected UTC-normalized clock envelope passed.'}
}
