在游戏中，如果想实现不同分辨率下，都可以支持当前的UI界面布局，都需要用到锚点功能。
‌[虚幻引擎](https://www.baidu.com/s?sa=re_dqa_generate&wd=%E8%99%9A%E5%B9%BB%E5%BC%95%E6%93%8E&rsv_pq=ca8de6dd007d16af&oq=%E8%99%9A%E5%B9%BB%E5%BC%95%E6%93%8Eui%E9%94%9A%E7%82%B9%E6%98%AF%E4%BB%80%E4%B9%88&rsv_t=51d7gQl1KDGIFZHot4xxk8eoDFmMyx2fKF46n5XUr4N9FLnLgEu0uIVIDyzrutkjPI9DBew&tn=15007414_12_dg&ie=utf-8)中的UI锚点（Anchor）是指控件在屏幕或父物体上的固定点，用于确定控件的位置和布局。‌ 锚点的作用是确保UI元素在屏幕缩放或形变时保持相对位置不变。

在虚幻引擎中，锚点可以理解为将子物体“挂”在父物体上的点。当父物体的位置或大小发生变化时，子物体的位置会相应地调整，保持它们之间的相对关系不变。锚点的位置可以在屏幕的任意角落，通常用于自适应屏幕尺寸和保持布局的稳定性‌。
具体来说，锚点有以下几种情况：
- 当锚点与父物体的某个顶点重合时，子物体在该点的位置不会改变，只有当父物体该点位置改变时，子物体才会跟着移动。
- 如果锚点不重合，子物体在父物体变形时会跟着缩放，保持与父物体各顶点的距离不变‌。

### 具体实现：
错误的UI锚点设置方法如下：

​​![image](https://github.com/user-attachments/assets/2d3e3cde-9b50-40bb-a8d5-fe2c12647b91)

如上图为锚点设置不准确，导致缩放时出现屏幕空缺

![image](https://github.com/user-attachments/assets/42bf721a-4ec0-4135-bf1b-a2a7abfd22a0)

将锚点修改为下图所示：

![image](https://github.com/user-attachments/assets/ab5e0012-f628-4f51-b31a-b8e8da498247)

如果想保持UI中内容部件和画布等比缩放，需要将锚点拉伸至和部件相同大小

![image](https://github.com/user-attachments/assets/49acc968-b5f1-4468-a0e6-cb2c061f37f2)

全部修改后现实正确：

![image](https://github.com/user-attachments/assets/adc0882f-78a9-4967-8a82-200f1f7a2b10)


​