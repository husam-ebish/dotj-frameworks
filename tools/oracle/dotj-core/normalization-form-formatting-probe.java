import System.Text.*;import System.IFormattable;import System.IFormatProvider;import System.Exception;import java.nio.file.*;
class NormalizationFormFormattingProbe{
 static void check(boolean ok,String context){if(!ok)throw new AssertionError(context);}
 public static void main(String[] args)throws java.lang.Exception{int groups=0;
  for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);NormalizationForm value=NormalizationForm.FromInt32(Integer.parseInt(p[0]));String format=p[1].equals("~")?null:p[1];IFormatProvider provider=type->{throw new AssertionError("unexpected provider query for "+p[2]);};
   for(int route=0;route<2;route++){try{String actual=route==0?value.ToString(format,provider):((IFormattable)value).ToString(format,provider);check(p[4].isEmpty()&&actual.equals(p[3]),"format "+line);groups++;}catch(Exception ex){check(ex.getClass().getName().equals(p[4])&&ex.get_HResult()==Integer.parseInt(p[5])&&ex.get_Message().equals(p[6]),"exception "+line);groups++;}}
   check(value.ToString().equals(p[7])&&value.ToString(provider).equals(p[7])&&value.toString().equals(p[7]),"default "+line);groups++;
  }java.lang.System.out.println("PASS normalization form formatting groups="+groups);
 }
}
