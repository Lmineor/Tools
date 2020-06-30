#!/bin/bash
# author:lex<luohai2233@163.com>

# config variables
# Path
CONDA_ENV=tools
PROJECT_F_BASE_PATH=/www/wwwroot/Tools/frontend/    # frontend
PROJECT_B_BASE_PATH=/www/wwwroot/Tools/backend/     # backend
PROJECT_PORT=5000                                   # backend port
GIT=git@github.com:Prolht/Tools.git

# Frontend Name
PROJECT_NAME_F=lextool                              # frontend name


# stop backend
#lsof -i:${PROJECT_PORT}|awk '{print$2}' |grep -v PID|xargs kill -9 # 暂停
cd /www/wwwroot
uwsgi --stop uwsgi.pid

# stop frontend
pm2 stop $PROJECT_NAME_F

#pull
cd /www/wwwroot/Tools
git pull

# install dependence & build
# backend
source activate $CONDA_ENV
cd $PROJECT_B_BASE_PATH
pip install -r requirements.txt
# start
#python manage.py db init --multidb # 多个数据库
# python manage.py db init  # 只使用一次
python manage.py db migrate # 检查模型字段是否修改,如果改变,就产生新的迁移文件.
python manage.py db upgrade # 对迁移文件进行迁移
#nohup python run.py >> server.log 2>&1 &
cd ..
uwsgi --ini uwsgi.ini
echo "==================Complete Backend=================="

# frontend
cd $PROJECT_F_BASE_PATH$PROJECT_NAME_F
npm install
npm run build


# pm2 start npm --name “lextool” -- run start  # 第一次启动用
# start
pm2 start $PROJECT_NAME_F
echo "==================Complete Frontend=================="