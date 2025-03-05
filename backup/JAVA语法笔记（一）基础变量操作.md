## 浮点数运算
在JAVA中，浮点数运算和整数运算相比，只能进行加减乘除这些数值计算，不能做位运算和移位运算。
在计算机中，浮点数虽然表示的范围大，但是，浮点数有个非常重要的特点，就是浮点数常常无法精确表示。
举个例子：
浮点数0.1在计算机中就无法精确表示，因为十进制的0.1换算成二进制是一个无限循环小数，很显然，无论使用float还是double，都只能存储一个0.1的近似值。但是，0.5这个浮点数又可以精确地表示。
因为浮点数常常无法精确表示，因此，浮点数运算会产生误差：
``` java
// 浮点数运算误差
public class Main {
    public static void main(String[] args) {
        double x = 1.0 / 10;
        double y = 1 - 9.0 / 10;
        // 观察x和y是否相等:
        System.out.println(x);
        System.out.println(y);
    }
}
```
运行结果：
![Image](https://github.com/user-attachments/assets/1c54bde0-31f5-47e5-b16d-981c908fdba7)

由于浮点数存在运算误差，所以比较两个浮点数是否相等常常会出现错误的结果。正确的比较方法是判断两个浮点数之差的绝对值是否小于一个很小的数：
``` java
// 比较x和y是否相等，先计算其差的绝对值:
double r = Math.abs(x - y);
// 再判断绝对值是否足够小:
if (r < 0.00001) {
    // 可以认为相等
} else {
    // 不相等
}
```
## 类型提升
如果参与运算的两个数其中一个是整型，那么整型可以自动提升到浮点型：
```  java
// 类型提升
public class Main {
    public static void main(String[] args) {
        int n = 5;
        double d = 1.2 + 24.0 / n; // 6.0
        System.out.println(d);
    }
}
```
需要特别注意，在一个复杂的四则运算中，两个整数的运算不会出现自动提升的情况。例如:
``` java
double d = 1.2 + 24 / 5; // 结果不是 6.0 而是 5.2
```
计算结果为5.2，原因是编译器计算24 / 5这个子表达式时，按两个整数进行运算，结果仍为整数4。
要修复这个计算结果，可以将24 / 5改为24.0 / 5。由于24.0是浮点数，因此，计算除法时自动将5提升为浮点数。
## 字符串连接
Java的编译器对字符串做了特殊照顾，可以使用+连接任意字符串和其他数据类型，这样极大地方便了字符串的处理。例如：
``` java
// 字符串连接
public class Main {
    public static void main(String[] args) {
        String s1 = "Hello";
        String s2 = "world";
        String s = s1 + " " + s2 + "!";
        System.out.println(s); // Hello world!
    }
}
```
如果用+连接字符串和其他数据类型，会将其他数据类型先自动转型为字符串，再连接：
``` java
// 字符串连接
public class Main {
    public static void main(String[] args) {
        int age = 25;
        String s = "age is " + age;
        System.out.println(s); // age is 25
    }
}
```
## 多行字符串
从Java 13开始，字符串可以用"""..."""表示多行字符串（Text Blocks）了。举个例子：
``` java
// 多行字符串
public class Main {
    public static void main(String[] args) {
        String s = """
                   SELECT * FROM
                     users
                   WHERE id > 100
                   ORDER BY name DESC
                   """;
        System.out.println(s);
    }
}
```

## 不可变特性
Java的字符串除了是一个引用类型外，还有个重要特点，就是字符串不可变。考察以下代码：
``` java
// 字符串不可变
public class Main {
    public static void main(String[] args) {
        String s = "hello";
        System.out.println(s); // 显示 hello
        s = "world";
        System.out.println(s); // 显示 world
    }
}
```
观察执行结果，难道字符串s变了吗？其实变的不是字符串，而是变量s的“指向”。
执行String s = "hello";时，JVM虚拟机先创建字符串"hello"，然后，把字符串变量s指向它：

![Image](https://github.com/user-attachments/assets/2338ebaa-a87d-4e9d-8795-7b2a7a63a81a)
紧接着，执行s = "world";时，JVM虚拟机先创建字符串"world"，然后，把字符串变量s指向它：

![Image](https://github.com/user-attachments/assets/a88ad82d-7df4-4dd2-b2b6-9febd88ca327)
原来的字符串"hello"还在，只是我们无法通过变量s访问它而已。因此，字符串的不可变是指字符串内容不可变。至于变量，可以一会指向字符串"hello"，一会指向字符串"world"。
``` java
// 字符串不可变
public class Main {
    public static void main(String[] args) {
        String s = "hello";
        String t = s;
        s = "world";
        System.out.println(t); // t是"hello"还是"world"?
    }
}
```
运行结果：
![Image](https://github.com/user-attachments/assets/e551d514-6e26-483b-8391-251a1a9d4b4c)

## 字符串数组
如果数组元素不是基本类型，而是一个引用类型，那么，修改数组元素会有哪些不同？
字符串是引用类型，因此我们先定义一个字符串数组：
``` java
String[] names = {
    "ABC", "XYZ", "zoo"
};
```
对于String[]类型的数组变量names，它实际上包含3个元素，但每个元素都指向某个字符串对象：
![Image](https://github.com/user-attachments/assets/6790fc8b-f4ff-4d11-a155-4f305a9fa80c)
对names[1]进行赋值，例如names[1] = "cat";，效果如下：
![Image](https://github.com/user-attachments/assets/8b02d5ba-51c2-43d1-8d07-ec72e568d1e6)
这里注意到原来names[1]指向的字符串"XYZ"并没有改变，仅仅是将names[1]的引用从指向"XYZ"改成了指向"cat"，其结果是字符串"XYZ"再也无法通过names[1]访问到了