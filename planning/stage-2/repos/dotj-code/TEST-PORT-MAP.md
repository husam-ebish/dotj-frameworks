# DJ-003 .j Code: test-port map

**Mandatory owner requirement: exact .NET names and concepts.** Preserve upstream public names, casing, namespaces, interface prefixes, method/Async suffixes and familiar workflows. Internal labels below do not authorize replacement public APIs. Apply [DOTNET-API-EXACT-001](../../08-DOTNET-API-COMPATIBILITY-POLICY.md) and this repository’s [API-COMPATIBILITY.md](API-COMPATIBILITY.md).

## Evidence versus designed fixtures

Source method rows below are lexical candidates from retrieved files. They are not all verified runnable tests, not a full upstream test census, and not proof of conformance. Attribute candidates identify nearby test annotations only. E03 must discover actual cases with the pinned upstream runner and assign them by behavior. Synthetic fixture IDs below are newly designed acceptance cases, never invented upstream identifiers.

| Source candidate | Method | Nearby test annotation |
|---|---|---|
| [src/Interactive/HostTest/StressTests.cs:21](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Interactive/HostTest/StressTests.cs#L21) | TestKill | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:33](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L33) | TestCreateScript | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:40](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L40) | TestCreateScript_CodeIsNull | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:46](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L46) | TestCreateFromStreamScript | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:53](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L53) | TestCreateFromStreamScript_StreamIsNull | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:59](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L59) | TestGetCompilation | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:67](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L67) | TestGetCompilationSourceText | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:75](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L75) | TestEmit_PortablePdb | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:78](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L78) | TestEmit_WindowsPdb | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:103](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L103) | TestCreateScriptDelegate | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:114](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L114) | TestCreateScriptDelegateWithGlobals | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:126](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L126) | TestRunScript | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:133](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L133) | TestCreateAndRunScript | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:142](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L142) | TestCreateFromStreamAndRunScript | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:151](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L151) | TestEvalScript | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:158](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L158) | TestRunScriptWithSpecifiedReturnType | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:165](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L165) | TestRunVoidScript | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:174](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L174) | TestRunExpressionStatement | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:183](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L183) | TestRunDynamicVoidScriptWithTerminatingSemicolon | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:188](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L188) | Do | not confirmed |
| [src/Scripting/CSharpTest/ScriptTests.cs:198](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L198) | TestRunDynamicVoidScriptWithoutTerminatingSemicolon | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:203](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L203) | Do | not confirmed |
| [src/Scripting/CSharpTest/ScriptTests.cs:213](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L213) | TestRunEmbeddedStatementNotFollowedBySemicolon | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:235](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L235) | TestRunEmbeddedStatementFollowedBySemicolon | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:243](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L243) | TestRunStatementFollowedBySpace | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:250](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L250) | TestRunStatementFollowedByNewLineNoSemicolon | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:260](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L260) | TestRunEmbeddedNoSemicolonFollowedByAnotherStatement | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:284](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L284) | TestRunScriptWithGlobals | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:291](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L291) | TestRunCreatedScriptWithExpectedGlobals | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:300](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L300) | TestRunCreatedScriptWithUnexpectedGlobals | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:309](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L309) | TestRunCreatedScriptWithoutGlobals | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:318](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L318) | TestRunCreatedScriptWithMismatchedGlobals | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:327](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L327) | ContinueAsync_Error1 | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:335](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L335) | ContinueAsync_Error2 | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:344](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L344) | TestRunScriptWithScriptState | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:352](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L352) | TestRepl | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:372](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L372) | TestCreateMethodDelegate | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:383](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L383) | ScriptVariables_Chain | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:413](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L413) | ScriptVariable_SetValue | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:432](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L432) | ScriptVariable_SetValue_Errors | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:452](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L452) | TestBranchingSubscripts | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:469](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L469) | StaticDelegate0 | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:478](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L478) | StaticDelegate1 | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:486](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L486) | StaticDelegate2 | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:494](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L494) | ReturnIntAsObject | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:503](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L503) | NoReturn | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:510](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L510) | ReturnAwait | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:518](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L518) | ReturnInNestedScopeNoTrailingExpression | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:531](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L531) | ReturnInNestedScopeWithTrailingVoidExpression | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:555](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L555) | ReturnInNestedScopeWithTrailingVoidExpressionAsInt | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:579](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L579) | ReturnIntWithTrailingDoubleExpression | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:603](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L603) | ReturnGenericAsInterface | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:623](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L623) | ReturnNullable | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:643](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L643) | ReturnInLoadedFile | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:661](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L661) | ReturnInLoadedFileTrailingExpression | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:684](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L684) | ReturnInLoadedFileTrailingVoidExpression | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:707](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L707) | MultipleLoadedFilesWithTrailingExpression | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:742](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L742) | MultipleLoadedFilesWithReturnAndTrailingExpression | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:777](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L777) | LoadedFileWithReturnAndGoto | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:808](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L808) | VoidReturn | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:826](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L826) | LoadedFileWithVoidReturn | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:842](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L842) | Pdb_CreateFromString_CodeFromFile_WithEmitDebugInformation_WithoutFileEncoding_CompilationErrorException | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:859](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L859) | Pdb_CreateFromString_CodeFromFile_WithEmitDebugInformation_WithFileEncoding_ResultInPdbEmitted | not confirmed |
| [src/Scripting/CSharpTest/ScriptTests.cs:866](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L866) | Pdb_CreateFromString_CodeFromFile_WithoutEmitDebugInformation_WithoutFileEncoding_ResultInPdbNotEmitted | not confirmed |
| [src/Scripting/CSharpTest/ScriptTests.cs:873](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L873) | Pdb_CreateFromString_CodeFromFile_WithoutEmitDebugInformation_WithFileEncoding_ResultInPdbNotEmitted | not confirmed |
| [src/Scripting/CSharpTest/ScriptTests.cs:881](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L881) | Pdb_CreateFromStream_CodeFromFile_WithEmitDebugInformation_ResultInPdbEmitted | not confirmed |
| [src/Scripting/CSharpTest/ScriptTests.cs:888](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L888) | Pdb_CreateFromStream_CodeFromFile_WithoutEmitDebugInformation_ResultInPdbNotEmitted | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:896](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L896) | Pdb_CreateFromString_InlineCode_WithEmitDebugInformation_WithoutFileEncoding_ResultInPdbEmitted | not confirmed |
| [src/Scripting/CSharpTest/ScriptTests.cs:904](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L904) | Pdb_CreateFromString_InlineCode_WithEmitDebugInformation_WithFileEncoding_ResultInPdbEmitted | not confirmed |
| [src/Scripting/CSharpTest/ScriptTests.cs:911](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L911) | Pdb_CreateFromString_InlineCode_WithoutEmitDebugInformation_WithoutFileEncoding_ResultInPdbNotEmitted | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:918](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L918) | Pdb_CreateFromString_InlineCode_WithoutEmitDebugInformation_WithFileEncoding_ResultInPdbNotEmitted | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:926](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L926) | Pdb_CreateFromStream_InlineCode_WithEmitDebugInformation_ResultInPdbEmitted | not confirmed |
| [src/Scripting/CSharpTest/ScriptTests.cs:933](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L933) | Pdb_CreateFromStream_InlineCode_WithoutEmitDebugInformation_ResultInPdbNotEmitted | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:940](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L940) | StreamWithOffset | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:949](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L949) | CreateScriptWithFeatureThatIsNotSupportedInTheSelectedLanguageVersion | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:962](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L962) | CreateScriptWithNullableContextWithCSharp8 | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:974](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L974) | SwitchPatternWithVar_WhenValidCode_ShouldReturnValidResult | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:997](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L997) | SwitchPatternWithVar_WhenNonExistentVariable_ShouldReturnNameNotInContextCompilationError | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:1019](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L1019) | SwitchPatternWithVar_WhenInvalidPattern_ShouldReturnUnsupportedTypeForRelationalPatternAndNoImplicitConvErrors | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:1044](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L1044) | SwitchPatternWithVar_WhenInvalidArm_ShouldReturnTheNameNotInContextError | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:1067](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L1067) | Function_ReturningPartialType | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:1087](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L1087) | Function_ReturningPartialType_CSharp13 | yes |
| [src/Scripting/CSharpTest/ScriptTests.cs:1099](https://github.com/dotnet/roslyn/blob/3645b6aa36ad41775a73e57a620787a3d38327a0/src/Scripting/CSharpTest/ScriptTests.cs#L1099) | ScriptInstantiation | yes |

## Designed acceptance fixtures

| Fixture ID | Package | Expected observation | Evidence status |
|---|---|---|---|
| DJ-003-F01-01 | WP-01 | Malformed input yields bounded diagnostics without hangs | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-003-F01-02 | WP-01 | source spans survive CRLF/Unicode edits | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-003-F01-03 | WP-01 | C#/VB capabilities remain in inventory even when frontend feasibility is pending | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-003-F02-01 | WP-02 | Shadowing/generic overload cases match the declared language profile | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-003-F02-02 | WP-02 | stale symbols are detected | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-003-F02-03 | WP-02 | no unsupported internal javac dependency becomes a public contract | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-003-F03-01 | WP-03 | Unrelated document edits avoid recomputing unaffected units | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-003-F03-02 | WP-03 | deleted references invalidate dependents | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-003-F03-03 | WP-03 | repeated edit cycles do not retain whole abandoned workspaces | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-003-F04-01 | WP-04 | Same locked inputs generate byte-identical source | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-003-F04-02 | WP-04 | stale code actions reject rather than overwrite newer text | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-003-F04-03 | WP-04 | analyzer failure cannot corrupt workspace state | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-003-F05-01 | WP-05 | Rename respects symbol scope | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-003-F05-02 | WP-05 | cancellation bounds response work | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-003-F05-03 | WP-05 | generated Java compiles against declared APIs | Designed; map actual upstream case or specify independent oracle in E03 |
| DJ-003-F05-04 | WP-05 | translation never labels approximate semantics as exact compatibility | Designed; map actual upstream case or specify independent oracle in E03 |

## Differential runner design

Use a versioned, language-neutral fixture envelope: fixture ID; input bytes/value schema; options; seed; clock/culture/timezone; platform requirements; expected output/errors/events/resource counters; allowed normalization; source pin; oracle/toolchain identity. Encode decimal and 64-bit integers as strings when transport would lose precision. Keep binary payloads exact with checksums. Run C# oracle and future Java implementation as separate processes, compare only approved normalized observables, preserve raw outputs, and classify mismatch as regression, documented adaptation or unresolved investigation. Do not normalize away ordering, precision, security failures or resource leaks.

## Required test dimensions

Incremental syntax edits; symbol resolution; diagnostic spans; generator reproducibility; malformed-source recovery.

Add negative inputs and each cleanup/cancellation edge from the architecture. Concurrency tests use controlled scheduling/barriers and fake clocks, with stress tests supplemental. Protocol/native/UI features use real reference processes/devices in the declared matrix. Performance budgets must be measured and agreed from baseline workloads; this plan invents no benchmark numbers.

## Porting completion

Every public feature has mapped cases or an explicit independent-oracle rationale. Every skip has a reason and blocking capability. Run the same immutable fixture payloads across environments; store results with source/toolchain/dependency locks. None of these future Java implementation tests has been executed by this planning task.

## Mandatory naming and concept regression cases

| Fixture | Required observation |
|---|---|
| DJ-003-NF01 | Supported public types/members/namespaces match the selected upstream identities with exact spelling and casing; no lowerCamelCase conversion, dropped I prefix, removed Async suffix or replacement domain name is introduced. |
| DJ-003-NF02 | Paired C#/.j examples use the same framework concepts, lifecycle and operation names; every syntax-only difference is documented and internal Java helper types do not become mandatory new public concepts. |
| DJ-003-NF03 | Unrepresentable signatures or semantics are reported as blocked/unsupported with source identity and evidence; no renamed API, JDK substitute type or changed behavior is falsely marked exact compatibility. |

These additional cases enforce the owner naming decision across public signatures, generated APIs and paired examples. They are designed requirements, not executed results.
