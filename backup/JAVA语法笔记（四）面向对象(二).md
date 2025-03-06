## 作用域
在Java中，我们经常看到`public`、`protected`、`private`这些修饰符。在Java中，这些修饰符可以用来限定访问作用域。
定义为`public`的`class`、`interface`可以被其他任何类访问.
定义为`private`的`field`、`method`无法被其他类访问.
由于Java支持嵌套类，如果一个类内部还定义了嵌套类，那么，嵌套类拥有访问private的权限：
```java
// private
public class Main {
    public static void main(String[] args) {
        Inner i = new Inner();
        i.hi();
    }

    // private方法:
    private static void hello() {
        System.out.println("private hello!");
    }

    // 静态内部类:
    static class Inner {
        public void hi() {
            Main.hello();
        }
    }
}
```
定义在一个`class`内部的`class`称为嵌套类（`nested class`），Java支持好几种嵌套类。
`protected`作用于继承关系。定义为`protected`的字段和方法可以被子类访问，以及子类的子类。

### package
包作用域是指一个类允许访问同一个`package`的没有`public`、`private`修饰的`class`，以及没有`public`、`protected`、`private`修饰的字段和方法。
只要在同一个包，就可以访问`package`权限的`class`、field和`method`：
```java
package abc;

class Main {
    void foo() {
        // 可以访问package权限的类:
        Hello h = new Hello();
        // 可以调用package权限的方法:
        h.hi();
    }
}
```
## 内部类
有一种类，它被定义在另一个类的内部，所以称为内部类（Nested Class）。Java的内部类分为好几种，通常情况用得不多，但也需要了解它们是如何使用的。
Java的内部类可分为Inner Class、Anonymous Class和Static Nested Class三种；
Inner Class和Anonymous Class本质上是相同的，都必须依附于Outer Class的实例，即隐含地持有Outer.this实例，并拥有Outer Class的`private`访问权限；
Static Nested Class是独立类，但拥有Outer Class的`private`访问权限。
## Inner Class
如果一个类定义在另一个类的内部，这个类就是Inner Class：
```java
class Outer {
    class Inner {
        // 定义了一个Inner Class
    }
}
```
上述定义的`Outer`是一个普通类，而`Inner`是一个Inner Class，它与普通类有个最大的不同，就是Inner Class的实例不能单独存在，必须依附于一个Outer Class的实例。示例代码如下：
```java
// inner class
public class Main {
    public static void main(String[] args) {
        Outer outer = new Outer("Nested"); // 实例化一个Outer
        Outer.Inner inner = outer.new Inner(); // 实例化一个Inner
        inner.hello();
    }
}

class Outer {
    private String name;

    Outer(String name) {
        this.name = name;
    }

    class Inner {
        void hello() {
            System.out.println("Hello, " + Outer.this.name);
        }
    }
}
```
要实例化一个`Inner`，我们必须首先创建一个`Outer`的实例，然后，调用`Outer`实例的`new`来创建`Inner`实例
这是因为`Inner Class`除了有一个`this`指向它自己，还隐含地持有一个`Outer Class`实例，可以用`Outer.this`访问这个实例。所以，实例化一个`Inner Class`不能脱离`Outer`实例。
`Inner Class`和普通Class相比，除了能引用`Outer`实例外，还有一个额外的“特权”，就是可以修改Outer Class的`private`字段，因为Inner Class的作用域在Outer Class内部，所以能访问Outer Class的`private`字段和方法。

观察Java编译器编译后的`.class`文件可以发现，Outer类被编译为`Outer.class`，而Inner类被编译为`Outer$Inner.class`。

### Anonymous Class
还有一种定义Inner Class的方法，它不需要在Outer Class中明确地定义这个Class，而是在方法内部，通过匿名类（Anonymous Class）来定义。示例代码如下：
```java
// Anonymous Class
public class Main {
    public static void main(String[] args) {
        Outer outer = new Outer("Nested");
        outer.asyncHello();
    }
}

class Outer {
    private String name;

    Outer(String name) {
        this.name = name;
    }

    void asyncHello() {
        Runnable r = new Runnable() {
            @Override
            public void run() {
                System.out.println("Hello, " + Outer.this.name);
            }
        };
        new Thread(r).start();
    }
}
```
观察`asyncHello()`方法，我们在方法内部实例化了一个`Runnable`。`Runnable`本身是接口，接口是不能实例化的，所以这里实际上是定义了一个实现了`Runnable`接口的匿名类，并且通过`new`实例化该匿名类，然后转型为`Runnable`。在定义匿名类的时候就必须实例化它，定义匿名类的写法如下：
```java
Runnable r = new Runnable() {
    // 实现必要的抽象方法...
};
```
匿名类和Inner Class一样，可以访问Outer Class的`private`字段和方法。之所以我们要定义匿名类，是因为在这里我们通常不关心类名，比直接定义Inner Class可以少写很多代码。
观察Java编译器编译后的`.class`文件可以发现，Outer类被编译为`Outer.class`，而匿名类被编译为`Outer$1.class`。如果有多个匿名类，Java编译器会将每个匿名类依次命名为`Outer$1`、`Outer$2`、`Outer$3`……

### Static Nested Class
最后一种内部类和Inner Class类似，但是使用`static`修饰，称为静态内部类（Static Nested Class）：
```java
// Static Nested Class
public class Main {
    public static void main(String[] args) {
        Outer.StaticNested sn = new Outer.StaticNested();
        sn.hello();
    }
}

class Outer {
    private static String NAME = "OUTER";

    private String name;

    Outer(String name) {
        this.name = name;
    }

    static class StaticNested {
        void hello() {
            System.out.println("Hello, " + Outer.NAME);
        }
    }
}
```
用static修饰的内部类和Inner Class有很大的不同，它不再依附于Outer的实例，而是一个完全独立的类，因此无法引用`Outer.this`，但它可以访问Outer的`private`静态字段和静态方法。如果把StaticNested移到Outer之外，就失去了访问`private`的权限。

# classpath和jar包
JVM通过环境变量`classpath`决定搜索`class`的路径和顺序；
强烈建议不要设置系统环境变量`classpath`，建议始终通过`-cp`命令传入；
jar包本质上是`zip`格式，相当于目录，可以包含很多`.class`文件，方便下载和使用；
`MANIFEST.MF`文件可以提供jar包的信息，如`Main-Class`，这样可以直接运行jar包。
## classpath
`classpath`是JVM用到的一个环境变量，它用来指示JVM如何搜索`class`。
因为Java是编译型语言，源码文件是`.java`，而编译后的`.class`文件才是真正可以被JVM执行的字节码。因此，JVM需要知道，如果要加载一个`abc.xyz.Hello`的类，应该去哪搜索对应的`Hello.class`文件。
所以，`classpath`就是一组目录的集合，它设置的搜索路径与操作系统相关。例如，在Windows系统上，用`;`分隔，带空格的目录用`""`括起来，可能长这样：
> C:\work\project1\bin;C:\shared;"D:\My Documents\project1\bin"

在Linux系统上，用`:`分隔，可能长这样：
> /usr/shared:/usr/local/bin:/home/liaoxuefeng/bin

现在我们假设`classpath`是`.;C:\work\project1\bin;C:\shared`，当JVM在加载`abc.xyz.Hello`这个类时，会依次查找：
- <当前目录>\abc\xyz\Hello.class
- C:\work\project1\bin\abc\xyz\Hello.class
- C:\shared\abc\xyz\Hello.class
注意到`.`代表当前目录。如果JVM在某个路径下找到了对应的`class`文件，就不再往后继续搜索。如果所有路径下都没有找到，就报错。
`classpath`的设定方法有两种：
在系统环境变量中设置`classpath`环境变量，不推荐；
在启动JVM时设置`classpath`变量，推荐。
我们强烈**不推荐**在系统环境变量中设置`classpath`，那样会污染整个系统环境。在启动JVM时设置`classpath`才是推荐的做法。实际上就是给java命令传入`-classpath`参数：
> java -classpath .;C:\work\project1\bin;C:\shared abc.xyz.Hello

或者使用`-cp`的简写：
> java -cp .;C:\work\project1\bin;C:\shared abc.xyz.Hello

没有设置系统环境变量，也没有传入`-cp`参数，那么JVM默认的`classpath`为`.`，即当前目录：
>java abc.xyz.Hello

上述命令告诉JVM只在当前目录搜索`Hello.class`。
在IDE中运行Java程序，IDE自动传入的`-cp`参数是当前工程的`bin`目录和引入的jar包。
通常，我们在自己编写的`class`中，会引用Java核心库的`class`，例如，`String`、`ArrayList`等。这些class应该上哪去找？
有很多“如何设置classpath”的文章会告诉你把JVM自带的`rt.jar`放入`classpath`，但事实上，根本不需要告诉JVM如何去Java核心库查找class，JVM怎么可能笨到连自己的核心库在哪都不知道！
>[!WARNING]
>不要把任何Java核心库添加到classpath中！JVM根本不依赖classpath加载核心库！

更好的做法是，不要设置`classpath`.默认的当前目录`.`对于绝大多数情况都够用了。
假设我们有一个编译后的`Hello.class`，它的包名是`com.example`，当前目录是`C:\work`，那么，目录结构必须如下：
C:\work
└─ com
   └─ example
      └─ Hello.class
运行这个`Hello.class`必须在当前目录下使用如下命令：
> C:\work> java -cp . com.example.Hello

JVM根据`classpath`设置的`.`在当前目录下查找`com.example.Hello`，即实际搜索文件必须位于`com/example/Hello.class`。如果指定的`.class`文件不存在，或者目录结构和包名对不上，均会报错。

## jar包
如果有很多`.class`文件，散落在各层目录中，肯定不便于管理。如果能把目录打一个包，变成一个文件，就方便多了。
jar包就是用来干这个事的，它可以把`package`组织的目录层级，以及各个目录下的所有文件（包括`.class`文件和其他文件）都打成一个jar文件，这样一来，无论是备份，还是发给客户，就简单多了。
**jar包实际上就是一个zip格式的压缩文件，而jar包相当于目录。**如果我们要执行一个jar包的`class`，就可以把jar包放到`classpath`中：
> java -cp ./hello.jar abc.xyz.Hello

这样JVM会自动在`hello.jar`文件里去搜索某个类。
那么问题来了：如何创建jar包？

因为jar就是zip包，所以，直接在资源管理器中，找到正确的目录，点击右键，在弹出的快捷菜单中选择“发送到”，“压缩(zipped)文件夹”，就制作了一个zip文件。然后，把后缀从`.zip`改为`.jar`，一个jar包就创建成功。
假设编译输出的目录结构是这样：

package_sample
└─ bin
   ├─ hong
   │  └─ Person.class
   │  ming
   │  └─ Person.class
   └─ mr
      └─ jun
         └─ Arrays.class
这里需要特别注意的是，jar包里的第一层目录，不能是`bin`，而应该是`hong`、`ming`、`mr`。如果在Windows的资源管理器中看，应该长这样：

![Image](https://github.com/user-attachments/assets/b94c1ade-54d2-4997-88de-59661bba557f)
如果长这样：

![Image](https://github.com/user-attachments/assets/56c13b85-1d3a-4cc9-a1f6-fa3634f02e9f)
上面的`hello.zip`包含有`bin`目录，说明打包打得有问题，JVM仍然无法从jar包中查找正确的`class`，原因是`hong.Person`必须按`hong/Person.class`存放，而不是`bin/hong/Person.class`。
jar包还可以包含一个特殊的`/META-INF/MANIFEST.MF`文件，`MANIFEST.MF`是纯文本，可以指定`Main-Class`和其它信息。JVM会自动读取这个`MANIFEST.MF`文件，如果存在`Main-Class`，我们就不必在命令行指定启动的类名，而是用更方便的命令：
> java -jar hello.jar

在大型项目中，不可能手动编写`MANIFEST.MF`文件，再手动创建jar包。Java社区提供了大量的开源构建工具，例如[**Maven**](https://liaoxuefeng.com/books/java/maven/index.html)，可以非常方便地创建jar包。

# class版本
在Java开发中，许多童鞋经常被各种版本的JDK搞得晕头转向，本节我们就来详细讲解Java程序编译后的class文件版本问题。
高版本的JDK可编译输出低版本兼容的class文件，但需注意，低版本的JDK可能不存在高版本JDK添加的类和方法，导致运行时报错。
运行时使用哪个JDK版本，编译时就尽量使用同一版本的JDK编译源码。
我们通常说的Java 8，Java 11，Java 17，是指JDK的版本，也就是JVM的版本，更确切地说，就是`java.exe`这个程序的版本：
>$ java -version
java version "17" 2021-09-14 LTS

而每个版本的JVM，它能执行的class文件版本也不同。例如，Java 11对应的class文件版本是55，而Java 17对应的class文件版本是61。

如果用Java 11编译一个Java程序，输出的class文件版本默认就是55，这个class既可以在Java 11上运行，也可以在Java 17上运行，因为Java 17支持的class文件版本是61，表示“最多支持到版本61”。
如果用Java 17编译一个Java程序，输出的class文件版本默认就是61，它可以在Java 17、Java 18上运行，但不可能在Java 11上运行，因为Java 11支持的class版本最多到55。如果使用低于Java 17的JVM运行，会得到一个`UnsupportedClassVersionError`，错误信息类似：
> java.lang.UnsupportedClassVersionError: Xxx has been compiled by a more recent version of the Java Runtime...

只要看到`UnsupportedClassVersionError`就表示当前要加载的class文件版本超过了JVM的能力，必须使用更高版本的JVM才能运行。
打个比方，用Word 2013保存一个Word文件，这个文件也可以在Word 2016上打开。但反过来，用Word 2016保存一个Word文件，就无法使用Word 2013打开。
但是，且慢，用Word 2016也可以保存一个格式为Word 2013的文件，这样保存的Word文件就可以用低版本的Word 2013打开，但前提是保存时必须明确指定文件格式兼容Word 2013。
类似的，对应到JVM的class文件，我们也可以用Java 17编译一个Java程序，指定输出的class版本要兼容Java 11（即class版本55），这样编译生成的class文件就可以在Java >=11的环境中运行。
指定编译输出有两种方式，一种是在`javac`命令行中用参数`--release`设置：
> $ javac --release 11 Main.java

参数`--release 11`表示源码兼容Java 11，编译的class输出版本为Java 11兼容，即class版本55。
第二种方式是用参数`--source`指定源码版本，用参数`--target`指定输出class版本：
> $ javac --source 9 --target 11 Main.java

上述命令如果使用Java 17的JDK编译，它会把源码视为Java 9兼容版本，并输出class为Java 11兼容版本。注意`--release`参数和`--source --target`参数只能二选一，不能同时设置。
然而，指定版本如果低于当前的JDK版本，会有一些潜在的问题。例如，我们用Java 17编译`Hello.java`，参数设置`--source 9`和`--target 11`：
```java
public class Hello {
    public static void hello(String name) {
        System.out.println("hello".indent(4));
    }
}
```
用低于Java 11的JVM运行`Hello`会得到一个`LinkageError`，因为无法加载`Hello.class`文件，而用Java 11运行`Hello`会得到一个`NoSuchMethodError`，因为`String.indent()`方法是从Java 12才添加进来的，Java 11的`String`版本根本没有`indent()`方法。
>[!IMPORTANT]
>如果使用--release 11则会在编译时检查该方法是否在Java 11中存在。

因此，如果运行时的JVM版本是Java 11，则编译时也最好使用Java 11，而不是用高版本的JDK编译输出低版本的class。
如果使用`javac`编译时不指定任何版本参数，那么相当于使用`--release` 当前版本编译，即源码版本和输出版本均为当前版本。
在开发阶段，多个版本的JDK可以同时安装，当前使用的JDK版本可由`JAVA_HOME`环境变量切换。

### 源码版本
在编写源代码的时候，我们通常会预设一个源码的版本。在编译的时候，如果用`--source`或`--release`指定源码版本，则使用指定的源码版本检查语法。
例如，使用了`lambda`表达式的源码版本至少要为8才能编译，使用了`var`关键字的源码版本至少要为10才能编译，使用`switch`表达式的源码版本至少要为12才能编译，且12和13版本需要启用`--enable-preview`参数。

# 模块
从Java 9开始，JDK又引入了模块（Module）。
什么是模块？这要从Java 9之前的版本说起。
我们知道，`.class`文件是JVM看到的最小可执行文件，而一个大型程序需要编写很多Class，并生成一堆`.class`文件，很不便于管理，所以，jar文件就是class文件的容器。
在Java 9之前，一个大型Java程序会生成自己的jar文件，同时引用依赖的第三方jar文件，而JVM自带的Java标准库，实际上也是以jar文件形式存放的，这个文件叫`rt.jar`，一共有60多M。
如果是自己开发的程序，除了一个自己的`app.jar`以外，还需要一堆第三方的jar包，运行一个Java程序，一般来说，命令行写这样：
```bash
java -cp app.jar:a.jar:b.jar:c.jar com.liaoxuefeng.sample.Main
```
如果漏写了某个运行时需要用到的jar，那么在运行期极有可能抛出`ClassNotFoundException`。
所以，jar只是用于存放class的容器，它并不关心class之间的依赖。
从Java 9开始引入的模块，主要是为了解决“依赖”这个问题。如果`a.jar`必须依赖另一个`b.jar`才能运行，那我们应该给`a.jar`加点说明啥的，让程序在编译和运行的时候能自动定位到`b.jar`，这种自带“依赖关系”的class容器就是模块。
为了表明Java模块化的决心，从Java 9开始，原有的Java标准库已经由一个单一巨大的`rt.jar`分拆成了几十个模块，这些模块以`.jmod`扩展名标识，可以在`$JAVA_HOME/jmods`目录下找到它们：

- **java.base.jmod**
- **java.compiler.jmod**
- **java.datatransfer.jmod**
- **java.desktop.jmod**
- **...**

这些`.jmod`文件每一个都是一个模块，模块名就是文件名。例如：模块`java.base`对应的文件就是`java.base.jmod`。模块之间的依赖关系已经被写入到模块内的`module-info.class`文件了。所有的模块都直接或间接地依赖`java.base`模块，只有`java.base`模块不依赖任何模块，它可以被看作是“根模块”，好比所有的类都是从`Object`直接或间接继承而来。

把一堆class封装为jar仅仅是一个打包的过程，而把一堆class封装为模块则不但需要打包，还需要写入依赖关系，并且还可以包含二进制代码（通常是JNI扩展）。此外，模块支持多版本，即在同一个模块中可以为不同的JVM提供不同的版本。

### 编写模块
那么，我们应该如何编写模块呢？还是以具体的例子来说。首先，创建模块和原有的创建Java项目是完全一样的，以`oop-module`工程为例，它的目录结构如下：
oop-module
├── bin
├── build.sh
└── src
    ├── com
    │   └── itranswarp
    │       └── sample
    │           ├── Greeting.java
    │           └── Main.java
    └── module-info.java

其中，`bin`目录存放编译后的class文件，`src`目录存放源码，按包名的目录结构存放，仅仅在src目录下多了一个`module-info.java`这个文件，这就是模块的描述文件。在这个模块中，它长这样：
```java
module hello.world {
	requires java.base; // 可不写，任何模块都会自动引入java.base
	requires java.xml;
}
```
其中，`module`是关键字，后面的`hello.world`是模块的名称，它的命名规范与包一致。花括号的`requires xxx`;表示这个模块需要引用的其他模块名。除了`java.base`可以被自动引入外，这里我们引入了一个`java.xml`的模块。
当我们使用模块声明了依赖关系后，才能使用引入的模块。例如，`Main.java`代码如下：
``` java
package com.itranswarp.sample;

// 必须引入java.xml模块后才能使用其中的类:
import javax.xml.XMLConstants;

public class Main {
	public static void main(String[] args) {
		Greeting g = new Greeting();
		System.out.println(g.hello(XMLConstants.XML_NS_PREFIX));
	}
}
```
如果把`requires java.xml;`从`module-info.java`中去掉，编译将报错。可见，模块的重要作用就是声明依赖关系。
下面，我们用JDK提供的命令行工具来编译并创建模块。

首先，我们把工作目录切换到`oop-module`，在当前目录下编译所有的`.java`文件，并存放到`bin`目录下，命令如下：
```bash
$ javac -d bin src/module-info.java src/com/itranswarp/sample/*.java
```
如果编译成功，现在项目结构如下：
oop-module
├── bin
│   ├── com
│   │   └── itranswarp
│   │       └── sample
│   │           ├── Greeting.class
│   │           └── Main.class
│   └── module-info.class
└── src
    ├── com
    │   └── itranswarp
    │       └── sample
    │           ├── Greeting.java
    │           └── Main.java
    └── module-info.java
注意到`src`目录下的`module-info.java`被编译到`bin`目录下的`module-info.class`。

下一步，我们需要把bin目录下的所有class文件先打包成jar，在打包的时候，注意传入`--main-class`参数，让这个jar包能自己定位`main`方法所在的类：
```bash
$ jar --create --file hello.jar --main-class com.itranswarp.sample.Main -C bin .
```
现在我们就在当前目录下得到了`hello.jar`这个jar包，它和普通jar包并无区别，可以直接使用命令`java -jar hello.jar`来运行它。但是我们的目标是创建模块，所以，继续使用JDK自带的`jmod`命令把一个jar包转换成模块：
```bash
$ jmod create --class-path hello.jar hello.jmod
```
于是，在当前目录下我们又得到了`hello.jmod`这个模块文件，这就是最后打包出来的传说中的模块！

### 运行模块
要运行一个jar，我们使用`java -jar xxx.jar`命令。要运行一个模块，我们只需要指定模块名。试试：
```bash
$ java --module-path hello.jmod --module hello.world
```
结果是一个错误：
>Error occurred during initialization of boot layer
java.lang.module.FindException: JMOD format not supported at execution time: hello.jmod

原因是`.jmod`不能被放入`--module-path`中。换成`.jar`就没问题了：
```bash
$ java --module-path hello.jar --module hello.world
Hello, xml!
```
那我们辛辛苦苦创建的`hello.jmod`有什么用？答案是我们可以用它来打包JRE。
### 打包JRE
前面讲了，为了支持模块化，Java 9首先带头把自己的一个巨大无比的`rt.jar`拆成了几十个`.jmod`模块，原因就是，运行Java程序的时候，实际上我们用到的JDK模块，并没有那么多。不需要的模块，完全可以删除。
过去发布一个Java应用程序，要运行它，必须下载一个完整的JRE，再运行jar包。而完整的JRE块头很大，有100多M。怎么给JRE瘦身呢？
现在，JRE自身的标准库已经分拆成了模块，只需要带上程序用到的模块，其他的模块就可以被裁剪掉。怎么裁剪JRE呢？并不是说把系统安装的JRE给删掉部分模块，而是“复制”一份JRE，但只带上用到的模块。为此，JDK提供了`jlink`命令来干这件事。命令如下：
```bash
$ jlink --module-path hello.jmod --add-modules java.base,java.xml,hello.world --output jre/
```
我们在`--module-path`参数指定了我们自己的模块`hello.jmod`，然后，在`--add-modules`参数中指定了我们用到的3个模块`java.base`、`java.xml`和`hello.world`，用,分隔。最后，在`--output`参数指定输出目录。

现在，在当前目录下，我们可以找到jre目录，这是一个完整的并且带有我们自己`hello.jmod`模块的JRE。试试直接运行这个JRE：
```bash
$ jre/bin/java --module hello.world
Hello, xml!
```
要分发我们自己的Java应用程序，只需要把这个`jre`目录打个包给对方发过去，对方直接运行上述命令即可，既不用下载安装JDK，也不用知道如何配置我们自己的模块，极大地方便了分发和部署。

### 访问权限
前面我们讲过，Java的class访问权限分为`public`、`protected`、`private`和默认的包访问权限。引入模块后，这些访问权限的规则就要稍微做些调整。
确切地说，class的这些访问权限只在一个模块内有效，模块和模块之间，例如，a模块要访问b模块的某个class，必要条件是b模块明确地导出了可以访问的包。
举个例子：我们编写的模块`hello.world`用到了模块`java.xml`的一个类`javax.xml.XMLConstants`，我们之所以能直接使用这个类，是因为模块`java.xml`的`module-info.java`中声明了若干导出：
```java
module java.xml {
    exports java.xml;
    exports javax.xml.catalog;
    exports javax.xml.datatype;
    ...
}
```
只有它声明的导出的包，外部代码才被允许访问。换句话说，如果外部代码想要访问我们的`hello.world`模块中的`com.itranswarp.sample.Greeting`类，我们必须将其导出：
```java
module hello.world {
    exports com.itranswarp.sample;

    requires java.base;
	requires java.xml;
}
```
因此，模块进一步隔离了代码的访问权限。