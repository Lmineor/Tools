#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 2020/12/13 20:21
@Author  : lex(luohai2233@163.com)
"""

from flask import (Blueprint, request,
                   jsonify, g, redirect)

from oocfg import cfg

from backend.lextool.auth import auth
from backend.lextool.common.logger import LOG
from backend.lextool.models import db
from backend.lextool.models.user import User
from backend.lextool.models.user import UserMemo
from backend.lextool.models.user import UserConfig
from backend.lextool.utils.tasks import send_register_active_email
from backend.lextool.common.constants import LOGINURL


identity = Blueprint('auth', __name__)


@identity.route('/logout', methods=['DELETE'])
@auth.login_required
def logout():
    username = request.get_json()['username']
    email = request.get_json()['email']
    LOG.info("User: {}, Email: {} logout.".format(username, email))
    return jsonify({'code': 200, 'description': 'Logout successful.'})


@identity.route('/register', methods=['POST'])
def register():
    """
    用户注册
    """
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = request.get_json()['password']
    try:
        user = User.query.filter_by(email=email).first()
        if user and not user.activate:
            # 用户已经注册，但是未点击激活链接，则重新生成激活链接并发送邮件
            # 先更新密码与用户
            user.password = password
            user.username = username

            token = user.generate_auth_token(expiration=5*60).decode('ascii')  # 此时token过期时间为5分钟
            send_register_active_email(user.email, user.username, token)
            msg = "注册成功,激活链接已发送到你注册时的邮箱，请及时激活"
            res = {
                'code': 200,
                'msg': msg
            }
        elif user and user.activate:
            # 用户已经注册，且已经激活
            msg = "该邮箱已经注册过，换个邮箱试试吧！"
            res = {
                'code': 401,
                'msg': msg
            }
        else:
            # 用户尚未注册
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.flush()
            config = UserConfig(role=False, user_id=user.id)
            db.session.add(config)
            memo = UserMemo(user_id=user.id)
            db.session.add(memo)
            db.session.commit()
            token = user.generate_auth_token(expiration=5 * 60).decode('ascii')  # 此时token过期时间为5分钟
            send_register_active_email(user.email, user.username, token)
            msg = "注册成功,激活链接已发送到你注册时的邮箱，请及时激活"
            res = {
                'code': 200,
                'msg': msg
            }
    except Exception as e:
        LOG.error(e)
        msg = "未知错误，请稍后再试，或直接发邮件到luohai2233@163.com"
        res = {
            'code': 404,
            'msg': msg
        }
    return jsonify(res)


@identity.route('/active/<token>', methods=['GET'])
def activate(token):
    """
    激活
    :return: None
    """
    if User.check_activate_token(token):
        return redirect('http://' + cfg.CONF.EMAIL.front_domain + '/login')
    else:
        return jsonify({'code': 401, 'msg': "令牌失效，请重新注册"})


@auth.verify_password
def verify_password(email_or_token, password):
    if request.path == LOGINURL:
        user = User.query.filter_by(email=email_or_token).first()
        if not user or not user.check_password_hash(password) or not user.activate:
            return False
    else:
        user = User.verify_auth_token(email_or_token)
        if not user:
            return False
    g.user = user
    return True


@identity.route('/login', methods=['POST'])
@auth.login_required
def get_auth_token():
    LOG.debug("User %s login" % g.user.username)
    token = g.user.generate_auth_token()
    username = g.user.username
    return jsonify({'token': token.decode('ascii'), 'username': username})
