package consumer;

import System.ArgumentException;
import System.ArgumentNullException;
import System.Exception;
import System.SystemException;
import System.InvalidOperationException;
import System.IO.FileLoadException;
import System.Globalization.CultureNotFoundException;

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
