--- 
title: 【C++】变量的作用域与内存管理
date: 2025-12-02T00:00:00+08:00
categories: ["侯捷面向对象"]
tags: ["内存管理", "c++", "堆", "栈"]
description: "C++内存管理涵盖栈、堆和全局/静态存储区。栈内存自动管理，用于局部变量；堆内存需手动分配释放，适合动态对象；全局/静态区存放全局和静态变量。对象生命周期因存储区而异，栈对象随作用域结束销毁，静态对象持续至程序结束，堆对象由程序员控制。"
cover: "/img/cpp.png"
headerImage: "/img/pink.png"
math: true
--- 

C++内存管理涉及栈、堆和全局/静态存储区。栈内存由编译器自动管理，用于局部变量；堆内存需手动分配释放，适用于动态对象；全局/静态区存放全局和静态变量。对象生命周期因存储区而异：栈对象随作用域结束而销毁，静态对象持续至程序结束，堆对象由程序员控制。 



## 堆,栈与内存管理

C++ 提供了多种内存管理机制，让程序员可以精细控制内存的分配和释放。

### Stack栈内存

- 由编译器自动分配和释放
- 存储局部变量、函数参数等
- 大小有限，通常几MB
- 分配和释放速度快

Stack是存在于某作用域(scope)的一块内存空间(memory space).例如当调用函数,函数本身就会形成一个stack用来放置它所接收的参数,以及返回地址.在函数本体(function body)内声明的任何变量,其所使用的内存块都取自该函数的stack.

### Heap堆内存

- 由程序员手动分配和释放
- 使用 `new`/`delete` 或 `malloc()`/`free()`
- 大小受系统可用内存限制
- 分配和释放速度较慢

Heap也叫system heap,是操作系统提供的一块global内存空间,程序可以通过动态分配(dynamic allocated)从其中获得区块.

> [!CAUTION]
>
> 程序中使用`new`/ `malloc()`分配的堆内存一定要手动释放:`delete`/`free()`

### **全局/静态存储区**

- 存储全局变量和静态变量
- 程序启动时分配，结束时释放
- 分为已初始化区和未初始化区

### Object的生命周期

在 C++ 中，对象的生命周期是指从对象被创建到被销毁的整个过程。

#### Stack objects栈对象:

- 在声明时构造
- 离开作用域时自动析构
- 分配在栈上
- 生命周期由作用域决定

下面的代码中的`c1`就是**stack objects**,其声明周期在作用域结束之际结束,这个作用域内的object,又被称为auto object,会被系统自动清理回收空间.

```cpp
class Complex{...};
{
    Complex c1(1,2);
}
```

#### Static object静态对象

- 全局变量：程序启动时构造，程序结束时析构
- 静态局部变量：第一次使用时构造，程序结束时析构
- 分配在全局/静态存储区
- 生命周期贯穿整个程序运行期

如果想让对象的声明周期突破作用域限制,可以使用`static`修饰符,**static local objects**的生命在其作用域结束之后依然存在,直到整个程序结束.

```cpp
class Complex{...};
{
    static Complex c2(1,2);
}
```

**global objects**全局变量 写在`main`函数的外面,可以将其视为一种特殊的static object,其作用域也是***整个程序***

```cpp
class Complex{...};
Complex c3(1,2);
int main()
{
    ...
}
```

#### heap objects堆对象

- 使用 `new` 时构造
- 必须显式调用 `delete` 析构
- 分配在堆上
- 生命周期由程序员控制(也可以说其生命在它被delete之际结束)

```cpp
class Complex{...};
{
    Complex* p=new Complex;
    ...
    delete p;
}
```

> [!CAUTION]
>
> 如果对于堆对象不进行delete,则在其作用域结束后,p所指的heap object仍然存在,但指针p的生命却结束了,作用域外再也看不到p,也就没机会delete p,造成内存泄漏.

### new与delete

**new关键字**先分配内存,在调用构造函数

```cpp
Complex* pc= new Complex(1,2);
```

如上new一个对象的流程,在编译器中会被转化为以下代码(不标准,但是思路类似):

```cpp
Complex *pc;//创建一个指向新对象的指针

void* mem=operator new(sizeof(Complex));//分配类大小的内存,new方法内部会调用C语言中的动态内存分配方法malloc(n);
pc=static_cast<Complex*>(mem); //转型
pc->Complex::Complex(1,2);     //调用构造函数
```

**delete关键字**先调用析构函数,再释放内存

```cpp
Complex*pc =new Complex(1,2);
...
delete pc;
```

如上delete一个对象在编译器中的会转化为:

```cpp
Complex::~Complex(pc);//析构函数
operator delete(pc);  //delete方法的内部会调用一个C语言中的方法free(pc)
```

### 动态分配得到的内存块

![image-20250511190610009](%E3%80%90C++%E3%80%91%E5%8F%98%E9%87%8F%E7%9A%84%E4%BD%9C%E7%94%A8%E5%9F%9F%E4%B8%8E%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86/image-20250511190610009.png)

> [!CAUTION]
> 对于动态内存分配对象而言**array new一定要搭配array delete使用,否则会导致内存泄漏**
>
> 同时建议:即使是不需要动态分配内存的无指针变量类,array new也要搭配array delete使用,这是一种安全规范的写法.

![image-20250511190850336](%E3%80%90C++%E3%80%91%E5%8F%98%E9%87%8F%E7%9A%84%E4%BD%9C%E7%94%A8%E5%9F%9F%E4%B8%8E%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86/image-20250511190850336.png)

## static 关键字

**static** 是 C++ 中一个多用途关键字，根据使用上下文有不同的含义。

`static`修饰的变量的作用域可能不同,但是统一存储在全局/静态存储区（非堆非栈）.

而`static`修饰的函数存储在代码段,与普通成员函数存储位置相同.

### 静态局部变量

在函数内部使用 `static` 修饰的变量：

```cpp
void counter() {
    static int count = 0;  // 只初始化一次
    count++;
    std::cout << count << std::endl;
}

int main() {
    counter();  // 输出1
    counter();  // 输出2
    counter();  // 输出3
}
```

特点：

- 只初始化一次（在第一次执行到声明处时）
- **生命周期持续到程序结束**
- **作用域仍限于函数内部**
- 默认初始化为零（如果没有显式初始化）

### 静态成员变量

```cpp
class MyClass {
public:
    static int sharedValue;  // 声明
};

int MyClass::sharedValue = 42;  // 定义和初始化

int main() {
    MyClass a, b;
    a.sharedValue = 10;
    std::cout << b.sharedValue;  // 输出10，因为所有实例共享
}
```

特点：

- 所有类实例共享同一个变量
- 必须在类外定义和初始化（C++17 起可以用 inline 在类内初始化）
- 可以通过类名或实例访问
- 没有 `this` 指针

### 静态成员函数

属于类而非实例的函数：

```cpp
class MyClass {
public:
    static void printMessage() {
        std::cout << "Static method" << std::endl;
        // 不能访问非静态成员
    }
};

int main() {
    MyClass::printMessage();  // 不需要实例
}
```

特点：

- 只能访问静态成员变量和其他静态成员函数
- 没有 `this` 指针
- 可以通过类名直接调用
- 不能是虚函数（因为与实例无关）

### 静态全局变量和函数

```cpp
// file1.cpp
static int hiddenVar = 42;  // 只在当前文件可见

static void hiddenFunc() {  // 只在当前文件可见
    std::cout << hiddenVar << std::endl;
}
```

### 静态与单例模式(Meyers Singleton)

**什么是单例模式?**

单例模式（Singleton Pattern）是一种创建型设计模式，它确保一个类**只有一个实例**存在，并提供一个**全局访问点**来获取这个实例。

传统单例模式:

```cpp
class A {
public:
    static A& getInstance() { return a; }
    void setup() {...}
private:
    A();
    A(const A& rhs);
    static A a;  // 静态成员变量
};

// 类外定义
A A::a;
```

静态单例模式:

```cpp
class A {
public:
    static A& getInstance() {
        static A a;  // 关键点：局部静态变量
        return a;
    }
    
    void setup() { /*...*/ }

private:
    A();  // 私有构造函数
    A(const A& rhs);  // 私有拷贝构造函数
    // 通常还会禁止赋值操作
    // A& operator=(const A& rhs);
};

// 使用方式
A::getInstance().setup();
```