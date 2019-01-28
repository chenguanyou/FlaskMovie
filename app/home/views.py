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
from flask import request
from flask import session
from flask import url_for  # url生成器

import os
from app import db
from app import app
from app.models import User
from app.models import UserLog

from app.home.forms import RegisterForm  # 导入注册表单验证
from app.home.forms import LoginForm  # 登陆表单验证
from app.home.forms import UserForm  # 导入会员中心的表单验证
from app.home.forms import PwdForm  # 修改密码表单验证

from werkzeug.security import generate_password_hash  # 导入加密工具
from app.home.decorator import user_login_req  # 登陆验证装饰器
from app.admin.updata import change_filename  # 导入修改上传头像的名称


@home.route("/")
def index():
    return render_template("home/index.html")


@home.route("/play/")
def play():
    return render_template("home/play.html")


@home.route("/search/")
def search():
    return render_template("home/search.html")


# 登陆
@home.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(email=data["email"]).first()
        if not user.check_pwd(data["pwd"]):
            flash("密码错误")
            return redirect(url_for("home.login"))
        # 账号密码正确
        session["user"] = data["email"]
        session["user_id"] = user.id
        userlog = UserLog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for("home.user"))
    return render_template("home/login.html", form=form)


# 退出
@home.route("/logout/")
@user_login_req
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for("home.login"))


# 注册
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
        session["user"] = data.get('email')
        session["user_id"] = user.id
        return redirect(url_for('home.user'))
    return render_template("home/register.html", form=form)


@home.route("/user/", methods=["GET", "POST"])
@user_login_req
def user():
    form = UserForm()
    user = User.query.get_or_404(session["user_id"])
    if request.method == "GET":
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        # 获取到头像文件
        face_name = form.face.data.filename
        # 判断文件夹是否存在，如果不存在就创建
        if not os.path.exists(app.config['UP_DIR'] + "/user/"):
            os.mkdir(app.config["UP_DIR"] + "/user/")
        # 对头像文件进行重命名
        face = change_filename(face_name)
        # 保存头像到本地文件
        form.face.data.save(app.config["UP_DIR"] + "/user/" + face)
        # 进行修改入库操作
        user.name = data.get('name')
        user.email = data.get('email')
        user.phone = data.get('phone')
        user.face = face
        user.info = data.get('info')
        db.session.add(user)
        db.session.commit()
        flash("资料修改成功")
        return redirect(url_for('home.user'))
    return render_template("home/user.html", form=form, user=user)


# 修改密码
@home.route("/pwd/", methods=["GET", "POST"])
@user_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(email=session.get('user')).first()
        user.pwd = generate_password_hash(data.get('newpwd'))
        db.session.add(user)
        db.session.commit()
        flash("密码修改成功, 请重新登录!")
        return redirect(url_for('home.logout'))
    return render_template("home/pwd.html", form=form)


@home.route("/comments/")
@user_login_req
def comments():
    return render_template("home/comments.html")


@home.route("/loginlog/")
@user_login_req
def loginlog():
    return render_template("home/loginlog.html")


@home.route("/moviecol/")
@user_login_req
def moviecol():
    return render_template("home/moviecol.html")


@home.route("/animation/")
def animation():
    return render_template("home/animation.html")
