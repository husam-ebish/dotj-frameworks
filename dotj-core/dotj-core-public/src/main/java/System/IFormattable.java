// SPDX-License-Identifier: MIT

package System;

/** Bounded public formatting contract candidate. */
public interface IFormattable {
    String ToString(String format, IFormatProvider formatProvider);
}
