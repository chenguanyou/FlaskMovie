#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 12:00
# @User    : zhunishengrikuaile
# @File    : views.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: TheMovie
from app.home import home
from flask import render_template  # 导入页面渲染函数
from flask import redirect  # 退出
from flask import url_for  # url生成器


@home.route("/")
def index():
    return render_template("home/index.html")


@home.route("/play/")
def play():
    return render_template("home/play.html")


@home.route("/search/")
def search():
    return render_template("home/search.html")


@home.route("/login/")
def login():
    return render_template("home/login.html")


@home.route("/logout/")
def logout():
    return redirect(url_for("home.login"))


@home.route("/register/")
def register():
    return render_template("home/register.html")


@home.route("/user/")
def user():
    return render_template("home/user.html")


@home.route("/pwd/")
def pwd():
    return render_template("home/pwd.html")


@home.route("/comments/")
def comments():
    return render_template("home/comments.html")


@home.route("/loginlog/")
def loginlog():
    return render_template("home/loginlog.html")


@home.route("/moviecol/")
def moviecol():
    return render_template("home/moviecol.html")


@home.route("/animation/")
def animation():
    return render_template("home/animation.html")
