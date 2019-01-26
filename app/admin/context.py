#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/26 21:46
# @User    : zhunishengrikuaile
# @File    : context.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: TheMovie
# 上下文处理器，可以封装全局变量，把全局变量展现到模板里面

from app.admin import admin
from datetime import datetime


@admin.context_processor
def tpl_extra():
    data = dict(
        online_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S "),
    )

    return data
