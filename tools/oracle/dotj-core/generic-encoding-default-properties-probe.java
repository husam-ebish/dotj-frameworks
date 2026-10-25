import System.Text.*;
import System.Byte;
import System.ReadOnlySpan;
import System.Span;
import System.Exception;
import System.ArgumentException;import System.ArgumentOutOfRangeException;
import System.InvalidOperationException;import System.IndexOutOfRangeException;
import java.nio.file.*;
import java.util.*;

class GenericEncodingDefaultPropertiesProbe {
    static class Fake extends Encoding {
        Fake(){super();}Fake(int cp){super(cp);}Fake(int cp,EncoderFallback e,DecoderFallback d){super(cp,e,d);}
        int multiplier, countMode, writeMode;
        List<String> trace = new ArrayList<>();
        void record(int kind,int index,int count,int offset){trace.add(kind+","+index+","+count+","+offset);}
        RuntimeException intercepted() { return new AssertionErrorAdapter(); }
        public int GetByteCount(char[] chars,int index,int count){record(0,index,count,-1);return count(count);}
        public int GetCharCount(Byte[] bytes,int index,int count){record(2,index,count,-1);return count(count);}
        int count(int n){if(countMode==1)throw new InvalidOperationException("array callback failure");return countMode==2?-1:n*multiplier;}
        int write(int n){if(writeMode==1)throw new InvalidOperationException("array callback failure");return writeMode==2?-1:n*multiplier;}
        public int GetBytes(char[] s,int i,int n,Byte[] b,int o) {record(1,i,n,o);if(n>0){if(o<0||o>=b.length)throw new IndexOutOfRangeException();b[o]=new Byte(42);}return write(n);}
        public int GetChars(Byte[] b,int i,int n,char[] s,int o) {record(3,i,n,o);if(n>0){if(o<0||o>=s.length)throw new IndexOutOfRangeException();s[o]=(char)42;}return write(n);}
        public int GetMaxByteCount(int n) { throw intercepted(); }
        public int GetMaxCharCount(int n) { throw intercepted(); }
        public String get_EncodingName() { return "probe"; }
        public String GetString(Byte[] b) { throw intercepted(); }
        public int GetCharCount(Byte[] b) { throw intercepted(); }
        public char[] GetChars(Byte[] b) { throw intercepted(); }
    }
    static class AssertionErrorAdapter extends RuntimeException { }





static int[] ints(String s){return s.isEmpty()?new int[0]:Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray();}static int[] units(String s){int[] r=new int[s.length()];for(int i=0;i<r.length;i++)r[i]=s.charAt(i);return r;}static String bits(boolean... v){StringBuilder b=new StringBuilder();for(boolean f:v)b.append(f?'1':'0');return b.toString();}static String decoded(String s){return new String(Base64.getDecoder().decode(s),java.nio.charset.StandardCharsets.UTF_8);}static String context;static void check(boolean ok,int id){if(!ok)throw new AssertionError(context+" group="+id);}
static boolean failure(Exception ex,String[] p,int start){String param=ex instanceof ArgumentException a?a.get_ParamName():null;Object actual=ex instanceof ArgumentOutOfRangeException a?a.get_ActualValue():null;return p[start].equals("0")&&ex.getClass().getName().equals(p[start+1])&&ex.get_HResult()==Integer.parseInt(p[start+2])&&Objects.equals(param,p[start+3].equals("~")?null:p[start+3])&&Objects.equals(actual,p[start+4].equals("~")?null:Integer.valueOf(p[start+4]))&&ex.get_Message().equals(decoded(p[start+5]));}
public static void main(String[] args)throws java.lang.Exception{int id=0;List<Encoding> owners=new ArrayList<>();EncoderFallback providedE=null,mutE=null;DecoderFallback providedD=null,mutD=null;Byte[] utf8Empty=new UTF8Encoding(false).GetPreamble();for(String line:Files.readAllLines(Path.of(args[0]))){context=line;String[] p=line.split("\t",-1);switch(p[0]){
case "C":{owners.clear();int kind=Integer.parseInt(p[2]),cp=Integer.parseInt(p[3]),profile=Integer.parseInt(p[4]);providedE=null;providedD=null;switch(profile){case 1:providedE=new EncoderReplacementFallback("AB");providedD=new DecoderReplacementFallback("CD");break;case 2:providedE=new EncoderReplacementFallback("");providedD=new DecoderReplacementFallback("");break;case 3:providedE=new EncoderReplacementFallback("\ud800\udc00");providedD=new DecoderReplacementFallback("\ud800\udc00");break;case 4:providedE=EncoderFallback.get_ExceptionFallback();providedD=DecoderFallback.get_ExceptionFallback();break;case 5:providedD=new DecoderReplacementFallback("CD");break;case 6:providedE=new EncoderReplacementFallback("AB");break;default:break;}mutE=new EncoderReplacementFallback("XY");mutD=new DecoderReplacementFallback("ZW");try{Encoding e=switch(kind){case 0->new Fake();case 1->new Fake(cp);case 2->new Fake(cp,providedE,providedD);default->throw new AssertionError();};owners.add(e);check(p[5].equals("1"),id++);}catch(Exception ex){check(failure(ex,p,5),id++);}break;}
case "A":{Encoding e=owners.get(Integer.parseInt(p[3]));try{switch(p[2]){case "Read":break;case "SetEncoder":e.set_EncoderFallback(mutE);break;case "SetDecoder":e.set_DecoderFallback(mutD);break;case "NullEncoder":e.set_EncoderFallback(null);break;case "NullDecoder":e.set_DecoderFallback(null);break;case "Clone":owners.add((Encoding)e.Clone());break;case "ResetEncoder":e.set_EncoderFallback(EncoderFallback.get_ReplacementFallback());break;case "ResetDecoder":e.set_DecoderFallback(DecoderFallback.get_ReplacementFallback());break;default:throw new AssertionError();}check(p[4].equals("1"),id++);}catch(Exception ex){check(failure(ex,p,4),id++);}break;}
case "S":{Encoding e=owners.get(Integer.parseInt(p[2]));EncoderFallback ef=e.get_EncoderFallback();DecoderFallback df=e.get_DecoderFallback();Byte[] preamble=e.GetPreamble();check(e.get_IsReadOnly()==p[3].equals("1")&&e.get_CodePage()==Integer.parseInt(p[4])&&e.get_IsSingleByte()==p[5].equals("1"),id++);check(ef.getClass().getName().equals(p[6])&&df.getClass().getName().equals(p[7]),id++);check(ef.get_MaxCharCount()==Integer.parseInt(p[8])&&df.get_MaxCharCount()==Integer.parseInt(p[9]),id++);check((ef instanceof EncoderReplacementFallback)==p[10].equals("1")&&(!(ef instanceof EncoderReplacementFallback r)||Arrays.equals(units(r.get_DefaultString()),ints(p[11]))),id++);check((df instanceof DecoderReplacementFallback)==p[12].equals("1")&&(!(df instanceof DecoderReplacementFallback r)||Arrays.equals(units(r.get_DefaultString()),ints(p[13]))),id++);check(bits(ef==EncoderFallback.get_ReplacementFallback(),df==DecoderFallback.get_ReplacementFallback(),ef==providedE,df==providedD,ef==mutE,df==mutD,preamble==e.GetPreamble(),preamble==owners.get(0).GetPreamble(),preamble==utf8Empty).equals(p[14]),id++);check(preamble!=null&&preamble.length==Integer.parseInt(p[15]),id++);break;}
default:throw new AssertionError();}}
java.lang.System.out.println("PASS generic Encoding default properties groups="+id);}}
