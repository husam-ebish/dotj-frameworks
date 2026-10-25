import System.Text.*;
import System.Byte;
import System.Exception;
import System.ArgumentException;
import System.InvalidOperationException;
import System.IndexOutOfRangeException;
import System.ReadOnlySpan;
import System.Span;
import java.nio.file.*;
import java.util.*;
class StatefulConvertSpansProbe {
    static int groups;
    static String context;
    static void check(boolean value) { groups++; if (!value) throw new AssertionError(context + ": group " + groups); }
    static int[] ints(String s) { return s.isEmpty() ? new int[0] : Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray(); }
    static String trace(List<int[]> values) { return String.join(";",values.stream().map(r -> String.join(",",Arrays.stream(r).mapToObj(Integer::toString).toList())).toList()); }
    static class Hooks {
        int multiplier,countMode,writeMode; List<int[]> trace = new ArrayList<>();
        Hooks(int m,int c,int w) { multiplier=m;countMode=c;writeMode=w; }
        int count(int length,int index,int n,boolean flush,int kind) { trace.add(new int[]{kind,index,n,0,flush?1:0,length,0}); if(countMode==1)throw new InvalidOperationException("count failure");return countMode==3?-1:n*multiplier+(countMode==2?1:0); }
        int write(int length,int index,int n,Byte[] bytes,char[] chars,int offset,boolean flush,int kind) { int targetLength=bytes==null?chars.length:bytes.length;trace.add(new int[]{kind,index,n,offset,flush?1:0,length,targetLength});if(writeMode==2)return -1;int result=n*multiplier;for(int i=0;i<result;i++){if(offset+i<0||offset+i>=targetLength)throw new IndexOutOfRangeException();if(bytes!=null)bytes[offset+i]=new Byte(i+1);else chars[offset+i]=(char)(i+1);if(writeMode==1)throw new InvalidOperationException("write failure");}return result; }
    }
    static class E extends Encoder {
        Hooks h; E(Hooks h){this.h=h;}
        public int GetByteCount(char[] v,int i,int n,boolean f){return h.count(v.length,i,n,f,0);}
        public int GetBytes(char[] v,int i,int n,Byte[] b,int o,boolean f){return h.write(v.length,i,n,b,null,o,f,1);}
        public void Convert(char[] c,int i,int n,Byte[] b,int o,int cap,boolean f,int[] a,int[] z,boolean[] done){throw new InvalidOperationException("array Convert intercepted");}
    }
    static class D extends Decoder {
        Hooks h; D(Hooks h){this.h=h;}
        public int GetCharCount(Byte[] v,int i,int n){return h.count(v.length,i,n,false,2);}
        public int GetCharCount(Byte[] v,int i,int n,boolean f){return h.count(v.length,i,n,f,0);}
        public int GetChars(Byte[] v,int i,int n,char[] c,int o){return h.write(v.length,i,n,null,c,o,false,3);}
        public int GetChars(Byte[] v,int i,int n,char[] c,int o,boolean f){return h.write(v.length,i,n,null,c,o,f,1);}
        public void Convert(Byte[] b,int i,int n,char[] c,int o,int cap,boolean f,int[] a,int[] z,boolean[] done){throw new InvalidOperationException("array Convert intercepted");}
    }
    static Encoding encoding(int profile){Encoding e=new UTF8Encoding(profile==1||profile==3,profile==2||profile==3);if(profile>=4){e=(Encoding)e.Clone();e.set_EncoderFallback(new EncoderReplacementFallback(profile==4?"XY":""));e.set_DecoderFallback(new DecoderReplacementFallback(profile==4?"XY":""));}return e;}
    static void call(Object state,boolean encode,String[] p,int start){int[] values=ints(p[start]);int cap=Integer.parseInt(p[start+1]),off=Integer.parseInt(p[start+2]);boolean alias=p[start+4].equals("1");char[] ci=new char[values.length+2],co=new char[cap+off+4];byte[] bi=new byte[values.length+2],bo=new byte[cap+off+4];ci[0]=(char)0xDC00;ci[ci.length-1]=(char)0xD800;bi[0]=(byte)255;bi[bi.length-1]=(byte)255;for(int i=0;i<values.length;i++){ci[i+1]=(char)values[i];bi[i+1]=(byte)values[i];}Arrays.fill(co,(char)99);Arrays.fill(bo,(byte)99);int[] a={-7,-8},b=alias?a:new int[]{-8};boolean[] done={true};
        try{if(encode)((Encoder)state).Convert(ReadOnlySpan.OfChars(ci).Slice(1,values.length),Span.OfUtf8Bytes(bo).Slice(off+1,cap),p[start+3].equals("1"),a,b,done);else((Decoder)state).Convert(ReadOnlySpan.OfUtf8Bytes(bi).Slice(1,values.length),Span.OfChars(co).Slice(off+1,cap),p[start+3].equals("1"),a,b,done);check(p[start+5].equals("1"));}
        catch(Exception ex){check(p[start+5].equals("0")&&ex.getClass().getName().equals(p[start+6])&&ex.get_HResult()==Integer.parseInt(p[start+7])&&Objects.equals(ex instanceof ArgumentException arg?arg.get_ParamName():null,p[start+8].equals("null")?null:p[start+8]));}
        check(Arrays.equals(new int[]{a[0],alias?a[1]:b[0]},ints(p[start+9])));check(done[0]==p[start+10].equals("1"));int[] actual=new int[cap+off+4];for(int i=0;i<actual.length;i++)actual[i]=encode?bo[i]&255:co[i];check(Arrays.equals(actual,ints(p[start+11])));
    }
    public static void main(String[] args)throws java.lang.Exception{Object state=null;boolean encode=false;for(String line:Files.readAllLines(Path.of(args[0]))){context=line;String[] p=line.split("\t",-1);if(p[0].equals("R")){encode=p[1].equals("encoder");Encoding e=encoding(Integer.parseInt(p[2]));state=encode?e.GetEncoder():e.GetDecoder();}else if(p[0].equals("Z")){if(encode)((Encoder)state).Reset();else((Decoder)state).Reset();}else call(state,encode,p,1);}
        for(String line:Files.readAllLines(Path.of(args[1]))){context=line;String[] p=line.split("\t",-1);encode=p[0].equals("encoder");Hooks h=new Hooks(Integer.parseInt(p[1]),Integer.parseInt(p[2]),Integer.parseInt(p[3]));state=encode?new E(h):new D(h);if(p[4].equals("1")){if(encode)((Encoder)state).get_FallbackBuffer().Fallback((char)0xDC00,0);else((Decoder)state).get_FallbackBuffer().Fallback(new Byte[]{new Byte(255)},0);}call(state,encode,p,5);check(trace(h.trace).equals(p[17]));}
        java.lang.System.out.println("PASS stateful Convert span groups="+groups);
    }
}
