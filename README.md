<img src="frontend\lextool\static\tools.png" />
<h1 align="left">LexTools</h1>
<p align="left">工具合集</p>
<p align="left">
    <a href="https://github.com/Prolht/Tools/blob/master/LICENSE">
        <img src="https://badgen.net/github/license/micromatch/micromatch" alt="MIT License" />
    </a>
    <a href="https://vuejs.org/">
        <img src="https://img.shields.io/badge/nuxt.js-v5.x-green.svg" alt="for Nuxt.js 5">
    </a>
    <a href="https://www.lex666.online/">
        <img src="https://badgen.net/badge/author/Lex/f2a" alt="Author">
    </a>
    <a href="http://tools.lex666.online/">
        <img src="https://img.shields.io/badge/%F0%9F%9A%80-open--in--browser-e10079.svg" alt="Live Demo">
    </a>
    <a>
        <img src="https://badgen.net/badge/icon/npm?icon=npm&label" alt="npm">
    </a>
</p>


### 工具合集
#### 说明
自己做的或收集的工具合集，项目持续更新中。。。
#### 技术栈
- 前端：vue全家桶 + nuxt
- 后端：Flask
- 数据库：MySQL

## 部署
### 后端
1、准备工作
 - conda虚拟环境
 - 安装依赖包
 ```py
 pip install -r requirements.txt
 ```

 2、 启动
 ```py
 python run.py
 ```

### 前端
1、准备工作
安装装[PM2](http://menvscode.com/detail/5ce21943e8c50a0870f41983)

2、项目clone到服务器
```bash
git clone git@github.com:Prolht/Tools.git
```

3、运行
cd进入改目录下，安装依赖：
```bash
npm install
npm run build
```
运行项目命令(若用pm则可省)
```bash
npm start
```
此时运行的是 http://localhost:3000

4、pm2开启进程守护
```bash
pm2 start npm --name lextool -- start
# lextool 是项目名称 在package.json中
```

5、修改项目，重新打包，然后重新部署，则需要重新启动 pm2
```bash
pm2 stop lextool   // 先停止

pm2 restart lextool  // 再重启
```

> 前端致敬 [MikuTools](https://tools.miku.ac/)

### 广告时间：
Github：[https://github.com/Prolht](https://github.com/Prolht) 点个star哟！

个人博客：[https://www.lex666.online](https://www.lex666.online)

新浪微博： [https://weibo.com/u/2415026333](https://weibo.com/u/2415026333)

微信公众号：Pylexton
<img src="https://yanxuan.nosdn.127.net/6d37e093859295a57cf7a1c9be5ad3b6.jpg" alt="" width="100" height="100" align="bottom" />
欢迎关注！

