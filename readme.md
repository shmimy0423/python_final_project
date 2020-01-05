期末项目介绍
===========================
姓名  |  学号 |项目URL |合作搭档
---  |  --- | --- | --- |
张铭睿  |  181013108 | https |曾拱韬 钟振升

![girl power.png](https://i.loli.net/2020/01/05/eObCn7V1mLfPGFt.png)

#### 项目背景
目前，虽然世界在性别平权方面取得了一定进展，但不同地区与领域在性别差距上仍存在不同程度的差异。

这个数据可视化项目主要目的是为了展示当前男女间在经济地位、学习机会、政治参与及医疗与生存四个范畴中的差距，

以实现在不同领域为女性赋权，针对性地提升女性权利，收窄男女间的差距。

#### 项目流程图

![liuchengtu.png](https://i.loli.net/2020/01/05/v9yK1XUeE7IfWCt.png)


#### 目录结构描述
目录 | 作用
--- | ---
Readme.md | help
static |  web静态资源加载
templates | 模块文件

#### HTML档
* base.html 基模板，定义了一个简单的 HTML 框架文档
* First.html 首页面，此页面有轮播图展示、项目介绍以及2006-2016年孕产妇死亡率世界分布图、中小学女生与男生的入学比例世界分布图、国家议会中妇女席位的比例世界分布图等。

#### Python档描述
* All.py作为程序启动页面，引用pandas、flask、plotly、pyecharts、dash模块。
1. pandas 用于数据导入及整理
2. flask 提供一个web应用后端处理的框架
3. plotly 用于数值运算与图形操作
4. pyecharts 用于生成 Echarts 图表
5. dash 构建基于web的交互式应用程序所需的所有技术和协议

* for循环语句运用

![for.png](https://i.loli.net/2020/01/05/xl95vFwCXBfi4bd.png)

* 通过路由实现页面跳转

![@.png](https://i.loli.net/2020/01/05/1jIQwsyLHZaGU98.png)

![页面.png](https://i.loli.net/2020/01/05/pqIYfb8WxwLUroG.png)

#### Web App动作描述
* 首页面设计了轮播图形式展示相关主题的图片，以吸引用户兴趣；
* 设计下拉框与按钮形成跳转。
