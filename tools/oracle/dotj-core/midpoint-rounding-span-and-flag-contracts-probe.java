import System.MidpointRounding;import System.Type;import System.DayOfWeek;import System.DateTimeKind;import System.Span;import System.ReadOnlySpan;import System.ISpanFormattable;import System.IFormatProvider;import System.Exception;import System.ArgumentException;import java.nio.file.*;import java.util.*;
class MidpointRoundingSpanAndFlagProbe{
 static void check(boolean ok,String context){if(!ok)throw new AssertionError(context);}
 public static void main(String[] args)throws java.lang.Exception{int groups=0;Type type=Type.GetType("System.MidpointRounding");for(String name:Files.readAllLines(Path.of(args[1]))){check(Type.GetType(name).IsAssignableFrom(type),"interface "+name);groups++;}check(!Type.GetType("System.IUtf8SpanFormattable").IsAssignableFrom(type),"no UTF8 enum interface");groups++;
  for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);MidpointRounding value=MidpointRounding.FromValue(Integer.parseInt(p[0]));String format=p[1].equals("~")?null:p[1];int capacity=Integer.parseInt(p[3]),offset=Integer.parseInt(p[4]),suffix=Integer.parseInt(p[5]);char[] buffer=new char[capacity+offset+suffix];Arrays.fill(buffer,'#');int[] written={99};IFormatProvider provider=t->{throw new AssertionError("provider consulted");};
   try{boolean actual=p[2].equals("array")?((ISpanFormattable)value).TryFormat(buffer,written,format,provider):value.TryFormat(Span.OfChars(buffer).Slice(offset,capacity),written,ReadOnlySpan.OfChars((format==null?"":format).toCharArray()),provider);check(p[9].isEmpty()&&actual==p[8].equals("1"),"outcome "+line);groups++;}catch(Exception ex){String param=ex instanceof ArgumentException a?a.get_ParamName():null;check(ex.getClass().getName().equals(p[9])&&ex.get_HResult()==Integer.parseInt(p[10])&&Objects.equals(param,p[11].equals("~")?null:p[11])&&ex.get_Message().equals(p[12]),"exception "+line);groups++;}
   check(written[0]==Integer.parseInt(p[6])&&new String(buffer).equals(p[7]),"written/buffer "+line);groups++;
  }groups+=MidpointRoundingFlagChecks.run(args[2]);java.lang.System.out.println("PASS MidpointRounding span and flags groups="+groups);
 }
}

class MidpointRoundingFlagChecks{
 static void check(boolean ok,String context){if(!ok)throw new AssertionError(context);}
 static int run(String vectorsPath)throws java.lang.Exception{int groups=0;
  for(String line:Files.readAllLines(Path.of(vectorsPath))){String[] p=line.split("\t",-1);MidpointRounding value=MidpointRounding.FromValue(Integer.parseInt(p[1]));Object flag=p[0].equals("P")?MidpointRounding.FromValue(Integer.parseInt(p[2])):switch(p[2]){case "null"->null;case "day"->DayOfWeek.Monday;case "date"->DateTimeKind.Utc;default->throw new AssertionError();};
   try{boolean actual=value.HasFlag(flag);check(p[4].isEmpty()&&actual==p[3].equals("1"),line);groups++;}catch(Exception ex){String param=ex instanceof ArgumentException a?a.get_ParamName():null;check(ex.getClass().getName().equals(p[4])&&ex.get_HResult()==Integer.parseInt(p[5])&&Objects.equals(param,p[6].equals("~")?null:p[6])&&ex.get_Message().equals(p[7]),line);groups++;}
  }return groups;
 }
}
