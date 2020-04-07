#!/bin/bash
# config variables
PROJECT_PATH = /www/wwwroot/Tools/frontend/lextool
PROJECT_NAME = lextools
GIT = git@github.com:Prolht/Tools.git


# stop and pull
pm2 stop $PROJECT_NAME
cd $PROJECT_PATH
git pull

# install dependence & build
npm run install
npm run build

# restart
pm2 restart $PROJECT_NAME