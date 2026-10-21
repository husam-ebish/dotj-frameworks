internal class NestedFamilyProbe
{
    protected sealed class Marker
    {
    }

    public static Type MarkerType => typeof(Marker);

    private sealed class PrivateMarker
    {
    }

    public static Type PrivateMarkerType => typeof(PrivateMarker);

    private sealed class PrivateOwner
    {
        public sealed class PublicChild
        {
        }
    }

    public static Type PrivateOwnerChildType => typeof(PrivateOwner.PublicChild);
}
