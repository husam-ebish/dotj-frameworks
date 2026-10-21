package System.Globalization;

/** Selected NumberStyles flag values; Java enum representation is provisional. */
public enum NumberStyles {
    None(0), Integer(7), AllowHexSpecifier(512), HexNumber(515);

    private final int value;

    NumberStyles(int value) {
        this.value = value;
    }

    public int get_Value() {
        return this.value;
    }
}
