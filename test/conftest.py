#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 2020/8/8 9:38
@Author  : lex(luohai2233@163.com)
@File    : conftest.py
@Software: PyCharm
"""


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def register(self, username='test', email='test@test.com', password='123456'):
        return self._client.post(
            '/user/register',
            data={
                "username": username,
                "email": email,
                "password": password
            }
        )

    def login(self, username='test', password='test'):
        return self._client.post(
            '/user/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
