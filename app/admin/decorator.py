#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 13:32
# @User    : zhunishengrikuaile
# @File    : decorator.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: TheMovie
from flask import redirect
from flask import url_for
from flask import request
from flask import session
from functools import wraps


# 用于访问权限控制
def admin_login_req(fun):
    @wraps(fun)
    def decorator_function(*args, **kwargs):
        if not session.get("admin", None) or session["admin"] is None:
            return redirect(url_for('admin.login', next=request.url))
        return fun(*args, **kwargs)

    return decorator_function
