package org.dotj.internal.types;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;
import java.util.Objects;

/** Internal JVM name mapping for members whose overloads erase to one signature. */
final class ErasureMethodNameMap {
    private ErasureMethodNameMap() {
    }

    static String backendName(String owner, String method, String metadataSignature) {
        Objects.requireNonNull(owner, "owner");
        Objects.requireNonNull(method, "method");
        Objects.requireNonNull(metadataSignature, "metadataSignature");
        if (!owner.equals("System.Threading.Tasks.Task")
                && !owner.equals("System.Threading.Tasks.ValueTask")) {
            throw new IllegalArgumentException("Unsupported owner: " + owner);
        }
        if (!ArityTypeReferenceBinder.isSourceIdentifier(method)
                || (!metadataSignature.contains(" " + method + "(")
                    && !metadataSignature.contains(" " + method + "["))) {
            throw new IllegalArgumentException("Method identity does not match metadata signature");
        }
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] bytes = digest.digest((owner + "\0" + metadataSignature).getBytes(StandardCharsets.UTF_8));
            return method + "__dotj_" + HexFormat.of().formatHex(bytes).substring(0, 12);
        } catch (NoSuchAlgorithmException exception) {
            throw new IllegalStateException("SHA-256 is unavailable", exception);
        }
    }
}
