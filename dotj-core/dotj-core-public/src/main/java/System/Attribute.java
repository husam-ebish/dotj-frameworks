// SPDX-License-Identifier: MIT

package System;

/** Bounded base for reflected custom attribute instances. */
public abstract class Attribute {
    protected Attribute() {
    }

    public Object get_TypeId() {
        return Type.fromJavaClass(this.getClass());
    }

    public boolean IsDefaultAttribute() {
        return false;
    }

    public boolean Match(Object other) {
        return this.Equals(other);
    }

    public boolean Equals(Object other) {
        return this.equals(other);
    }
}
