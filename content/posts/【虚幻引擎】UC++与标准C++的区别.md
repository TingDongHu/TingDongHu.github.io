--- 
title: 【虚幻引擎】UC++与标准C++的区别
date: 2024-03-19T00:00:00+08:00
categories: ["虚幻引擎"]
tags: ["C++", "语法", "UnrealEngine"]
description: "Unreal C++通过宏和反射机制支持运行时类型信息与动态访问，并采用自动垃圾回收；而标准C++则依赖手动管理或智能指针，且反射功能有限。"
cover: "/img/unrealengine.png"
headerImage: "/img/sakura.png"
math: true
--- 


## 1. 类声明与反射系统
### 1.1 类定义语法
#### Unreal C++

```cpp
// 必须继承UObject且使用反射宏
UCLASS(Blueprintable, meta=(DisplayName="My Object"))
class UMyObject : public UObject {
    GENERATED_BODY() // 必须包含
    
    UPROPERTY(EditAnywhere, Category="Stats")
    float Health = 100.0f;

    UFUNCTION(BlueprintCallable)
    void Heal(float Amount);
};
```


#### 标准 C++

```cpp
class MyObject {
public:
    float Health = 100.0f;
    
    void Heal(float Amount) {
        Health += Amount;
    }
};
```

### 1.2 反射机制对比

| 特性           | Unreal C++                        | 标准 C++             |
| -------------- | --------------------------------- | -------------------- |
| 运行时类型信息 | 通过UCLASS宏自动生成              | 仅支持有限RTTI       |
| 动态属性访问   | UPROPERTY字段可通过名字字符串访问 | 需要手动实现反射系统 |
| 方法调用       | UFUNCTION支持蓝图调用和RPC        | 只能静态调用         |

## 2. 内存管理模型

### 2.1 对象生命周期

#### Unreal C++

```cpp
// 自动垃圾回收
UMyObject* Obj = NewObject<UMyObject>();
Obj->MarkPendingKill(); // 标记销毁

// 手动控制引用
Obj->AddToRoot(); // 防止被GC
Obj->RemoveFromRoot();
```

#### 标准 C++

```cpp
// 手动管理
MyObject* obj = new MyObject();
delete obj;

// 或使用智能指针
auto ptr = std::make_shared<MyObject>();
```

### 2.2 内存分配器对比

```cpp
// Unreal自定义分配器
FMemory::Malloc(Size);
FMemory::Free(Ptr);

// 标准库分配器
void* p = std::malloc(size);
std::free(p);
```

## 3. 核心数据类型差异

### 3.1 字符串处理

#### Unreal C++

```cpp
FString Str = TEXT("Hello"); // UTF-16
FText Text = NSLOCTEXT("NS", "Key", "Localized Text");

// 格式化
FString Format = FString::Printf(TEXT("%s:%d"), *Str, 42);
```

#### 标准 C++

```cpp
std::string str = "Hello"; // 依赖编码
std::string format = std::format("{}:{}", str, 42); // C++20
```

### 3.2 容器类对比

#### 数组操作

```cpp
// Unreal
TArray<int32> Arr;
Arr.Add(1);
Arr.Remove(0);

// 标准库
std::vector<int> vec;
vec.push_back(1);
vec.erase(vec.begin());
```

#### 字典操作

```cpp
// Unreal
TMap<FName, FString> Map;
Map.Add("Key", "Value");

// 标准库
std::unordered_map<std::string, std::string> map;
map.emplace("Key", "Value");
```

## 4. 多线程编程

### 4.1 任务系统

#### Unreal C++

```cpp
// GameThread执行
AsyncTask(ENamedThreads::GameThread, [](){
    UE_LOG(LogTemp, Warning, TEXT("Main thread"));
});

// 并行任务
ParallelFor(10, [](int32 Index){
    // 并行执行
});
```

#### 标准 C++

```cpp
std::thread t([](){
    std::cout << "New thread" << std::endl;
});
t.join();
```

## 5. 编译系统差异

### 5.1 模块定义

#### Unreal模块

```cpp
// MyModule.Build.cs
public class MyModule : ModuleRules {
    public MyModule(ReadOnlyTargetRules Target) {
        PublicDependencyModuleNames.AddRange(new string[] { "Core" });
    }
}
```

#### CMake示例

```cmake
add_library(MyModule STATIC src.cpp)
target_link_libraries(MyModule PUBLIC Core)
```

## 6. 常用宏对比

### 6.1 常用Unreal宏

```cpp
UE_LOG(LogTemp, Warning, TEXT("Message")); // 日志
check(ptr != nullptr); // 断言
ensureMsgf(bCondition, TEXT("Message")); // 带消息断言
```

### 6.2 标准C++等效

```cpp
std::cout << "Message" << std::endl; // 日志
assert(ptr != nullptr); // 断言
if(!bCondition) throw std::runtime_error("Message"); // 异常
```

## 7. 最佳实践建议

1. **在Unreal项目中**：
   - 始终使用`UCLASS()`/`UFUNCTION()`暴露需要反射的类
   - 对`UObject`派生类不要使用智能指针
   - 使用`TArray`代替`std::vector`以获得更好性能
2. **在独立模块中**：
   - 可使用标准库容器和智能指针
   - 通过纯接口类与Unreal代码交互
   - 将标准C++代码封装在`Private`目录
3. **通用规则**：
   - 避免在头文件中混合两种风格的代码
   - 对性能关键路径使用Unreal优化容器
   - 跨平台代码优先使用Unreal封装