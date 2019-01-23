#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 11:57
# @User    : zhunishengrikuaile
# @File    : __init__.py.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: TheMovie
from flask import Flask

app = Flask(__name__)
app.debug = True

from app.admin import admin
from app.home import home

app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(home)
