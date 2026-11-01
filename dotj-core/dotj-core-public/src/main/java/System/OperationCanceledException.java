// SPDX-License-Identifier: MIT

package System;

import System.Threading.CancellationToken;

/** Selected System.OperationCanceledException candidate. */
public class OperationCanceledException extends SystemException {
    private static final String DEFAULT_MESSAGE = "The operation was canceled.";
    private final CancellationToken token;

    public OperationCanceledException() {
        this(null, new CancellationToken());
    }

    public OperationCanceledException(String message) {
        this(message, new CancellationToken());
    }

    public OperationCanceledException(String message, CancellationToken token) {
        super(message == null ? DEFAULT_MESSAGE : message);
        this.set_HResult(-2146233029);
        this.token = token;
    }

    public CancellationToken get_CancellationToken() {
        return token;
    }
}
