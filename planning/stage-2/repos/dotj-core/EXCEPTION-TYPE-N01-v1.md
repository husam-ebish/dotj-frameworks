# Selected managed exception Type hierarchy

Batch 2065 advances `DJ-001-WP-01-T1`; no implementation acceptance is claimed.

The logical base of System.Exception now projects System.Object instead of exposing its Java RuntimeException carrier. The nineteen selected managed exception classes enumerate and resolve inherited ISerializable, and ISerializable assignability includes their descendants. Interface ignoreCase preserves the namespace's native case requirement while allowing the selected leaf-name case variation.

IndexOutOfRangeException now reports native sealed metadata and its Java carrier is final. A packaged negative consumer confirms that subclassing is rejected. Other selected exception classes retain their native non-sealed metadata.

The pinned CoreLib 10.0.12 oracle records nineteen metadata/interface rows, 418 interface lookups and 418 assignability/subclass/instance triples. The packaged consumer passes 874 groups. Null lookup arguments go through MethodInfo.Invoke with object-array arguments to preserve a real null String; coverage guards require native ArgumentNullException with fullname. PowerShell's direct String argument adaptation is not used for this null boundary.

These checks qualify the selected type relations and one Java inheritance constraint. Full serialization dispatch, arbitrary exception subclasses, complete reflection, CLR boxing/language representation and release qualification remain open. Product runtime dependencies remain JDK-only.
