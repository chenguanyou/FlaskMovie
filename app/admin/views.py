#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 12:00
# @User    : zhunishengrikuaile
# @File    : views.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: TheMovie
from app.admin import admin
from flask import render_template
from flask import redirect
from flask import url_for


@admin.route("/")
def index():
    return render_template("admin/index.html")


@admin.route("/login/")
def login():
    return render_template("admin/login.html")


@admin.route("/pwd/")
def pwd():
    return render_template("admin/pwd.html")


@admin.route("/tagadd/")
def tagAdd():
    return render_template("admin/tag_add.html")


@admin.route("/taglist/")
def tagList():
    return render_template("admin/tag_list.html")


@admin.route("/movieAdd/")
def movieAdd():
    return render_template("admin/movie_add.html")


@admin.route("/movieList/")
def movieList():
    return render_template("admin/movie_list.html")


@admin.route("/previewAdd/")
def previewAdd():
    return render_template("admin/preview_add.html")


@admin.route("/previewList/")
def previewList():
    return render_template("admin/preview_list.html")


@admin.route("/userList/")
def userList():
    return render_template("admin/user_list.html")


@admin.route("/commentList/")
def commentList():
    return render_template("admin/comment_list.html")


@admin.route("/moviecolList/")
def moviecolList():
    return render_template("admin/moviecol_list.html")


@admin.route("/oplogList/")
def oplogList():
    return render_template("admin/oplog_list.html")


@admin.route("/adminLoginLogList/")
def adminLoginLogList():
    return render_template("admin/adminloginlog_list.html")


@admin.route("/userLoginLogList/")
def userLoginLogList():
    return render_template("admin/userloginlog_list.html")


@admin.route("/authAdd/")
def authAdd():
    return render_template("admin/auth_add.html")


@admin.route("/authList/")
def authList():
    return render_template("admin/auth_list.html")


@admin.route("/roleAdd/")
def roleAdd():
    return render_template("admin/role_add.html")


@admin.route("/roleList/")
def roleList():
    return render_template("admin/role_list.html")


@admin.route("/adminadd/")
def adminAdd():
    return render_template("admin/admin_add.html")


@admin.route("/adminlist")
def adminList():
    return render_template("admin/admin_list.html")
