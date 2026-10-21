package consumer;

import System.ArgumentException;
import System.ArgumentNullException;
import System.Exception;
import System.SystemException;
import System.InvalidOperationException;
import System.Type;
import org.dotj.internal.throwing.ThrowSite;
import System.IO.FileLoadException;
import System.Globalization.CultureNotFoundException;
import System.Runtime.Serialization.FormatterConverter;
import System.Runtime.Serialization.ISerializable;
import System.Runtime.Serialization.SerializationInfo;
import System.Runtime.Serialization.SerializationInfoEnumerator;
import System.Runtime.Serialization.StreamingContext;
import System.Runtime.Serialization.StreamingContextStates;
import System.Reflection.MemberTypes;
import System.Collections.IDictionary;
import System.Collections.ICollection;
import System.Collections.IEnumerable;
import System.Collections.IEnumerator;
import System.Collections.IDictionaryEnumerator;
import System.Collections.DictionaryEntry;

/** Selected constructor and inner-exception checks against the packaged classes. */
public final class ProductExceptionContractConsumer {
    public static void main(String[] args) {
        Exception inner = new Exception("inner");
        ArgumentException outer = new ArgumentException("outer", "value", inner);
        if (!"outer (Parameter 'value')".equals(outer.get_Message()) || !"value".equals(outer.get_ParamName())
                || outer.get_InnerException() != inner || outer.getCause() != inner) {
            throw new AssertionError("ArgumentException selected cause or parameter changed");
        }
        ArgumentNullException nullArgument = new ArgumentNullException("typeName", "missing type");
        if (!"typeName".equals(nullArgument.get_ParamName())
                || !"missing type (Parameter 'typeName')".equals(nullArgument.get_Message())) {
            throw new AssertionError("ArgumentNullException selected constructor changed");
        }
        ArgumentNullException chained = new ArgumentNullException("missing type", inner);
        if (chained.get_InnerException() != inner) {
            throw new AssertionError("ArgumentNullException selected inner identity changed");
        }
        Exception root = new InvalidOperationException("root");
        Exception middle = new Exception("middle", root);
        ArgumentException chain = new ArgumentException("outer", "value", middle);
        if (inner.GetBaseException() != inner || root.GetBaseException() != root
                || middle.GetBaseException() != root || chain.GetBaseException() != root
                || chain.get_InnerException() != middle
                || !(chain.GetBaseException() instanceof InvalidOperationException)
                || !"root".equals(chain.GetBaseException().get_Message())) {
            throw new AssertionError("Selected base exception chain changed");
        }
        Exception withData = new Exception("data");
        IDictionary data = withData.get_Data();
        if (data.get_Count() != 0 || withData.get_Data() != data) {
            throw new AssertionError("Selected exception data identity changed");
        }
        data.Add("key", "value");
        Exception otherData = new Exception("other");
        if (withData.get_Data().get_Count() != 1 || !"value".equals(withData.get_Data().get_Item("key"))
                || otherData.get_Data() == data || otherData.get_Data().get_Count() != 0) {
            throw new AssertionError("Selected exception data isolation changed");
        }
        if (java.util.Map.class.isAssignableFrom(IDictionary.class)) {
            throw new AssertionError("IDictionary exposes Java Map methods");
        }
        IDictionary dictionary = new Exception("dictionary").get_Data();
        if (dictionary.get_Count() != 0 || dictionary.get_IsReadOnly()
                || dictionary.get_IsFixedSize()
                || Type.GetType("System.Collections.IDictionary") == null
                || !Type.GetType("System.Collections.IDictionary").get_IsInterface()
                || Type.GetType("System.Collections.IDictionary").GetInterfaces().length != 2
                || Type.GetType("System.Collections.IDictionary").GetInterfaces()[0]
                        != Type.GetType("System.Collections.ICollection")
                || Type.GetType("System.Collections.IDictionary").GetInterfaces()[1]
                        != Type.GetType("System.Collections.IEnumerable")
                || !Type.GetType("System.Collections.IDictionary").IsInstanceOfType(dictionary)
                || !Type.GetType("System.Collections.ICollection").IsAssignableFrom(
                        Type.GetType("System.Collections.IDictionary"))
                || !Type.GetType("System.Collections.DictionaryEntry").get_IsValueType()) {
            throw new AssertionError("Selected IDictionary identity changed");
        }
        dictionary.Add("key", "first");
        IDictionaryEnumerator dictionaryEnumerator = dictionary.GetEnumerator();
        DictionaryEntry[] copied = new DictionaryEntry[1];
        dictionary.CopyTo(copied, 0);
        if (!dictionary.Contains("key") || !"first".equals(dictionary.get_Item("key"))
                || dictionary.get_Keys().get_Count() != 1
                || dictionary.get_Values().get_Count() != 1
                || !dictionaryEnumerator.MoveNext()
                || !"key".equals(dictionaryEnumerator.get_Key())
                || !"first".equals(dictionaryEnumerator.get_Value())
                || !"key".equals(copied[0].get_Key())
                || !"first".equals(copied[0].get_Value())) {
            throw new AssertionError("Selected IDictionary operations changed");
        }
        try {
            dictionary.Add("key", "duplicate");
            throw new AssertionError("Duplicate dictionary key accepted");
        } catch (ArgumentException expected) {
            // Pinned CLR failure type.
        }
        dictionary.set_Item("key", "second");
        if (!"second".equals(dictionary.get_Item("key"))) {
            throw new AssertionError("Selected IDictionary replacement changed");
        }
        dictionary.Remove("key");
        if (dictionary.get_Count() != 0) {
            throw new AssertionError("Selected IDictionary removal changed");
        }
        dictionary.Add("another", 42);
        dictionary.Clear();
        if (dictionary.get_Count() != 0) {
            throw new AssertionError("Selected IDictionary clear changed");
        }
        expectNullKey(() -> dictionary.Add(null, "value"));
        expectNullKey(() -> dictionary.Contains(null));
        expectNullKey(() -> dictionary.get_Item(null));
        expectNullKey(() -> dictionary.set_Item(null, "value"));
        expectNullKey(() -> dictionary.Remove(null));
        dictionary.Add("nullable", null);
        Object objectKey = new Object();
        dictionary.Add(objectKey, 42);
        if (!dictionary.Contains("nullable") || dictionary.get_Item("nullable") != null
                || !dictionary.Contains(objectKey) || !Integer.valueOf(42).equals(dictionary.get_Item(objectKey))) {
            throw new AssertionError("Selected IDictionary key or null-value boundary changed");
        }
        IDictionaryEnumerator boundaryEnumerator = dictionary.GetEnumerator();
        expectInvalidEnumerator(() -> boundaryEnumerator.get_Entry());
        verifyEnumeratorMutation(value -> value.Add("third", 3));
        verifyEnumeratorMutation(value -> value.set_Item("second", 20));
        verifyEnumeratorMutation(value -> value.Remove("second"));
        verifyEnumeratorMutation(IDictionary::Clear);
        for (boolean keys : new boolean[]{true, false}) {
            verifyViewEnumeratorMutation(keys, value -> value.Add("third", 3), 3);
            verifyViewEnumeratorMutation(keys, value -> value.set_Item("second", 20), 2);
            verifyViewEnumeratorMutation(keys, value -> value.Remove("second"), 1);
            verifyViewEnumeratorMutation(keys, IDictionary::Clear, 0);
        }
        while (boundaryEnumerator.MoveNext()) {
            // Advance beyond the final entry.
        }
        expectInvalidEnumerator(() -> boundaryEnumerator.get_Entry());
        if (new Exception().get_HResult() != -2146233088
                || new Exception("message").get_HResult() != -2146233088
                || new Exception("outer", inner).get_HResult() != -2146233088
                || new ArgumentException("argument").get_HResult() != -2147024809
                || new InvalidOperationException("invalid").get_HResult() != -2146233079) {
            throw new AssertionError("Selected exception HResult values changed");
        }
        Exception withHelpLink = new Exception("help");
        if (withHelpLink.get_HelpLink() != null) {
            throw new AssertionError("Selected HelpLink default changed");
        }
        withHelpLink.set_HelpLink("https://example.invalid/help");
        if (!"https://example.invalid/help".equals(withHelpLink.get_HelpLink())
                || new Exception("other").get_HelpLink() != null) {
            throw new AssertionError("Selected HelpLink mutation changed");
        }
        withHelpLink.set_HelpLink(null);
        if (withHelpLink.get_HelpLink() != null) {
            throw new AssertionError("Selected HelpLink reset changed");
        }
        Exception withSource = new Exception("source");
        if (withSource.get_Source() != null) {
            throw new AssertionError("Selected Source default changed");
        }
        withSource.set_Source("selected.component");
        if (!"selected.component".equals(withSource.get_Source())
                || new Exception("other").get_Source() != null) {
            throw new AssertionError("Selected Source mutation changed");
        }
        withSource.set_Source(null);
        if (withSource.get_Source() != null) {
            throw new AssertionError("Selected Source reset changed");
        }
        Exception serialized = new Exception("boom", new InvalidOperationException("inner"));
        serialized.set_HelpLink("https://example.test/help");
        serialized.set_Source("dotj-test");
        SerializationInfo serializedInfo = new SerializationInfo(
                Type.GetType("System.Exception"), new FormatterConverter());
        StreamingContext serializationContext = new StreamingContext(StreamingContextStates.All);
        serialized.GetObjectData(serializedInfo, serializationContext);
        String[] expectedNames = {"ClassName", "Message", "Data", "InnerException",
                "HelpURL", "StackTraceString", "RemoteStackTraceString", "RemoteStackIndex",
                "ExceptionMethod", "HResult", "Source", "WatsonBuckets"};
        java.util.List<String> serializedNames = new java.util.ArrayList<>();
        SerializationInfoEnumerator entries = serializedInfo.GetEnumerator();
        while (entries.MoveNext()) {
            serializedNames.add(entries.get_Name());
        }
        if (!(serialized instanceof ISerializable)
                || Type.GetType("System.Exception").GetInterfaces().length != 1
                || Type.GetType("System.Exception").GetInterfaces()[0]
                        != Type.GetType("System.Runtime.Serialization.ISerializable")
                || serializedInfo.get_MemberCount() != 12
                || !serializedNames.equals(java.util.Arrays.asList(expectedNames))
                || !"System.Exception".equals(serializedInfo.GetString("ClassName"))
                || !"boom".equals(serializedInfo.GetString("Message"))
                || serializedInfo.GetValue("Data", Type.GetType("System.Object")) != null
                || serializedInfo.GetValue("InnerException", Type.GetType("System.Exception"))
                        != serialized.get_InnerException()
                || serializedInfo.GetString("StackTraceString") != null
                || serializedInfo.GetString("RemoteStackTraceString") != null
                || serializedInfo.GetInt32("RemoteStackIndex") != 0
                || serializedInfo.GetString("ExceptionMethod") != null
                || serializedInfo.GetValue("WatsonBuckets", Type.GetType("System.Object")) != null
                || serializedInfo.GetInt32("HResult") != -2146233088
                || !"https://example.test/help".equals(serializedInfo.GetString("HelpURL"))
                || !"dotj-test".equals(serializedInfo.GetString("Source"))) {
            throw new AssertionError("Selected Exception serialization changed");
        }
        try {
            serialized.GetObjectData(null, serializationContext);
            throw new AssertionError("Null Exception serialization info accepted");
        } catch (ArgumentNullException expected) {
            if (!"info".equals(expected.get_ParamName())) {
                throw new AssertionError("Exception serialization null parameter changed", expected);
            }
        }
        if (!"System.Exception: message".equals(new Exception("message").ToString())
                || !"System.Exception: Exception of type 'System.Exception' was thrown."
                        .equals(new Exception().ToString())
                || !"System.ArgumentException: invalid (Parameter 'value')"
                        .equals(new ArgumentException("invalid", "value").ToString())
                || !"System.InvalidOperationException: invalid"
                        .equals(new InvalidOperationException("invalid").ToString())) {
            throw new AssertionError("Selected exception ToString output changed");
        }
        String twoLevel = "System.Exception: outer\r\n ---> System.Exception: inner"
                + "\r\n   --- End of inner exception stack trace ---";
        String threeLevel = "System.ArgumentException: outer (Parameter 'value')"
                + "\r\n ---> System.Exception: middle"
                + "\r\n ---> System.InvalidOperationException: root"
                + "\r\n   --- End of inner exception stack trace ---"
                + "\r\n   --- End of inner exception stack trace ---";
        if (!twoLevel.equals(new Exception("outer", new Exception("inner")).ToString())
                || !threeLevel.equals(new ArgumentException("outer", "value",
                        new Exception("middle", new InvalidOperationException("root"))).ToString())) {
            throw new AssertionError("Selected inner exception ToString output changed");
        }
        if (new Exception("base").GetType() != Type.GetType("System.Exception")
                || new ArgumentException("argument").GetType() != Type.GetType("System.ArgumentException")
                || new InvalidOperationException("invalid").GetType()
                        != Type.GetType("System.InvalidOperationException")
                || new Exception().GetType() != new Exception().GetType()) {
            throw new AssertionError("Selected exception runtime Type identity changed");
        }
        if (new Exception("before throw").getStackTrace().length == 0) {
            throw new AssertionError("Java constructor stack boundary changed");
        }
        Exception captured = new Exception("capture");
        if (captured.get_StackTrace() != null || captured.get_TargetSite() != null) {
            throw new AssertionError("Selected prethrow stack changed");
        }
        try {
            throw ThrowSite.capture(captured);
        } catch (Exception caught) {
            if (caught != captured || caught.get_StackTrace() == null
                    || !caught.get_StackTrace().contains("ProductExceptionContractConsumer.main")
                    || caught.get_TargetSite() == null
                    || !"main".equals(caught.get_TargetSite().get_Name())
                    || caught.get_TargetSite().get_MemberType() != MemberTypes.Method
                    || caught.get_TargetSite() != caught.get_TargetSite()) {
                throw new AssertionError("Selected throw-site capture changed");
            }
        }
        if (Exception.class.getConstructors().length != 3
                || SystemException.class.getConstructors().length != 3
                || ArgumentException.class.getConstructors().length != 5
                || ArgumentNullException.class.getConstructors().length != 4
                || InvalidOperationException.class.getConstructors().length != 3
                || FileLoadException.class.getConstructors().length != 5
                || CultureNotFoundException.class.getConstructors().length != 8
                || new FileLoadException("invalid", "corelib", inner).get_InnerException() != inner
                || !"corelib".equals(new FileLoadException("invalid", "corelib").get_FileName())
                || !(new InvalidOperationException("invalid", inner) instanceof SystemException)
                || new InvalidOperationException("invalid", inner).get_InnerException() != inner) {
            throw new AssertionError("Selected exception constructor counts changed");
        }
        java.lang.System.out.println("PASS external selected Exception constructors and inner identity");
    }

    private static void expectNullKey(Runnable operation) {
        try {
            operation.run();
            throw new AssertionError("Null dictionary key accepted");
        } catch (ArgumentNullException expected) {
            if (!"key".equals(expected.get_ParamName())) {
                throw new AssertionError("Null dictionary key parameter changed");
            }
        }
    }

    private static void expectInvalidEnumerator(Runnable operation) {
        try {
            operation.run();
            throw new AssertionError("Unpositioned dictionary enumerator accepted");
        } catch (InvalidOperationException expected) {
            // Pinned CLR failure type.
        }
    }

    private static void verifyEnumeratorMutation(java.util.function.Consumer<IDictionary> mutation) {
        IDictionary value = new Exception("enumerator").get_Data();
        value.Add("first", 1);
        value.Add("second", 2);
        IDictionaryEnumerator enumerator = value.GetEnumerator();
        if (!enumerator.MoveNext()) {
            throw new AssertionError("Dictionary enumerator did not move to first entry");
        }
        mutation.accept(value);
        if (!"first".equals(enumerator.get_Entry().get_Key())) {
            throw new AssertionError("Enumerator current entry changed after mutation");
        }
        expectInvalidEnumerator(() -> enumerator.MoveNext());
        expectInvalidEnumerator(enumerator::Reset);
    }

    private static void verifyViewEnumeratorMutation(boolean keys,
            java.util.function.Consumer<IDictionary> mutation, int expectedCount) {
        IDictionary value = new Exception("views").get_Data();
        value.Add("first", 1);
        value.Add("second", 2);
        ICollection view = keys ? value.get_Keys() : value.get_Values();
        IEnumerator enumerator = view.GetEnumerator();
        if (!enumerator.MoveNext()) {
            throw new AssertionError("Dictionary view enumerator did not move");
        }
        Object first = enumerator.get_Current();
        mutation.accept(value);
        if (!java.util.Objects.equals(first, enumerator.get_Current())
                || !java.util.Objects.equals(first, keys ? "first" : 1)
                || view.get_Count() != expectedCount) {
            throw new AssertionError("Dictionary view current or live count changed");
        }
        expectInvalidEnumerator(() -> enumerator.MoveNext());
        expectInvalidEnumerator(enumerator::Reset);
    }
}
