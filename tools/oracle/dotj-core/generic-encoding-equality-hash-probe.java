import System.Text.*;import System.Byte;import java.nio.file.*;import java.util.*;
class GenericEncodingEqualityHashProbe{
 static class Minimal extends Encoding{
  Minimal(int cp,EncoderFallback e,DecoderFallback d){super(cp,e,d);}
  public int GetByteCount(char[] c,int i,int n){return n;}public int GetCharCount(Byte[] b,int i,int n){return n;}
  public int GetBytes(char[] c,int i,int n,Byte[] b,int o){return n;}public int GetChars(Byte[] b,int i,int n,char[] c,int o){return n;}
  public int GetMaxByteCount(int n){return n;}public int GetMaxCharCount(int n){return n;}
 }
 static class Reported extends Minimal{Reported(int cp,EncoderFallback e,DecoderFallback d){super(cp,e,d);}public int get_CodePage(){return 65001;}}
 static void check(boolean ok,String context){if(!ok)throw new AssertionError(context);}
 public static void main(String[] args)throws java.lang.Exception{
  List<Encoding> states=new ArrayList<>();int groups=0;
  for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t");int kind=Integer.parseInt(p[0]),cp=Integer.parseInt(p[1]),profile=Integer.parseInt(p[2]);EncoderFallback e=null;DecoderFallback d=null;
   switch(profile){case 1:e=new EncoderReplacementFallback("AB");d=new DecoderReplacementFallback("CD");break;case 2:e=new EncoderReplacementFallback("\ufffd");d=new DecoderReplacementFallback("\ufffd");break;case 3:e=new EncoderReplacementFallback("");d=new DecoderReplacementFallback("");break;case 4:e=EncoderFallback.get_ExceptionFallback();d=DecoderFallback.get_ExceptionFallback();break;default:break;}
   Encoding owner=kind==0?new Minimal(cp,e,d):kind==1?new Reported(cp,e,d):new UTF8Encoding(kind==3||kind==5,kind==4||kind==5);
   if(kind>=2&&profile!=0){owner=(Encoding)owner.Clone();owner.set_EncoderFallback(e);owner.set_DecoderFallback(d);}if(p[3].equals("1"))owner=(Encoding)owner.Clone();int index=states.size();states.add(owner);
   int expectedHash=cp+owner.get_EncoderFallback().GetHashCode()+owner.get_DecoderFallback().GetHashCode()+((kind==3||kind==5)?1:0);check(owner.GetHashCode()==expectedHash,"hash formula state="+index+" actual="+owner.GetHashCode()+" expected="+expectedHash);groups++;
   check(owner.Equals(null)==p[7].equals("1"),"null state="+index);groups++;
   check(owner.Equals("owned")==p[8].equals("1"),"string state="+index);groups++;
   check(owner.get_IsReadOnly()==p[4].equals("1")&&owner.get_CodePage()==Integer.parseInt(p[5]),"properties state="+index);groups++;
  }
  for(String line:Files.readAllLines(Path.of(args[1]))){String[] p=line.split("\t");int l=Integer.parseInt(p[0]),r=Integer.parseInt(p[1]);check(states.get(l).Equals(states.get(r))==p[2].equals("1"),"pair="+l+","+r);groups++;}
  java.lang.System.out.println("PASS generic Encoding equality/hash groups="+groups);
 }
}
