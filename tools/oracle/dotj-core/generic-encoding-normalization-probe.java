import System.Text.*;import System.Byte;import System.Type;import System.Exception;import System.InvalidOperationException;import java.nio.file.*;import java.util.*;
class GenericEncodingNormalizationProbe{
 static class Minimal extends Encoding{
  public int GetByteCount(char[] c,int i,int n){return n;}public int GetCharCount(Byte[] b,int i,int n){return n;}
  public int GetBytes(char[] c,int i,int n,Byte[] b,int o){return n;}public int GetChars(Byte[] b,int i,int n,char[] c,int o){return n;}
  public int GetMaxByteCount(int n){return n;}public int GetMaxCharCount(int n){return n;}
 }
 static class Normalized extends Minimal{int mode,seen=12345;Normalized(int mode){this.mode=mode;}public boolean IsAlwaysNormalized(NormalizationForm form){seen=form.get_Value();if(mode==-1)throw new InvalidOperationException("normalization callback");return mode==seen;}}
 static void check(boolean ok,String context){if(!ok)throw new AssertionError(context);}
 public static void main(String[] args)throws java.lang.Exception{
  int groups=0;Type t=Type.GetType("System.Text.NormalizationForm");check(t!=null&&t.get_FullName().equals(NormalizationForm.class.getName()),"identity");groups++;check(Type.GetType("system.text.normalizationform",false,true)==t,"case alias");groups++;check(Type.GetType("system.text.normalizationform")==null,"exact case");groups++;check(Type.GetType("System.Text.NormalizationForm[]")==t.MakeArrayType(),"array");groups++;check(t.get_IsEnum(),"enum");groups++;check(t.get_BaseType()==Type.GetType("System.Enum"),"base");groups++;check(t.GetEnumUnderlyingType()==Type.GetType("System.Int32"),"underlying");groups++;check(t.GetEnumNames().length==4&&t.GetEnumValues().length==4,"names count");groups++;
  int index=0;for(String line:Files.readAllLines(Path.of(args[1]))){String[] p=line.split("\t");String name=p[0];int value=Integer.parseInt(p[1]);NormalizationForm f=NormalizationForm.values()[index++];check(f.get_Value()==value&&f.get_Name().equals(name),"constant "+name);groups++;check(t.GetEnumName(value).equals(name)&&t.GetEnumValuesAsUnderlyingType()[index-1]==value,"enum name "+name);groups++;check(t.IsEnumDefined(f)&&t.IsEnumDefined(name),"defined "+name);groups++;}
  for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);int kind=Integer.parseInt(p[0]),form=Integer.parseInt(p[2]);Encoding e=kind==0?new Minimal():kind==1?new UTF8Encoding(false,false):new Normalized(kind==2?1:kind==3?6:-1);if(p[1].equals("1"))e=(Encoding)e.Clone();try{boolean result=p[3].equals("1")?e.IsAlwaysNormalized():e.IsAlwaysNormalized(NormalizationForm.FromInt32(form));check(p[5].isEmpty()&&result==p[4].equals("1"),line);groups++;}catch(Exception ex){check(ex.getClass().getName().equals(p[5])&&ex.get_HResult()==Integer.parseInt(p[6])&&ex.get_Message().equals(p[7]),line);groups++;}check((e instanceof Normalized n?n.seen:12345)==Integer.parseInt(p[8]),"dispatch "+line);groups++;}
  java.lang.System.out.println("PASS generic Encoding normalization groups="+groups);
 }
}
