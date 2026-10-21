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
        java.util.Map<Object, Object> data = withData.get_Data();
        if (!data.isEmpty() || withData.get_Data() != data) {
            throw new AssertionError("Selected exception data identity changed");
        }
        data.put("key", "value");
        Exception otherData = new Exception("other");
        if (withData.get_Data().size() != 1 || !"value".equals(withData.get_Data().get("key"))
                || otherData.get_Data() == data || !otherData.get_Data().isEmpty()) {
            throw new AssertionError("Selected exception data isolation changed");
        }
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
        if (captured.get_StackTrace() != null) {
            throw new AssertionError("Selected prethrow stack changed");
        }
        try {
            throw ThrowSite.capture(captured);
        } catch (Exception caught) {
            if (caught != captured || caught.get_StackTrace() == null
                    || !caught.get_StackTrace().contains("ProductExceptionContractConsumer.main")) {
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
}
