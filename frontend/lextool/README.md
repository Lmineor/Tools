# lextool

> 工具合集

## Build Setup

```bash
# install dependencies
$ npm install

# serve with hot reload at localhost:3000
$ npm run dev

# build for production and launch server
$ npm run build
$ npm run start

# generate static project
$ npm run generate
```

For detailed explanation on how things work, check out [Nuxt.js docs](https://nuxtjs.org).

## 部署
1、准备工作
安装装[PM2](http://menvscode.com/detail/5ce21943e8c50a0870f41983)
2、项目clone到服务器
```bash
git clone xxx
```
把本地文件的.nuxt、static,package.json、nuxt.config.js，这四个文件夹放到服务器目录文件下
3、运行
cmd进入改目录下，安装依赖：
```bash
npm install
npm run build
```
运行项目命令
```bash
npm start
```
此时运行的是 http://localhost:3000

4、pm2开启进程守护
```bash
pm2 start npm --name "xxx" -- run start
# xxx 是项目名称 在package.json中
```

5、修改项目，重新打包，然后重新部署，则需要重新启动 pm2
```bash
pm2 stop xxx   // 先停止

pm2 restart xxx  // 再重启
```