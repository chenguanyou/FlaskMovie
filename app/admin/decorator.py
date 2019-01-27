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
from flask import abort
from functools import wraps

from app.models import Admin
from app.models import Role
from app.models import Auth


# 用于访问权限控制
def admin_login_req(fun):
    @wraps(fun)
    def decorator_function(*args, **kwargs):
        if not session.get("admin", None) or session["admin"] is None:
            return redirect(url_for('admin.login', next=request.url))
        return fun(*args, **kwargs)

    return decorator_function


# 权限控制装饰器
def admin_auth(f):
    @wraps(f)
    def decorator_function(*args, **kwargs):
        admin = Admin.query.join(Role).filter(Role.id == Admin.role_id, Admin.id == session['admin_id']).first()
        if admin is not None:
            auths = admin.role.auths
            auths = list(map(lambda v: int(v), str(auths).split(',')))
            auth_list = Auth.query.all()
            urls = [v.url for v in auth_list for val in auths if val == v.id]
            roule = request.url_rule
            # 如果roule不在urls里面就导出404错误
            if str(roule) not in urls:
                abort(404)
        return f(*args, **kwargs)

    return decorator_function
