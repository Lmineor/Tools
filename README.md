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

Ps 目前先着重按照自己的兴趣把诗词部分做好，其他的以后有时间慢慢更新
- 前端部分为frontend分支
- 后端部分为master分支

#### 技术栈

- 前端：vue全家桶 + nuxt
- 后端：Flask
- 数据库：MySQL

## 部署

### 后端

1、准备工作
- 准备好conda虚拟环境
- 安装依赖包（切换到准备好的虚拟环境中）

```py
pip install -r requirements.txt
```

2、 数据库初始化与表创建

```py
python manage.py db init     # 初始化数据库
python manage.py db migrate # 检查模型字段是否修改,如果改变,就产生新的迁移文件.
python manage.py db upgrade # 对迁移文件进行迁移
```

3、 启动

- 方式一：传统方法，适合本地调试

```py
python run.py
```

- 方式二：nohup

```py
nohup python run.py >> server.log 2>&1 &
```

- 方式三：uwsgi的方式（暂且认为最高b格）

```py
# cd 到项目根目录然后执行
uwsgi --ini uwsgi.ini
```

### 前端
1、准备工作
安装装[PM2](http://menvscode.com/detail/5ce21943e8c50a0870f41983)

2、项目clone到服务器
```bash
git clone git@github.com:Prolht/Tools.git
```

3、运行
cd进入项目前端根目录下，安装依赖：
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
