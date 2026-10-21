// SPDX-License-Identifier: MIT

package System.Runtime.Serialization;

import System.DateTime;
import System.Decimal;
import System.Type;
import System.TypeCode;

/** Public converter contract used by serialization metadata. */
public interface IFormatterConverter {
    Object Convert(Object value, Type type);
    Object Convert(Object value, TypeCode typeCode);
    boolean ToBoolean(Object value);
    short ToByte(Object value);
    char ToChar(Object value);
    DateTime ToDateTime(Object value);
    Decimal ToDecimal(Object value);
    double ToDouble(Object value);
    short ToInt16(Object value);
    int ToInt32(Object value);
    long ToInt64(Object value);
    byte ToSByte(Object value);
    float ToSingle(Object value);
    String ToString(Object value);
    int ToUInt16(Object value);
    long ToUInt32(Object value);
    java.math.BigInteger ToUInt64(Object value);
}
