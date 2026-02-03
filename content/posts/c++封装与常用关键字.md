---
title: "【C++】封装与常用关键字"
date: 2025-12-15T12:00:00+08:00  
categories: ["侯捷面向对象"]
tags: ["面相对象", "c++", "封装", "内存管理"]
description: "组合（Composition）、继承（Inheritance）和多态（Polymorphism）是C++中面向对象编程（OOP）的三大支柱。本文从内存管理的角度深入挖掘了这三大支柱的细节。"
cover: "/img/cpp.png"
headerImage: "/img/pink.png"
math: true
---

## 基本概念

### 封装的概念

**封装（Encapsulation）** 是面向对象编程（OOP）的三大特性之一，简单来说，封装就是将**数据（属性）**和**操作数据的函数（行为）**绑定在一起，形成一个名为“类（Class）”的单位，并对外部隐藏内部实现的细节。

封装的核心思想是**“对外提供接口，对内隐藏实现”**。它的好处包括：

- **安全性（数据隐藏）：** 防止外部代码随意修改对象内部的关键数据，避免程序进入非法状态。
- **易维护性：** 如果内部逻辑需要修改，只要外部接口（函数名、参数）不变，调用者的代码就不需要改动。
- **模块化：** 代码结构更清晰，每个类负责自己的逻辑。

### 访问修饰符

C++ 通过三个关键字来控制成员的访问权限。它们是实现封装的关键工具：

| **关键字**      | **访问权限说明**                                             |
| --------------- | ------------------------------------------------------------ |
| **`public`**    | **公有**：类内部和类外部都可以直接访问。通常用于存放成员函数。 |
| **`private`**   | **私有**：**（默认）** 只有类内部的函数可以访问，外部无法直接访问。通常用于存放成员变量。 |
| **`protected`** | **保护**：类内部及**派生类（子类）**可以访问，但类外部无法直接访问。 |

**`this` 指针**：是一个指向当前对象实例的指针。常用于在成员函数中区分“成员变量”和“同名参数”。

`class` 的成员默认是 `private`，而 `struct` 的成员默认是 `public`。通常建议用 `class` 实现复杂的逻辑封装。

**`friend`（友元）**：如果你希望某个外部函数或类能访问当前类的 `private` 成员，可以用 `friend` 声明。它会打破封装，所以要谨慎使用。

> [!note]
>
> `friend`：破坏封装还是增强封装？
>
> `friend` 允许特定的类或函数访问私有成员。
>
> - **视角一**：它破坏了封装，因为它打开了后门。
> - **视角二（更深层）**：它**增强了封装**。通过将紧密耦合的工具类设为友元，可以避免为了让外部访问而被迫将成员声明为 `public`，从而将权限精确控制在最小范围内。

**`const`**：在封装中，常用于修饰不修改成员变量的函数（如 `getBalance() const`），这被称为**常成员函数**，能提高代码的安全性和可读性。

### Example

来一个银行账户的栗子：我们不希望别人直接修改我们的余额（`balance`），而是必须通过存款或取款函数来操作。

```cpp
#include <iostream>
#include <string>

class BankAccount {
private:
    // 私有成员：外部无法直接访问
    double balance;
    std::string ownerName;

public:
    // 构造函数：初始化数据
    BankAccount(std::string name, double initialBalance) {
        ownerName = name;
        if (initialBalance >= 0) {
            balance = initialBalance;
        } else {
            balance = 0;
        }
    }

    // 公有成员函数：提供受控的访问接口（Getter）
    double getBalance() const {
        return balance;
    }

    // 公有成员函数：存款（Setter/Action）
    void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            std::cout << "存入: " << amount << " 元" << std::endl;
        }
    }

    // 公有成员函数：取款
    void withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            std::cout << "取出: " << amount << " 元" << std::endl;
        } else {
            std::cout << "余额不足或金额非法！" << std::endl;
        }
    }
};

int main() {
    BankAccount myAccount("张三", 1000.0);

    // myAccount.balance = 1000000; // 错误！编译会报错，因为 balance 是 private 的
    
    myAccount.deposit(500);       // 正确：通过公有接口操作
    myAccount.withdraw(200);      // 正确：通过公有接口操作

    std::cout << "当前余额: " << myAccount.getBalance() << " 元" << std::endl;

    return 0;
}
```

## 进阶部分

### 访问控制的边界与编译时检查

在 C++ 中，封装不仅仅是“隐藏变量”，它是**一种编译器层面的协议**。

**编译时 vs 运行时**

- **编译时约束**：`private` 和 `protected` 的限制仅存在于**编译阶段**。编译器会检查你的代码是否违背了访问规则。
- **运行时透明**：一旦程序编译完成，生成的机器码中并没有“私有”的概念。通过**指针算术（Pointer Arithmetic）**或偏移量，理论上你可以访问任何内存位置。

> [!note]
>
> 封装是 C++ 提供的**静态类型安全保障**，而非内存防火墙。

### Pimpl 指子（Pointer to Implementation）

传统的封装在头文件中暴露了私有成员变量。如果你修改了一个私有变量的类型，所有引用该头文件的源文件都需要**重新编译**。

为了实现**完全的解耦**，资深开发者会使用 **Pimpl 模式**（也叫编译防火墙）：

```cpp
// MyClass.h
#include <memory>

class MyClass {
public:
    MyClass();
    ~MyClass();
    void doSomething();

private:
    struct Impl;           // 前向声明
    std::unique_ptr<Impl> pImpl; // 真正的私有数据和实现都在 Impl 里
};
```

### 对象模型与内存对齐

从内存布局（Memory Layout）看封装：

**布局顺序**：C++ 保证在同一个访问块（例如同一个 `public` 块）内的成员在内存中是连续的。

**Padding（填充）**：由于内存对齐，类的大小并不总是成员大小之和。

**Vtable 指针**：如果类有虚函数，编译器会在对象最前端（通常）插入一个指向虚函数表的指针。

如果你有两个连续的 `public` 和 `private` 块，编译器并不强制要求这两块在内存中是连续的，虽然大多数编译器会这么做。这意味着**封装并不保证物理连续性**。

### explicit 与 mutable

#### explicit --语义严谨性的“安全阀”

`explicit` 主要用于修饰类中的构造函数（尤其是单参数构造函数）或类型转换运算符。

它的核心功能是彻底封锁编译器的隐式转换路径。在默认情况下，C++ 编译器为了灵活性，会自动尝试将基本类型或其他兼容类型隐式转换为类对象，而一旦标记了 `explicit`，这种“擅自操作”将被禁止。开发者必须通过显式的构造语法（如直接初始化）来创建对象，否则代码在编译阶段就会报错。

这主要是为了防止由于语义歧义而引发的隐式 Bug。

在大型工程中，隐式转换往往会产生令人困惑的行为。例如，一个本意是“设置缓冲区大小”的整型参数，可能会被编译器误解为“将整数隐式转换为缓冲区对象”，从而在函数传参时触发昂贵的内存分配或错误的逻辑操作。

通过使用 `explicit`，C++ 强制要求开发者必须显式地表达意图，从而实现了更严谨的接口封装，确保“所写即所得”，提升了代码的安全性与可读性。

```cpp
class SmartPtr {
public:
    explicit operator bool() const { return ptr != nullptr; }
private:
    void* ptr;
};

SmartPtr p;
if (p) { ... }        // OK：在 if 语句中会自动尝试转换为 bool（上下文转换）
// int x = p + 10;    // 编译报错！防止了意外的算术运算
```



#### mutable--物理与逻辑的“柔性窗口”

`mutable` 是 C++ 访问控制权限中的一个特殊例外，它作用于类的非静态成员变量。

它的直接功能是赋予该变量“突破 `const` 约束”的权力：即在一个被声明为 `const` 的成员函数内部，依然可以合法地修改被 `mutable` 修饰的变量。即便对象本身被定义为常量对象，其内部的 `mutable` 成员也依然保持可变性

源于 C++ 对“逻辑常量性”与“物理常量性”的深刻区分。

在封装逻辑中，物理常量性要求内存字节绝对不动，但有时为了维持逻辑上的常量性，内部实现必须做出调整。典型的例子是“缓存机制”和“多线程互斥锁”：为了加速查询，`const` 接口可能需要修改内部的缓存计数器；为了保证并发安全，`const` 接口必须操作互斥锁来改变其锁定状态。

在这些场景下，外部用户感知不到对象状态的变化，但内部却必须进行必要的读写。`mutable` 的存在，让开发者能够在不破坏对象对外承诺（`const` 契约）的前提下，灵活地处理这些底层实现细节。

```cpp
class SharedData {
private:
    int data;
    mutable std::mutex mtx; // 必须是 mutable

public:
    int getData() const {
        std::lock_guard<std::mutex> lock(mtx); // 修改了 mtx 的内部状态
        return data;
    }
};
```

在多线程环境下，即使是 `const` 的只读操作（如 `getValue()`），也需要加锁来保证并发安全。但 `std::mutex::lock()` 本身会修改锁的状态。如果没有 `mutable`，你无法在 `const` 函数里加锁。这里`mutable` 告诉编译器：“这个变量不参与对象的常量语义检查，请在 `const` 函数中对它网开一面。”

