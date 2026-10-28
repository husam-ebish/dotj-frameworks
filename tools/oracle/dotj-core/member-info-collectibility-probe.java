import System.Type;
import System.InvalidOperationException;
import System.Reflection.MemberInfo;
import System.Reflection.MemberTypes;
import java.nio.file.*;
import java.util.*;
class MemberInfoCollectibilityProbe {
 static class Spy extends MemberInfo {int calls;InvalidOperationException fail(){calls++;return new InvalidOperationException("metadata getter");}public String get_Name(){throw fail();}public MemberTypes get_MemberType(){throw fail();}public Type get_DeclaringType(){throw fail();}public Type get_ReflectedType(){throw fail();}}
 static String token(Object o){return o==null?"~":o.toString();}
 public static void main(String[] args)throws java.lang.Exception{Spy a=new Spy(),b=new Spy();Type list=Type.GetType("System.Collections.Generic.List`1"),listS=list.MakeGenericType(new Type[]{Type.GetType("System.String")}),nullable=Type.GetType("System.Nullable`1[System.Int32]");Map<String,MemberInfo> objects=new HashMap<>();objects.put("A",a);objects.put("A2",a);objects.put("B",b);objects.put("I",Type.GetType("System.Int32"));objects.put("Array",Type.GetType("System.Int32[]"));objects.put("C",nullable);objects.put("P",Type.GetType("System.Nullable`1").GetGenericArguments()[0]);objects.put("ListD",list);objects.put("ListS",listS);objects.put("Dispose",Type.GetType("System.IDisposable").GetMethod("Dispose"));objects.put("Compare",Type.GetType("System.IComparable").GetMethod("CompareTo"));objects.put("Format",Type.GetType("System.IFormatProvider").GetMethod("GetFormat"));objects.put("Chars",Type.GetType("System.String").GetDefaultMembers()[0]);objects.put("ListItem",listS.GetDefaultMembers()[0]);objects.put("NullableArray",nullable.MakeArrayType());int calls=0,groups=0;
 for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);if(p[0].equals("G")){int count=p[1].equals("A")?a.calls:b.calls;if(count!=Integer.parseInt(p[2]))throw new AssertionError(line);groups++;continue;}MemberInfo member=objects.get(p[0]);boolean first=member.get_IsCollectible(),second=member.get_IsCollectible();Integer otherCalls=member instanceof Spy spy?spy.calls:null;Object[] actual={first,second,otherCalls};for(int i=0;i<actual.length;i++){if(!token(actual[i]).equals(p[1+i]))throw new AssertionError(line+" field="+i+" actual="+token(actual[i]));groups++;}calls+=2;}
 java.lang.System.out.println("PASS collectibility calls="+calls+" groups="+groups);}
}
