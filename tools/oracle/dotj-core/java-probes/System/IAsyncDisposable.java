package System;

import System.Threading.Tasks.ValueTask;

/** Compile-only exact-name probe; not product API. */
public interface IAsyncDisposable {
    ValueTask DisposeAsync();
}
