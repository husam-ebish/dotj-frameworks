package System;

/** Bounded subset of the public conversion contract; other members remain open. */
public interface IConvertible {
    int GetTypeCode();

    boolean ToBoolean(IFormatProvider provider);

    char ToChar(IFormatProvider provider);

    byte ToSByte(IFormatProvider provider);

    short ToByte(IFormatProvider provider);

    short ToInt16(IFormatProvider provider);

    int ToUInt16(IFormatProvider provider);

    int ToInt32(IFormatProvider provider);

    long ToUInt32(IFormatProvider provider);

    long ToInt64(IFormatProvider provider);

    java.math.BigInteger ToUInt64(IFormatProvider provider);

    float ToSingle(IFormatProvider provider);

    double ToDouble(IFormatProvider provider);

    java.math.BigDecimal ToDecimal(IFormatProvider provider);

    java.time.LocalDateTime ToDateTime(IFormatProvider provider);

    String ToString(IFormatProvider provider);

    Object ToType(Type conversionType, IFormatProvider provider);
}
