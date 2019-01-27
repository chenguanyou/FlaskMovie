#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/27 18:29
# @User    : zhunishengrikuaile
# @File    : decorator.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: TheMovie
# 用户登陆控制权限
from functools import wraps
from flask import session
from flask import redirect
from flask import url_for
from flask import request


# 用于访问权限控制
def user_login_req(fun):
    @wraps(fun)
    def decorator_function(*args, **kwargs):
        if not session.get("user", None) or session["user"] is None:
            return redirect(url_for('home.login', next=request.url))
        return fun(*args, **kwargs)

    return decorator_function
