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
2、nuxt打包上传
```bash
npm run build
```
把本地文件的.nuxt、static,package.json、nuxt.config.js，这四个文件夹放到服务器目录文件下
3、运行
cmd进入改目录下，安装依赖：
```bash
npm install
```
运行项目命令
```bash
npm start
```
此时运行的是 http://localhost:3000