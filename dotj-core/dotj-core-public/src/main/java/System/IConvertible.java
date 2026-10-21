package System;

/** Bounded subset of the public conversion contract; other members remain open. */
public interface IConvertible {
    int ToInt32(IFormatProvider provider);

    String ToString(IFormatProvider provider);
}
