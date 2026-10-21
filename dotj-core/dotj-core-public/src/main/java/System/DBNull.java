// SPDX-License-Identifier: MIT

package System;

import System.Runtime.Serialization.ISerializable;
import System.Runtime.Serialization.SerializationInfo;
import System.Runtime.Serialization.StreamingContext;

/** Singleton marker for a missing database or parameter default value. */
public final class DBNull implements IConvertible, ISerializable {
    public static final DBNull Value = new DBNull();

    private DBNull() {
    }

    public String ToString() {
        return "";
    }

    public String ToString(IFormatProvider provider) {
        return "";
    }

    public TypeCode GetTypeCode() {
        return TypeCode.DBNull;
    }

    public boolean ToBoolean(IFormatProvider provider) {
        throw invalidConversion();
    }

    public char ToChar(IFormatProvider provider) {
        throw invalidConversion();
    }

    public byte ToSByte(IFormatProvider provider) {
        throw invalidConversion();
    }

    public short ToByte(IFormatProvider provider) {
        throw invalidConversion();
    }

    public short ToInt16(IFormatProvider provider) {
        throw invalidConversion();
    }

    public int ToUInt16(IFormatProvider provider) {
        throw invalidConversion();
    }

    public int ToInt32(IFormatProvider provider) {
        throw invalidConversion();
    }

    public long ToUInt32(IFormatProvider provider) {
        throw invalidConversion();
    }

    public long ToInt64(IFormatProvider provider) {
        throw invalidConversion();
    }

    public java.math.BigInteger ToUInt64(IFormatProvider provider) {
        throw invalidConversion();
    }

    public float ToSingle(IFormatProvider provider) {
        throw invalidConversion();
    }

    public double ToDouble(IFormatProvider provider) {
        throw invalidConversion();
    }

    public Decimal ToDecimal(IFormatProvider provider) {
        throw invalidConversion();
    }

    public DateTime ToDateTime(IFormatProvider provider) {
        throw invalidConversion();
    }

    public Object ToType(Type conversionType, IFormatProvider provider) {
        if (conversionType == null) {
            throw new ArgumentNullException("targetType");
        }
        if (conversionType == Type.GetType("System.String")) {
            return "";
        }
        if (conversionType == Type.GetType("System.DBNull")) {
            return Value;
        }
        throw invalidConversion();
    }

    public void GetObjectData(SerializationInfo info, StreamingContext context) {
        if (info == null) {
            throw new NullReferenceException();
        }
        throw new UnsupportedOperationException("DBNull serialization is not mapped");
    }

    private static InvalidCastException invalidConversion() {
        return new InvalidCastException("DBNull cannot be converted to the requested type");
    }

    @Override
    public String toString() {
        return this.ToString();
    }
}
