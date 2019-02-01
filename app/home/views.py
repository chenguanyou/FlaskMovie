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
from app.models import Tag
from app.models import User
from app.models import Movie
from app.models import UserLog
from app.models import Comment
from app.models import MovieCol
from app.models import PreView

from app.home.forms import RegisterForm  # 导入注册表单验证
from app.home.forms import LoginForm  # 登陆表单验证
from app.home.forms import UserForm  # 导入会员中心的表单验证
from app.home.forms import PwdForm  # 修改密码表单验证
from app.home.forms import CommentForms  # 评论验证表单

from werkzeug.security import generate_password_hash  # 导入加密工具
from app.home.decorator import user_login_req  # 登陆验证装饰器
from app.admin.updata import change_filename  # 导入修改上传头像的名称


@home.route("/<int:page>", methods=["GET"])
def index(page=1):
    tid = request.args.get("tid", 0)  # 标签
    star = request.args.get("star", 0)  # 星级
    time = request.args.get("time", 0)  # 上映时间
    pm = request.args.get("pm", 0)  # 播放数量
    cm = request.args.get("cm", 0)  # 评论数量
    tages = Tag.query.all()  # 获取所有的标签
    movie = Movie.query
    p = dict(
        tid=tid,
        star=star,
        time=time,
        pm=pm,
        cm=cm
    )
    datanum = {k: int(v) for k, v in p.items() if int(v) > 0}
    if datanum.get('tid'):
        movie = movie.filter_by(tag_id=datanum.get('tid'))
    if datanum.get('star'):
        movie = movie.filter_by(star=datanum.get('star'))
    if datanum.get('time'):
        if datanum.get('time') == 1:
            movie = movie.order_by(Movie.addtime.desc())
        if datanum.get('time') == 2:
            movie = movie.order_by(Movie.addtime.asc())

    if datanum.get('pm'):
        if datanum.get('pm') == 1:
            movie = movie.order_by(Movie.playnum.desc())
        if datanum.get('pm') == 2:
            movie = movie.order_by(Movie.playnum.asc())

    if datanum.get('cm'):
        if datanum.get('cm') == 1:
            movie = movie.order_by(Movie.commentnum.desc())
        if datanum.get('cm') == 2:
            movie = movie.order_by(Movie.commentnum.asc())
    page_data = movie.paginate(page=int(page), per_page=10)
    return render_template("home/index.html", tages=tages, p=p, page_data=page_data)


# 电影播放
@home.route("/play/<int:id>", methods=["GET", "POST"])
@user_login_req
def play(id=None):
    if id is not None:
        form = CommentForms()
        play_movie = Movie.query.filter_by(id=int(id)).first()
        if play_movie is None:
            return redirect(url_for('home.index', page=1))
        # 播放数量加一
        play_movie.playnum += 1
        db.session.add(play_movie)
        db.session.commit()
        # 获取当前电影的评论-==
        commit = Comment.query.filter_by(movie_id=id).order_by(Comment.addtime.desc())
        # 添加评论
        if request.method == "POST":
            if form.validate_on_submit():
                data = form.data
                comment = Comment(
                    content=data.get('content'),
                    movie_id=id,
                    user_id=session['user_id']
                )
                db.session.add(comment)
                db.session.commit()
                return redirect(url_for('home.play', id=id))
    return render_template("home/play.html", play_movie=play_movie, commit=commit, form=form)


# 电影搜索
@home.route("/search/<int:page>", methods=["GET"])
def search(page=1):
    key = request.args.get("key", None)
    if key is None:
        key = session.get('key')
    else:
        session['key'] = key
    page_data = Movie.query.filter(Movie.title.ilike("%" + key + "%")).order_by(Movie.addtime.desc())
    page_data = page_data.paginate(page=page, per_page=10)
    search_num = len(page_data.items)
    return render_template("home/search.html", page_data=page_data, key=key, search_num=search_num)


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


# 会员中心
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


# 评论列表
@home.route("/comments/<int:page>", methods=["GET"])
@user_login_req
def comments(page=1):
    data_page = Comment.query.filter_by(user_id=session.get('user_id')).order_by(Comment.addtime.desc()).paginate(
        page=page, per_page=10)
    return render_template("home/comments.html", data_page=data_page)


# 登陆日志
@home.route("/loginlog/", methods=["GET"])
@user_login_req
def loginlog():
    data_page = UserLog.query.filter_by(user_id=session.get('user_id')).order_by(UserLog.add_time.desc())[:10]
    return render_template("home/loginlog.html", data_page=data_page)


# 获取用户收藏的电影
@home.route("/moviecol/<int:page>", methods=["GET"])
@user_login_req
def moviecol(page=1):
    data_page = MovieCol.query.filter_by(user_id=session.get('user_id')).order_by(MovieCol.addtime.desc()).paginate(
        page=page, per_page=1)
    return render_template("home/moviecol.html", data_page=data_page)


@home.route("/animation/")
def animation():
    preview_data = PreView.query.all()
    return render_template("home/animation.html", data=preview_data)
