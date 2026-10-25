// SPDX-License-Identifier: MIT

package org.dotj.internal.text;

/** Pinned little-endian Marvin mixing with an opaque process-local string seed. */
public final class MarvinStringHash {
    private static final long PROCESS_SEED = new java.security.SecureRandom().nextLong();
    private MarvinStringHash() { }
    public static int hash(String value) {
        return computeString(value, (int)PROCESS_SEED, (int)(PROCESS_SEED >>> 32));
    }
    public static int computeString(String value, int seed0, int seed1) {
        byte[] data = new byte[Math.multiplyExact(value.length(), 2)];
        for (int i = 0; i < value.length(); i++) {
            char unit = value.charAt(i);
            data[2 * i] = (byte)unit; data[2 * i + 1] = (byte)(unit >>> 8);
        }
        return compute(data, seed0, seed1);
    }
    public static int compute(byte[] data, int seed0, int seed1) {
        int left = seed0, right = seed1, offset = 0;
        while (data.length - offset >= 4) {
            int word = (data[offset] & 255) | ((data[offset + 1] & 255) << 8)
                    | ((data[offset + 2] & 255) << 16) | ((data[offset + 3] & 255) << 24);
            long mixed = mix(left + word, right);
            left = (int)(mixed >>> 32); right = (int)mixed; offset += 4;
        }
        int tail = 0x80 << ((data.length - offset) * 8);
        for (int i = 0; offset + i < data.length; i++) tail |= (data[offset + i] & 255) << (i * 8);
        long mixed = mix(left + tail, right);
        mixed = mix((int)(mixed >>> 32), (int)mixed);
        return (int)(mixed >>> 32) ^ (int)mixed;
    }
    private static long mix(int left, int right) {
        right ^= left; left = Integer.rotateLeft(left, 20);
        left += right; right = Integer.rotateLeft(right, 9);
        right ^= left; left = Integer.rotateLeft(left, 27);
        left += right; right = Integer.rotateLeft(right, 19);
        return ((long)left << 32) | Integer.toUnsignedLong(right);
    }
}
