#!/bin/bash
# author:lex<luohai2233@163.com>

# config variables
# Path
CONDA_ENV=tools
PROJECT_F_BASE_PATH=/www/wwwroot/Tools/frontend/ # frontend
PROJECT_B_BASE_PATH=/www/wwwroot/Tools/backend/ # backend

# Name
PROJECT_NAME_F=lextool # frontend name
# PROJECT_NAME_B=$1 # backend name
PROJECT_PORT=$1 # backend port
PROJECT_NAME_B=services
PROJECT_PORT=5000 # backend port

GIT=git@github.com:Prolht/Tools.git

if [[ $PROJECT_NAME_B && $PROJECT_PORT ]]
then
    # stop backend
    lsof -i:${PROJECT_PORT}|awk '{print$2}' |grep -v PID|xargs kill -9 # 暂停

    # stop frontend
    pm2 stop $PROJECT_NAME_F

    #pull
    git pull

    # install dependence & build
    # backend
    cd $PROJECT_B_BASE_PATH$PROJECT_NAME_B
    pip install -r requirements.txt
    # start
    source activate $CONDA_ENV
    nohup python main.py >> server.log 2>&1 &
    echo "Complete Backend"

    # frontend
    cd $PROJECT_F_BASE_PATH$PROJECT_NAME_F
    npm install
    npm run build

    # start
    pm2 restart $PROJECT_NAME_F
    echo "Complete Fronteend"
else
    echo "error!!!"
fi