import System.Exception;
import System.ArgumentException;
import System.InvalidOperationException;
import System.Type;
import System.TypeCode;
import System.Int32;
import System.Byte;
import System.SByte;
import System.UInt16;
import System.UInt32;
import System.DateTime;
import System.Decimal;
import System.Runtime.Serialization.*;
import java.nio.file.*;
import java.util.*;
class NullableInt32BoxedTypeRelationsProbe {
 static Type shape(String name){Type definition=Type.GetType("System.Nullable`1");return switch(name){case "D"->definition;case "C"->Type.GetType("System.Nullable`1[System.Int32]");case "P"->definition.GetGenericArguments()[0];case "null"->null;default->Type.GetType("System."+name);};}
 static Object actual(String name,boolean owned){return switch(name){case "null"->null;case "Boolean"->true;case "Byte"->new Byte((short)42);case "Char"->'A';case "DateTime"->new DateTime(0L);case "Decimal"->new Decimal(42);case "Double"->1.25d;case "Int16"->(short)-42;case "Int32"->owned?new Int32(-42):Integer.valueOf(-42);case "Int64"->-42L;case "SByte"->new SByte((byte)-42);case "Single"->1.25f;case "String"->"sentinel";case "UInt16"->new UInt16(42);case "UInt32"->new UInt32(42L);case "UInt64"->java.math.BigInteger.valueOf(42);default->throw new AssertionError(name);};}
 public static void main(String[] args)throws java.lang.Exception{int calls=0;for(String line:Files.readAllLines(Path.of(args[0]))){String[] p=line.split("\t",-1);for(int representation=0;representation<(p[0].equals("instance")&&p[2].equals("Int32")?2:1);representation++){Type target=shape(p[1]);boolean value=switch(p[0]){case "assign"->target.IsAssignableFrom(shape(p[2]));case "subclass"->target.IsSubclassOf(shape(p[2]));case "instance"->target.IsInstanceOfType(actual(p[2],representation==1));default->throw new AssertionError(p[0]);};if(value!=Boolean.parseBoolean(p[3]))throw new AssertionError(line+": actual="+value);calls++;}}java.lang.System.out.println("PASS Nullable relations calls="+calls+" groups="+calls);}
}
