--- 
title: 【虚幻引擎】UC++的宏定义语法
date: 2024-04-10T00:00:00+08:00
categories: ["虚幻引擎"]
tags: ["UnrealEngine", "语法", "c++"]
description: "Unreal Engine通过UCLASS、UPROPERTY和UFUNCTION等反射宏，将C++代码暴露给引擎反射系统与蓝图编辑器，实现可视化编辑。GENERATED_BODY()宏必须置于类定义起始处，关键宏参数则控制属性与函数在编辑器中的可见性、可编辑性和蓝图交互能力。"
cover: "/img/unrealengine.png"
headerImage: "/img/yuzu.png"
math: true
--- 

Unreal Engine通过UCLASS、UPROPERTY和UFUNCTION等反射宏，将C++类、属性和函数暴露给引擎反射系统与蓝图编辑器，实现可视化编辑和脚本交互。GENERATED_BODY()宏必须置于类定义起始处。 



## Unreal Engine中宏定义语法的使用

### 示例代码：

```cpp
// 类声明宏：使类被纳入Unreal反射系统
// - Blueprintable：允许在蓝图中创建该类的子类
// - meta=(DisplayName="My Object")：在编辑器中显示的自定义名称
UCLASS(Blueprintable, meta=(DisplayName="My Object"))
class UMyObject : public UObject  // 必须继承UObject或其子类
{
    // 代码生成宏：必须出现在类体内第一个位置
    // - 展开后会包含类型信息、反射数据等引擎所需的内容
    GENERATED_BODY()
    
    // 属性声明宏：将成员变量暴露给反射系统
    // - EditAnywhere：可在编辑器的任意位置（如蓝图、细节面板）编辑此属性
    // - Category="Stats"：在编辑器中归入"Stats"分类组
    UPROPERTY(EditAnywhere, Category="Stats")
    float Health = 100.0f;  // 带默认值的公开属性

    // 函数声明宏：将函数暴露给反射系统
    // - BlueprintCallable：允许蓝图调用此方法
    // - 可添加其他说明符如：
    //   - Category="Gameplay"：函数分组
    //   - meta=(ToolTip="Heal amount")：悬停提示文本
    UFUNCTION(BlueprintCallable)
    void Heal(float Amount);  // 可被蓝图调用的方法
};
```

### 关键宏参数详解：

#### UCLASS 常用参数：

| 参数               | 作用                         |
| ------------------ | ---------------------------- |
| Blueprintable      | 允许基于此类创建蓝图         |
| BlueprintType      | 允许在蓝图中作为变量类型使用 |
| NotBlueprintable   | 明确禁止蓝图继承（默认）     |
| meta=(DisplayName) | 编辑器显示名称               |

#### UPROPERTY 常用参数：

| 参数              | 作用                   |
| ----------------- | ---------------------- |
| VisibleAnywhere   | 属性可见但不可编辑     |
| EditAnywhere      | 属性可任意编辑         |
| EditDefaultsOnly  | 仅允许在类默认值中编辑 |
| BlueprintReadOnly | 蓝图只读访问           |
| Category          | 属性分类（编辑器分组） |
| meta=(ClampMin=0) | 元数据：限制最小值     |

#### UFUNCTION 常用参数：

| 参数              | 作用               |
| ----------------- | ------------------ |
| BlueprintCallable | 可从蓝图调用       |
| BlueprintPure     | 纯函数（无副作用） |
| Category          | 函数分类           |
| meta=(Deprecated) | 标记为已弃用       |

### 特殊说明：

1. `GENERATED_BODY()` 必须：

   - 放在类定义的最开始位置
   - 每个反射类必须有且仅有一个
   - 展开后包含类型标识符等关键信息

2. 命名规范要求：

   - 反射类必须以`U`开头（如`UMyObject`）
   - 非反射类不应使用`U`前缀

3. 继承规则：

   ```cpp
   // 正确：继承自UObject派生类
   class UMyActor : public AActor {
       GENERATED_BODY()
       // ...
   };
   
   // 错误：不能直接从非UObject继承
   class UInvalidClass : public std::enable_shared_from_this { /*...*/ };
   ```

这些宏共同构成了Unreal的反射系统基础，使C++类能够与蓝图编辑器、序列化系统等引擎功能无缝交互。