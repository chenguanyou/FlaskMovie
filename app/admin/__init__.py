#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 11:59
# @User    : zhunishengrikuaile
# @File    : __init__.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: TheMovie
from flask import Blueprint

admin = Blueprint("admin", __name__)

import app.admin.views
