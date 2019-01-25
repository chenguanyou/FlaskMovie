#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 12:00
# @User    : zhunishengrikuaile
# @File    : views.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: TheMovie
import os
from app import app
from app import db
from app.admin import admin
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash  # 消息闪现
from flask import session  # 登陆成功后建立会话
from app.admin.forms import LoginForm  # 导入自定义的账号密码验证器
from app.admin.forms import TagForm  # 导入标签验证表单
from app.admin.forms import MovieForm  # 导入电影添加验证表单
from app.models import Admin  # 导入管理员数据库模型
from app.models import Tag  # 导入标签数据库模型
from app.models import Movie  # 导入电影数据库模型
from app.admin.decorator import admin_login_req  # 导入访问权限装饰器

from app.admin.updata import change_filename  # 更改长传的文件名


# 首页视图
@admin.route("/")
@admin_login_req
def index():
    return render_template("admin/index.html")


# 登陆
@admin.route("/login/", methods=['GET', 'POST'])
def login():
    # 进行表单实例化
    form = LoginForm()
    # 提交表单的时候进行验证
    if form.validate_on_submit():
        # 获取表单的账号密码
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        if not admin.check_pwd(data["pwd"]):
            flash("密码错误")
            return redirect(url_for("admin.login"))
        # 账号密码正确
        session["admin"] = data["account"]
        return redirect(url_for("admin.index"))
    return render_template("admin/login.html", form=form)


# 退出
@admin.route("/logout/")
@admin_login_req
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


@admin.route("/pwd/")
@admin_login_req
def pwd():
    return render_template("admin/pwd.html")


# 添加标签
@admin.route("/tagadd/", methods=['GET', 'POST'])
@admin_login_req
def tagAdd():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tagnum = Tag.query.filter_by(name=data.get('name', None)).count()
        if tagnum != 0:
            flash("标签重复")
            return redirect(url_for("admin.tagAdd"))
        newtag = Tag(
            name=data.get('name'),

        )
        # 不管是修改或者是增加一定要进行提交，不然是不会生效的
        db.session.add(newtag)
        db.session.commit()
        flash("标签添加成功")
        return redirect(url_for("admin.tagAdd"))
    return render_template("admin/tag_add.html", form=form)


# 展示标签列表
@admin.route('/taglist/<int:page>/', methods=['GET'])
@admin_login_req
def tagList(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(Tag.addtime.desc()).paginate(page=page, per_page=5)  # 查询数据并进行分页

    return render_template('admin/tag_list.html', page_data=page_data)


# 标签的删除
@admin.route('/tagdel/<int:id>/', methods=['GET'])
@admin_login_req
def tagDel(id=None):
    if id is not None:
        tag = Tag.query.filter_by(id=id).first_or_404()
        db.session.delete(tag)
        db.session.commit()
        flash("删除成功")
        return redirect(url_for("admin.tagList", page=1))


# 标签的编辑
@admin.route("/tagedit/<int:id>", methods=['GET', 'POST'])
@admin_login_req
def tagEdit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tagnum = Tag.query.filter_by(name=data.get('name', None)).count()
        if tag.name != data.get('name') and tagnum == 1:
            flash("标签重复")
            return redirect(url_for("admin.tagEdit", id=id))
        tag.name = data.get('name')
        # 不管是修改或者是增加一定要进行提交，不然是不会生效的.
        db.session.add(tag)
        db.session.commit()
        flash("标签编辑成功")
        return redirect(url_for("admin.tagEdit", id=id))
    return render_template("admin/tag_edit.html", form=form, tag=tag)


# 添加电影
@admin.route("/movieAdd/", methods=["GET", "POST"])
@admin_login_req
def movieAdd():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        # 获取到视频的地址
        file_url = form.url.data.filename
        # 获取到封面文件
        file_logo = form.logo.data.filename
        # 定义文件的保存
        # 文件是否存在
        if not os.path.exists(app.config['UP_DIR']):
            # 如果不存在就创建
            os.mkdir(app.config['UP_DIR'])
        # 对视频的名称进行重命名
        url = change_filename(file_url)
        # 对封面图片进行重命名
        logo = change_filename(file_logo)
        # 保存视频
        form.url.data.save(app.config["UP_DIR"] + url)
        # 保存封面
        form.logo.data.save(app.config["UP_DIR"] + logo)
        movie = Movie(
            title=data.get('title'),
            url=url,
            info=data.get('info'),
            logo=logo,
            star=int(data.get('star')),
            playnum=0,
            commentnum=0,
            tag_id=int(data.get('tag_id')),
            arga=data.get('arga'),
            release_time=data.get('release_time'),
            length=data.get('length')
        )
        db.session.add(movie)
        db.session.commit()
        flash("电影添加成功")
        return redirect(url_for("admin.movieAdd"))
    return render_template("admin/movie_add.html", form=form)


# 电影列表
@admin.route("/movieList/<int:page>", methods=["GET", "POST"])
@admin_login_req
def movieList(page=None):
    if page is None:
        page = 1
    page_data = Movie.query.order_by(Movie.addtime.desc()).paginate(page=page, per_page=10)  # 查询到数据进行分页
    return render_template("admin/movie_list.html", page_data=page_data)


# 电影删除
@admin.route("/movieDelete/<int:id>", methods=["GET", "POST"])
@admin_login_req
def movieDelete(id=None):
    if id is not None:
        movie = Movie.query.filter_by(id=id).first_or_404()
        # 删除视频文件
        os.remove(app.config["UP_DIR"] + movie.url)
        # 删除封面图
        os.remove(app.config["UP_DIR"] + movie.logo)
        db.session.delete(movie)
        db.session.commit()
        flash("删除成功")
    return redirect(url_for("admin.movieList", page=1))


@admin.route("/previewAdd/")
@admin_login_req
def previewAdd():
    return render_template("admin/preview_add.html")


@admin.route("/previewList/")
@admin_login_req
def previewList():
    return render_template("admin/preview_list.html")


@admin.route("/userList/")
@admin_login_req
def userList():
    return render_template("admin/user_list.html")


@admin.route("/commentList/")
@admin_login_req
def commentList():
    return render_template("admin/comment_list.html")


@admin.route("/moviecolList/")
@admin_login_req
def moviecolList():
    return render_template("admin/moviecol_list.html")


@admin.route("/oplogList/")
@admin_login_req
def oplogList():
    return render_template("admin/oplog_list.html")


@admin.route("/adminLoginLogList/")
@admin_login_req
def adminLoginLogList():
    return render_template("admin/adminloginlog_list.html")


@admin.route("/userLoginLogList/")
@admin_login_req
def userLoginLogList():
    return render_template("admin/userloginlog_list.html")


@admin.route("/authAdd/")
@admin_login_req
def authAdd():
    return render_template("admin/auth_add.html")


@admin.route("/authList/")
@admin_login_req
def authList():
    return render_template("admin/auth_list.html")


@admin.route("/roleAdd/")
@admin_login_req
def roleAdd():
    return render_template("admin/role_add.html")


@admin.route("/roleList/")
@admin_login_req
def roleList():
    return render_template("admin/role_list.html")


@admin.route("/adminadd/")
@admin_login_req
def adminAdd():
    return render_template("admin/admin_add.html")


@admin.route("/adminlist")
@admin_login_req
def adminList():
    return render_template("admin/admin_list.html")
