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
from flask import request
from flask import flash  # 消息闪现
from flask import session  # 登陆成功后建立会话

from app.admin.forms import LoginForm  # 导入自定义的账号密码验证器
from app.admin.forms import TagForm  # 导入标签验证表单
from app.admin.forms import MovieForm  # 导入电影添加验证表单
from app.admin.forms import PreViewForm  # 导入电影预告片的表单验证
from app.admin.forms import PwdForm  # 导入修改密码的表单验证
from app.admin.forms import AuthForm  # 添加权限管理的表单验证
from app.admin.forms import RoleForm  # 添加角色的表单验证
from app.admin.forms import AdminForm  # 添加管理员的表单验证

from app.models import Admin  # 导入管理员数据库模型
from app.models import Tag  # 导入标签数据库模型
from app.models import Movie  # 导入电影数据库模型
from app.models import PreView  # 导入电影预告片数据模型
from app.models import User  # 导入会员数据模型
from app.models import Comment  # 导入评论列表
from app.models import MovieCol  # 导入电影收藏数据模型
from app.models import OpLog  # 管理员操作日志
from app.models import AdminLog  # 管理员登陆日志
from app.models import UserLog  # 导入用户的登陆日志数据模型
from app.models import Auth  # 添加权限数据库模型
from app.models import Role  # 导入角色数据库模型

from app.admin.decorator import admin_login_req  # 导入访问权限装饰器
from app.admin.updata import change_filename  # 更改长传的文件名
from werkzeug.security import generate_password_hash  # 密码加密工具
from app.admin.context import tpl_extra  # 导入全局上下文管理器


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
        session["admin_id"] = admin.id
        adminlog = AdminLog(
            admin_id=admin.id,
            ip=request.remote_addr
        )
        db.session.add(adminlog)
        db.session.commit()
        return redirect(url_for("admin.index"))
    return render_template("admin/login.html", form=form)


# 退出
@admin.route("/logout/")
@admin_login_req
def logout():
    session.pop('admin', None)
    session.pop('admin_id', None)
    return redirect(url_for('admin.login'))


# 修改密码
@admin.route("/pwd/", methods=["GET", "POST"])
@admin_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        name = session.get("admin")
        admin = Admin.query.filter_by(name=name).first()
        print(admin)
        admin.pwd = generate_password_hash(data.get('new_pwd'))
        db.session.add(admin)
        db.session.commit()
        flash("密码修改成功，请重新登录")
        return redirect(url_for('admin.logout'))
    return render_template("admin/pwd.html", form=form)


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
        oplog = OpLog(
            admin_id=session.get("admin_id"),
            ip=request.remote_addr,
            reason="添加标签：{tag}".format(tag=data.get('name'))
        )
        db.session.add(oplog)
        db.session.commit()
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
        oplog = OpLog(
            admin_id=session.get("admin_id"),
            ip=request.remote_addr,
            reason="删除标签：{tag}".format(tag=tag.name)
        )
        db.session.add(oplog)
        db.session.commit()
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
        oplog = OpLog(
            admin_id=session.get("admin_id"),
            ip=request.remote_addr,
            reason="编辑标签：{tag}-->{new_tag}".format(tag=tag.name, new_tag=data.get('name'))
        )
        db.session.add(oplog)
        db.session.commit()
        tag.name = data.get('name')

        # 不管是修改或者是增加一定要进行提交，不然是不会生效的.
        db.session.add(tag)
        db.session.commit()
        flash("标签编辑成功")
        return redirect(url_for("admin.tagEdit", id=id))
    return render_template("admin/tag_edit.html", form=form, tag=tag)


# 添加电影
@admin.route("/movieAdd/", methods=["GET", "POST"])
# @admin_login_req
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
        oplog = OpLog(
            admin_id=session.get("admin_id"),
            ip=request.remote_addr,
            reason="添加电影：{movie}".format(movie=data.get("title"))
        )
        db.session.add(oplog)
        db.session.commit()
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
        oplog = OpLog(
            admin_id=session.get("admin_id"),
            ip=request.remote_addr,
            reason="删除电影：{movie}".format(movie=movie.title)
        )
        db.session.add(oplog)
        db.session.commit()
    return redirect(url_for("admin.movieList", page=1))


# 电影信息的编辑
@admin.route("/movieEdit/<int:id>", methods=["GET", "POST"])
@admin_login_req
def movieEdit(id=None):
    if id is not None:
        form = MovieForm()
        movie = Movie.query.get_or_404(id)
        movie_title = movie.title
        if request.method == "GET":
            form.info.data = movie.info
            form.star.data = movie.star
            form.tag_id.data = movie.tag_id
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
            # 删除之前的数据, 如果文件不存在，有可能抛出异常
            try:
                # 删除视频文件
                os.remove(app.config["UP_DIR"] + movie.url)
                # 删除封面图
                os.remove(app.config["UP_DIR"] + movie.logo)
            except:
                pass
            movie.title = data.get('title')
            movie.url = url
            movie.info = data.get('info')
            movie.logo = logo
            movie.star = int(data.get('star'))
            movie.tag_id = int(data.get('tag_id'))
            movie.arga = data.get('arga')
            movie.release_time = data.get('release_time')
            movie.length = data.get('length')
            db.session.add(movie)
            db.session.commit()
            flash("电影修改成功")
            oplog = OpLog(
                admin_id=session.get("admin_id"),
                ip=request.remote_addr,
                reason="编辑电影：{movie_title}-->{movie}".format(movie_title=movie_title, movie=data.get('title'))
            )
            db.session.add(oplog)
            db.session.commit()
            return redirect(url_for("admin.movieEdit", id=id))
        return render_template("admin/movie_edit.html", form=form, movie=movie)


# 添加预告片
@admin.route("/previewAdd/", methods=["GET", "POST"])
@admin_login_req
def previewAdd():
    form = PreViewForm()
    if form.validate_on_submit():
        data = form.data
        # 获取到封面文件
        file_logo = form.logo.data.filename

        # 判断文件夹是否存在
        if not os.path.exists(app.config['UP_DIR']):
            # 如果不存在就创建
            os.mkdir(app.config['UP_DIR'])
        # 对封面文件进行重名了
        logo = change_filename(file_logo)
        # 保存封面文件
        form.logo.data.save(app.config['UP_DIR'] + logo)
        preview = PreView(
            title=data.get('title'),
            logo=logo
        )
        db.session.add(preview)
        db.session.commit()
        flash("预告片添加成功")
        oplog = OpLog(
            admin_id=session.get("admin_id"),
            ip=request.remote_addr,
            reason="添加预告片：{preview}".format(preview=data.get('title'))
        )
        db.session.add(oplog)
        db.session.commit()
    return render_template("admin/preview_add.html", form=form)


# 预告片列表
@admin.route("/previewList/<int:page>", methods=["GET"])
@admin_login_req
def previewList(page=None):
    if page is None:
        page = 1
    page_data = PreView.query.order_by(PreView.addtime.desc()).paginate(page=page, per_page=10)  # 查询到数据进行分页
    return render_template("admin/preview_list.html", page_data=page_data)


# 预告片删除
@admin.route("/previewDel/<int:id>", methods=["GET", "POST"])
@admin_login_req
def perViewDel(id=None):
    if id is not None:
        preview = PreView.query.filter_by(id=id).first_or_404()
        # 删除封面图
        os.remove(app.config['UP_DIR'] + preview.logo)
        oplog = OpLog(
            admin_id=session.get("admin_id"),
            ip=request.remote_addr,
            reason="删除预告片：{preview}".format(preview=preview.title)
        )
        db.session.add(oplog)
        db.session.commit()

        # 提交删除数据
        db.session.delete(preview)
        db.session.commit()
        flash("删除成功")
    return redirect(url_for('admin.previewList', page=1))


# 预告片的编辑
@admin.route("/previewEdit/<int:id>", methods=["GET", "POST"])
@admin_login_req
def perViewEdit(id=None):
    if id is not None:
        form = PreViewForm()
        preview = PreView.query.get_or_404(id)
        if form.validate_on_submit():
            data = form.data
            # 获取到封面文件
            file_logo = form.logo.data.filename

            # 判断文件夹是否存在
            if not os.path.exists(app.config['UP_DIR']):
                # 如果不存在就创建
                os.mkdir(app.config['UP_DIR'])
            # 对封面文件进行重名了
            logo = change_filename(file_logo)
            # 保存封面文件
            form.logo.data.save(app.config['UP_DIR'] + logo)

            # 对旧的封面图进行删除
            try:
                os.remove(app.config['UP_DIR'] + preview.logo)
            except:
                pass
            preview.title = data.get('title')
            preview.logo = logo
            db.session.add(preview)
            db.session.commit()
            flash("预告片编辑成功")
            oplog = OpLog(
                admin_id=session.get("admin_id"),
                ip=request.remote_addr,
                reason="编辑预告片：{preview}".format(preview=preview.title)
            )
            db.session.add(oplog)
            db.session.commit()
            return redirect(url_for("admin.perViewEdit", id=id))
        return render_template("admin/preview_edit.html", form=form, preview=preview)


# 会员列表
@admin.route("/userList/<int:page>", methods=["GET", "POST"])
@admin_login_req
def userList(page=None):
    if page is None:
        page = 1
    page_data = User.query.order_by(User.addtime.desc()).paginate(page=page, per_page=10)
    return render_template("admin/user_list.html", page_data=page_data)


# 会员详情
@admin.route("/userview/<int:id>", methods=["GET", "POST"])
@admin_login_req
def userView(id=None):
    if id is not None:
        user = User.query.get_or_404(id)
    return render_template("admin/user_view.html", user=user)


# 会员删除
@admin.route("/userDelete/<int:id>", methods=["GET", "POST"])
@admin_login_req
def userDelete(id=None):
    if id is not None:
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        flash("删除成功")
        oplog = OpLog(
            admin_id=session.get("admin_id"),
            ip=request.remote_addr,
            reason="删除会员：{user}".format(user=user.name)
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.userList', page=1))


# 评论列表
@admin.route("/commentList/<int:page>", methods=["GET", "POST"])
@admin_login_req
def commentList(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.order_by(Comment.addtime.desc()).paginate(page=page, per_page=1)
    return render_template("admin/comment_list.html", page_data=page_data)


# 评论的删除
@admin.route("/commentDelete/<int:id>", methods=["GET", "POST"])
@admin_login_req
def commentDelete(id=None):
    if id is not None:
        comment = Comment.query.get_or_404(id)
        db.session.delete(comment)
        db.session.commit()
        flash("删除成功")
        oplog = OpLog(
            admin_id=session.get("admin_id"),
            ip=request.remote_addr,
            reason="删除评论：{comment}".format(comment=comment.content)
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.commentList', page=1))


# 电影的收藏列表
@admin.route("/moviecolList/<int:page>", methods=["GET", "POST"])
@admin_login_req
def moviecolList(page=None):
    if page is None:
        page = 1
    page_data = MovieCol.query.order_by(MovieCol.addtime.desc()).paginate(page=page, per_page=1)
    return render_template("admin/moviecol_list.html", page_data=page_data)


# 电影收藏的删除
@admin.route("/moviecolDelete/<int:id>", methods=["GET", "POST"])
@admin_login_req
def movieColDelete(id=None):
    if id is not None:
        moviecol = MovieCol.query.get_or_404(id)
        db.session.delete(moviecol)
        db.session.commit()
        flash("删除成功")
        oplog = OpLog(
            admin_id=session.get("admin_id"),
            ip=request.remote_addr,
            reason="删除收藏：{moviecol}".format(moviecol=moviecol.movie_id)
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.moviecolList', page=1))


# 操作日志列表
@admin.route("/oplogList/<int:page>", methods=["GET", "POST"])
@admin_login_req
def oplogList(page=None):
    if page is None:
        page = 1
    page_data = OpLog.query.order_by(OpLog.add_time.desc()).paginate(page=page, per_page=5)
    return render_template("admin/oplog_list.html", page_data=page_data)


# 管理员登陆日志
@admin.route("/adminLoginLogList/<int:page>", methods=["GET"])
@admin_login_req
def adminLoginLogList(page=None):
    if page is None:
        page = 1
    page_data = AdminLog.query.order_by(AdminLog.add_time.desc()).paginate(page=page, per_page=5)
    return render_template("admin/adminloginlog_list.html", page_data=page_data)


# 用户登陆日志
@admin.route("/userLoginLogList/<int:page>", methods=["GET"])
@admin_login_req
def userLoginLogList(page=None):
    if page is None:
        page = 1
    page_data = UserLog.query.order_by(UserLog.add_time.desc()).paginate(page=page, per_page=5)
    return render_template("admin/userloginlog_list.html", page_data=page_data)


# 添加权限
@admin.route("/authAdd/", methods=["GET", "POST"])
@admin_login_req
def authAdd():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth(
            name=data.get('name'),
            url=data.get('url')
        )
        db.session.add(auth)
        db.session.commit()
        flash("添加权限成功")
        return redirect(url_for('admin.authAdd'))
    return render_template("admin/auth_add.html", form=form)


# 权限列表
@admin.route("/authList/<int:page>", methods=["GET"])
@admin_login_req
def authList(page=1):
    page_data = Auth.query.order_by(Auth.addtime.desc()).paginate(page=page, per_page=5)  # 权限列表
    return render_template("admin/auth_list.html", page_data=page_data)


# 删除权限
@admin.route("/authDelete/<int:id>", methods=["GET"])
@admin_login_req
def authDelete(id=None):
    if id is not None:
        auth = Auth.query.get_or_404(id)
        db.session.delete(auth)
        db.session.commit()
        flash("权限删除成功")
    return redirect(url_for('admin.authList', page=1))


# 权限编辑
@admin.route("/authEdit/<int:id>", methods=["GET", "POST"])
@admin_login_req
def authEdit(id=None):
    if id is not None:
        form = AuthForm()
        auth = Auth.query.get_or_404(id)
        if form.validate_on_submit():
            data = form.data
            auth.name = data.get('name')
            auth.url = data.get('url')
            db.session.add(auth)
            db.session.commit()
            flash("添加编辑成功")
            return redirect(url_for('admin.authEdit', id=id))
        return render_template("admin/auth_edit.html", form=form, auth=auth)


# 添加角色
@admin.route("/roleAdd/", methods=["GET", "POST"])
@admin_login_req
def roleAdd():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        # 使用map(lambda v: str(v), data.get('auths') 把数组的数据转换为字符串
        role = Role(
            name=data.get('name'),
            auths=",".join(map(lambda v: str(v), data.get('auths')))
        )
        db.session.add(role)
        db.session.commit()
        flash("角色添加成功！")
    return render_template("admin/role_add.html", form=form)


# 角色列表
@admin.route("/roleList/<int:page>", methods=["GET", ])
@admin_login_req
def roleList(page=1):
    page_data = Role.query.order_by(Role.addtime.desc()).paginate(page=page, per_page=10)  # 权限列表
    return render_template("admin/role_list.html", page_data=page_data)


# 角色删除
@admin.route("/roleDelete/<int:id>", methods=["GET"])
@admin_login_req
def roleDelete(id=None):
    if id is not None:
        role = Role.query.get_or_404(id)
        db.session.delete(role)
        db.session.commit()
        flash("角色删除成功")
        return redirect(url_for('admin.roleList', page=1))


# 角色编辑
@admin.route("/roleEdit/<int:id>", methods=["GET", "POST"])
@admin_login_req
def roleEdit(id=None):
    if id is not None:
        form = RoleForm()
        role = Role.query.get_or_404(id)
        if request.method == "GET":
            form.auths.data = list(map(lambda v: int(v), role.auths.split(',')))

        if form.validate_on_submit():
            data = form.data
            # 使用map(lambda v: str(v), data.get('auths') 把数组的数据转换为字符串
            role.name = data.get('name')
            role.auths = ",".join(map(lambda v: str(v), data.get('auths')))
            db.session.add(role)
            db.session.commit()
            flash("角色编辑成功！")
            return redirect(url_for('admin.roleEdit', id=id))
        return render_template("admin/role_edit.html", form=form, role=role)


# 添加管理员
@admin.route("/adminadd/", methods=["GET", "POST"])
@admin_login_req
def adminAdd():
    form = AdminForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin(
            name=data.get('name'),
            pwd=generate_password_hash(data.get('pwd')),
            is_super=1,
            role_id=data.get('role_id')
        )
        db.session.add(admin)
        db.session.commit()
        flash("管理员添加成功")
    return render_template("admin/admin_add.html", form=form)


# 管理员列表
@admin.route("/adminlist/<int:page>", methods=["GET"])
@admin_login_req
def adminList(page=1):
    page_data = Admin.query.order_by(Admin.addtime.desc()).paginate(page=page, per_page=10)  # 权限列表
    return render_template("admin/admin_list.html", page_data=page_data)
