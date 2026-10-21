package consumer;

import System.ArgumentException;
import System.ArgumentNullException;
import System.Exception;
import System.SystemException;
import System.InvalidOperationException;
import System.IO.FileLoadException;

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
        if (Exception.class.getConstructors().length != 3
                || SystemException.class.getConstructors().length != 3
                || ArgumentException.class.getConstructors().length != 5
                || ArgumentNullException.class.getConstructors().length != 4
                || InvalidOperationException.class.getConstructors().length != 3
                || FileLoadException.class.getConstructors().length != 5
                || new FileLoadException("invalid", "corelib", inner).get_InnerException() != inner
                || !"corelib".equals(new FileLoadException("invalid", "corelib").get_FileName())
                || !(new InvalidOperationException("invalid", inner) instanceof SystemException)
                || new InvalidOperationException("invalid", inner).get_InnerException() != inner) {
            throw new AssertionError("Selected exception constructor counts changed");
        }
        java.lang.System.out.println("PASS external selected Exception constructors and inner identity");
    }
}
