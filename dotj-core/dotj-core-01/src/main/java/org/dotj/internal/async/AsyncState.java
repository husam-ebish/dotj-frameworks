package org.dotj.internal.async;

/** Internal observation states for the bounded async prototype. */
enum AsyncState {
    PENDING,
    SUCCEEDED,
    FAULTED,
    CANCELED
}
