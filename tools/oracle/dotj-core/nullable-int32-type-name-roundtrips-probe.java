import System.Type;
import System.Exception;
import System.TypeLoadException;
import System.ArgumentException;
import java.nio.file.*;
class NullableInt32TypeNameRoundtripsProbe {
 static String input(String s){StringBuilder b=new StringBuilder();for(String c:s.split(","))b.append((char)Integer.parseInt(c));return b.toString();}
 static String token(Object o){return o==null?"~":o.toString();}
 public static void main(String[] args)throws java.lang.Exception {int calls=0,groups=0;for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);Object[] a={"null",null,0,null,null,null,null,null,null,null,null,null,null,null,null,null};try{Type t=Type.GetType(input(p[0]),Boolean.parseBoolean(p[1]),Boolean.parseBoolean(p[2]));if(t!=null){a[0]="type";a[5]=t.get_FullName();a[6]=t.get_AssemblyQualifiedName();a[7]=t.get_Name();a[8]=t.get_Namespace();a[9]=t.get_IsArray();a[10]=t.get_IsByRef();a[11]=t.get_IsPointer();a[12]=t.get_ContainsGenericParameters();a[13]=t.get_IsGenericTypeDefinition();a[14]=t==Type.GetType(t.get_FullName(),true,false);a[15]=t==Type.GetType(t.get_AssemblyQualifiedName(),true,false);}}catch(Exception expected){a[0]="error";a[1]=expected.getClass().getName();a[2]=expected.get_HResult();if(expected instanceof TypeLoadException load)a[4]=load.get_TypeName();if(expected instanceof ArgumentException argument)a[3]=argument.get_ParamName();}for(int i=0;i<a.length;i++){if(!token(a[i]).equals(p[3+i]))throw new AssertionError("input="+p[0]+" throw="+p[1]+" ignore="+p[2]+" field="+i+" actual="+token(a[i])+" expected="+p[3+i]);groups++;}calls++;}java.lang.System.out.println("PASS nullable names calls="+calls+" groups="+groups);}
}
