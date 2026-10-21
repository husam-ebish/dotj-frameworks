package System.Reflection;

/** Selected CLR generic parameter attribute names and values. */
public enum GenericParameterAttributes {
    None(0), Covariant(1), Contravariant(2), VarianceMask(3),
    ReferenceTypeConstraint(4), NotNullableValueTypeConstraint(8),
    DefaultConstructorConstraint(16), SpecialConstraintMask(28),
    AllowByRefLike(32);

    private final int value;

    GenericParameterAttributes(int value) {
        this.value = value;
    }

    public int get_Value() {
        return this.value;
    }
}
