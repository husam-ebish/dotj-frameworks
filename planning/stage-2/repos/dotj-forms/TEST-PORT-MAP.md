# DJ-041 .j Forms: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:18](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L18) | TextBox_Ctor_Default | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:129](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L129) | TextBox_CreateParams_GetDefault_ReturnsExpected | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:149](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L149) | TextBox_CanEnableIme_GetWithoutHandle_ReturnsExpected | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:161](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L161) | TextBox_CanEnableIme_GetWithHandle_ReturnsExpected | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:187](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L187) | TextBox_ImeMode_GetWithoutHandle_ReturnsExpected | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:199](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L199) | TextBox_ImeMode_GetWithHandle_ReturnsExpected | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:225](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L225) | TextBox_ImeModeBase_GetWithoutHandle_ReturnsExpected | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:237](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L237) | TextBox_ImeModeBase_GetWithHandle_ReturnsExpected | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:264](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L264) | TextBox_AutoCompleteMode_SetInvalidValue_ThrowsInvalidEnumArgumentException | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:274](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L274) | TextBox_AutoCompleteSource_Set_GetReturnsExpected | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:289](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L289) | TextBox_AutoCompleteSource_InvalidAutoCompleteSource_ThrowsInvalidEnumArgumentException | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:298](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L298) | TextBox_PasswordChar_GetWithoutHandle_ReturnsExpected | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:310](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L310) | TextBox_PasswordChar_GetWithHandle_ReturnsExpected | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:336](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L336) | TextBox_PlaceholderText | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:346](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L346) | TextBox_PlaceholderText_DefaultValue | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:353](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L353) | TextBox_PlaceholderText_When_InAccessibility_Doesnot_Raise_TextChanged | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:385](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L385) | TextBox_ShouldRenderPlaceHolderText | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:394](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L394) | TextBox_PlaceholderText_NullValue_CoercedTo_StringEmpty | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:406](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L406) | TextBox_PlaceholderText_Overridden | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:414](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L414) | TextBox_PlaceholderTextAlignments | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:432](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L432) | TextBox_PlaceholderTextAlignmentsInRightToLeft | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:453](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L453) | TextBox_CreateAccessibilityInstance_Invoke_ReturnsExpected | yes |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:473](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L473) | TextBox_CreateAccessibilityInstance_InvokeWithCustomRole_ReturnsExpected | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:489](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L489) | TextBox_GetAutoSizeMode_Invoke_ReturnsExpected | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:516](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L516) | TextBox_GetStyle_Invoke_ReturnsExpected | yes |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:526](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L526) | TextBox_GetTopLevel_Invoke_ReturnsExpected | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:534](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L534) | TextBox_OnHandleCreated_Invoke_CallsHandleCreated | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:562](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L562) | TextBox_OnHandleCreated_InvokeWithHandle_CallsHandleCreated | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:591](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L591) | TextBox_OnHandleDestroyed_Invoke_CallsHandleDestroyed | not confirmed |
| [src/test/unit/System.Windows.Forms/TextBoxTests.cs:626](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/unit/System.Windows.Forms/TextBoxTests.cs#L626) | TextBox_OnHandleDestroyed_InvokeWithHandle_CallsHandleDestroyed | not confirmed |
| [src/test/integration/UIIntegrationTests/MDITests.cs:16](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/integration/UIIntegrationTests/MDITests.cs#L16) | MDIForm_ResizeWhenMdiChildrenMinimizedAnchorBottom_DefaultAsync | not confirmed |
| [src/test/integration/UIIntegrationTests/MDITests.cs:38](https://github.com/dotnet/winforms/blob/c4891de0851184dcbe95d16ca543969fe2540245/src/test/integration/UIIntegrationTests/MDITests.cs#L38) | MDIForm_ResizeWhenMdiChildrenMinimizedAnchorBottom_FalseAsync | not confirmed |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-041-F01-01 | WP-01 | Disposed controls stop dispatching | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-041-F01-02 | WP-01 | child ownership is explicit | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-041-F01-03 | WP-01 | handle recreation preserves documented state without leaking listeners | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-041-F02-01 | WP-02 | Message ordering has fixture-backed expectations | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-041-F02-02 | WP-02 | native callbacks cannot outlive owners | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-041-F02-03 | WP-02 | non-Windows support is not inferred | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-041-F03-01 | WP-03 | Binding updates avoid feedback loops | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-041-F03-02 | WP-03 | DPI changes relayout correctly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-041-F03-03 | WP-03 | modal ownership and cancellation release native resources | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-041-F04-01 | WP-04 | Generated forms compile | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-041-F04-02 | WP-04 | designer round trips preserve user-owned regions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-041-F04-03 | WP-04 | missing design-time capabilities are reported explicitly | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-041-F05-01 | WP-05 | A control is supported only with behavior and accessibility evidence | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-041-F05-02 | WP-05 | native handle counts return to baseline | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-041-F05-03 | WP-05 | visual baselines identify OS/theme | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Focus/tab order; message-loop reentrancy; high DPI; drag/drop; clipboard; handle disposal; designer round trips.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
