之前在看韩老魔的JAVA教程时，由于是文字教程，总感觉WEB这块的知识很懵懂，学不明白，故打算看黑马程序员教程，重新总结一下自己的笔记。
## HTML
### css修改样式
css引入分为三种：行内样式、内嵌样式、外联样式。
一般使用内嵌和外联较多，行内样式只有效果非常简单的时候会使用。
外联样式示例
```css
h1{
    color:red
}
```
```html
 <link rel="stylesheet" href="./css/news.css">
```

### css选择器
选择器分为三种：元素选择器、id选择器、类选择器。
几个修改器可同时修饰同一个元素，优先级：id选择器>类选择器>元素选择器。
示例：
```html
<style>
    
    span{
        color:cadetblue;
    }
    .timelan{
        color:rgb(47, 73, 47)
    }
    #timeclock{
        color: rgb(0, 0, 0);
    }
    #center{
        width: 65%;
        margin:0% 17.5% 0% 17.5%;/*上 右 下 左 */
    }

</style>
```
```html
 <span class="timelan">2025年03月17日</span>  <span id="timeclock"  >21：50 央视网</span>
```

### 超链接
示例：
```html
<h3><a href="https://tingdonghu.github.io/index.html" target="_self">古月月仔的技术博客</a></h3>
```

- `href` 键表示转到链接。
- `target` 键表示使用哪种方式打开新的链接,`_self`表示在当前浏览器界面打开。

###多媒体
audio示例：
```html
 <audio src="./audio/VØJ,Narvent - Memory Reboot.flac" controls></audio>
```
`src` 键后附要播放的多媒体链接路径、想对路径/绝对路径均可。
`controls` 表示多媒体控制器，不加改键无法播放多媒体

video示例：
```html
<video src="./video/bladerunner.mp4" controls width="950px"></video>
```
`src`和`audio`的用法一样，`width`和`height`表示视频播放组件的大小（长宽），单位为`px`，一般设置一个就可以，另一个会根据设置的那个等比缩放。
效果：

![Image](https://github.com/user-attachments/assets/ac553cdc-a63a-4cf7-b2cd-5da9abb019c4)

### 排版和布局
盒子模型：页面中所有的元素(标签)，都可以看做是一个 盒子，由盒子将页面中的元素包含在一个矩形区域内，通过盒子的视角更方便的进行页面布局。
盒子模型组成:内容区域(content)、内边距区域(padding)、边框区域(border)、外边距区域(margin)。
![Image](https://github.com/user-attachments/assets/789cba39-0a6c-46af-b0fb-63b26228a0c4)

示例-设置整体居中对齐：
```html
<html>
    <head>
        <title>焦点访谈：如何俘获美女芳心</title>
        <link rel="stylesheet" href="./css/news.css">
        <style>           
            span{
                color:cadetblue;
            }
            .timelan{
                color:rgb(47, 73, 47)
            }
            #timeclock{
                color: rgb(0, 0, 0);
            }
            #center{
                width: 65%;
                margin:0% 17.5% 0% 17.5%;/*上 右 下 左 */
            }
        </style>
    </head>
    <body>
        <div id="center">
            <h1>对王茜的诗意告白</h1>
         
            <hr>
            <span class="timelan">2025年03月17日</span>  <span id="timeclock"  >21：50 央视网</span>
            <hr>
            <h3><a href="https://tingdonghu.github.io/index.html" target="_self">古月月仔的技术博客</a></h3>
            <video src="./video/bladerunner.mp4" controls width="950px"></video>
            <br>
            <audio src="./audio/VØJ,Narvent - Memory Reboot.flac" controls></audio>
        </div>
    </body>
</html>
```
将整个网页内容包裹在标签`<div>`中，通过css 的id选择器进行设置样式。
```css
#center{
    width: 65%;
    margin:0% 17.5% 0% 17.5%;/*上 右 下 左 */
}
```

### 表格和表单
**表格**
**表格的标签**：

- `<table>`:定义表格整体，可以包裹多个<tr>
- `<tr>`:表格的行，可以包裹多个<td>
- `<td>`:表格的单元格（普通），包裹内容，如果是表头单元格，可以替换为标签`<th>`.

简单表格示例：
```html
  <h2>学生成绩表</h2>
  <table border="1px" cellspacing="0" width="600px">
      <thead>
          <tr>
              <th>姓名</th>
              <th>语文</th>
              <th>数学</th>
              <th>英语</th>
              <th>科学</th>
              <th>道法</th>
          </tr>
      </thead>
      <tbody>
          <tr>
              <td>王茜</td>
              <td>88</td>
              <td>66</td>
              <td>95</td>
              <td>40</td>
              <td>47</td>
          </tr>
      </tbody>
  </table>
```
![Image](https://github.com/user-attachments/assets/3ba69d00-0fdd-40df-b168-f3371b2d7681)

**表单**
表单使用场景：在网页中主要负责数据采集功能，比如登录注册等

表单的标签：`<form>`

表单项：不同类型的input元素、下拉表单、文本域等
- `<input>`:定义表单项，通过type熟悉控制输入形式。
- `<select>`：定义下拉列表。
- `<textarea>`:定义文本域。

属性：
- `action`：规定当提交表单时向何处发送表单数据。
- `method`：规定用于发送表单数据的方式。例如GET、POST

简单表单示例：
```html
<form action="" method="get">
    用户名：<input type="text" name="username">
    年龄：<input type="text" name="age">
    
    <input type="submit" value="提交信息">
</form>
```

![Image](https://github.com/user-attachments/assets/a5744697-538e-4afe-a62a-d4be15a078cf)

复杂表单示例：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>用户信息表单</title>
</head>
<body>
    <h1>用户信息表单</h1>
    <form action="/submit" method="post" enctype="multipart/form-data">
        <!-- 密码输入框 -->
        <label for="password">密码：</label>
        <input type="password" id="password" name="password" required>
        <br><br>

        <!-- 性别单选按钮 -->
        <label>性别：</label>
        <label><input type="radio" name="gender" value="1" checked> 男</label>
        <label><input type="radio" name="gender" value="2"> 女</label>
        <br><br>

        <!-- 爱好复选框 -->
        <label>爱好：</label>
        <label><input type="checkbox" name="hobby" value="java"> Java</label>
        <label><input type="checkbox" name="hobby" value="game"> 游戏</label>
        <label><input type="checkbox" name="hobby" value="sing"> 唱歌</label>
        <br><br>

        <!-- 文件上传 -->
        <label for="image">图像：</label>
        <input type="file" id="image" name="image">
        <br><br>

        <!-- 生日日期选择 -->
        <label for="birthday">生日：</label>
        <input type="date" id="birthday" name="birthday">
        <br><br>

        <!-- 时间选择 -->
        <label for="time">时间：</label>
        <input type="time" id="time" name="time">
        <br><br>

        <!-- 日期时间选择 -->
        <label for="datetime">日期时间：</label>
        <input type="datetime-local" id="datetime" name="datetime">
        <br><br>

        <!-- 邮箱输入框 -->
        <label for="email">邮箱：</label>
        <input type="email" id="email" name="email" required>
        <br><br>

        <!-- 年龄输入框 -->
        <label for="age">年龄：</label>
        <input type="number" id="age" name="age" min="0" max="120">
        <br><br>

        <!-- 学历下拉菜单 -->
        <label for="degree">学历：</label>
        <select id="degree" name="degree">
            <option value="">请选择</option>
            <option value="1">大专</option>
            <option value="2">本科</option>
            <option value="3">硕士</option>
            <option value="4">博士</option>
        </select>
        <br><br>

        <!-- 描述文本域 -->
        <label for="description">描述：</label><br>
        <textarea id="description" name="description" rows="5" cols="30"></textarea>
        <br><br>

        <!-- 隐藏输入 -->
        <input type="hidden" name="image_id" value="1">

        <!-- 表单按钮 -->
        <input type="button" value="按钮">
        <input type="reset" value="重置">
        <input type="submit" value="提交">
    </form>
</body>
</html>
```
![Image](https://github.com/user-attachments/assets/c9a9c302-bb5f-4ad6-9c74-6dc97ab8b30f)

示例中主要的表单标签用法和意义：
---

#### 1. **密码输入框**
```html
<input type="password" name="password">
```
• **作用**：用于输入密码，输入内容会被隐藏（显示为圆点或星号）。
• **属性**：
  • `type="password"`：指定输入类型为密码。
  • `name="password"`：用于标识该字段，提交表单时会作为字段名称。

---

#### 2. **性别选择（单选按钮）**
```html
<label><input type="radio" name="gender" value="1">男</label>
<label><input type="radio" name="gender" value="2">女</label>
```
• **作用**：允许用户从一组选项中选择一个。
• **属性**：
  • `type="radio"`：指定输入类型为单选按钮。
  • `name="gender"`：用于将单选按钮分组，确保同一组中只能选择一个。
  • `value="1"` 和 `value="2"`：表示选中该选项时提交的值。
• **`<label>`**：将文本与输入框关联，点击文本也可以选中按钮。

---

#### 3. **爱好选择（复选框）**
```html
<label><input type="checkbox" name="hobby" value="java">Java</label>
<label><input type="checkbox" name="hobby" value="game">游戏</label>
<label><input type="checkbox" name="hobby" value="sing">唱歌</label>
```
• **作用**：允许用户从一组选项中选择多个。
• **属性**：
  • `type="checkbox"`：指定输入类型为复选框。
  • `name="hobby"`：用于标识该字段，提交表单时会作为字段名称。
  • `value="java"` 等：表示选中该选项时提交的值。

---

#### 4. **文件上传**
```html
<input type="file" name="image">
```
• **作用**：允许用户上传文件（如图片、文档等）。
• **属性**：
  • `type="file"`：指定输入类型为文件上传。
  • `name="image"`：用于标识该字段，提交表单时会作为字段名称。

---

#### 5. **日期和时间输入**
```html
<input type="date" name="birthday">
<input type="time" name="time">
<input type="datetime-local" name="datetime">
```
• **作用**：
  • `type="date"`：允许用户选择日期。
  • `type="time"`：允许用户选择时间。
  • `type="datetime-local"`：允许用户选择日期和时间。
• **属性**：
  • `name="birthday"` 等：用于标识该字段，提交表单时会作为字段名称。

---

#### 6. **邮箱输入**
```html
<input type="email" name="email">
```
• **作用**：用于输入邮箱地址，浏览器会自动验证输入格式。
• **属性**：
  • `type="email"`：指定输入类型为邮箱。
  • `name="email"`：用于标识该字段，提交表单时会作为字段名称。

---

#### 7. **年龄输入**
```html
<input type="number" name="age">
```
• **作用**：用于输入数字（如年龄）。
• **属性**：
  • `type="number"`：指定输入类型为数字。
  • `name="age"`：用于标识该字段，提交表单时会作为字段名称。

---

#### 8. **学历选择（下拉菜单）**
```html
<select name="degree">
  <option value="">请选择</option>
  <option value="1">大专</option>
  <option value="2">本科</option>
  <option value="3">硕士</option>
  <option value="4">博士</option>
</select>
```
• **作用**：允许用户从下拉列表中选择一个选项。
• **属性**：
  • `name="degree"`：用于标识该字段，提交表单时会作为字段名称。
  • `<option>`：定义下拉列表中的选项。
    ◦ `value="1"` 等：表示选中该选项时提交的值。

---

#### 9. **描述文本域**
```html
<textarea name="description" cols="30" rows="10"></textarea>
```
• **作用**：用于输入多行文本（如个人描述）。
• **属性**：
  • `name="description"`：用于标识该字段，提交表单时会作为字段名称。
  • `cols="30"`：指定文本域的列数（宽度）。
  • `rows="10"`：指定文本域的行数（高度）。

---

###3 10. **隐藏输入**
```html
<input type="hidden" name="id" value="1">
```
• **作用**：用于在表单中传递隐藏数据，用户不可见。
• **属性**：
  • `type="hidden"`：指定输入类型为隐藏。
  • `name="id"`：用于标识该字段，提交表单时会作为字段名称。
  • `value="1"`：表示提交的值。

---

#### 11. **按钮**
```html
<input type="button" value="按钮">
<input type="reset" value="重置">
<input type="submit" value="提交">
```
• **作用**：
  • `type="button"`：普通按钮，通常用于触发 JavaScript 事件。
  • `type="reset"`：重置按钮，用于清空表单内容。
  • `type="submit"`：提交按钮，用于提交表单数据。
• **属性**：
  • `value="按钮"` 等：按钮上显示的文本。

---

#### 12. **表单标签**
```html
<form action="/submit" method="post" enctype="multipart/form-data">
```
• **作用**：定义表单的开始和结束。
• **属性**：
  • `action="/submit"`：指定表单提交的目标 URL。
  • `method="post"`：指定表单提交的方式（`GET` 或 `POST`）。
  • `enctype="multipart/form-data"`：指定表单数据的编码方式，通常用于文件上传。

---
