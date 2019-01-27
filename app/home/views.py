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
from flask import flash  # 消息闪现
from flask import session
from flask import url_for  # url生成器

from app import db
from app import app
from app.models import User

from app.home.forms import RegisterForm  # 导入注册表单验证
from werkzeug.security import generate_password_hash  # 导入加密工具


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


@home.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            pwd=generate_password_hash(data.get('pwd')),
            info="他很懒，什么也没有填写！"
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功")
        # 进行登陆并且保存session
        session["user"] = data.get('name')
        session["user_id"] = user.id
        return redirect(url_for('home.index'))
    return render_template("home/register.html", form=form)


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
