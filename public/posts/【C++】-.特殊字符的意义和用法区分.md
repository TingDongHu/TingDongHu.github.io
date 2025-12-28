--- 
title: 【C++】::|->|.|*特殊字符的意义和用法区分
date: 2024-04-05T00:00:00+08:00
categories: ["侯捷面向对象"]
tags: ["语法", "c++", "指针", "智能指针", "引用", "作用域"]
description: "C++中四种运算符的核心区别：`::`用于访问命名空间、类或静态成员；`->`通过指针访问对象成员；`.`通过对象实例访问成员；`*`用于指针解引用。"
cover: "/img/cpp.png"
headerImage: "/img/pink.png"
math: true
--- 

C++中四种运算符的核心区别：`::`用于访问命名空间、类或静态成员；`->`通过指针访问对象成员；`.`通过对象实例访问成员；`*`用于指针解引用。 



在 C++ 中，`::`、`->` 、`.` 和`*`是四种不同的运算符，分别用于不同的上下文场景。它们的详细解释和用法对比：


## **1. 作用域解析运算符 `::`**

### **用途**

- 访问 **命名空间、类、结构体或枚举** 的成员
- 调用 **静态成员**（变量或函数）
- 区分同名的全局变量和局部变量

### **示例**

```cpp
#include <iostream>

namespace MyNamespace {
    int value = 42;
}

class MyClass {
public:
    static int staticValue;
    static void staticMethod() {
        std::cout << "Static method called!" << std::endl;
    }
};

int MyClass::staticValue = 100; // 静态成员变量定义

int main() {
    // 访问命名空间成员
    std::cout << MyNamespace::value << std::endl; // 输出: 42

    // 访问类的静态成员
    std::cout << MyClass::staticValue << std::endl; // 输出: 100
    MyClass::staticMethod(); // 输出: Static method called!

    return 0;
}
```

### **关键点**

- `::` **不依赖对象实例**，直接通过类名或命名空间访问成员。
- 常用于 **全局变量、静态成员、嵌套类** 等场景。

------

## **2. 成员访问运算符 `->`**

### **用途**

- 通过 **指针** 访问对象的成员（变量或函数）
- 等价于 `(*ptr).member`（先解引用，再用 `.` 访问）

### **示例**

```cpp
#include <iostream>

class MyClass {
public:
    int value = 10;
    void print() {
        std::cout << "Value: " << value << std::endl;
    }
};

int main() {
    MyClass obj;
    MyClass* ptr = &obj; // 指向对象的指针

    // 通过指针访问成员
    ptr->value = 20;     // 等价于 (*ptr).value = 20;
    ptr->print();        // 输出: Value: 20

    return 0;
}
```

### **关键点**

- `->` **只能用于指针**，不能用于普通对象。
- 在 **智能指针**（如 `std::shared_ptr`）和 **迭代器** 中也常用。

------

## **3. 成员访问运算符 `.`**

### **用途**

- 通过 **对象实例**（非指针）访问成员（变量或函数）
- 适用于 **结构体、类、联合体** 等

### **示例**

```cpp
#include <iostream>

class MyClass {
public:
    int value = 30;
    void print() {
        std::cout << "Value: " << value << std::endl;
    }
};

int main() {
    MyClass obj;

    // 通过对象访问成员
    obj.value = 40;
    obj.print(); // 输出: Value: 40

    return 0;
}
```

### **关键点**

- `.` **只能用于对象实例**，不能用于指针。
- 在 **结构体、类、联合体** 中通用。



## 4. 解引用/指针运算符 `*`

### **用途**

1. **指针声明**：表示变量是指针类型
2. **解引用**：获取指针指向的实际值
3. **乘法运算**：算术乘法（本文不讨论，因与其他运算符无关）

### **示例与详解**

#### **(1) 指针声明**

```cpp
int num = 42;
int* ptr = &num;  // ptr 是一个指向 int 的指针
```

- `int* ptr` 表示 `ptr` 存储的是内存地址，而非直接的值。

#### **(2) 解引用（获取指针指向的值）**

```cpp
int num = 42;
int* ptr = &num;

std::cout << *ptr;  // 输出: 42（通过 * 获取指针指向的实际值）
*ptr = 100;         // 修改指针指向的值
std::cout << num;   // 输出: 100
```

#### **(3) 与 `->` 的关系**

`ptr->member` 等价于 `(*ptr).member`：

```cpp
class MyClass {
public:
    int value;
};

MyClass obj;
MyClass* ptr = &obj;

ptr->value = 10;     // 使用 -> 访问成员
(*ptr).value = 10;   // 等价写法：先解引用，再用 . 访问
```

------

## **四者对比总结**

| 运算符 | 名称             | 适用场景                           | 示例                             |
| ------ | ---------------- | ---------------------------------- | -------------------------------- |
| `::`   | 作用域解析符     | 访问命名空间、类静态成员、全局变量 | `MyClass::staticMethod()`        |
| `->`   | 成员访问（指针） | 通过指针访问对象的成员             | `ptr->value = 10;`               |
| `.`    | 成员访问（对象） | 通过对象实例访问成员               | `obj.value = 10;`                |
| `*`    | 解引用/指针声明  | 1. 声明指针 2. 获取指针指向的值    | `int* ptr;` `std::cout << *ptr;` |

------

## **关键区别**

1. **`*` vs `->`**
   - `*` 是解引用运算符，单独使用时不涉及成员访问。
   - `->` 是组合操作：**先解引用，再访问成员**（即 `->` = `*` + `.`）。
2. **`::` 的特殊性**
   - 唯一不依赖对象/指针的运算符，直接通过类名或命名空间访问成员。
3. **何时用 `->` 何时用 `.`**
   - 对象用 `.`，指针用 `->`。
   - 智能指针（如 `std::shared_ptr`）也使用 `->`。

------

## **综合示例**

```cpp
#include <iostream>

namespace MyNamespace {
    int global = 50;
}

class MyClass {
public:
    static int staticVar;
    int instanceVar = 0;
};

int MyClass::staticVar = 100; // 静态成员定义

int main() {
    // 1. 作用域解析符 ::
    std::cout << MyNamespace::global << std::endl; // 输出: 50
    std::cout << MyClass::staticVar << std::endl;  // 输出: 100

    // 2. 指针与解引用 *
    MyClass obj;
    MyClass* ptr = &obj;
    *ptr = MyClass();          // 解引用并赋值新对象
    std::cout << (*ptr).instanceVar << std::endl; // 输出: 0

    // 3. -> 和 . 的对比
    ptr->instanceVar = 42;     // 指针用 ->
    obj.instanceVar = 10;      // 对象用 .
    std::cout << ptr->instanceVar << " " << obj.instanceVar; // 输出: 42 10

    return 0;
}
```

------

## **常见问题**

### **1. `::` 可以访问非静态成员吗？**

❌ **不可以**。`::` 只能访问 **静态成员、命名空间成员、嵌套类型**。

### **2. `*` 和 `&` 的关系？**

- `&` 取地址（如 `int* ptr = #`）
- `*` 解引用（如 `int val = *ptr;`）
- 二者互为逆操作。

### **4. 什么时候用 `->`，什么时候用 `.`？**

- 如果变量是 **指针**（如 `MyClass* ptr`），用 `->`。
- 如果变量是 **对象**（如 `MyClass obj`），用 `.`。

### **5. 为什么 `->` 不能用于对象？**

因为 `->` 的设计初衷是简化指针操作（`(*ptr).member` 的语法糖），而对象本身不需要解引用。

### **6. 智能指针怎么用？**

智能指针（如 `std::shared_ptr`）也使用 `->`：

```cpp
std::shared_ptr<MyClass> ptr = std::make_shared<MyClass>();
ptr->print(); // 正确
ptr.print();  // 错误！智能指针本身不是对象
```

### **7. 智能指针的 `->` 和普通指针有何不同？**

无本质区别，只是智能指针（如 `std::shared_ptr`）重载了 `->` 运算符，行为与原生指针一致：

```cpp
std::shared_ptr<MyClass> smartPtr = std::make_shared<MyClass>();
smartPtr->instanceVar = 30; // 用法相同
```

------

掌握这四种运算符的差异，能彻底避免 C++ 中的指针和成员访问错误！