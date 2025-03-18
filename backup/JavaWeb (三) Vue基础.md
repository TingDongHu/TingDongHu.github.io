![Image](https://github.com/user-attachments/assets/537c9762-2767-4c32-be46-9637fce6552d)

## 什么是Vue？
Vue 是一个用于构建用户界面的渐进式 JavaScript 框架。它的核心思想是通过数据驱动视图，使开发者能够更高效地构建交互式的前端应用。

核心概念：数据绑定、指令、组件和生命周期钩子。
**​双向绑定**：Vue 使用 v-model 实现表单元素与数据的双向绑定。
**与 DOM 的关系**：通过虚拟 DOM 和数据驱动视图，减少手动操作 DOM 的繁琐。

![Image](https://github.com/user-attachments/assets/3b1b66d8-8514-41b1-9ca4-e70320cffc54)

## Vue的常用指令

在 Vue 中，​指令 是带有 v- 前缀的特殊属性，用于在模板中实现动态绑定和逻辑控制。

- `​v-bind`动态绑定 HTML 属性。​语法`v-bind:属性名="表达式" `或简写为 :`属性名="表达式"`。
- `v-model`作用：实现表单元素与数据的双向绑定。语法：`v-model="数据"`。
- `v-on`​作用：绑定事件监听器。​语法：`v-on:事件名="方法"` 或简写为 `@事件名="方法"`。
- `v-if` / `v-else` / `v-else-if`作用：条件渲染，根据表达式的值决定是否渲染元素。

示例代码：
```html
<!DOCTYPE html>
<html>
<head>
  <title>Vue 指令示例</title>
  <script src="https://cdn.jsdelivr.net/npm/vue@2"></script>
</head>
<body>
  <div id="app">
    <!-- v-model -->
    <input v-model="message">
    <p>{{ message }}</p>

    <!-- v-if -->
     年龄<input type="text" v-model="age">经判定，为：
    <span v-if="age>=50">老年人</span>
    <span v-else-if="age>15&&age<50" >年轻人</span>
    <span v-else>小屁孩</span>
    <br><br>
    年龄<input type="text" v-model="age">经判定，为：
    <span v-show="age>=30">老年人</span>
    
    <!-- v-for -->
    <ul>
      <li v-for="(item, index) in items" :key="index">{{ item }}</li>
    </ul>

    <!-- v-on -->
    <button @click="handleClick">点击我</button>
  </div>

  <script>
    var app = new Vue({
      el: '#app',
      data: {
        message: 'Hello Vue!',
        isVisible: true,
        age:50,
        items: ['苹果', '香蕉', '橙子']
      },
      methods: {
        handleClick: function() {
          alert('按钮被点击了！');
          data.isVisible=false;
        }
      }
    });
  </script>
</body>
</html>
```

## Vue的生命周期
​生命周期 是指 Vue 实例从创建到销毁的整个过程。Vue 提供了一系列生命周期**钩子函数**，允许开发者在不同阶段执行自定义逻辑。

Vue 实例的生命周期可以分为以下 4 个阶段：

- ​创建阶段：实例初始化、数据观测和模板编译。
- ​挂载阶段：实例挂载到 DOM。
- ​更新阶段：数据变化导致视图更新。
- ​销毁阶段：实例销毁。

Vue 生命周期中的主要钩子函数：

- `beforeCreate`触发时机：实例初始化之后，数据观测和事件配置之前。通常用于插件开发或全局配置。
- `created`​触发时机：实例创建完成，数据观测和事件配置已完成，但 DOM 还未挂载。常用于异步数据请求或初始化数据。
- `beforeMount`:模板编译完成，但 DOM 还未挂载。很少使用，通常用于在挂载前对 DOM 进行最后操作。
- `mounted`:触发时机：实例挂载到 DOM 后。常用于操作 DOM 或初始化第三方库。

mounted示例：
```javascript
created() {
  console.log('created：实例创建完成，数据观测和事件配置已完成');
}
```

## Ajax
**什么是Ajax？**
**Ajax（Asynchronous JavaScript and XML）​** 是一种在无需重新加载整个网页的情况下，能够与服务器进行异步通信的技术。它允许网页在后台与服务器交换数据，并动态更新部分页面内容，从而提升用户体验。

 **​Ajax 的核心概念**

- ​异步通信：Ajax 通过异步方式与服务器通信，不会阻塞用户操作。
- ​局部更新：只更新页面的部分内容，而不是重新加载整个页面。
- ​数据格式：虽然名字中包含 XML，但 Ajax 支持多种数据格式，如 JSON、HTML、纯文本

示例代码：
```html
<!DOCTYPE html>
<html>
<head>
  <title>Ajax 示例</title>
</head>
<body>
  <h1>Ajax 示例</h1>
  <button id="loadData">加载数据</button>
  <div id="output"></div>

  <script>
    document.getElementById('loadData').addEventListener('click', function() {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', 'https://jsonplaceholder.typicode.com/posts/1', true);
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          document.getElementById('output').innerHTML = `
            <p>标题：${response.title}</p>
            <p>内容：${response.body}</p>
          `;
        }
      };
      xhr.send();
    });
  </script>
</body>
</html>
```
>[!NOTE]
>Ajax 是一种用于实现异步通信的技术，能够在不重新加载整个页面的情况下更新部分内容。Fetch API 和 Axios 提供了更现代和简洁的 API。
