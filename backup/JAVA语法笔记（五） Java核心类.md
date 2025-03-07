## 字符串和编码
`Java`字符串`String`是不可变对象；
字符串操作不改变原字符串内容，而是返回新字符串；
常用的字符串操作：提取子串、查找、替换、大小写转换等；
`Java`使用`Unicode`编码表示`String`和`char`；
转换编码就是将`String`和`byte[]`转换，需要指定编码；
转换为`byte[]`时，始终优先考虑`UTF-8`编码。
### String
在Java中，`String`是一个引用类型，它本身也是一个`class`。但是，Java编译器对`String`有特殊处理，即可以直接用`"..."`来表示一个字符串
实际上字符串在`String`内部是通过一个`char[]`数组表示的，因此，按下面的写法也是可以的：
```java
String s1 = "Hello!";
String s2 = new String(new char[] {'H', 'e', 'l', 'l', 'o', '!'});
```
因为`String`太常用了，所以Java提供了`"..."`这种字符串字面量表示方法。
Java字符串的一个重要特点就是字符串**不可变**。这种不可变性是通过内部的`private final char[]`字段，以及没有任何修改`char[]`的方法实现的。
```java
// String
public class Main {
    public static void main(String[] args) {
        String s = "Hello";
        System.out.println(s);
        s = s.toUpperCase();
        System.out.println(s);
    }
}
```
运行结果：
>Hello
HELLO
Process finished with exit code 0


### 字符串比较
当我们想要比较两个字符串是否相同时，要特别注意，我们实际上是想比较字符串的内容是否相同。必须使用`equals()`方法而不能用`==`。
我们看下面的例子：
```java
// String
public class Main {
    public static void main(String[] args) {
        String s1 = "hello";
        String s2 = "hello";
        System.out.println(s1 == s2);
        System.out.println(s1.equals(s2));
    }
}
```
从表面上看，两个字符串用`==`和`equals()`比较都为`true`，但实际上那只是**Java编译器在编译期，会自动把所有相同的字符串当作一个对象放入常量池，自然`s1`和`s2`的引用就是相同的。**

所以，这种`==`比较返回`true`纯属巧合。换一种写法，`==`比较就会失败：
```java
// String
public class Main {
    public static void main(String[] args) {
        String s1 = "hello";
        String s2 = "HELLO".toLowerCase();
        System.out.println(s1 == s2);
        System.out.println(s1.equals(s2));
    }
}
```
结论：两个字符串比较，必须总是使用`equals()`方法。
要忽略大小写比较，使用`equalsIgnoreCase()`方法。
`String`类还提供了多种方法来搜索子串、提取子串。常用的方法有：
```java
// 是否包含子串:
"Hello".contains("ll"); // true
```
注意到`contains()`方法的参数是`CharSequence`而不是`String`，因为`CharSequence`是`String`实现的一个接口。

搜索子串的更多的例子：
```java
"Hello".indexOf("l"); // 2
"Hello".lastIndexOf("l"); // 3
"Hello".startsWith("He"); // true
"Hello".endsWith("lo"); // true
```
提取子串的例子：
```java
"Hello".substring(2); // "llo"
"Hello".substring(2, 4); "ll"
```
注意**索引号是从`0`开始的**。

### 去除首尾空白字符
使用`trim()`方法可以移除字符串首尾空白字符。空白字符包括空格，`\t`，`\r`，`\n`：
```java
"  \tHello\r\n ".trim(); // "Hello"
```
>[!NOTE]
>注意：`trim()`并没有改变字符串的内容，而是返回了一个新字符串。

另一个`strip()`方法也可以移除字符串首尾空白字符。它和`trim()`不同的是，类似中文的空格字符`\u3000`也会被移除：
```JAVA
"\u3000Hello\u3000".strip(); // "Hello"
" Hello ".stripLeading(); // "Hello "
" Hello ".stripTrailing(); // " Hello"
```
String还提供了`isEmpty()`和`isBlank()`来判断字符串是否为空和空白字符串：
```JAVA
"".isEmpty(); // true，因为字符串长度为0
"  ".isEmpty(); // false，因为字符串长度不为0
"  \n".isBlank(); // true，因为只包含空白字符
" Hello ".isBlank(); // false，因为包含非空白字符
```
### 格式化字符串
字符串提供了`formatted()`方法和`format()`静态方法，可以传入其他参数，替换占位符，然后生成新的字符串：
``` java
// String
public class Main {
    public static void main(String[] args) {
        String s = "Hi %s, your score is %d!";
        System.out.println(s.formatted("Alice", 80));
        System.out.println(String.format("Hi %s, your score is %.2f!", "Bob", 59.5));
    }
}
```
### 类型转换
要把任意基本类型或引用类型转换为字符串，可以使用静态方法`valueOf()`。这是一个重载方法，编译器会根据参数自动选择合适的方法：
```java
String.valueOf(123); // "123"
String.valueOf(45.67); // "45.67"
String.valueOf(true); // "true"
String.valueOf(new Object()); // 类似java.lang.Object@636be97c
```
要把字符串转换为其他类型，就需要根据情况。
```java
int n1 = Integer.parseInt("123"); // 123
int n2 = Integer.parseInt("ff", 16); // 按十六进制转换，255
boolean b1 = Boolean.parseBoolean("true"); // true
boolean b2 = Boolean.parseBoolean("FALSE"); // false
```
>[!CAUTION]
>要特别注意，`Integer`有个`getInteger(String)`方法，它不是将字符串转换为`int`，而是把该字符串对应的系统变量转换为`Integer`：

```JAVA
Integer.getInteger("java.version"); // 版本号，11
```
### 转换为char[]
`String`和`char[]`类型可以互相转换，方法是：
```java
char[] cs = "Hello".toCharArray(); // String -> char[]
String s = new String(cs); // char[] -> String
```
如果修改了`char[]`数组，`String`并不会改变：
这是因为通过`new String(char[])`创建新的`String`实例时，它并不会直接引用传入的`char[]`数组，而是会复制一份，所以，修改外部的`char[]`数组不会影响`String`实例内部的`char[]`数组，因为这是两个不同的数组。
从`String`的不变性设计可以看出，如果传入的对象有可能改变，我们需要复制而不是直接引用。

## StringBuilder
`StringBuilder`是可变对象，用来高效拼接字符串；
`StringBuilder`可以支持链式操作，实现链式操作的关键是返回实例本身；
`StringBuffer`是`StringBuilder`的线程安全版本，现在很少使用。
`Java`编译器对`String`做了特殊处理，使得我们可以直接用`+`拼接字符串。
考察下面的循环代码：
```java
String s = "";
for (int i = 0; i < 1000; i++) {
    s = s + "," + i;
}
```
虽然可以直接拼接字符串，但是，在循环中，每次循环都会创建新的字符串对象，然后扔掉旧的字符串。这样，绝大部分字符串都是临时对象，不但浪费内存，还会影响GC效率。
为了能高效拼接字符串，Java标准库提供了`StringBuilder`，它是一个可变对象，可以预分配缓冲区，这样，往`StringBuilder`中新增字符时，不会创建新的临时对象：
```java
StringBuilder sb = new StringBuilder(1024);
for (int i = 0; i < 1000; i++) {
    sb.append(',');
    sb.append(i);
}
String s = sb.toString();
```
`StringBuilder`还可以进行链式操作：
``` java
// 链式操作
public class Main {
    public static void main(String[] args) {
        var sb = new StringBuilder(1024);
        sb.append("Mr ")
          .append("Bob")
          .append("!")
          .insert(0, "Hello, ");
        System.out.println(sb.toString());
    }
}
```
如果我们查看`StringBuilder`的源码，可以发现，进行链式操作的关键是，定义的`append()`方法会返回`this`，这样，就可以不断调用自身的其他方法。
仿照`StringBuilder`，我们也可以设计支持链式操作的类。例如，一个可以不断增加的计数器：
```java
// 链式操作
public class Main {
    public static void main(String[] args) {
        Adder adder = new Adder();
        adder.add(3)
             .add(5)
             .inc()
             .add(10);
        System.out.println(adder.value());
    }
}

class Adder {
    private int sum = 0;

    public Adder add(int n) {
        sum += n;
        return this;
    }

    public Adder inc() {
        sum ++;
        return this;
    }

    public int value() {
        return sum;
    }
}
```
>[!CAUTION]
>注意：对于普通的字符串+操作，并不需要我们将其改写为`StringBuilder`，因为Java编译器在编译时就自动把多个连续的+操作编码为`StringConcatFactory`的操作。在运行期，`StringConcatFactory`会自动把字符串连接操作优化为数组复制或者`StringBuilder`操作。

你可能还听说过`StringBuffer`，这是Java早期的一个`StringBuilder`的线程安全版本，它通过同步来保证多个线程操作`StringBuffer`也是安全的，但是同步会带来执行速度的下降。
`StringBuilder`和`StringBuffer`接口完全相同，现在完全没有必要使用StringBuffer。

## 包装类型
Java核心库提供的包装类型可以把基本类型包装为`class；`
自动装箱和自动拆箱都是在编译期完成的（JDK>=1.5）；
装箱和拆箱会影响执行效率，且拆箱时可能发生`NullPointerException；`
包装类型的比较必须使用`equals()；`
整数和浮点数的包装类型都继承自`Number；`
包装类型提供了大量实用方法。

我们已经知道，Java的数据类型分两种：
基本类型：`byte`，`short`，`int`，`long`，`boolean`，`float`，`double`，`char`；
引用类型：所有`class`和`interface`类型。
引用类型可以赋值为`null`，表示空，但基本类型不能赋值为`null`：
那么，如何把一个基本类型视为对象（引用类型）？
比如，想要把`int`基本类型变成一个引用类型，我们可以定义一个`Integer`类，它只包含一个实例字段`int`，这样，`Integer`类就可以视为`int`的包装类（Wrapper Class）：
```java
public class Integer {
    private int value;

    public Integer(int value) {
        this.value = value;
    }

    public int intValue() {
        return this.value;
    }
}
```
定义好了`Integer`类，我们就可以把`int`和`Integer`互相转换：
```java
Integer n = null;
Integer n2 = new Integer(99);
int n3 = n2.intValue();
```
实际上，因为包装类型非常有用，Java核心库为每种基本类型都提供了对应的包装类型：

<!-- Failed to upload "image.png" -->

我们可以直接使用，并不需要自己去定义：
```java
// Integer:
public class Main {
    public static void main(String[] args) {
        int i = 100;
        // 通过new操作符创建Integer实例(不推荐使用,会有编译警告):
        Integer n1 = new Integer(i);
        // 通过静态方法valueOf(int)创建Integer实例:
        Integer n2 = Integer.valueOf(i);
        // 通过静态方法valueOf(String)创建Integer实例:
        Integer n3 = Integer.valueOf("100");
        System.out.println(n3.intValue());
    }
}
```
### Auto Boxing
因为`int`和`Integer`可以互相转换：
```java
int i = 100;
Integer n = Integer.valueOf(i);
int x = n.intValue();
```
所以，Java编译器可以帮助我们自动在`int`和`Integer`之间转型：
```java
Integer n = 100; // 编译器自动使用Integer.valueOf(int)
int x = n; // 编译器自动使用Integer.intValue()
```
这种直接把`int`变为`Integer`的赋值写法，称为自动装箱（Auto Boxing），反过来，把`Integer`变为`int`的赋值写法，称为自动拆箱（Auto Unboxing）。
>[!IMPORTANT]
>自动装箱和自动拆箱只发生在编译阶段，目的是为了少写代码。


### 不变类
所有的包装类型都是不变类。我们查看`Integer`的源码可知，它的核心代码如下：
```java
public final class Integer {
    private final int value;
}
```
因此，一旦创建了`Integer`对象，该对象就是不变的。
>[!IMPORTANT]
>对两个`Integer`实例进行比较要特别注意：绝对不能用`==`比较，因为`Integer`是引用类型，必须使用`equals()`比较

```java
// == or equals?
public class Main {
    public static void main(String[] args) {
        Integer x = 127;
        Integer y = 127;
        Integer m = 99999;
        Integer n = 99999;
        System.out.println("x == y: " + (x==y)); // true
        System.out.println("m == n: " + (m==n)); // false
        System.out.println("x.equals(y): " + x.equals(y)); // true
        System.out.println("m.equals(n): " + m.equals(n)); // true
    }
}
```
仔细观察结果的童鞋可以发现，`==`比较，较小的两个相同的`Integer`返回`true`，较大的两个相同的`Integer`返回`false`，这是因为`Integer`是不变类，编译器把`Integer x = 127;`自动变为`Integer x = Integer.valueOf(127);`，为了节省内存，`Integer.valueOf()`对于较小的数，始终返回相同的实例，因此，`==`比较“恰好”为`true`，但我们绝不能因为Java标准库的`Integer`内部有缓存优化就用`==`比较，必须用`equals()`方法比较两个`Integer`。
因为`Integer.valueOf()`可能始终返回同一个`Integer`实例，因此，在我们自己创建`Integer`的时候，以下两种方法：

- 方法1：`Integer n = new Integer(100);`
- 方法2：`Integer n = Integer.valueOf(100);`

方法2更好，因为方法1总是创建新的`Integer`实例，方法2把内部优化留给`Integer`的实现者去做，即使在当前版本没有优化，也有可能在下一个版本进行优化。
我们把能创建“新”对象的静态方法称为静态工厂方法。`Integer.valueOf()`就是静态工厂方法，它尽可能地返回缓存的实例以节省内存。
>[!TIP]
>创建新对象时，优先选用静态工厂方法而不是new操作符。

如果我们考察`Byte.valueOf()`方法的源码，可以看到，标准库返回的`Byte`实例全部是缓存实例，但调用者并不关心静态工厂方法以何种方式创建新实例还是直接返回缓存的实例。

### 进制转换
`Integer`类本身还提供了大量方法，例如，最常用的静态方法`parseInt()`可以把字符串解析成一个整数：
```java
int x1 = Integer.parseInt("100"); // 100
int x2 = Integer.parseInt("100", 16); // 256,因为按16进制解析
```
`Integer`还可以把整数格式化为指定进制的字符串：
```java
// Integer:
public class Main {
    public static void main(String[] args) {
        System.out.println(Integer.toString(100)); // "100",表示为10进制
        System.out.println(Integer.toString(100, 36)); // "2s",表示为36进制
        System.out.println(Integer.toHexString(100)); // "64",表示为16进制
        System.out.println(Integer.toOctalString(100)); // "144",表示为8进制
        System.out.println(Integer.toBinaryString(100)); // "1100100",表示为2进制
    }
}
```
注意：上述方法的输出都是`String`，在计算机内存中，只用二进制表示，不存在十进制或十六进制的表示方法。`int n = 100`在内存中总是以4字节的二进制表示：
┌──────┬──────┬──────┬──────┐
│ 00000000│00000000│00000000│01100100│
└──────┴──────┴──────┴──────┘

我们经常使用的`System.out.println(n);`是依靠核心库自动把整数格式化为10进制输出并显示在屏幕上，使用`Integer.toHexString(n)`则通过核心库自动把整数格式化为16进制。
这里我们注意到程序设计的一个重要原则：数据的存储和显示要分离。
Java的包装类型还定义了一些有用的静态变量
```java
// boolean只有两个值true/false，其包装类型只需要引用Boolean提供的静态字段:
Boolean t = Boolean.TRUE;
Boolean f = Boolean.FALSE;
// int可表示的最大/最小值:
int max = Integer.MAX_VALUE; // 2147483647
int min = Integer.MIN_VALUE; // -2147483648
// long类型占用的bit和byte数量:
int sizeOfLong = Long.SIZE; // 64 (bits)
int bytesOfLong = Long.BYTES; // 8 (bytes)
```
最后，所有的整数和浮点数的包装类型都继承自`Number`，因此，可以非常方便地直接通过包装类型获取各种基本类型：
```java
// 向上转型为Number:
Number num = new Integer(999);
// 获取byte, int, long, float, double:
byte b = num.byteValue();
int n = num.intValue();
long ln = num.longValue();
float f = num.floatValue();
double d = num.doubleValue();
```
### 处理无符号整型
在Java中，并没有无符号整型（Unsigned）的基本数据类型。`byte`、`short`、`int`和`long`都是带符号整型，最高位是符号位。而C语言则提供了CPU支持的全部数据类型，包括无符号整型。无符号整型和有符号整型的转换在Java中就需要借助包装类型的静态方法完成。
例如，byte是有符号整型，范围是`-128`~`+127`，但如果把byte看作无符号整型，它的范围就是`0~255`。我们把一个负的byte按无符号整型转换为`int`：
```java
// Byte
public class Main {
    public static void main(String[] args) {
        byte x = -1;
        byte y = 127;
        System.out.println(Byte.toUnsignedInt(x)); // 255
        System.out.println(Byte.toUnsignedInt(y)); // 127
    }
}
因为`byte`的`-1`的二进制表示是`11111111`，以无符号整型转换后的`int`就是`255`。
类似的，可以把一个`short`按`unsigned`转换为`int`，把一个`int`按`unsigned`转换为`long`。

## JavaBean
JavaBean是一种符合命名规范的`class`，它通过`getter`和`setter`来定义属性；
属性是一种通用的叫法，并非Java语法规定；
可以利用IDE快速生成`getter`和`setter`；
使用`Introspector.getBeanInfo()`可以获取属性列表。

## 枚举
>Java使用enum定义枚举类型，它被编译器编译为final class Xxx extends Enum { … }；
通过name()获取常量定义的字符串，注意不要使用toString()；
通过ordinal()返回常量定义的顺序（无实质意义）；
可以为enum编写构造方法、字段和方法
enum的构造方法要声明为private，字段强烈建议声明为final；
enum适合用在switch语句中。


**通过enum定义的枚举类，和其他的class有什么区别？**
答案是没有任何区别。`enum`定义的类型就是`class`，只不过它有以下几个特点：
- 定义的`enum`类型总是继承自`java.lang.Enum`，且无法被继承；
- 只能定义出`enum`的实例，而无法通过`new`操作符创建`enum`的实例；
- 定义的每个实例都是引用类型的唯一实例；
- 可以将`enum`类型用于`switch`语句。

例如，我们定义的Color枚举类：
```java
public enum Color {
    RED, GREEN, BLUE;
}
```
编译器编译出的class大概就像这样：
```java
public final class Color extends Enum { // 继承自Enum，标记为final class
    // 每个实例均为全局唯一:
    public static final Color RED = new Color();
    public static final Color GREEN = new Color();
    public static final Color BLUE = new Color();
    // private构造方法，确保外部无法调用new操作符:
    private Color() {}
}
```
**name()**
返回常量名，例如：
```java
String s = Weekday.SUN.name(); // "SUN"
```
**ordinal()**
返回定义的常量的顺序，从0开始计数，例如：
```java
int n = Weekday.MON.ordinal(); // 1
```
改变枚举常量定义的顺序就会导致`ordinal()`返回值发生变化。

## record类
从Java 14开始，引入了新的Record类。我们定义Record类时，使用关键字record。把上述Point类改写为Record类，代码如下：
```java
// Record
public class Main {
    public static void main(String[] args) {
        Point p = new Point(123, 456);
        System.out.println(p.x());
        System.out.println(p.y());
        System.out.println(p);
    }
}

record Point(int x, int y) {}
```
仔细观察`Point`的定义：
```java
record Point(int x, int y) {}
```
把上述定义改写为class，相当于以下代码：
```java
final class Point extends Record {
    private final int x;
    private final int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int x() {
        return this.x;
    }

    public int y() {
        return this.y;
    }

    public String toString() {
        return String.format("Point[x=%s, y=%s]", x, y);
    }

    public boolean equals(Object o) {
        ...
    }
    public int hashCode() {
        ...
    }
}
```
除了用`final`修饰`class`以及每个字段外，编译器还自动为我们创建了构造方法，和字段名同名的方法，以及覆写`toString()`、`equals()`和`hashCode()`方法。
换句话说，使用`record`关键字，可以一行写出一个不变类。
>[!CAUTION]
>和`enum`类似，我们自己不能直接从`Record`派生，只能通过`record`关键字由编译器实现继承。

### 构造方法
编译器默认按照`record`声明的变量顺序自动创建一个构造方法，并在方法内给字段赋值。那么问题来了，如果我们要检查参数，应该怎么办？
假设`Point`类的`x`、`y`不允许负数，我们就得给`Point`的构造方法加上检查逻辑：
```java
public record Point(int x, int y) {
    public Point {
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException();
        }
    }
}
```
注意到方法`public Point {...}`被称为`Compact Constructor`，它的目的是让我们编写检查逻辑，编译器最终生成的构造方法如下：
```java
public final class Point extends Record {
    public Point(int x, int y) {
        // 这是我们编写的Compact Constructor:
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException();
        }
        // 这是编译器继续生成的赋值代码:
        this.x = x;
        this.y = y;
    }
    ...
}
```
作为`record`的`Point`仍然可以添加静态方法。一种常用的静态方法是`of()`方法，用来创建`Point`：
```java
public record Point(int x, int y) {
    public static Point of() {
        return new Point(0, 0);
    }
    public static Point of(int x, int y) {
        return new Point(x, y);
    }
}
```
这样我们可以写出更简洁的代码：
```java
var z = Point.of();
var p = Point.of(123, 456);
```

## BigInteger
`BigInteger`用于表示任意大小的整数；
`BigInteger`是不变类，并且继承自`Number`；
将`BigInteger`转换成基本类型时可使用`longValueExact()`等方法保证结果准确。
如果我们使用的整数范围超过了`long`型怎么办？这个时候，就只能用软件来模拟一个大整数。`java.math.BigInteger`就是用来表示任意大小的整数。`BigInteger`内部用一个`int[]`数组来模拟一个非常大的整数：
```java
BigInteger bi = new BigInteger("1234567890");
System.out.println(bi.pow(5)); // 2867971860299718107233761438093672048294900000
```
对`BigInteger`做运算的时候，只能使用实例方法，例如，加法运算：
```java
BigInteger i1 = new BigInteger("1234567890");
BigInteger i2 = new BigInteger("12345678901234567890");
BigInteger sum = i1.add(i2); // 12345678902469135780
```
和`long`型整数运算比，`BigInteger`不会有范围限制，但缺点是速度比较慢。

也可以把`BigInteger`转换成`long`型：
```java
BigInteger i = new BigInteger("123456789000");
System.out.println(i.longValue()); // 123456789000
System.out.println(i.multiply(i).longValueExact()); // java.lang.ArithmeticException: BigInteger out of long range
```
### BigDecimal
和`BigInteger`类似，`BigDecimal`可以表示一个任意大小且精度完全准确的浮点数。
`BigDecimal`用于表示精确的小数，常用于财务计算；
比较`BigDecimal`的值是否相等，必须使用`compareTo()`而不能使用`equals()`。


## 常用工具类

SecureRandom
有伪随机数，就有真随机数。实际上真正的真随机数只能通过量子力学原理来获取，而我们想要的是一个不可预测的安全的随机数，`SecureRandom`就是用来创建安全的随机数的：
```java
SecureRandom sr = new SecureRandom();
System.out.println(sr.nextInt(100));
```
`SecureRandom`无法指定种子，它使用RNG（`random number generator`）算法。JDK的`SecureRandom`实际上有多种不同的底层实现，有的使用安全随机种子加上伪随机数算法来产生安全的随机数，有的使用真正的随机数生成器。实际使用的时候，可以优先获取高强度的安全随机数生成器，如果没有提供，再使用普通等级的安全随机数生成器：
```java
import java.util.Arrays;
import java.security.SecureRandom;
import java.security.NoSuchAlgorithmException;

public class Main {
    public static void main(String[] args) {
        SecureRandom sr = null;
        try {
            sr = SecureRandom.getInstanceStrong(); // 获取高强度安全随机数生成器
        } catch (NoSuchAlgorithmException e) {
            sr = new SecureRandom(); // 获取普通的安全随机数生成器
        }
        byte[] buffer = new byte[16];
        sr.nextBytes(buffer); // 用安全随机数填充buffer
        System.out.println(Arrays.toString(buffer));
    }
}
```
`SecureRandom`的安全性是通过操作系统提供的安全的随机种子来生成随机数。这个种子是通过CPU的热噪声、读写磁盘的字节、网络流量等各种随机事件产生的“熵”。
在密码学中，安全的随机数非常重要。如果使用不安全的伪随机数，所有加密体系都将被攻破。因此，时刻牢记必须使用`SecureRandom`来产生安全的随机数。