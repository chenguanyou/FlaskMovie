#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 12:00
# @User    : zhunishengrikuaile
# @File    : views.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: TheMovie
from app import db
from app.admin import admin
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash  # 消息闪现
from flask import session  # 登陆成功后建立会话
from app.admin.forms import LoginForm  # 导入自定义的账号密码验证器
from app.admin.forms import TagForm  # 导入标签验证表单
from app.models import Admin  # 导入管理员数据库模型
from app.models import Tag  # 导入标签数据库模型
from app.admin.decorator import admin_login_req  # 导入访问权限装饰器


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
    # Tag.addtime.desc()  # 按照时间排序
    # paginate(page=page, per_page=5) page是页数，per_page每页显示的数据数量
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
        # 不管是修改或者是增加一定要进行提交，不然是不会生效的
        db.session.add(tag)
        db.session.commit()
        flash("标签编辑成功")
        return redirect(url_for("admin.tagEdit", id=id))
    return render_template("admin/tag_edit.html", form=form, tag=tag)


@admin.route("/movieAdd/")
@admin_login_req
def movieAdd():
    return render_template("admin/movie_add.html")


@admin.route("/movieList/")
@admin_login_req
def movieList():
    return render_template("admin/movie_list.html")


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
