## JavaScript

**JavaScript**​（简称：JS）是一门跨平台、面向对象的脚本语言。是用来控制网页行为的，它能使网页可交互。

- ​**JavaScript 和 Java 的区别**：  
  JavaScript 和 Java 是完全不同的语言，不论是概念还是设计。但是基础语法类似。

- ​**发明历史**：  
  JavaScript 在 1995 年由 Brendan Eich 发明，并于 1997 年成为 ECMA 标准。

- ​**最新版本**：  
  ECMAScript 6（ES6）是最新的 JavaScript 版本（发布于 2015 年）。




## JavaScript 引入方式

### 内部脚本
将 JS 代码定义在 HTML 页面中。

- JavaScript 代码必须位于 `<script>` 标签之间。
  ```html
  <script>
    alert("Hello JavaScript");
  </script>
  ```
- 在 HTML 文档中，可以在任意地方放置任意数量的 `<script>` 标签。
- 一般会把脚本置于 `<body>` 元素的底部，以改善显示速度。

### 外部脚本
将 JS 代码定义在外部 JS 文件中，然后引入到 HTML 页面中。

- 外部 JS 文件中，只包含 JS 代码，不包含 `<script>` 标签。
  ```javascript
  // demo.js
  alert("Hello JavaScript");
  ```
- `<script>` 标签不能自闭合，自闭合无法触发事件。
  ```html
  <script src="js/demo.js"></script>
  ```


## JavaScript书写语法

### 区分大小写
与 Java 一样，JavaScript 中的变量名、函数名以及其他一切东西都是区分大小写的。

例如：
```javascript
let myVariable = 10;
let MyVariable = 20; // 这是两个不同的变量
```

### 每行结尾的分号
在 JavaScript 中，每行结尾的分号（`;`）是 **可有可无** 的。但为了代码规范和避免潜在问题，建议在每行结尾添加分号。

例如：
```javascript
let a = 10; // 推荐
let b = 20  // 不推荐
```

### 注释
JavaScript 支持两种注释方式：
- **单行注释**：使用 `//`，后跟注释内容。
  ```javascript
  // 这是一个单行注释
  let x = 5; // 这是对变量的注释
  ```
- **多行注释**：使用 `/*` 和 `*/` 包围注释内容。
  ```javascript
  /*
  这是一个多行注释
  可以跨越多行
  */
  let y = 10;
  ```

### 大括号表示代码块
通过大括号 `{}` 来表示代码块，通常用于控制结构（如 `if`、`for`、`function` 等）。

例如：
```javascript
// 判断语句
if (count == 3) {
    alert(count);
}
```

**示例代码**
以下是一个完整的判断语句示例：
```javascript
// 判断
if (count == 3) {
    alert(count); // 弹出 count 的值
}
```


### 输出
**`window.alert()`**在浏览器中弹出一个警告框，显示指定的消息。
**语法**：
  ```javascript
  window.alert("消息内容");
  ```

 **`document.write()`**将指定的内容写入 HTML 文档中，显示在浏览器页面上。
**语法**：
  ```javascript
  document.write("内容");
  ```
**注意**：如果在页面加载完成后使用 `document.write()`，它会覆盖整个页面的内容。

**`console.log()`**将指定的内容输出到浏览器的控制台（Console），通常用于调试。
**语法**：
  ```javascript
  console.log("内容");
  ```

**示例代码**
```javascript
<script>
  window.alert("Hello JavaScript"); // 浏览器弹出警告框
  document.write("Hello JavaScript"); // 写入HTML，在浏览器展示
  console.log("Hello JavaScript"); // 写入浏览器控制台
</script>
```

### 变量
在 JavaScript 中，变量可以存储不同类型的数据，如数字、字符串、布尔值等。
- JavaScript 是弱类型语言，变量的数据类型可以动态变化。
- 变量名是标识符，用于在代码中引用变量。

**语法：**
```javascript
var 变量名 = 值;
```

**作用域：**

- **`var` 的作用域**：函数作用域或全局作用域。
```javascript
function test() {
  var x = 10; // x 在函数内部有效
}
```
- **`let`和 `const` 的作用域**：块级作用域。
```javascript
if (true) {
  let y = 20; // y 只在 if 块中有效
}
```
- `let`定义局部变量，不能重复定义
- `const` 定义常量,不可被改变


### 数据类型
JavaScript 数据类型分为原始类型和引用类型
 **​原始类型（Primitive Types）​**JavaScript 中最基本的数据类型，包括以下 5 种：
​**number（数字）​**、​**string（字符串）​**、​**boolean（布尔值）​**、 ​**null（空值）​**​、**undefined（未定义）​**。

**​引用类型（Reference Types）​**是复杂的数据类型，包括对象、数组、函数等。引用类型的值存储在堆内存中，变量存储的是指向堆内存的地址。

**typeof 运算符**用于获取变量的数据类型。
语法：
```javascript
typeof 变量;
```
示例：
```javascript
var a = 20;
var b = "张三";
var c = true;
var d = null;
var e;

console.log(typeof a); // 输出 "number"
console.log(typeof b); // 输出 "string"
console.log(typeof c); // 输出 "boolean"
console.log(typeof d); // 输出 "object"（null 是特殊值）
console.log(typeof e); // 输出 "undefined"
```

### 运算符==与===
 ​**==（宽松相等）​**会进行类型转换，如果两个值的类型不同，会尝试将它们转换为相同类型后再比较。
```javascript
var a = 10;
alert(a == "10"); // true，字符串 "10" 被转换为数字 10
```

- 如果一个是数字，另一个是字符串，字符串会被转换为数字。
- 如果一个是布尔值，另一个是非布尔值，布尔值会被转换为数字（true 为 1，false 为 0）。
- `null` 和 `undefined` 在 `==` 下相等。
- 如果一个是对象，另一个是原始类型，对象会被转换为原始类型后再比较。

**===（严格相等）​**不会进行类型转换，只有在类型和值都相同时才返回 `true`。
```javascript
var a = 10;
alert(a === "10"); // false，类型不同（数字 vs 字符串）
alert(a === 10); // true，类型和值都相同
```
**其他比较运算符**:

- **!=**：宽松不相等（会进行类型转换）。
- ​**!==**：严格不相等（不会进行类型转换）。
- ​**>、<、>=、<=**：用于比较数值大小。
示例代码
```javascript
var a = 10;
var b = "10";

// 宽松比较
console.log(a == b); // true
console.log(a != b); // false

// 严格比较
console.log(a === b); // false
console.log(a !== b); // true

// 数值比较
console.log(a > 5); // true
console.log(a <= 10); // true
```

### 函数function
函数是被设计为执行特定任务的代码块。
语法：使用 `function`关键字定义函数。
```javascript
function functionName(参数1, 参数2, ...) {
  // 要执行的代码
  return 返回值; // 可选
}
```
JavaScript 是弱类型语言，因此：

- ​形式参数不需要定义类型：函数可以接收任意类型的参数。
- ​返回值不需要定义类型：函数可以直接使用 return 返回任意类型的值。

函数调用
语法：通过函数名称和实际参数列表调用函数。
```javascript
functionName(实际参数1, 实际参数2, ...);
```
示例代码：
```javascript
// 定义函数
function add(a, b) {
  return a + b;
}

// 调用函数
var result = add(3, 5);
console.log(result); // 输出 8
```

## JavaScript中的对象
对象是 JavaScript 中的一种复杂数据类型，用于存储键值对（key-value pairs）
大体分为三种：基础对象、BOM（浏览器对象模型）​ 和 ​DOM（文档对象模型）

### 基础对象
#### Array
JavaScript 中 Array对象用于定义数组。
>[!TIP]
>JavaScript 中的数组相当于Java 中集合，数组的长度是可变的，而JavaScript 是弱类型，所以可以存储任意的类型的数据。

Array的属性：`length`,用于获取数组长度
Array的方法：
`forEach():`遍历数组中每个有值的元素，并调用一次传入的函数。
`push():`添加新元素，并返回新的长度。
`splice():`从数组中删除元素。

示例代码：
```javascript
let animals = ["猫", "狗", "兔子"];

// 使用 forEach() 遍历数组
animals.forEach(function(animal, index) {
  console.log("索引 " + index + " 的动物是 " + animal);
});

// 使用 push() 添加新元素
let newLength = animals.push("鸟", "鱼");
console.log("添加新元素后的数组是 " + animals); // 输出 "添加新元素后的数组是 猫,狗,兔子,鸟,鱼"
console.log("新数组长度是 " + newLength); // 输出 "新数组长度是 5"

// 使用 splice() 删除和添加元素
let removed = animals.splice(1, 2, "仓鼠", "乌龟");
console.log("删除的元素是 " + removed); // 输出 "删除的元素是 狗,兔子"
console.log("修改后的数组是 " + animals); // 输出 "修改后的数组是 猫,仓鼠,乌龟,鸟,鱼"
```

#### String
String 对象是 JavaScript 中用于表示和操作字符串的对象。创建字符串有两种方式：`new String()`和`var str1 = "Hello World"`创建。引号使用单双引号都可以。
**String 对象的属性**`length`返回字符串的长度（字符的数量）。
 ​String 对象的方法：
- `charAt()`,返回字符串中指定位置的字符。
- `indexOf()`返回指定子字符串在字符串中首次出现的位置。
- `trim()`去除字符串两端的空格。
- `substring()`提取字符串中两个指定索引号之间的字符。

示例代码：
```javascript
// 创建字符串
var str1 = new String("Hello World"); // 方式一
var str2 = "Hello World"; // 方式二

// 使用属性
console.log(str1.length); // 输出 11
console.log(str2.length); // 输出 11

// 使用方法
console.log(str1.charAt(1)); // 输出 "e"
console.log(str2.indexOf("World")); // 输出 6

var str3 = "   Hello World   ";
console.log(str3.trim()); // 输出 "Hello World"

console.log(str2.substring(0, 5)); // 输出 "Hello"
console.log(str2.substring(6)); // 输出 "World"
```
#### JavaScript自定义对象
通用格式：
```javascript
var 对象名 = {
  属性名1: 属性值1,
  属性名2: 属性值2,
  属性名3: 属性值3,
  函数名称: function(形参列表) {
    // 函数体
  }
};
示例代码：
```javascript
var user = {
  name: "Tom",       // 属性：姓名
  age: 20,           // 属性：年龄
  gender: "male",    // 属性：性别
  eat: function() {  // 方法：吃饭
    alert("用膳~");
  }
};
```
属性调用：使用点符号（.）或方括号（[]）访问对象的属性。
示例：
```javascript
var user = {
  name: "Tom",
  age: 20,
  gender: "male"
};

// 使用点符号访问属性
console.log(user.name); // 输出 "Tom"

// 使用方括号访问属性
console.log(user["age"]); // 输出 20
```
方法调用：使用点符号（.）调用对象的方法，并传递参数（如果有）
示例代码：
```javascript
var user = {
  name: "Tom",
  eat: function() {
    alert("用膳~");
  }
};

// 调用方法
user.eat(); // 弹出提示框显示 "用膳~"
```

### JSON
**JSON（JavaScript Object Notation）​** 是一种轻量级的数据交换格式，基于 JavaScript 对象的语法，但独立于编程语言。它广泛用于前后端数据传输和配置文件。
其优势：
- 易于阅读和编写。
- 易于解析和生成。
- 独立于编程语言，支持多种语言（如 JavaScript、Python、Java 等）。


**语法**
​键和值：
- 键必须是双引号包裹的字符串。
- 值可以是字符串、数字、布尔值、数组、对象或 `null`。
不支持:
函数、`undefined`、`NaN` 等 JavaScript 特有的数据类型。
示例：
```json
{
  "name": "张三",
  "age": 20,
  "isStudent": true,
  "hobbies": ["读书", "跑步", "编程"],
  "address": {
    "city": "北京",
    "street": "长安街"
  }
}
```
### JSON方法：
​**JSON.stringify()**：将 JavaScript 对象转换为 JSON 字符串。
```javascript
var obj = {
  name: "张三",
  age: 20,
  isStudent: true
};

var jsonStr = JSON.stringify(obj);
console.log(jsonStr); // 输出 {"name":"张三","age":20,"isStudent":true}
```
​**JSON.parse()**将 JSON 字符串解析为 JavaScript 对象。
```javascript
var jsonStr = '{"name":"张三","age":20,"isStudent":true}';
var obj = JSON.parse(jsonStr);
console.log(obj.name); // 输出 "张三"
```

>[!NOTE]
>键名必须用双引号：JSON 中的键名必须用双引号包裹，单引号或没有引号都会导致解析错误。
​不支持注释：JSON 不支持注释，如果需要注释，可以在解析前删除注释内容。
​数据类型有限：JSON 仅支持字符串、数字、布尔值、数组、对象和 `null`，不支持函数、`undefined` 等。


### Browser Object Model(BOM)
BOM（Browser Object Model）​：浏览器对象模型，是 JavaScript 中用于与浏览器窗口交互的对象集合。
特点：
- BOM 提供了访问和操作浏览器窗口及其相关功能的对象。
- BOM 不是标准化的，不同浏览器可能有不同的实现。

**Window 对象**
​作用：表示浏览器窗口，是 BOM 的顶级对象。
​常用属性：

- `window.innerWidth` 和 `window.innerHeight`：获取浏览器窗口的内部宽度和高度。
- `history`:对History对象的只读引用。
- `location`:用于窗口或框架的Location对象。
- `navigator`:对Navigator对象的只读引用。

方法

- `alert()`：显示带有一段消息和确认按钮的的警告框。
- `confirm()`:显示带有一段消息以及消息确认按钮和取消按钮的对话框。
- `setInterval()`:按照指定的周期(以毫秒计)来调用函数或计算表达式。(每隔多少事件实现一次)
- `setTimeout()`:在指定的毫秒数后调用函数或计算表达式。（倒计时）

示例代码：
```javascript
// 输出浏览器窗口的宽度
console.log(window.innerWidth);

// 弹出警告框
window.alert("Hello BOM!");

// 弹出确认对话框，并根据用户选择输出结果
var flag = confirm("您确认删除该记录吗？");
alert(flag);

// 每隔 3 秒输出 i 的值
var i = 0;
setInterval(function() {
  i++;
  console.log(i);
}, 3000);

// 3 秒后弹出警告框
setTimeout(function() {
  alert("JS");
}, 3000);
```

### Document Object Model（DOM）
**文档对象模型DOM（Document Object Model）​** 是 JavaScript 中用于操作 HTML 和 XML 文档的接口。它将文档解析为一个树形结构，每个节点都是一个对象，可以通过 JavaScript 访问和操作。

![Image](https://github.com/user-attachments/assets/dfdfd4dd-c1f0-4c08-873f-cc9f03ec120a)

​树形结构：DOM 将文档解析为一个树形结构，每个节点都是一个对象。

​节点类型：
- ​文档节点（Document）​：整个文档的根节点。
- ​元素节点（Element）​：HTML 标签（如 `<div>`、`<p>`）。
- ​文本节点（Text）​：元素中的文本内容。
- ​属性节点（Attribute）​：元素的属性（如 `id`、`class`）。

​常用方法：获取元素、操作内容、操作属性、操作样式、创建和插入元素、删除元素。

事件处理：通过 `addEventListener() `为元素添加事件监听器。

示例代码：
```html

<!DOCTYPE html>
<html>
<head>
  <title>课程表</title>
  <style>
    /* 表格样式 */
    table {
      width: 100%;
      border-collapse: collapse;
      background-color: #f2f2f2; /* 灰色背景 */
      font-family: Arial, sans-serif;
    }
    th, td {
      border: 1px solid #ddd;
      padding: 8px;
      text-align: center;
    }
    th {
      background-color: #4CAF50; /* 表头绿色背景 */
      color: white; /* 表头白色文字 */
    }
    tr:nth-child(even) {
      background-color: #f9f9f9; /* 偶数行浅灰色背景 */
    }
    tr:hover {
      background-color: #e0e0e0; /* 鼠标悬停时深灰色背景 */
    }
  </style>
</head>
<body>
  <h2 style="text-align: center;">课程表</h2>
  <table id="courseTable">
    <thead>
      <tr>
        <th>学号</th>
        <th>姓名</th>
        <th>分数</th>
        <th>评语</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>001</td>
        <td>张三</td>
        <td>90</td>
        <td>很优秀</td>
      </tr>
      <tr>
        <td>002</td>
        <td>李四</td>
        <td>92</td>
        <td>优秀</td>
      </tr>
      <tr>
        <td>003</td>
        <td>王五</td>
        <td>83</td>
        <td>很努力，不错</td>
      </tr>
      <tr>
        <td>004</td>
        <td>赵六</td>
        <td>98</td>
        <td>666</td>
      </tr>
    </tbody>
  </table>

  <div style="text-align: center; margin-top: 20px;">
    <button onclick="changeContent()">修改第一行内容</button>
    <button onclick="addRow()">添加新行</button>
    <button onclick="changeStyle()">修改表头样式</button>
  </div>

  <script>
    // 修改第一行内容
    function changeContent() {
      var firstRow = document.querySelector("#courseTable tbody tr:first-child");
      firstRow.cells[0].textContent = "010"; // 修改学号
      firstRow.cells[1].textContent = "小明"; // 修改姓名
      firstRow.cells[2].textContent = "95"; // 修改分数
      firstRow.cells[3].textContent = "进步很大"; // 修改评语
    }

    // 添加新行
    function addRow() {
      var tbody = document.querySelector("#courseTable tbody");
      var newRow = document.createElement("tr");

      newRow.innerHTML = `
        <td>005</td>
        <td>小红</td>
        <td>88</td>
        <td>继续加油</td>
      `;

      tbody.appendChild(newRow);
    }

    // 修改表头样式
    function changeStyle() {
      var headers = document.querySelectorAll("#courseTable th");
      headers.forEach(function(header) {
        header.style.backgroundColor = "#FF5733"; // 修改背景颜色
        header.style.color = "#FFF"; // 修改文字颜色
        header.style.fontSize = "18px"; // 修改字体大小
      });
    }
  </script>
</body>
</html>
```
DOM中的三个部分：
**Core DOM**所有文档类型的标准模型。
- ​Document：整个文档对象。
- ​Element：元素对象。
- ​Attribute：属性对象。
- ​Text：文本对象。
- ​Comment：注释对象。

**XML DOM**XML 文档的标准模型。

**HTML DOM**HTML 文档的标准模型.
- ​Image：`<img>` 标签。
- ​Button：`<input type="button">` 标签。

DOM常用方法：
- `document.getElementById()` 通过` id `获取元素。
- `document.getElementsByClassName()`通过 class 获取元素集合。
- `document.getElementsByTagName()`通过标签名获取元素集合。
- `document.querySelector()`通过 CSS 选择器获取第一个匹配的元素。
- `document.querySelectorAll()`通过 CSS 选择器获取所有匹配的元素。
- `getAttribute()`、`setAttribute()`、`removeAttribute()`获取修改操作元素的属性值。

### 事件监听

两种方法：
直接在 HTML 标签中定义事件属性
```html
<button onclick="alert('按钮被点击了！')">点击我</button>
```
使用 `addEventListener() `方法为元素添加事件监听。
```javascript
var button = document.querySelector("button");
button.addEventListener("click", function() {
  alert("按钮被点击了！");
});
```

