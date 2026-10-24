import System.DateTime;
public class WallClockProbe {
    public static void main(String[] args) {
        DateTime value = switch(args[0]) {
            case "UtcNow" -> DateTime.get_UtcNow();
            case "Now" -> DateTime.get_Now();
            case "Today" -> DateTime.get_Today();
            default -> throw new AssertionError("Unknown clock property");
        };
        java.lang.System.out.println(value.get_Ticks()+"|"+value.get_Kind()+"|"+value.get_Date().get_Ticks()+"|"+value.get_TimeOfDay().get_Ticks()+"|"+java.time.ZoneId.systemDefault());
    }
}
