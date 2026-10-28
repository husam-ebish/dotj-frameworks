import System.Type;
import java.nio.file.*;
import java.util.*;
class NullableInt32TypeMetadataProbe {
 static String value(Type t) { return t == null ? null : t.get_FullName(); }
 static String names(Type[] a) { StringJoiner j=new StringJoiner(";"); for(Type t:a) j.add(t.get_FullName()==null?t.get_Name():t.get_FullName()); return j.toString(); }
 static boolean copy(Type t, boolean constructed) { Type[] a=constructed?t.get_GenericTypeArguments():t.GetGenericArguments();if(a.length==0)return true;Type saved=a[0];a[0]=null;return saved==(constructed?t.get_GenericTypeArguments():t.GetGenericArguments())[0]; }
 public static void main(String[] args) throws java.lang.Exception {
  Type definition=Type.GetType("System.Nullable`1"),closed=Type.GetType("System.Nullable`1[System.Int32]");int groups=0;
  for(String line:Files.readAllLines(Path.of(args[0]))) { String[] p=line.split("\t",-1);Type t=p[0].equals("D")?definition:p[0].equals("C")?closed:definition.GetGenericArguments()[0];
   Object actual=switch(p[1]) {
    case "Name"->t.get_Name();case "Namespace"->t.get_Namespace();case "FullName"->t.get_FullName();case "AssemblyQualifiedName"->t.get_AssemblyQualifiedName();case "BaseType"->value(t.get_BaseType());case "DeclaringType"->value(t.get_DeclaringType());
    case "IsValueType"->t.get_IsValueType();case "IsPrimitive"->t.get_IsPrimitive();case "IsClass"->t.get_IsClass();case "IsSealed"->t.get_IsSealed();case "IsSerializable"->t.get_IsSerializable();case "IsPublic"->t.get_IsPublic();case "IsNested"->t.get_IsNested();
    case "IsGenericType"->t.get_IsGenericType();case "IsGenericTypeDefinition"->t.get_IsGenericTypeDefinition();case "IsConstructedGenericType"->t.get_IsConstructedGenericType();case "ContainsGenericParameters"->t.get_ContainsGenericParameters();case "IsGenericParameter"->t.get_IsGenericParameter();case "IsTypeDefinition"->t.get_IsTypeDefinition();
    case "GenericArguments"->names(t.GetGenericArguments());case "GenericTypeArguments"->names(t.get_GenericTypeArguments());case "ArgumentsDefensiveCopy"->copy(t,false);case "GenericTypeArgumentsDefensiveCopy"->copy(t,true);
    case "GenericDefinition"->value(t.GetGenericTypeDefinition());case "GenericParameterAttributes"->t.get_GenericParameterAttributes().get_Value();case "GenericParameterPosition"->t.get_GenericParameterPosition();case "Constraints"->names(t.GetGenericParameterConstraints());
    case "ConstraintsDefensiveCopy"->{Type[] a=t.GetGenericParameterConstraints();Type saved=a[0];a[0]=null;yield saved==t.GetGenericParameterConstraints()[0];}default->throw new AssertionError(p[1]);
   };String result=actual==null?"~":actual.toString();if(!result.equals(p[2]))throw new AssertionError(p[0]+" "+p[1]+": "+result+" != "+p[2]);groups++;
  }java.lang.System.out.println("PASS Nullable metadata groups="+groups);
 }
}
