## 前言
C++ 和 Java 都是面向对象的编程语言，但它们在面向对象编程（OOP）的实现上有一些关键区别。 C++ 和 Java 在面向对象方面的主要差异：

###  内存管理
   - **C++**：C++ 允许手动管理内存，程序员可以使用 `new` 和 `delete` 来分配和释放内存。这提供了更高的灵活性，但也增加了内存泄漏和悬空指针的风险。
   - **Java**：Java 使用自动垃圾回收机制（Garbage Collection），程序员不需要手动管理内存。垃圾回收器会自动回收不再使用的对象，减少了内存泄漏的风险，但可能会带来一定的性能开销。

###  多重继承
   - **C++**：C++ 支持多重继承，即一个类可以从多个基类继承。这增加了灵活性，但也可能导致复杂的继承关系和“菱形继承”问题。
   - **Java**：Java 不支持多重继承，一个类只能继承自一个父类。不过，Java 通过接口（`interface`）实现了类似多重继承的功能，一个类可以实现多个接口。

### 类和对象
   - **C++**：C++ 中的类可以定义在栈上或堆上，对象的生命周期可以由程序员显式控制。C++ 还支持友元函数和友元类，允许非成员函数或其他类访问私有成员。
   - **Java**：Java 中的对象只能在堆上创建，对象的生命周期由垃圾回收器管理。Java 没有友元函数或友元类的概念，访问控制严格依赖于 `public`、`protected`、`private` 等修饰符。

### 访问控制
   - **C++**：C++ 提供了 `public`、`protected` 和 `private` 三种访问控制级别。C++ 还支持友元机制，允许特定的函数或类访问私有成员。
   - **Java**：Java 也有 `public`、`protected`、`private` 和默认（包私有）四种访问控制级别。Java 没有友元机制，访问控制更加严格。

### 多态性
   - **C++**：C++ 通过虚函数（`virtual` 关键字）实现运行时多态。C++ 还支持运算符重载和函数重载。
   - **Java**：Java 通过方法重写（`@Override`）实现运行时多态。Java 不支持运算符重载，但支持方法重载。

###  接口与抽象类
   - **C++**：C++ 没有接口的概念，但可以通过纯虚函数（`virtual void func() = 0;`）实现类似接口的功能。C++ 的抽象类可以包含数据成员和具体方法的实现。
   - **Java**：Java 提供了 `interface` 关键字来定义接口，接口中的方法默认是抽象的（Java 8 以后可以在接口中定义默认方法）。Java 的抽象类可以包含抽象方法和具体方法。

### 异常处理
   - **C++**：C++ 的异常处理机制相对简单，支持 `try`、`catch` 和 `throw`。C++ 不强制要求处理异常，程序员可以选择是否捕获异常。
   - **Java**：Java 的异常处理机制更加严格，分为检查异常（checked exceptions）和未检查异常（unchecked exceptions）。检查异常必须在编译时处理，否则代码无法通过编译。

### 标准库
   - **C++**：C++ 标准库（STL）提供了丰富的容器和算法，支持泛型编程。C++ 的标准库相对底层，提供了更多的灵活性。
   - **Java**：Java 标准库（Java Class Library）非常庞大，提供了大量的预定义类和接口，涵盖了从数据结构到网络编程、图形用户界面等各个方面。Java 的标准库更加高层，使用起来更加方便。

### 指针与引用
   - **C++**：C++ 支持指针和引用，允许直接操作内存地址。指针是 C++ 中非常强大的工具，但也容易引发错误。
   - **Java**：Java 没有指针的概念，只有引用。Java 的引用类似于 C++ 的指针，但不能进行指针算术运算，也不能直接操作内存地址。

### 编译与运行
   - **C++**：C++ 是编译型语言，源代码被编译成机器码，直接在操作系统上运行。
   - **Java**：Java 是半编译半解释型语言，源代码被编译成字节码，然后在 JVM 上解释执行或即时编译（JIT）执行。

# 查缺知识点
## 可变参数
可变参数用类型...定义，可变参数相当于数组类型：‘
```java
class Group {
    private String[] names;

    public void setNames(String... names) {
        this.names = names;
    }
}
```
完全可以把可变参数改写为String[]类型：
```java
class Group {
    private String[] names;

    public void setNames(String[] names) {
        this.names = names;
    }
}
```
但是，调用方需要自己先构造String[]，比较麻烦。例如：
```java
 Group g = new Group();
g.setNames(new String[] {"Xiao Ming", "Xiao Hong", "Xiao Jun"}); // 传入1个String[]
```
另一个问题是，调用方可以传入null：
```java
 Group g = new Group();
g.setNames(null);
```
而可变参数可以保证无法传入null，因为传入0个参数时，接收到的实际值是一个空数组而不是null

## 多个构造方法
一个类可以可以定义多个构造方法，在通过new操作符调用的时候，编译器通过构造方法的参数数量、位置和类型自动区分：
```java
class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public Person(String name) {
        this.name = name;
        this.age = 12;
    }

    public Person() {
    }
}
```
如果调用new Person("Xiao Ming", 20);，会自动匹配到构造方法public Person(String, int)。
如果调用new Person("Xiao Ming");，会自动匹配到构造方法public Person(String)。
如果调用new Person();，会自动匹配到构造方法public Person()。
**一个构造方法可以调用其他构造方法，这样做的目的是便于代码复用。调用其他构造方法的语法是this(…)：**
```java
class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public Person(String name) {
        this(name, 18); // 调用另一个构造方法Person(String, int)
    }

    public Person() {
        this("Unnamed"); // 调用另一个构造方法Person(String)
    }
}
```
## 继承
**Java只允许一个class继承自一个类，因此，一个类有且仅有一个父类**。只有Object特殊，它没有父类。
![Image](https://github.com/user-attachments/assets/2ba8cb5d-8212-4a75-a50f-51435d436129)
### protected
继承有个特点，就是子类无法访问父类的private字段或者private方法。例如，Student类就无法访问Person类的name和age字段：
```java
class Person {
    private String name;
    private int age;
}
class Student extends Person {
    public String hello() {
        return "Hello, " + name; // 编译错误：无法访问name字段
    }
}
```
这使得继承的作用被削弱了。为了让子类可以访问父类的字段，我们需要把private改为protected。用protected修饰的字段可以被子类访问：
```java
class Person {
    protected String name;
    protected int age;
}

class Student extends Person {
    public String hello() {
        return "Hello, " + name; // OK!
    }
}
```
因此，protected关键字可以把字段和方法的访问权限控制在继承树内部，一个protected字段和方法可以被其子类，以及子类的子类所访问，后面我们还会详细讲解。
### super
super关键字表示父类（超类）。子类引用父类的字段时，可以用super.fieldName。例如：
```java
class Student extends Person {
    public String hello() {
        return "Hello, " + super.name;
    }
}
```
实际上，这里使用super.name，或者this.name，或者name，效果都是一样的。编译器会自动定位到父类的name字段。
但是，在某些时候，就必须使用super。我们来看一个例子：
```java
// super
public class Main {
    public static void main(String[] args) {
        Student s = new Student("Xiao Ming", 12, 89);
    }
}

class Person {
    protected String name;
    protected int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
}

class Student extends Person {
    protected int score;

    public Student(String name, int age, int score) {
        this.score = score;
    }
}
```
运行上面的代码，会得到一个编译错误，大意是在Student的构造方法中，无法调用Person的构造方法。
这是因为在Java中，任何class的构造方法，第一行语句必须是调用父类的构造方法。如果没有明确地调用父类的构造方法，编译器会帮我们自动加一句super();，所以，Student类的构造方法实际上是这样：
```java
class Student extends Person {
    protected int score;

    public Student(String name, int age, int score) {
        super(); // 自动调用父类的构造方法
        this.score = score;
    }
}
```
但是，Person类并没有无参数的构造方法，因此，编译失败。
解决方法是调用Person类存在的某个构造方法。例如：
```java
class Student extends Person {
    protected int score;

    public Student(String name, int age, int score) {
        super(name, age); // 调用父类的构造方法Person(String, int)
        this.score = score;
    }
}
```
这样就可以正常编译了！
因此我们得出结论：如果父类没有默认的构造方法，子类就必须显式调用super()并给出参数以便让编译器定位到父类的一个合适的构造方法。
这里还顺带引出了另一个问题：即子类不会继承任何父类的构造方法。子类默认的构造方法是编译器自动生成的，不是继承的。
## 阻止继承
正常情况下，只要某个class没有final修饰符，那么任何类都可以从该class继承。
从Java 15开始，允许使用sealed修饰class，并通过permits明确写出能够从该class继承的子类名称。
例如，定义一个Shape类：
```java
public sealed class Shape permits Rect, Circle, Triangle {
    ...
}
```
上述Shape类就是一个sealed类，它只允许指定的3个类继承它。如果写：
```java
public final class Rect extends Shape {...}
```
是没问题的，因为Rect出现在Shape的permits列表中。但是，如果定义一个Ellipse就会报错：
```java
public final class Ellipse extends Shape {...}
// Compile error: class is not allowed to extend sealed class: Shape
```
原因是Ellipse并未出现在Shape的permits列表中。这种sealed类主要用于一些框架，防止继承被滥用。
sealed类在Java 15中目前是预览状态，要启用它，必须使用参数--enable-preview和--source 15

## 向上转型
如果一个引用变量的类型是Student，那么它可以指向一个Student类型的实例：
```java
Student s = new Student();
```
如果一个引用类型的变量是Person，那么它可以指向一个Person类型的实例：
```java
Person p = new Person();
```
现在问题来了：如果Student是从Person继承下来的，那么，一个引用类型为Person的变量，能否指向Student类型的实例？
```java
Person p = new Student(); // ???
```
测试一下就可以发现，这种指向是允许的！
这是因为Student继承自Person，因此，它拥有Person的全部功能。Person类型的变量，如果指向Student类型的实例，对它进行操作，是没有问题的！
**这种把一个子类类型安全地变为父类类型的赋值，被称为向上转型（upcasting）。**
向上转型实际上是把一个子类型安全地变为更加抽象的父类型：
```java
Student s = new Student();
Person p = s; // upcasting, ok
Object o1 = p; // upcasting, ok
Object o2 = s; // upcasting, ok
```
注意到继承树是Student > Person > Object，所以，可以把Student类型转型为Person，或者更高层次的Object。
## 向下转型
和向上转型相反，如果把一个父类类型强制转型为子类类型，就是向下转型（downcasting）。例如：
```java
Person p1 = new Student(); // upcasting, ok
Person p2 = new Person();
Student s1 = (Student) p1; // ok
Student s2 = (Student) p2; // runtime error! ClassCastException!
```
如果测试上面的代码，可以发现：
Person类型p1实际指向Student实例，Person类型变量p2实际指向Person实例。在向下转型的时候，把p1转型为Student会成功，因为p1确实指向Student实例，把p2转型为Student会失败，因为p2的实际类型是Person，不能把父类变为子类，因为子类功能比父类多，多的功能无法凭空变出来。
因此，向下转型很可能会失败。失败的时候，Java虚拟机会报ClassCastException。
为了避免向下转型出错，Java提供了**instanceof操作符**，可以先判断一个实例究竟是不是某种类型：
```java
Person p = new Person();
System.out.println(p instanceof Person); // true
System.out.println(p instanceof Student); // false

Student s = new Student();
System.out.println(s instanceof Person); // true
System.out.println(s instanceof Student); // true

Student n = null;
System.out.println(n instanceof Student); // false
```
instanceof实际上判断一个变量所指向的实例是否是指定类型，或者这个类型的子类。如果一个引用变量为null，那么对任何instanceof的判断都为false。
利用instanceof，在向下转型前可以先判断：
```java
Person p = new Student();
if (p instanceof Student) {
    // 只有判断成功才会向下转型:
    Student s = (Student) p; // 一定会成功
}
```
从Java 14开始，判断instanceof后，可以直接转型为指定变量，避免再次强制转型。例如，对于以下代码：
```java
Object obj = "hello";
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.toUpperCase());
}
```
可以改写如下：
```java
// instanceof variable:
public class Main {
    public static void main(String[] args) {
        Object obj = "hello";
        if (obj instanceof String s) {
            // 可以直接使用变量s:
            System.out.println(s.toUpperCase());
        }
    }
}
```
这种使用instanceof的写法更加简洁。
## 多态
在继承关系中，子类如果定义了一个与父类方法签名完全相同的方法，被称为覆写（Override）。
Override和Overload不同的是，如果方法签名不同，就是Overload，Overload方法是一个新方法；如果方法签名相同，并且返回值也相同，就是Override。
> [!TIP]
>方法名相同，方法参数相同，但方法返回值不同，也是不同的方法。在Java程序中，出现这种情况，编译器会报错。

```java
class Person {
    public void run() { … }
}

class Student extends Person {
    // 不是Override，因为参数不同:
    public void run(String s) { … }
    // 不是Override，因为返回值不同:
    public int run() { … }
}
```
加上`@Override`可以让编译器帮助检查是否进行了正确的覆写。希望进行覆写，但是不小心写错了方法签名，编译器会报错。
```java
// override
public class Main {
    public static void main(String[] args) {
    }
}

class Person {
    public void run() {}
}

public class Student extends Person {
    @Override // Compile error!
    public void run(String s) {}
}
```
但是`@Override`不是必需的。
在上一节中，我们已经知道，引用变量的声明类型可能与其实际类型不符，例如：
``` java
Person p = new Student();
```
现在，我们考虑一种情况，如果子类覆写了父类的方法：
```java
// override
public class Main {
    public static void main(String[] args) {
        Person p = new Student();
        p.run(); // 应该打印Person.run还是Student.run?
    }
}

class Person {
    public void run() {
        System.out.println("Person.run");
    }
}

class Student extends Person {
    @Override
    public void run() {
        System.out.println("Student.run");
    }
}
```
那么，一个实际类型为`Student`，引用类型为`Person`的变量，调用其`run()`方法，调用的是`Person`还是`Student`的`run()`方法？
运行一下上面的代码就可以知道，实际上调用的方法是`Student`的`run()`方法。因此可得出结论：
>[!NOTE]
>Java的实例方法调用是基于运行时的实际类型的动态调用，而非变量的声明类型。这个非常重要的特性在面向对象编程中称之为多态。它的英文拼写非常复杂：Polymorphic。
多态是指，针对某个类型的方法调用，其真正执行的方法取决于运行时期实际类型的方法。例如：
```java
Person p = new Student();
p.run(); // 无法确定运行时究竟调用哪个run()方法
```
有同学会说，从上面的代码一看就明白，肯定调用的是`Student`的`run()`方法啊。
但是，假设我们编写这样一个方法：
```
public void runTwice(Person p) {
    p.run();
    p.run();
}
```
它传入的参数类型是`Person`，我们是无法知道传入的参数实际类型究竟是`Person`，还是`Student`，还是`Person`的其他子类例如`Teacher`，因此，也无法确定调用的是不是`Person`类定义的`run()`方法。
所以，**多态的特性就是，运行期才能动态决定调用的子类方法。对某个类型调用某个方法，执行的实际方法可能是某个子类的覆写方法。**
举个栗子：
```java
// Polymorphic
public class Main {
    public static void main(String[] args) {
        // 给一个有普通收入、工资收入和享受国务院特殊津贴的小伙伴算税:
        Income[] incomes = new Income[] {
            new Income(3000),
            new Salary(7500),
            new StateCouncilSpecialAllowance(15000)
        };
        System.out.println(totalTax(incomes));
    }

    public static double totalTax(Income... incomes) {
        double total = 0;
        for (Income income: incomes) {
            total = total + income.getTax();
        }
        return total;
    }
}

class Income {
    protected double income;

    public Income(double income) {
        this.income = income;
    }

    public double getTax() {
        return income * 0.1; // 税率10%
    }
}

class Salary extends Income {
    public Salary(double income) {
        super(income);
    }

    @Override
    public double getTax() {
        if (income <= 5000) {
            return 0;
        }
        return (income - 5000) * 0.2;
    }
}

class StateCouncilSpecialAllowance extends Income {
    public StateCouncilSpecialAllowance(double income) {
        super(income);
    }

    @Override
    public double getTax() {
        return 0;
    }
}
```
利用多态，`totalTax()`方法只需要和`Income`打交道，它完全不需要知道`Salary`和`StateCouncilSpecialAllowance`的存在，就可以正确计算出总的税。如果我们要新增一种稿费收入，只需要从`Income`派生，然后正确覆写`getTax()`方法就可以。把新的类型传入`totalTax()`，不需要修改任何代码。
>[!NOTE]
>多态具有一个非常强大的功能，就是允许添加更多类型的子类实现功能扩展，却不需要修改基于父类的代码。

## final关键字
继承可以允许子类覆写父类的方法。如果一个父类不允许子类对它的某个方法进行覆写，可以把该方法标记为`final`。用`final`修饰的方法不能被`Override`：
```java
class Person {
    protected String name;
    public final String hello() {
        return "Hello, " + name;
    }
}

class Student extends Person {
    // compile error: 不允许覆写
    @Override
    public String hello() {
    }
}
```
如果一个类不希望任何其他类继承自它，那么可以把这个类本身标记为`final`。用`final`修饰的类不能被继承：
```java
final class Person {
    protected String name;
}

// compile error: 不允许继承自Person
class Student extends Person {
}
```
对于一个类的实例字段，同样可以用`final`修饰。用`final`修饰的字段在初始化后不能被修改。例如：
```java
class Person {
    public final String name = "Unamed";
}
```
对`final`字段重新赋值会报错,但是可以在构造方法中初始化`final`字段:
```java
class Person {
    public final String name;
    public Person(String name) {
        this.name = name;
    }
}
```
## 抽象方法和抽象类
如果父类的方法本身不需要实现任何功能，仅仅是为了定义方法签名，目的是让子类去覆写它，那么，可以把父类的方法声明为抽象方法：
```java
abstract class Person {
    public abstract void run();
}
```
当我们定义了抽象类`Person`，以及具体的`Student`、`Teacher`子类的时候，我们可以通过抽象类`Person`类型去引用具体的子类的实例：
```java
Person s = new Student();
Person t = new Teacher();
```
这种引用抽象类的好处在于，我们对其进行方法调用，并不关心`Person`类型变量的具体子类型：
```java
// 不关心Person变量的具体子类型:
s.run();
t.run();
```
## 接口
在抽象类中，抽象方法本质上是定义接口规范：即规定高层类的接口，从而保证所有子类都有相同的接口实现，这样，多态就能发挥出威力。
如果一个抽象类没有字段，所有方法全部都是抽象方法：
```java
abstract class Person {
    public abstract void run();
    public abstract String getName();
}
```
就可以把该抽象类改写为接口：`interface`。
在Java中，使用`interface`可以声明一个接口：
``` java
interface Person {
    void run();
    String getName();
}
```
所谓```interface```，就是比抽象类还要抽象的纯抽象接口，因为它连字段都不能有。因为接口定义的所有方法默认都是```public abstract```的，所以这两个修饰符不需要写出来（写不写效果都一样）。
当一个具体的```class```去实现一个```interface```时，需要使用```implements```关键字。举个栗子：
```java
class Student implements Person {
    private String name;

    public Student(String name) {
        this.name = name;
    }

    @Override
    public void run() {
        System.out.println(this.name + " run");
    }

    @Override
    public String getName() {
        return this.name;
    }
}
```
>[!TIP]
>在Java中，一个类只能继承自另一个类，不能从多个类继承。但是，一个类可以实现多个`interface`

```java
class Student implements Person, Hello { // 实现了两个interface
    ...
}
```
### 接口继承
一个`interface`可以继承自另一个`interface`。`interface`继承自`interface`使用`extends`，它相当于扩展了接口的方法。
```java
interface Hello {
    void hello();
}

interface Person extends Hello {
    void run();
    String getName();
}
```
此时，`Person`接口继承自`Hello`接口，因此，`Person`接口现在实际上有3个抽象方法签名，其中一个来自继承的`Hello`接口。
### 继承关系
合理设计`interface`和`abstract class`的继承关系，可以充分复用代码。一般来说，公共逻辑适合放在`abstract class`中，具体逻辑放到各个子类，而接口层次代表抽象程度。可以参考Java的集合类定义的一组接口、抽象类以及具体子类的继承关系：

![Image](https://github.com/user-attachments/assets/2ec4bd4c-eb21-4e4e-8596-4552e6d00d20)
在使用的时候，实例化的对象永远只能是某个具体的子类，但总是通过接口去引用它，因为接口比抽象类更抽象：
### default方法
``` java
// interface
public class Main {
    public static void main(String[] args) {
        Person p = new Student("Xiao Ming");
        p.run();
    }
}

interface Person {
    String getName();
    default void run() {
        System.out.println(getName() + " run");
    }
}

class Student implements Person {
    private String name;

    public Student(String name) {
        this.name = name;
    }

    public String getName() {
        return this.name;
    }
}
```
实现类可以不必覆写`default`方法。`default`方法的目的是，当我们需要给接口新增一个方法时，会涉及到修改全部子类。如果新增的是`default`方法，那么子类就不必全部修改，只需要在需要覆写的地方去覆写新增方法。
`default`方法和抽象类的普通方法是有所不同的。因为`interface`没有字段，`default`方法无法访问字段，而抽象类的普通方法可以访问实例字段。
## static关键字
在一个`class`中定义的字段，我们称之为实例字段。实例字段的特点是，每个实例都有独立的字段，各个实例的同名字段互不影响。
还有一种字段，是用`static`修饰的字段，称为静态字段：`static field`。
实例字段在每个实例中都有自己的一个独立“空间”，但是静态字段只有一个共享“空间”
```java
// static field
public class Main {
    public static void main(String[] args) {
        Person ming = new Person("Xiao Ming", 12);
        Person hong = new Person("Xiao Hong", 15);
        ming.number = 88;
        System.out.println(hong.number);
        hong.number = 99;
        System.out.println(ming.number);
    }
}

class Person {
    public String name;
    public int age;

    public static int number;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
}
```
对于静态字段，无论修改哪个实例的静态字段，效果都是一样的：所有实例的静态字段都被修改了，原因是静态字段并不属于实例：
![Image](https://github.com/user-attachments/assets/4387f3f2-a0bf-493b-a730-6d66b370ebca)
虽然实例可以访问静态字段，但是它们指向的其实都是`Person class`的静态字段。所以，所有实例共享一个静态字段。
因此，不推荐用实例变量.静态字段去访问静态字段，因为在Java程序中，实例对象并没有静态字段。在代码中，实例对象能访问静态字段只是因为编译器可以根据实例类型自动转换为类名.静态字段来访问静态对象。
推荐用类名来访问静态字段。可以把静态字段理解为描述class本身的字段。对于上面的代码，更好的写法是：
```java
Person.number = 99;
System.out.println(Person.number);
```
### 静态方法
有静态字段，就有静态方法。用`static`修饰的方法称为静态方法。
调用实例方法必须通过一个实例变量，而调用静态方法则不需要实例变量，通过类名就可以调用。静态方法类似其它编程语言的函数。例如：
```java
// static method
public class Main {
    public static void main(String[] args) {
        Person.setNumber(99);
        System.out.println(Person.number);
    }
}

class Person {
    public static int number;

    public static void setNumber(int value) {
        number = value;
    }
}
```
因为静态方法属于`class`而不属于实例，因此，静态方法内部，无法访问`this`变量，也无法访问实例字段，它只能访问静态字段。
通过实例变量也可以调用静态方法，但这只是编译器自动帮我们把实例改写成类名而已。
通常情况下，通过实例变量访问静态字段和静态方法，会得到一个编译警告。
静态方法经常用于工具类。例如：
>Arrays.sort()
>Math.random()

>[!TIP]
>静态方法也经常用于辅助方法。注意到Java程序的入口main()也是静态方法。

### 接口的静态字段
因为`interface`是一个纯抽象类，所以它不能定义实例字段。但是，`interface`是可以有静态字段的，并且静态字段必须为`final`类型：
```java
public interface Person {
    public static final int MALE = 1;
    public static final int FEMALE = 2;
}
```
实际上，因为`interface`的字段只能是`public static final`类型，所以我们可以把这些修饰符都去掉，上述代码可以简写为：
```java
public interface Person {
    // 编译器会自动加上public static final:
    int MALE = 1;
    int FEMALE = 2;
}
```
编译器会自动把该字段变为`public static final`类型。


