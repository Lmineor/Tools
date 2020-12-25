#!/bin/bash
# author:lex<luohai2233@163.com>

CONDA_ENV=tools
PROJECT_B_BASE_PATH=/www/wwwroot/Tools/backend/     # backend

# Stop service
cd /www/wwwroot
uwsgi --stop uwsgi.pid

#git pull
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
