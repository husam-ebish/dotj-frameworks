import System.Text.*;
import System.Exception;
import System.ArgumentException;
import System.ReadOnlySpan;
import System.Span;
import java.nio.file.*;
import java.util.*;
class GenericSpanDispatchProbe {
    static int groups;
    static String context;
    static void check(boolean v){groups++;if(!v)throw new AssertionError(context+": group "+groups);}
    static String csv(int[] v){return String.join(",",Arrays.stream(v).mapToObj(Integer::toString).toList());}
    public static void main(String[] args)throws java.lang.Exception{for(String line:Files.readAllLines(Path.of(args[0]))){context=line;String[] p=line.split("\t",-1);boolean encode=p[0].equals("encoder"),write=p[8].equals("1"),flush=p[7].equals("1");int n=Integer.parseInt(p[4]),cap=Integer.parseInt(p[5]),off=Integer.parseInt(p[6]);StatefulConvertSpansProbe.Hooks h=new StatefulConvertSpansProbe.Hooks(Integer.parseInt(p[1]),Integer.parseInt(p[2]),Integer.parseInt(p[3]));Encoder e=encode?new StatefulConvertSpansProbe.E(h):null;Decoder d=encode?null:new StatefulConvertSpansProbe.D(h);char[] ci=new char[n+2],co=new char[cap+off+4];byte[] bi=new byte[n+2],bo=new byte[cap+off+4];Arrays.fill(ci,'A');Arrays.fill(bi,(byte)65);ci[0]=(char)0xDC00;ci[ci.length-1]=(char)0xD800;bi[0]=(byte)255;bi[bi.length-1]=(byte)255;Arrays.fill(co,(char)99);Arrays.fill(bo,(byte)99);
        try{int value;if(encode)value=write?e.GetBytes(ReadOnlySpan.OfChars(ci).Slice(1,n),Span.OfUtf8Bytes(bo).Slice(off+1,cap),flush):e.GetByteCount(ReadOnlySpan.OfChars(ci).Slice(1,n),flush);else value=write?d.GetChars(ReadOnlySpan.OfUtf8Bytes(bi).Slice(1,n),Span.OfChars(co).Slice(off+1,cap),flush):d.GetCharCount(ReadOnlySpan.OfUtf8Bytes(bi).Slice(1,n),flush);check(p[9].equals("1")&&value==Integer.parseInt(p[10]));}
        catch(Exception ex){check(p[9].equals("0")&&ex.getClass().getName().equals(p[11])&&ex.get_HResult()==Integer.parseInt(p[12])&&Objects.equals(ex instanceof ArgumentException a?a.get_ParamName():null,p[13].equals("null")?null:p[13]));}
        check(StatefulConvertSpansProbe.trace(h.trace).equals(p[15]));if(write){int[] actual=new int[cap+off+4];for(int i=0;i<actual.length;i++)actual[i]=encode?bo[i]&255:co[i];check(csv(actual).equals(p[14]));}
    }java.lang.System.out.println("PASS generic span dispatch groups="+groups);}
}
