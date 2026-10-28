import System.Type;
import System.InvalidOperationException;
import System.Reflection.MemberInfo;
import System.Reflection.MemberTypes;
import java.nio.file.*;
import java.util.*;
class MemberInfoBaseEqualityProbe {
 static class Spy extends MemberInfo {int calls;InvalidOperationException fail(){calls++;return new InvalidOperationException("metadata getter");}public String get_Name(){throw fail();}public MemberTypes get_MemberType(){throw fail();}public Type get_DeclaringType(){throw fail();}public Type get_ReflectedType(){throw fail();}}
 static String token(Object o){return o==null?"~":o.toString();}
 public static void main(String[] args)throws java.lang.Exception{Spy a=new Spy(),b=new Spy();Map<String,Object> objects=new HashMap<>();objects.put("A",a);objects.put("A2",a);objects.put("B",b);objects.put("I",Type.GetType("System.Int32"));objects.put("I2",Type.GetType("System.Int32"));objects.put("C",Type.GetType("System.Nullable`1[System.Int32]"));objects.put("Array",Type.GetType("System.Int32[]"));objects.put("O",new Object());objects.put("S","sentinel");int groups=0,calls=0;
 for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);switch(p[0]){case "E"->{boolean value=((MemberInfo)objects.get(p[1])).Equals(objects.get(p[2]));if(value!=Boolean.parseBoolean(p[3]))throw new AssertionError(line);groups++;calls++;}case "H"->{MemberInfo member=(MemberInfo)objects.get(p[1]);int first=member.GetHashCode(),second=member.GetHashCode();Boolean identity=member instanceof Spy?first==java.lang.System.identityHashCode(member):null;if(!Boolean.toString(first==second).equals(p[2])||!token(identity).equals(p[3]))throw new AssertionError(line);groups+=2;calls+=2;}case "G"->{int value=p[1].equals("A")?a.calls:b.calls;if(value!=Integer.parseInt(p[2]))throw new AssertionError(line);groups++;}case "P"->{Spy positive=new Spy();try{positive.get_Name();throw new AssertionError("Missing positive failure");}catch(InvalidOperationException expected){if(!expected.get_Message().equals("metadata getter"))throw new AssertionError();}if(positive.calls!=Integer.parseInt(p[1]))throw new AssertionError(line);calls++;groups++;}default->throw new AssertionError(line);}}
 java.lang.System.out.println("PASS MemberInfo equality calls="+calls+" groups="+groups);}
}
