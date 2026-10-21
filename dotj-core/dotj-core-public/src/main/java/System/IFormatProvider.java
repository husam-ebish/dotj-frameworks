// SPDX-License-Identifier: MIT

package System;

/** Bounded public formatting-provider contract candidate. */
public interface IFormatProvider {
    Object GetFormat(Type formatType);
}
