import System.Text.*;import System.Exception;import System.ArgumentException;import System.DayOfWeek;import System.DateTimeKind;import java.nio.file.*;import java.util.*;
class NormalizationFormHasFlagProbe{
 static void check(boolean ok,String context){if(!ok)throw new AssertionError(context);}
 public static void main(String[] args)throws java.lang.Exception{int groups=0;
  for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);NormalizationForm value=NormalizationForm.FromInt32(Integer.parseInt(p[1]));Object flag=p[0].equals("P")?NormalizationForm.FromInt32(Integer.parseInt(p[2])):switch(p[2]){case "null"->null;case "day"->DayOfWeek.Monday;case "date"->DateTimeKind.Utc;default->throw new AssertionError();};
   try{boolean actual=value.HasFlag(flag);check(p[4].isEmpty()&&actual==p[3].equals("1"),line);groups++;}catch(Exception ex){String param=ex instanceof ArgumentException a?a.get_ParamName():null;check(ex.getClass().getName().equals(p[4])&&ex.get_HResult()==Integer.parseInt(p[5])&&Objects.equals(param,p[6].equals("~")?null:p[6])&&ex.get_Message().equals(p[7]),line);groups++;}
  }java.lang.System.out.println("PASS normalization form HasFlag groups="+groups);
 }
}
