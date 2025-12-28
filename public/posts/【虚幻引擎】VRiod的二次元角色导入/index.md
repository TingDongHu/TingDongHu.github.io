--- 
title: 【虚幻引擎】VRiod的二次元角色导入
date: 2023-11-20T00:00:00+08:00
categories: ["游戏开发", "虚幻功能记录"]
tags: ["模型", "UnrealEngine", "骨骼绑定", "动画映射", "插件", "打包"]
description: "详细讲解VRoid Studio二次元角色模型导入虚幻引擎的完整流程，涵盖VRM文件导出、VRM4U插件安装配置、常见问题解决及动画重定向方法。"
cover: "/img/unrealengine.png"
headerImage: "/img/yuzu.png"
math: true
--- 

本文介绍了将VRoid Studio创建的二次元角色模型导入虚幻引擎的完整流程。首先在VRoid Studio中设计并导出VRM格式的角色文件，然后通过VRM4U插件将其导入虚幻引擎项目，并提供了插件安装、配置及常见问题的解决方法。 



# VRiod的二次元角色导入虚幻引擎

突然想在虚幻项目中用点二次元角色,找了些资料以及自己实践作如下博客,附一篇视频教程:[如何在UE5中快速导入VroidStudio的二次元萌妹](https://www.bilibili.com/video/BV1ox4y1v7dD/?share_source=copy_web&vd_source=a06df7b174b0e55e45242729b8ce1758)

## VRoid Studio使用

**VRoid Studio**是由`pixiv`开发的一款3D角色绘制软件,可以在Steam上免费下载使用.

> 软件的主要功能就是通过类似绘画的方式进行人物的建模，让用户可以更加轻松地创造自己的虚拟人物（形象）。软件的操作界面也非常的简单直观，里面配备了许多预设项目和参数，让用户不需要从头开始建模，只需选择项目、组合它们并调整参数即可创建自己的角色，其中就包含了面部、发型、衣服、化妆等等可定制的参数。同时，用户能直接想画画一样直观的模拟发型，还能直接在3D模型上绘制特定的面部表情、眼睛或服装设计。此外，用户可以通过全尺寸钢笔工具绘制自己所需要的纹理，它支持数位板压力感应，用户可以直接在3D模型或UV开发上直接实时绘制纹理用来创建角色。

对于我们这种只会写代码的人来说,使用`VRoid Studio`只需要把他提供的资源组合一下,就能得到很好看的角色.

比如我们选择软件提供的模板,这个蓝头发的美眉,进入微调界面:

![image-20250424222850712](image-20250424222850712.png)

调整为自己心仪的模样后点击右上角导出为`VRM`文件.

![image-20250424223042603](image-20250424223042603.png)

不进行骨骼贴图调整,直接使用默认选项导出:

![image-20250424223201161](image-20250424223201161.png)



## 导入虚幻引擎

要将VRM文件导入到虚幻引擎中需要使用一个插件[VRM4U](https://github.com/ruyo/VRM4U/releases)

从GitHub上下载对应版本的源码,导入到项目文件的`Plugins`目录下(不建议保存到引擎的`Plugins`中)

![image-20250424223907223](image-20250424223907223.png)

用虚幻引擎打开项目,在项目-设置-插件中开启该插件,重启项目.

![image-20250424225055135](image-20250424225055135.png)

之后就可以将之前制作好的VRM文件导入了(直接拖到某一文件夹下就行).需要注意的是在导入的时候要将高级选项-`Generate IK bone`勾选上:

![image-20250424225515367](image-20250424225515367.png)

> [!WARNING]
>
> 如果这里这步遇到导入失败/引擎崩溃等情况,建议检查是否插件版本与虚幻引擎版本对不上的问题,如果确认没有版本问题,可以在制作模型的时候将毛发/面数适当减少,防止内存爆炸

>[!warning]
>
>后来在又一个新的项目中导入模型时一直闪退崩溃,检查插件版本和资源也没有问题,检查日志发现时因为`VRM4U`插件与我项目中的多人联机功能冲突,查询资料后得知是因为
>
>> - VRM4U插件会在运行时动态修改骨骼网格体和动画（如重定向、表情控制），但多人联机要求所有客户端的数据**严格同步**。
>>
>> - 插件对模型的实时修改可能导致**服务器与客户端数据不一致**（例如骨骼位移不同步），触发引擎崩溃。
>
>解决方法就是不使用`VRM4U`插件,先使用`Blender+VRM插件`将模型转换为`FBX`格式或者其他虚幻兼容的格式,再直接导入使用.

## 重定向动画

使用`VRM4U`插件导入后的模型文件目录下提供了一个自动重定向器叫做`RTG_yourmodlename`

![image-20250424234857831](image-20250424234857831.png)

将模型与原骨骼保持相同的姿态,将骨骼调整为对应,保存即可.

就可以发现角色已经可以使用我们原本的动画了.

> [!tip]
>
> 如果你使用的插件版本过低,导致没有相应的重定向器,也可使用传统的`动画复制`/`骨骼替换`/`骨骼重定向`方法,最终能实现效果即可.

![image-20250424235303283](image-20250424235303283.png)

## 打包的问题

项目开发测试阶段,本来想打包给我的队友看一下效果,结果在打包的时候报了以下错误:

```
UATHelper: Packaging (Windows): LogInit: Display: LogAssetRegistry: Error: Package F:/UE/GoodIdea/WeiKeFh 5.1/Plugins/VRM4U/Content/VrmAssetListObjectBPUE5.uasset is too new. Engine Version: 1008 Package Version: 1009
UATHelper: Packaging (Windows): LogInit: Display: LogAssetRegistry: Error: Package F:/UE/GoodIdea/WeiKeFh 5.1/Plugins/VRM4U/Content/Maps/VRM4U_PostToon.umap is too new. Engine Version: 1008 Package Version: 1009
UATHelper: Packaging (Windows): LogInit: Display: LogAssetRegistry: Error: Package F:/UE/GoodIdea/WeiKeFh 5.1/Plugins/VRM4U/Content/ImportDataSet/UE5/DS_VRM_UE5_Unlit.uasset is too new. Engine Version: 1008 Package Version: 1009
UATHelper: Packaging (Windows): LogInit: Display: LogAssetRegistry: Error: Package F:/UE/GoodIdea/WeiKeFh 5.1/Plugins/VRM4U/Content/ImportDataSet/UE5/DS_VRM_UE5_SSSProfile.uasset is too new. Engine Version: 1008 Package Version: 1009
UATHelper: Packaging (Windows): LogInit: Display: LogAssetRegistry: Error: Package F:/UE/GoodIdea/WeiKeFh 5.1/Plugins/VRM4U/Content/ImportDataSet/UE5/DS_VRM_UE5_MToonUnLit.uasset is too new. Engine Version: 1008 Package Version: 1009
UATHelper: Packaging (Windows): LogInit: Display: LogAssetRegistry: Error: Package F:/UE/GoodIdea/WeiKeFh 5.1/Plugins/VRM4U/Content/Maps/latest/VRM4U_Outline.umap is too new. Engine Version: 1008 Package Version: 1009
UATHelper: Packaging (Windows): LogInit: Display: LogAssetRegistry: Error: Package F:/UE/GoodIdea/WeiKeFh 5.1/Plugins/VRM4U/Content/Maps/latest/VRM4U_SceneCapture.umap is too new. Engine Version: 1008 Package Version: 1009
UATHelper: Packaging (Windows): LogInit: Display: LogAssetRegistry: Error: Package F:/UE/GoodIdea/WeiKeFh 5.1/Plugins/VRM4U/Content/Util/Actor/latest/BP_SceneCapture.uasset is too new. Engine Version: 1008 Package Version: 1009
UATHelper: Packaging (Windows): LogInit: Display: LogAssetRegistry: Error: Package F:/UE/GoodIdea/WeiKeFh
```

![image-20250424233609721](image-20250424233609721.png)

和插件作者交流后得知是插件版本太新了,插件的资源文件中多了一些只有高版本虚幻引擎(5.2/5.3以上)才支持的资源,但是这些资源对于我们的项目并无用处,所以直接根据这些报错的资源路径把不兼容旧版本的资源文件全部删掉就可以了.

删掉之后即可正常打包项目.