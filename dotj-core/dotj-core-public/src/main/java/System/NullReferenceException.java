// SPDX-License-Identifier: MIT

package System;

/** Selected null-reference failure type. */
public class NullReferenceException extends SystemException {
    public NullReferenceException() {
        super();
    }

    public NullReferenceException(String message) {
        super(message);
    }
}
