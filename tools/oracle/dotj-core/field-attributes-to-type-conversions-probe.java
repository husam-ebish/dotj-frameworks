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
class FieldAttributesToTypeConversionsProbe {
 static String units(String s){if(s==null)return "~";StringJoiner j=new StringJoiner(",");for(char c:s.toCharArray())j.add(Integer.toString(c));return j.toString();}
 static String value(Object o,Type self){if(o==null)return null;if(o instanceof Type t)return t==self?"self":"type:"+t.ToString();if(o instanceof MemberTypes v)return Integer.toString(v.get_Value());if(o instanceof GenericParameterAttributes v)return Integer.toString(v.get_Value());if(o instanceof TypeCode v)return Integer.toString(v.get_Value());if(o.getClass().isArray()){StringJoiner j=new StringJoiner(";");for(int i=0;i<java.lang.reflect.Array.getLength(o);i++)j.add(value(java.lang.reflect.Array.get(o,i),self));return j.toString();}return o.toString();}
 static Type resolve(String name){return switch(name){case "null"->null;case "ListS"->Type.GetType("System.Collections.Generic.List`1").MakeGenericType(new Type[]{Type.GetType("System.String")});case "NullableInt"->Type.GetType("System.Nullable`1").MakeGenericType(new Type[]{Type.GetType("System.Int32")});default->Type.GetType("System."+name);};}
 static final class Spy implements IFormatProvider {int calls;public Object GetFormat(Type type){calls++;throw new InvalidOperationException("provider consulted");}}
 static String normalize(Object value,FieldAttributes self,String target){if(value==null)return null;if(value instanceof FieldAttributes)return "self:"+(value==self);if(value instanceof String text)return "System.String:"+text;if(value instanceof Boolean flag)return "System.Boolean:"+flag;if(value instanceof Character c)return "System.Char:"+(int)c;if(value instanceof Float n)return "System.Single:"+String.format(java.util.Locale.ROOT,"%08X",Float.floatToRawIntBits(n));if(value instanceof Double n)return "System.Double:"+String.format(java.util.Locale.ROOT,"%016X",Double.doubleToRawLongBits(n));String text=value instanceof IConvertible c?c.ToString(null):value.toString();return "System."+target+":"+text;}
 public static void main(String[] args)throws java.lang.Exception{int calls=0,groups=0;try(var reader=Files.newBufferedReader(Path.of(args[0]))){String line;while((line=reader.readLine())!=null){String[] p=line.split("\t",-1);String result=null,error="none",message=null,param=null;int hResult=0;Spy spy=new Spy();try{FieldAttributes e=FieldAttributes.FromInt32(Integer.parseInt(p[1]));Type target=resolve(p[2]);IFormatProvider provider=null;switch(p[3]){case "Invariant"->provider=NumberFormatInfo.get_InvariantInfo();case "Custom"->{NumberFormatInfo custom=(NumberFormatInfo)NumberFormatInfo.get_InvariantInfo().Clone();custom.set_NegativeSign("minus");custom.set_NumberDecimalSeparator(":");provider=custom;}case "Hostile"->provider=spy;default->{}}result=normalize(e.ToType(target,provider),e,p[2]);}catch(Exception expected){error=expected.getClass().getName();message=expected.get_Message();hResult=expected.get_HResult();if(expected instanceof ArgumentException argument)param=argument.get_ParamName();}String[] actual={units(result),error,units(message),Integer.toString(hResult),units(param),Integer.toString(spy.calls)};for(int i=0;i<actual.length;i++){if(!actual[i].equals(p[4+i]))throw new AssertionError("id="+p[0]+" value="+p[1]+" target="+p[2]+" provider="+p[3]+" field="+i+" actual="+actual[i]+" expected="+p[4+i]);groups++;}calls++;}}java.lang.System.out.println("PASS FieldAttributes ToType calls="+calls+" groups="+groups);}
}
