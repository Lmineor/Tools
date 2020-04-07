#!/bin/bash
# author:lex<luohai2233@163.com>
# config variables
PROJECT_BASE_PATH=/www/wwwroot/Tools/frontend/
PROJECT_NAME=$1
GIT=git@github.com:Prolht/Tools.git

if [ $PROJECT_NAME ]
then
    # stop and pull
    pm2 stop $PROJECT_NAME
    git pull

    # install dependence & build
    cd $PROJECT_BASE_PATH$PROJECT_NAME
    npm run install
    npm run build

    # restart
    pm2 restart $PROJECT_NAME
    echo "重启完成"
else
    echo "请输入项目名称"
fi