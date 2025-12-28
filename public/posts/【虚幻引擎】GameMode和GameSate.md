--- 
title: 【虚幻引擎】GameMode和GameSate
date: 2024-04-21T00:00:00+08:00
categories: ["虚幻引擎"]
tags: ["UnrealEngine", "游戏模式", "继承"]
description: "GameMode是服务器端权威的游戏规则管理者，定义核心逻辑；GameState则负责在服务器与客户端间同步全局游戏状态，如比分和时间。"
cover: "/img/unrealengine.png"
headerImage: "/img/sakura.png"
math: true
--- 

GameMode是服务器端权威的游戏规则管理者，定义核心逻辑；GameState则负责在服务器与客户端间同步全局游戏状态，如比分和时间。 



![image-20250422211945454](【虚幻引擎】GameMode和GameSate/image-20250422211945454.png)

在虚幻引擎（Unreal Engine）中，**GameMode** 和 **GameState** 都是多人游戏中的核心类，但它们的分工和用途有显著区别。以下是它们的对比和典型应用场景：

------

### **1. GameMode（游戏规则管理者）**

#### **职责**

- **仅存在于服务器端**（不会复制到客户端）。
- **定义游戏的核心规则**：胜利条件、玩家生成逻辑、回合制规则等。
- **管理玩家登录/退出**（通过`Login`/`Logout`等事件）。
- **生成并持有PlayerController、PlayerState等**。

#### **典型用途**

```cpp
// 示例：在GameMode中设置玩家生成逻辑
void AMyGameMode::PostLogin(APlayerController* NewPlayer) {
    Super::PostLogin(NewPlayer);
    // 生成玩家角色
    if (NewPlayer->GetPawn() == nullptr) {
        SpawnPlayerAtTransform(NewPlayer, SpawnTransform);
    }
}
```

#### **关键特性**

- **服务器权威**：客户端无法修改GameMode的逻辑。
- **不复制**：客户端无法直接访问GameMode。

------

### **2. GameState（游戏状态同步者）**

#### **职责**

- **存在于服务器和客户端**（自动复制到所有客户端）。
- **存储并同步游戏全局状态**：比分、剩余时间、玩家列表等。
- **提供客户端可见的数据**（如通过`PlayerArray`访问所有玩家的`PlayerState`）。

#### **典型用途**

```cpp
// 示例：在GameState中同步比分
void AMyGameState::OnRep_TeamScores() {
    // 客户端更新UI显示比分
    UpdateScoreboardUI(TeamAScore, TeamBScore);
}
```

#### **关键特性**

- **数据同步**：通过属性复制（`Replicated`）或RPC同步到客户端。
- **客户端可读**：UI可以直接绑定GameState的数据（如剩余时间）。

------

### **核心区别对比**

| **特性**             | **GameMode**               | **GameState**            |
| -------------------- | -------------------------- | ------------------------ |
| **存在位置**         | 仅服务器                   | 服务器 + 客户端（复制）  |
| **用途**             | 定义规则、逻辑控制         | 存储和同步全局状态       |
| **是否复制到客户端** | ❌ 否                       | ✅ 是                     |
| **客户端访问权限**   | 无法直接访问               | 可读取数据（如显示比分） |
| **生命周期**         | 游戏开始时创建，结束时销毁 | 随游戏运行持续存在       |

------

### **协作流程示例**

1. **服务器**：
   - GameMode决定玩家生成规则（如出生点选择）。
   - GameState更新并同步比分到所有客户端。
2. **客户端**：
   - 通过GameState获取实时比分，更新UI。
   - 无法修改规则（必须通过服务器GameMode）。

------

### **何时使用？**

- **用GameMode**：
  - 需要权威控制游戏逻辑（如判断胜利条件）。
  - 处理玩家登录/退出等敏感操作。
- **用GameState**：
  - 需要让所有客户端知道全局状态（如倒计时、玩家列表）。
  - UI需要绑定的动态数据（如实时比分）。

通过这种分工，虚幻引擎实现了**逻辑与状态的分离**，确保多人游戏的同步性和安全性。