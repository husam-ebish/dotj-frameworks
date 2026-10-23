using System.Globalization;

public sealed class SelectedDecimalProvider : IFormatProvider
{
    private readonly NumberFormatInfo format;

    public SelectedDecimalProvider(NumberFormatInfo format)
    {
        this.format = format;
    }

    public object? GetFormat(Type? formatType)
    {
        return formatType == typeof(NumberFormatInfo) ? this.format : null;
    }
}
