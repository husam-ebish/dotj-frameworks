import System.Span;
import System.ReadOnlySpan;
import System.Globalization.NumberFormatInfo;
import System.InvalidOperationException;
import System.IFormatProvider;
import System.Decimal;
import System.Int32;
import System.Reflection.FieldAttributes;
import System.Reflection.FieldInfo;
import System.IConvertible;
import System.Reflection.MemberInfo;
import System.Reflection.MemberTypes;
import System.Reflection.MemberFilter;
import System.Reflection.TypeFilter;
import System.Reflection.MethodInfo;
import System.Reflection.ParameterInfo;
import System.Reflection.BindingFlags;
import System.Type;
import System.Exception;
import System.ArgumentException;
import System.Reflection.BindingFlags;
import System.Reflection.MemberTypes;
import System.Reflection.GenericParameterAttributes;
import System.TypeCode;
import java.nio.file.*;
import java.util.*;
class FieldAttributesSpanFormattingProbe {
 static String units(String s){if(s==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:s.toCharArray())j.add(Integer.toString(c));return j.toString();}
 static String value(Object o,Type self){if(o==null)return null;if(o instanceof Type t)return t==self?"self":"type:"+t.ToString();if(o instanceof MemberTypes v)return Integer.toString(v.get_Value());if(o instanceof GenericParameterAttributes v)return Integer.toString(v.get_Value());if(o instanceof TypeCode v)return Integer.toString(v.get_Value());if(o.getClass().isArray()){StringJoiner j=new StringJoiner(";");for(int i=0;i<java.lang.reflect.Array.getLength(o);i++)j.add(value(java.lang.reflect.Array.get(o,i),self));return j.toString();}return o.toString();}
 static Type resolve(String name){return switch(name){case "null"->null;case "ListS"->Type.GetType("System.Collections.Generic.List`1").MakeGenericType(new Type[]{Type.GetType("System.String")});case "NullableInt"->Type.GetType("System.Nullable`1").MakeGenericType(new Type[]{Type.GetType("System.Int32")});default->Type.GetType("System."+name);};}
 static final class Spy implements IFormatProvider {int calls;public Object GetFormat(Type type){calls++;throw new InvalidOperationException("provider consulted");}}
 static String decode(String units){if(units.equals("~"))return null;StringBuilder b=new StringBuilder();if(!units.isEmpty())for(String part:units.split(","))b.append((char)Integer.parseInt(part));return b.toString();}
 public static void main(String[] args)throws java.lang.Exception{int calls=0,groups=0;try(var reader=Files.newBufferedReader(Path.of(args[0]))){String line;while((line=reader.readLine())!=null){String[] p=line.split("\t",-1);String format=decode(p[2]),text=format==null?"":format;int cap=Integer.parseInt(p[3]),offset=Integer.parseInt(p[5]),suffix=p[4].equals("Array")?0:3;boolean alias=Boolean.parseBoolean(p[6]);int size=offset+cap+suffix;if(alias)size=Math.max(size,text.length()+2);char[] backing=new char[size];Arrays.fill(backing,'#');char[] formatChars=("!"+text+"!").toCharArray();int formatStart=1;if(alias){formatChars=backing;formatStart=0;for(int i=0;i<text.length();i++)backing[i]=text.charAt(i);}int[] written={177};Spy spy=new Spy();IFormatProvider provider=p[7].equals("Hostile")?spy:null;String result=null,error="none",message=null,param=null;int hResult=0;try{FieldAttributes e=FieldAttributes.FromInt32(Integer.parseInt(p[1]));boolean ok=p[4].equals("Array")?e.TryFormat(backing,written,format,provider):e.TryFormat(Span.OfChars(backing).Slice(offset,cap),written,ReadOnlySpan.OfChars(formatChars,formatStart,text.length()),provider);result=Boolean.toString(ok);}catch(Exception expected){error=expected.getClass().getName();message=expected.get_Message();hResult=expected.get_HResult();if(expected instanceof ArgumentException argument)param=argument.get_ParamName();}String[] actual={units(result),error,units(message),Integer.toString(hResult),units(param),Integer.toString(written[0]),units(new String(backing)),units(new String(formatChars)),Integer.toString(spy.calls)};for(int i=0;i<actual.length;i++){if(!actual[i].equals(p[8+i]))throw new AssertionError("id="+p[0]+" route="+p[4]+" value="+p[1]+" format="+p[2]+" capacity="+cap+" field="+i+" actual="+actual[i]+" expected="+p[8+i]);groups++;}calls++;}}java.lang.System.out.println("PASS FieldAttributes span calls="+calls+" groups="+groups);}
}
