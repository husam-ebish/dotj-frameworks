# Selected invariant DateTime format lists

Batch 2072 advances `DJ-001-WP-05-T1`; no implementation task is accepted.

All four GetDateTimeFormats overloads now expose the selected invariant pattern lists. Short dates include slash and ISO variants; short times include padded/unpadded 24-hour and 12-hour AM/PM variants. Combined formats preserve native date-major/time-minor order. The all-format overload concatenates the nineteen native standard character groups, retaining all 34 entries and their duplicates. U converts to UTC before building the full-date/time list.

The pinned CoreLib 10.0.12 reference records 2,438 calls across UTC endpoints and modern Local/Unspecified/overlap values. It retains the native invariant pattern reference and tests default/provider-only and character/character-provider overloads, all standard characters and three invalid characters including zero. The packaged consumer checks complete ordered arrays and native FormatException identities/HResults.

Returned arrays are constructed per call. This is an invariant provider-null Java profile compared with native invariant provider/culture, using the selected modern W. Europe/Europe Zurich conversion scope. Other cultures/calendars/providers, historical Local conversion, arbitrary custom formatting, full language and release qualification remain open. No product runtime dependency changes.
