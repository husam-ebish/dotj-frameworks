import System.Text.*;
import System.Byte;
import System.ReadOnlySpan;
import System.Span;
import System.Exception;
import System.ArgumentException;import System.ArgumentOutOfRangeException;import System.NotSupportedException;import System.Type;
import System.InvalidOperationException;import System.IndexOutOfRangeException;
import java.nio.file.*;
import java.util.*;

class GenericEncodingCodepageMetadataProbe {
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
        public String GetString(Byte[] b) { throw intercepted(); }
        public int GetCharCount(Byte[] b) { throw intercepted(); }
        public char[] GetChars(Byte[] b) { throw intercepted(); }
    }
    static class AssertionErrorAdapter extends RuntimeException { }






static class Reported extends Fake {Reported(int cp){super(cp);}public int get_CodePage(){return 65001;}}
static String context;static void check(boolean ok,int id){if(!ok)throw new AssertionError(context+" group="+id);}static String decoded(String s){return new String(Base64.getDecoder().decode(s),java.nio.charset.StandardCharsets.UTF_8);}
static boolean failure(Exception ex,String[] p,int start){String param=ex instanceof ArgumentException a?a.get_ParamName():null;Object actual=ex instanceof ArgumentOutOfRangeException a?a.get_ActualValue():null;return p[start].equals("0")&&ex.getClass().getName().equals(p[start+1])&&ex.get_HResult()==Integer.parseInt(p[start+2])&&Objects.equals(param,p[start+3].equals("~")?null:p[start+3])&&Objects.equals(actual,p[start+4].equals("~")?null:Integer.valueOf(p[start+4]))&&ex.get_Message().equals(decoded(p[start+5]));}
public static void main(String[] args)throws java.lang.Exception{int id=0;for(String line:Files.readAllLines(Path.of(args[0]))){context=line;String[] p=line.split("\t",-1);switch(p[0]){
case "C":{try{Encoding e=p[2].equals("1")?new Reported(Integer.parseInt(p[1])):new Fake(Integer.parseInt(p[1]));check(p[3].equals("1"),id++);}catch(Exception ex){check(failure(ex,p,3),id++);}break;}
case "P":{Encoding e=p[2].equals("1")?new Reported(Integer.parseInt(p[1])):new Fake(Integer.parseInt(p[1]));try{Object value=switch(p[3]){case "BodyName"->e.get_BodyName();case "EncodingName"->e.get_EncodingName();case "HeaderName"->e.get_HeaderName();case "WebName"->e.get_WebName();case "WindowsCodePage"->e.get_WindowsCodePage();case "IsBrowserDisplay"->e.get_IsBrowserDisplay();case "IsBrowserSave"->e.get_IsBrowserSave();case "IsMailNewsDisplay"->e.get_IsMailNewsDisplay();case "IsMailNewsSave"->e.get_IsMailNewsSave();case "IsSingleByte"->e.get_IsSingleByte();case "CodePage"->e.get_CodePage();default->throw new AssertionError();};boolean same=switch(p[4]){case "System.String"->value instanceof String v&&v.equals(decoded(p[5]));case "System.Int32"->value instanceof Integer v&&v==Integer.parseInt(p[5]);case "System.Boolean"->value instanceof Boolean v&&v==p[5].equals("1");default->false;};check(p[6].equals("1")&&same,id++);}catch(Exception ex){check(failure(ex,p,6),id++);}break;}
case "E":{Exception inner=new Exception("inner");String message=p[2].equals("1")?null:decoded(p[3]);NotSupportedException ex=switch(Integer.parseInt(p[1])){case 0->new NotSupportedException();case 1->new NotSupportedException(message);case 2->new NotSupportedException(message,inner);default->throw new AssertionError();};check(ex.get_Message().equals(decoded(p[4])),id++);check(ex.get_HResult()==Integer.parseInt(p[5]),id++);check((ex.get_InnerException()==inner)==p[6].equals("1"),id++);check(ex.GetType().get_FullName().equals(p[7])&&ex.GetType().get_BaseType().get_FullName().equals(p[8]),id++);check(ex.GetType()==Type.GetType(p[7])&&ex.GetType()==Type.GetType(p[7].toLowerCase(java.util.Locale.ROOT),true,true),id++);break;}
default:throw new AssertionError();}}
java.lang.System.out.println("PASS generic Encoding code-page metadata groups="+id);}}
