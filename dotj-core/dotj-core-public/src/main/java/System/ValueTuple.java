// SPDX-License-Identifier: MIT

package System;

/** Selected two-field CLR ValueTuple carrier. */
public final class ValueTuple<T1, T2> {
    public T1 Item1;
    public T2 Item2;

    public ValueTuple(T1 item1, T2 item2) {
        this.Item1 = item1;
        this.Item2 = item2;
    }
}
