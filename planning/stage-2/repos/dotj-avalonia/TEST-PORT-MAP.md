# DJ-043 .j Avalonia: test-port map

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [tests/Avalonia.LeakTests/ControlTests.cs:29](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L29) | Canvas_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:65](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L65) | Named_Canvas_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:106](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L106) | ScrollViewer_With_Content_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:147](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L147) | TextBox_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:185](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L185) | TextBox_With_Xaml_Binding_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:235](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L235) | TextBox_Class_Listeners_Are_Freed | yes |
| [tests/Avalonia.LeakTests/ControlTests.cs:271](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L271) | TreeView_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:325](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L325) | Slider_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:361](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L361) | TabItem_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:401](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L401) | RendererIsDisposed | yes |
| [tests/Avalonia.LeakTests/ControlTests.cs:430](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L430) | Control_With_Style_RenderTransform_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:482](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L482) | Attached_ContextMenu_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:527](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L527) | Attached_Control_From_ContextMenu_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:568](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L568) | Standalone_ContextMenu_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:619](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L619) | Path_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:658](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L658) | Polyline_WithObservableCollectionPointsBinding_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:700](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L700) | ElementName_Binding_In_DataTemplate_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:788](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L788) | HotKeyManager_Should_Release_Reference_When_Control_Detached | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:826](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L826) | HotKeyManager_Should_Release_Reference_When_Control_In_Item_Template_Detached | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:892](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L892) | ToolTip_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:948](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L948) | Flyout_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:1002](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L1002) | LayoutTransformControl_Is_Freed | not confirmed |
| [tests/Avalonia.LeakTests/ControlTests.cs:1051](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.LeakTests/ControlTests.cs#L1051) | Menu_Is_Freed | not confirmed |
| [tests/Avalonia.Base.UnitTests/RectTests.cs:8](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.Base.UnitTests/RectTests.cs#L8) | Union_Should_Return_Correct_Value_For_Intersecting_Rects | yes |
| [tests/Avalonia.Base.UnitTests/RectTests.cs:16](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.Base.UnitTests/RectTests.cs#L16) | Union_Should_Return_Correct_Value_For_NonIntersecting_Rects | yes |
| [tests/Avalonia.Base.UnitTests/RectTests.cs:24](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.Base.UnitTests/RectTests.cs#L24) | Union_Should_Ignore_Empty_This_rect | yes |
| [tests/Avalonia.Base.UnitTests/RectTests.cs:32](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.Base.UnitTests/RectTests.cs#L32) | Union_Should_Ignore_Empty_Other_rect | yes |
| [tests/Avalonia.Base.UnitTests/RectTests.cs:40](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.Base.UnitTests/RectTests.cs#L40) | Normalize_Should_Reverse_Negative_Size | yes |
| [tests/Avalonia.Base.UnitTests/RectTests.cs:48](https://github.com/AvaloniaUI/Avalonia/blob/66b7273b9a2b5ba8416feb4376b9cdc3078b8573/tests/Avalonia.Base.UnitTests/RectTests.cs#L48) | Normalize_Should_Make_Invalid_Rects_Empty | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-043-F01-01 | WP-01 | Priority fixtures resolve identically within profile | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-043-F01-02 | WP-01 | style removal restores lower values | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-043-F01-03 | WP-01 | detached controls release subscriptions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-043-F02-01 | WP-02 | Renderer feasibility has a concrete native dependency record | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-043-F02-02 | WP-02 | text tests pin fonts | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-043-F02-03 | WP-02 | layout loops are detected with diagnostics | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-043-F03-01 | WP-03 | IME composition survives focus transitions | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-043-F03-02 | WP-03 | accessibility nodes match controls | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-043-F03-03 | WP-03 | handles close once on each tested platform | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-043-F04-01 | WP-04 | Markup diagnostics refer to original lines | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-043-F04-02 | WP-04 | previews recover from invalid edits | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-043-F04-03 | WP-04 | generated output is reproducible | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-043-F05-01 | WP-05 | Control coverage is explicit | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-043-F05-02 | WP-05 | native interop resources remain owned | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-043-F05-03 | WP-05 | MIT root text does not erase third-party obligations | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Headless layout fixtures; text shaping; focus/input; compositor timing; high DPI; backend resource lifetimes.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.
