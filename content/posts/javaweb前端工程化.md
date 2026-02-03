--- 
title: 【JavaWeb】前端工程化
date: 2024-03-25T00:00:00+08:00
categories: ["Java"]
tags: ["前端", "vue", "环境配置"]
description: "文章分析了Ajax的兼容性、SEO和调试问题，推荐使用基于Promise的Axios简化HTTP请求。同时介绍了前后端分离开发的优势、YAPI接口管理平台的功能，以及通过Vue CLI创建和管理前端工程化项目的方法。"
cover: "/img/javaweb.png"
headerImage: "/img/classmate.png"
math: true
--- 




**​Ajax 的缺点**：

- 浏览器兼容性：不同浏览器对 XMLHttpRequest 的实现可能不同。
- SEO 不友好：动态加载的内容可能无法被搜索引擎抓取。
- 调试复杂：异步通信的调试相对复杂。

## Axios

Axios 是一个基于 ​Promise 的 HTTP 客户端，用于浏览器和 Node.js。它简化了与服务器的 HTTP 请求，并提供了强大的功能，如拦截请求和响应、自动转换 JSON 数据等。

**Axios 的特点**

- 基于 Promise：支持异步操作，代码更简洁。
- 跨平台：适用于浏览器和 Node.js。
- 自动转换数据：自动将请求和响应的数据转换为 JSON。
- 拦截器：可以拦截请求和响应，添加全局处理逻辑。
- 取消请求：支持取消未完成的请求。
- 错误处理：提供统一的错误处理机制。

基本使用：
安装axios：
```bash
npm install axios
```
导入axios
```
import axios 'axios'
```
使用Axios发送请求，并获取响应结果，官方提供的api很多，此处给出2种，如下
发送 get 请求
```javascript
axios({
    method:"get",
    url:"http://localhost:8080/ajax-demo1/aJAXDemo1?username=zhangsan"
}).then(function (resp){
    alert(resp.data);
})
```
发送 post 请求
```javascript
axios({
    method:"post",
    url:"http://localhost:8080/ajax-demo1/aJAXDemo1",
    data:"username=zhangsan"
}).then(function (resp){
    alert(resp.data);
});
```
## 前后端分离开发
前后端分离开发 是一种现代 Web 开发架构，将前端（客户端）和后端（服务器）分离为两个独立的项目，通过 API 进行通信。这种方式提高了开发效率、代码可维护性和团队协作能力。

![Image](https://github.com/user-attachments/assets/cec68513-d1eb-474b-b7f8-1233d444a4fd)

### YAPI
前后台分离开发中，我们前后台开发人员都需要遵循接口文档，所以接下来我们介绍一款撰写接口文档的平台。

YApi 是高效、易用、功能强大的 api 管理平台，旨在为开发、产品、测试人员提供更优雅的接口管理服务。

其官网地址：http://yapi.smart-xwork.cn/

![Image](https://github.com/user-attachments/assets/0f6832e6-eb3f-4f9d-85d0-b8974b087e31)

YApi主要提供了2个功能：
- API接口管理：根据需求撰写接口，包括接口的地址，参数，响应等等信息。
- Mock服务：模拟真实接口，生成接口的模拟测试数据，用于前端的测试。


## 前端工程化
安装 `node.js`与vue官方脚手架`Vue-cli`。
通过命令创建vue项目：
```bash
vue create vue-project01
```
或者通过图形化界面创建项目：
```bash
vue ui
```
![Image](https://github.com/user-attachments/assets/d2a8de03-1517-4e0d-97c6-bb2b31161966)

vue项目的标准目录结构与相对应的解释：

![Image](https://github.com/user-attachments/assets/3e10e1d9-a91e-49c3-abb1-975822bbeb1d)

vs-code运行项目，并跳转到终端输出的端口地址：
![Image](https://github.com/user-attachments/assets/79506b65-6619-4c59-93dd-35dd4ea75240)
![Image](https://github.com/user-attachments/assets/dc3fd528-4c7f-4c95-af67-c75ce9d70078)
>[!TIP]
>如果此处服务器启用失败，先检查node.js的安装和路径问题，如果都没有问题尝试回退版本到上两个长期维护版本

## Element
Element:是饿了么团队研发的，一套为开发者、设计师和产品经理准备的基于 Vue 2.0 的桌面端组件库。
**组件:**组成网页的部件，例如 超链接、按钮、图片、表格、表单、分页条等等。
官网:https://element.eleme.cn/#/zh-CNListener

![Image](https://github.com/user-attachments/assets/36cc8abd-bdd9-4a90-8be2-0ec263160c9a)

安装ElementUI组件库：
```bash
npm install element-ui@2.15.3 
```
其余使用方式，直接上Element官网查看快速入门。

## Vue路由

vue官方提供了路由插件Vue Router,其主要组成如下：
- `VueRouter`：路由器类，根据路由请求在路由视图中动态渲染选中的组件
- `<router-link>`：请求链接组件，浏览器会解析成<a>
- `<router-view>`：动态视图组件，用来渲染展示与路由路径对应的组件

基本用法：
安装vue-router插件：
```bash
npm install vue-router@3.5.1
```
要在src/router/index.js文件中定义路由表:
```javascript
import Vue  'vue'
import VueRouter  'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/emp',  //地址hash
    name: 'emp',
    component:  () => import('../views/tlias/EmpView.vue')  //对应的vue组件
  },
  {
    path: '/dept',
    name: 'dept',
    component: () => import('../views/tlias/DeptView.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
```
xxxxxxxxxx import pickleimport jsonimport numpy as npimport os​# 指定需要查看的 frame_idtarget_frame_id = "000015"​# 所有模型的推理结果文件路径result_paths = [    '/home/tdhu/OpenPCDet/output/kitti_models/PartA2_free/default/eval/eval_with_train/epoch_80/val/result.pkl',    '/home/tdhu/OpenPCDet/output/kitti_models/pointpillar/default/eval/eval_with_train/epoch_80/val/result.pkl',    '/home/tdhu/OpenPCDet/output/kitti_models/pointrcnn/default/eval/eval_with_train/epoch_80/val/result.pkl',    '/home/tdhu/OpenPCDet/output/kitti_models/pointrcnn_iou/default/eval/eval_with_train/epoch_80/val/result.pkl',    '/home/tdhu/OpenPCDet/output/kitti_models/pv_rcnn/default/eval/eval_with_train/epoch_80/val/result.pkl',    '/home/tdhu/OpenPCDet/output/kitti_models/second/default/eval/eval_with_train/epoch_80/val/result.pkl',    '/home/tdhu/OpenPCDet/output/kitti_models/second_iou/default/eval/eval_with_train/epoch_80/val/result.pkl']​# 处理 numpy 数据，转换为 Python 可序列化的数据结构def convert_to_serializable(obj):    if isinstance(obj, np.ndarray):        return obj.tolist()  # numpy 数组转换为列表    elif isinstance(obj, (np.float32, np.float64)):        return float(obj)  # numpy 浮点数转换为 Python float    elif isinstance(obj, (np.int32, np.int64)):        return int(obj)  # numpy 整数转换为 Python int    return obj  # 其他数据类型保持不变​# 存储所有模型推理出的 `frame_id` 结果all_model_results = {}​for result_path in result_paths:    # 修正模型名称提取方式    path_parts = result_path.split('/')    if "kitti_models" in path_parts:        model_index = path_parts.index("kitti_models") + 1  # 获取模型名索引        model_name = path_parts[model_index]  # 获取模型名称    else:        model_name = "Unknown"​    try:        with open(result_path, "rb") as f:            result_data = pickle.load(f)​        # 确保数据是列表        if isinstance(result_data, list):            # 查找匹配的 frame_id            matched_frames = [frame for frame in result_data if frame.get("frame_id") == target_frame_id]​            if matched_frames:                print(f"模型 {model_name} 找到 {len(matched_frames)} 个匹配 frame_id = {target_frame_id} 的数据")                all_model_results[model_name] = matched_frames  # 存储该模型的匹配数据            else:                print(f"模型 {model_name} 未找到 frame_id = {target_frame_id} 的数据")        else:            print(f"模型 {model_name} 数据格式异常: {type(result_data)}")​    except Exception as e:        print(f"加载模型 {model_name} 的数据时发生错误: {e}")​# 如果找到数据，则保存为 JSON 文件if all_model_results:    output_json_path = "output.json"    with open(output_json_path, "w", encoding="utf-8") as f:        json.dump(all_model_results, f, indent=4, ensure_ascii=False, default=convert_to_serializable)        print(f"所有模型推理的 JSON 结果已保存为 {output_json_path}")else:    print("未找到任何匹配的 frame_id 数据")​python
```html
<el-menu-item index="1-1">
    <router-link to="/dept">部门管理</router-link>
</el-menu-item>
<el-menu-item index="1-2">
    <router-link to="/emp">员工管理</router-link>
</el-menu-item>
```
App.vue中定义route-view:
```html
<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>
```
路由配置中/对应的路由组件:
```javascript
const routes = [
  {
    path: '/emp',
    name: 'emp',
    component:  () => import('../views/tlias/EmpView.vue')
  },
  {
    path: '/dept',
    name: 'dept',
    component: () => import('../views/tlias/DeptView.vue')
  },
  {
    path: '/',
    redirect:'/emp' //表示重定向到/emp即可
  },
]
```
## 打包部署
直接通过VS Code的NPM脚本中提供的`build`按钮来完成：
![Image](https://github.com/user-attachments/assets/5b0c421a-dd6e-4d37-af04-96bd2f279bcc)
会在工程目录下生成一个`dist`目录，用于存放需要发布的前端资源
![Image](https://github.com/user-attachments/assets/10de8a84-49e2-49e9-af13-9d73152e3827)

## 部署前端工程
nginx: Nginx是一款轻量级的Web服务器/反向代理服务器及电子邮件（IMAP/POP3）代理服务器。其特点是占有内存少，并发能力强，在各大型互联网公司都有非常广泛的使用。

![Image](https://github.com/user-attachments/assets/f7bc76af-2059-4006-85fe-ecf4451f8332)
直接将资源放入到html目录中,运行`nginx.exe`.

直接访问默认的80端口即可查看发布的网页。

>[!TIP]
>有的主机系统默认占用了80端口，会导致nginx服务无法启用，到`conf/nginx.conf`配置文件来修改端口号,保存后重新运行即可。


![Image](https://github.com/user-attachments/assets/1874bce2-7c0e-41a1-aa86-8a8af3cd8f1b)