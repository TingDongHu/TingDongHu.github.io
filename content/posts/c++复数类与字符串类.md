---
title: 【C++】复数类与字符串类
date: 2025-12-02T00:00:00+08:00
categories: ["侯捷面向对象"]
tags: ["语法", "c++", "面相对象"]
description: "本文以Complex类为例，讲解了C++程序的基本结构，包括头文件与实现文件的分离、防御性声明、命名空间的使用、inline函数的定义方式以及访问级别关键字的作用。"
cover: "/img/cpp.png"
headerImage: "/img/pink.png"
math: true
---

本文以Complex类为例，介绍了C++程序的基本结构，包括头文件与实现文件的分离、防御性声明、命名空间的使用，以及inline函数的定义方式与注意事项。 



## C++ programs 代码的基本形式(以Complex class为例)

### 头文件与类声明

在写C++项目时,一般将类声明和实现分为两部分存储,即`.h`和`.cpp`文件中.`.cpp`文件中要包含`#inlcude`他的声明头文件

> [!Warning]
>
> 在`.cpp`文件中,自己的头文件一般用引号,而引用标准库文件则用尖括号:
>
> ```c++
> #include<iostream.h>
> #inlcude'complex.h'
> ```

#### 头文件的防御性声明

在大型项目中,一个写好的类声明文件可能会被引用到程序的各个部分,而有一种规范安全的写法可以解决程序四处引用导致类重复声明的问题

示例:

```cpp
#ifndef _COMPLEX_
#define _COMPLEX_
...
#endif
```

#### namespace命名空间

namesapce主要的用途是免去每个函数之前都加一个类名,举个栗子:

```cpp
//使用命名空间
#include<iostram>
using namespace std;
int main()
{
    cin<<...;
    cout<<...;
    return 0;
}
//使用更加具体的命名空间
#include<iostram>
using namespace std::cout;
int main()
{
    std::cin<<...;
    cout<<...;
    return 0;
}
//不使用命名空间
#include<iostram>

int main()
{
    std::cin<<...;
    std::cout<<...;
    return 0;
}
```



#### inline方式书写类

对于某一个C++类,我们可以将其声明和定义直接写在一起(就是像C语音中一串写下来一样),示例:

```c++
class complex
{
public:
    complex(double r=0,double i=0)
        : re(r),im(i)
    {
        ....
    }
    complex& operator +=(const complex&);
    double real() const{return re;}
    double imag() const{retrun im;}
private:
    double re,im;
    friend complex&_doapl(complex*,const complex&);
};
```

像如上内容中,在类定义中直接将函数具体实现写在`{...}`中就是`inline`写法

> [!CAUTION]
>
> 使用`inline`方式书写的函数编译之后不一定就是真正的`inline`函数,该函数只会成为一个`inline`候选,编译器会基于其复杂程度最终确定其是否为真正的`inline`,就比如上述类中的两个`double`函数,其函数内容非常简单,编译器一般会将其编译为真正的`inline`.

除此之外也可以向如下写法在类外定义函数,编译器检测到`inline`关键字后会将该函数与声明编译到一块

```cpp
inline double
imag(const complex& x)
{
	return x.imag();
}
```

### access level(访问级别)关键字

在C++中，**访问级别（access level）**用于控制类成员（属性和方法）的可见性和可访问性，这是封装（encapsulation）的核心机制。C++提供了三个关键字来定义访问级别：`public`、`protected` 和 `private`。

**`public`（公有成员）**

- **作用**：在任何地方都可以直接访问。
- 使用场景
  - 类的接口（供外部调用的方法）。
  - 需要被全局访问的常量或工具函数。

**`private`（私有成员）**

- **作用**：仅在**类内部**或**友元（friend）**中可访问，外部代码无法直接访问。
- **设计目的**：隐藏实现细节，防止外部意外修改数据。

**`protected`（保护成员）**

- **作用**：在类内部和**派生类（子类）**中可访问，外部代码不可访问。
- **设计目的**：支持继承时的成员共享，同时限制外部访问。

| 关键字      | 类内部 | 子类 | 外部代码 | 友元 |
| ----------- | ------ | ---- | -------- | ---- |
| `public`    | ✔      | ✔    | ✔        | ✔    |
| `protected` | ✔      | ✔    | ✖        | ✔    |
| `private`   | ✔      | ✖    | ✖        | ✔    |

1. **默认访问级别**：
   - **class**：成员默认是 `private`。
   - **struct**：成员默认是 `public`（设计初衷是兼容C的数据结构）。
2. **友元（friend）**：
   - 通过 `friend` 关键字，可以允许特定函数或类突破访问限制（慎用，破坏封装性）。
3. **继承时的访问控制**：
   - 派生类继承时可通过 `public`、`protected`、`private` 继承改变基类成员的访问权限（例如：`class Derived : private Base`）。

### 构造函数与析构函数

在C++中，**构造函数（Constructor）**和**析构函数（Destructor）**是类的特殊成员函数，分别用于对象的**初始化**和**清理**。它们是面向对象编程中资源管理的关键机制。

还是以之前的代码为例子:

```cpp
complex(double r = 0, double i = 0) : re(r), im(i) { ... }
```

- 使用**初始化列表**（`: re(r), im(i)`）直接初始化成员变量（比在函数体内赋值更高效）。

- 是**参数化构造函数**，同时也是一个**默认构造函数**（因为所有参数都有默认值 `0`）。

> [!TIP]
>
> 由于我这里写的类是不带指针的,不需要显性的定义析构函数(自带的就够用),带指针的类需要手动释放资源.

### 参数传递与返回值

#### const member function(常量成员函数)

`const`是C++中一个非常重要的关键字，它用于定义常量、保护数据不被修改，并在编译时强制执行不变性规则。

还是以上面的示例:
```cpp
double real() const{return re;}
double imag() const{retrun im;}
```

这样写的意义在于保证程序无论在哪种情况下都能正常使用

比如下面的两种调用方式:
```cpp
//方式一
{
    complex c1(2,1);
    cout<<c1.real();
    cout<<c1.imag();
}
//方式二
{
    const complex c1(2,1);
    cout<<c1.real();
    cout<<c1.imag();
}
```

如果在类的定义中我们没有将const写在函数内容之前,那么方法二就会报错.

#### 函数传参:pass by value与pass by reference(to const)

在C++中，函数参数传递主要有两种方式：**值传递**和**引用传递**。如下示例:

```cpp
void increment1(int x) {
    x++;  // 只修改局部副本
}
// 普通引用传递（可修改原始数据）
void increment2(int& x) {
    x++;  // 修改原始数据
}

// const引用传递（不可修改原始数据）
void printLargeObject(const BigObject& obj) {
    // 只能读取obj，不能修改
}
```

值传递 (Pass by Value):将实参的**副本**传递给函数，函数内对参数的修改不会影响原始数据。

- 优点：
  - 简单直接
  - 不会意外修改原始数据
  - 线程安全（每个线程有自己的副本）
- 缺点：
  - 对于大型对象（如类、结构体），复制开销大
  - 无法通过参数返回额外信息

引用传递 (Pass by Reference to const):将实参的**别名**传递给函数，避免了复制开销。`const`引用还能保证原始数据不被修改。

- 优点：
  - 无复制开销，性能高
  - 可以修改原始数据（非`const`引用）
  - `const`引用既保证效率又保证安全性
- 缺点：
  - 非`const`引用可能意外修改原始数据
  - 比值传递稍复杂

|         特性         |      值传递      |        引用传递         |  const引用传递   |
| :------------------: | :--------------: | :---------------------: | :--------------: |
|     **复制开销**     |  有（完整复制）  |     无（传递引用）      |  无（传递引用）  |
| **能否修改原始数据** |       不能       |           能            |       不能       |
|     **线程安全**     | 安全（独立副本） |         不安全          |       安全       |
|     **典型用途**     | 小型简单数据类型 | 需要修改的参数/输出参数 | **大型只读对象** |

#### 返回值传递:retrun by value与return by reference(to const)

特征与用法与上面参数传递部分基本一样,这里就不再赘述,需要注意的点是,**返回引用需要保证该值的生命周期**,如果无法确保生命周期可能引起灾难性的bug

```cpp
// 绝对不要这样写！
const std::string& badIdea() {
    std::string local = "temp";
    return local; // 灾难！
}
```

#### friend友元

友元是C++中一种打破封装性的特殊机制，它允许特定的**非成员函数**或**其他类**访问当前类的私有(private)和保护(protected)成员。

```cpp
class Engine;  // 前向声明

class Car {
private:
    int speed;
    friend class Engine;  // 允许Engine访问私有成员
};

class Engine {
public:
    void accelerate(Car& car) {
        car.speed += 10;  // 可以访问Car的私有成员
    }
};
```

> [!tip]
>
> 有一个特殊写法可以理解为:相同class的各个objects互为friends(友元)
>
> ps: 上面的解释是侯捷老师上课的时候给出的,查阅了的一些资料发现好像并不是这样的.

如下示例:
```cpp
class complex {
public:
    complex(double r=0, double i=0) : re(r), im(i) { }
    
    double func(const complex& param) { 
        return param.re + param.im; 
    }
    
private:
    double re, im;
};

int main() {
    complex c1(2,1);
    complex c2;
    c2.func(c1);
}
```

此处在对象`c2`中直接访问了`c1`的私有成员,这是C++访问控制机制的一个重要特性。

> C++的访问控制（`private/protected/public`）是**类级别**的，而不是对象级别的。这意味着：
>
> - **类的成员函数**可以访问**该类所有对象**的私有成员（包括通过参数传入的其他对象）。
> - 这种设计是为了让同类对象之间能高效协作，同时对外部代码保持封装性。

**对比**

|             场景             |      能否访问私有成员？       |                             原因                             |
| :--------------------------: | :---------------------------: | :----------------------------------------------------------: |
| **同类成员函数访问其他对象** |            ✅ 可以             | 访问权限基于类（`complex::func`可以访问任何`complex`对象的私有成员） |
|       **外部普通函数**       |            ❌ 不能             |                       非成员函数无特权                       |
|         **友元函数**         |            ✅ 可以             |                         被类显式授权                         |
|      **派生类成员函数**      | ❌ 不能（除非是protected成员） |                  派生类不能访问基类私有成员                  |

### 操作符重载

#### 操作成员函数

如下代码示例:
```cpp
inline complex& __doapl(complex* ths, const complex& r) {
    ths->re += r.re;  // 实部相加
    ths->im += r.im;  // 虚部相加
    return *ths;      // 返回修改后的对象
}
inline complex& complex::operator+=(const complex& r) {
    return __doapl(this, r);  // 委托给辅助函数
}
complex a(1,2), b(3,4);
a += b;  // 比 a.add(b) 更符合数学直觉
```

> [!caution]
>
> 所以成员函数一定带着一个隐藏的参数`this`,但是不可以在程序中写出来,否则会报错.

所以其实在编辑器看来我们的运算符重载函数为:

```cpp
inline complex& complex::operator+=(this,const complex& r) {
    return __doapl(this, r);  // 委托给辅助函数
}
```

> [!caution]
>
> C++允许重载大多数运算符（如 `+`, `-`, `<<`, `==`），但不能重载以下运算符：
>
> ```cpp
> .  .*  ::  ?:  sizeof  #  ##
> ```

#### 操作非成员函数与临时对象

```cpp
inline complex operator + (const complex& x, const complex& y) {
    return complex(real(x) + real(y), imag(x) + imag(y));
}
inline complex operator + (const complex& x, double y) {
    return complex(real(x) + y, imag(x));
}
inline complex operator + (double x, const complex& y) {
    return complex(x + real(y), imag(y));
}
```

如上代码可以同时处理多种复数加法运算的情况

> [!warning]
>
> 上面的函数绝对不可以return by reference,因为,他们返回的必定是local object

`typename( .. , ..)`的写法为定义一个临时对象.

## String class

### Big Three

相比上面的复数类,下面重写的String class需要特别注意三个特殊函数 `拷贝复制`,`拷贝构造`,`析构函数`

```cpp
class String    
{
public:
    String(const char* cstr=0);
    String(const String& str);
    String& operator=(const String& str);
    ~String();
    char* get_c_str() const{return m_data;}
private:
    char* m_data;
};
```

#### ctor和dtor(构造函数 和 析构函数)

class中如果有指针,那么该类的变量中多半使用了动态内存分配,要再析构函数中将该内存释放掉,否则会造成**内存泄漏**

```cpp
inline
String::string(const char* cstr=0)
{
    if(cstr){
        m_data=new char[strlen(cstr)+1];
        strcpy(m_data,cstr);
    }
    else{//未指定初始值的情况
        m_data=new char[1];
        *m_data='\0';
	}
}

inline
String::~String()
{
    delete[] m_data;
}
```

#### copy ctor和copy op= (拷贝构造和拷贝赋值)

> [!caution]
>
> class with  pointer members类中存在指针变量成员,则必须为其书写特殊的`copy ctor`和`copy op =`

**浅拷贝和深拷贝**

如果指针类的变量直接使用默认的copy,则会造成两个变量同时指向一个地址(其实就是别名),而且原本内存泄漏掉

![image-20250511153941283](c++复数类与字符串类/%E3%80%90C++%E3%80%91%E5%A4%8D%E6%95%B0%E7%B1%BB%E4%B8%8E%E5%AD%97%E7%AC%A6%E4%B8%B2%E7%B1%BB/image-20250511153941283.png)

```cpp
inline
String::String(const String& str)
{
    m_data = new char[ strlen(str.m_data)+1];//同类型的对象可以直接取另一个的object的private data.
    strcpy(m_data,str.m_data);
}
//下面为使用场景
{
    String s1("Hello");
    String s2(s1);
    String s2=s1;
}
```

```cpp
inline
String& String::operator=(const String& str)
{
    if(this==&str)//检测自我赋值,是十分有必要的,因为后续的逻辑会清除原本self的地址空间
        return *this;
    delete[] m_data;
    m_data = new char[ strlen(str.m_data)+1];
    strcpy(m_data,str.m_data);
    return *this;
}
{
    String s1("Hello");
    String s2(s1);
   	s2=s1;
}
```

### 输出cout

全局函数,在`cout`的定义部分重载`<<`符号,如下图所示:
![image-20250511223901096](%E3%80%90C++%E3%80%91%E5%A4%8D%E6%95%B0%E7%B1%BB%E4%B8%8E%E5%AD%97%E7%AC%A6%E4%B8%B2%E7%B1%BB/image-20250511223901096.png)

```cpp
#inlcude<istream.h>
ostream& operator<<(ostream& os,const String& str)
{
    os<<str.get_c_str();
    return os;//返回os类型,用于符合用户书写习惯在后面跟其他的东西.
}
{
    String s1("hello ");
    cout<<s1;
    cout<<s1<<endl;
}
```

## class template类模板

```cpp
template<typename T>
class complex
{
public:
    complex(T r=0;T i=0)
        :re(r),im(i)
    {}
    complex& operator +=(const complex&);
    T real()const{return re;}
    T imag()const{return im;}
private:
    T re,im;
    friend complex& _doapl(complex*,const complex&);
};
\\使用模板创建类
{
    complex<double>c1(2.5,1.5);
    complex<int>c2(2,6);
    ...
}
```

类模板可以使***代码膨胀***,一次书写,多次使用.

## function template函数模板

```cpp
template<class T>
inline
const T& min(const T& a,const T& b)
{
    return b<a?b:a;
}

//某一个类定义
class stone
{
public:
    stone(int w,int h,int we)
        : _w(w), _h(h), _weight(we)
        {}
    bool operator< (const stone& rhs) const
    {
        return _weight<rhs._weight;
    }
private:
    int _w, _h, _weight;
}

//具体使用
{
    stone r1(2,3),r2(3,3),r3;
    r3=min(r1,r2);
}
```

对于上面的函数模板使用,编译器首先会对function template进行参数推导（Argument Deduction）,参数推导的结果是`T`为`stone`,于是调用`stone::operator<`,如果该类没有实现`<`的重载则会报错.