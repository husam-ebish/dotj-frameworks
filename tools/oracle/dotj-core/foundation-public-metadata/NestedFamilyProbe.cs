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
}
