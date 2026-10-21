// SPDX-License-Identifier: MIT

package System;

/** Singleton marker for a missing database or parameter default value. */
public final class DBNull {
    public static final DBNull Value = new DBNull();

    private DBNull() {
    }
}
