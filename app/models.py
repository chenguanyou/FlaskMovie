#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 11:58
# @User    : zhunishengrikuaile
# @File    : model.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: TheMovie
from datetime import datetime
from app import db


class User(db.Model):
    '''
    用户表模型：
    id  --》编号
    name    --》用户名
    pwd --》密码
    email   --》邮箱地址
    phone   --》手机号
    info    --》个人简介
    face    --》头像
    addtime --》注册时间
    uuid    --》唯一标识符
    '''
    __tablename__ = "user"  # 指定在数据库中的表名
    id = db.Column(db.Integer, primary_key=True)  # 编号，设置为主键
    name = db.Column(db.String(100), unique=True)  # 用户名，设置唯一
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱唯一
    phone = db.Column(db.String(11), unique=True)  # 手机号码唯一
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255), unique=True)  # 头像地址唯一
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标志符
    comment = db.relationship('Comment', backref='user')  # 用户和评论进行关系绑定关联
    moviecol = db.relationship('MovieCol', backref='user')  # 用户和电影收藏进行关系绑定
    userlogs = db.relationship('UserLog', backref="user")  # 会员日志关系绑定

    def __repr__(self):
        return '<User {0}>'.format(self.name)


class UserLog(db.Model):
    '''
    用户登陆日志模型：
    id  --》编号
    user_id --》关联用户id
    ip  --》登陆IP
    addtime --》登陆时间
    '''
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号并且设置为主键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 用户登陆的IP
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 登陆时间

    def __repr__(self):
        return '<UserLog {0}>'.format(self.id)


class Tag(db.Model):
    '''
    电影标签模型：
    id  --》标签id编号
    name    --》标签名称
    addtime --》标签添加时间
    movies  --》标签和电影模型进行绑定
    '''
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)  # 标签id并且设置为主键
    name = db.Column(db.String(100), unique=True)  # 电影标签名称并且设置为唯一
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 电影标签的添加时间
    movies = db.relationship('Movie', backref='tag')  # 电影标签模型和电影模型绑定

    def __repr__(self):
        return "<Tage {0}>".format(self.name)


class Movie(db.Model):
    '''
    电影模型：
    id  --》编号id
    title   --》名称
    url --》播放地址
    info    --》简介
    logo    --》封面图
    star    --》星级
    playnum --》播放数
    commentnum  --》评论数
    tag_id  --》关联的标签id
    arga    --》上映地区
    release_time    --》上映时间
    length  --》播放时间
    addtime --》添加时间
    '''
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)  # id编号并设置id为主键
    title = db.Column(db.String(255), unique=True)  # 电影名称并设置电影名称为唯一
    url = db.Column(db.String(255), unique=True)  # 电影播放地址并且设置唯一
    info = db.Column(db.Text)  # 电影简介
    logo = db.Column(db.String(255), unique=True)  # 电影的封面
    star = db.Column(db.SmallInteger)  # 电影的星级
    playnum = db.Column(db.BigInteger)  # 电影的播放量
    commentnum = db.Column(db.BigInteger)  # 电影的评论数
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 电影的标签并且和标签id绑定
    arga = db.Column(db.String(255))  # 电影的上映地区
    release_time = db.Column(db.Date)  # 电影的上映时间
    length = db.Column(db.String(100))  # 电影的播放时间
    comment = db.relationship('Comment', backref="movie")  # 和评论模型进行关系绑定
    moviecol = db.relationship('MovieCol', backref='movie')  # 和收藏模型进行关系绑定
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 电影添加时间

    def __repr__(self):
        return '<Movie {0}>'.format(self.title)


class PreView(db.Model):
    '''
    电影预告模型
    id  --》电影预告编号
    title   --》电影预告片title
    logo    --》电影预告片logo
    addtime --》电影预告片添加时间
    '''
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)  # 预告片ID编号并且设置为主键
    title = db.Column(db.String(255), unique=True)  # 预告片的名称并且设置唯一
    logo = db.Column(db.String(255), unique=True)  # 预告片的封面图并且设置唯一
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 预告片的添加时间

    def __repr__(self):
        return '<PreView {0}>'.format(self.title)


class Comment(db.Model):
    '''
    电影评论模型
    id  --》电影编号
    content --》电影评论
    movie_id    --》所属电影ID
    user_id --》所属电影用户
    addtime --》电影评论时间
    '''
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)  # 电影评论的id编号
    content = db.Column(db.Text)  # 电影的评论内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 评论的电影并且和电影的ID进行绑定
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 评论的用户并且和用户的id进行绑定
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 电影的评论时间

    def __repr__(self):
        return '<Comment {0}>'.format(self.content)


class MovieCol(db.Model):
    '''
    电影收藏的模型
    id  --》电影收藏的id
    movie_id    --》电影的id
    user_id --》用户的id
    addtime --》添加时间
    '''
    __tablename__ = 'moviecol'
    id = db.Column(db.Integer, primary_key=True)  # 电影的收藏id编号
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 收藏的电影，和电影的id进行绑定
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 收藏电影的用户，和用户的id进行绑定
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 收藏的时间

    def __repr__(self):
        return '<MovieCol {0}>'.format(self.id)


class Auth(db.Model):
    '''
    系统权限模型
    id --》编号
    name --》权限名称
    url --》权限的url
    addtime --》添加时间
    '''
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 权限的id编号
    name = db.Column(db.String(100), unique=True)  # 权限的名称并且设置唯一
    url = db.Column(db.String(255), unique=True)  # 权限的地址并且设置唯一
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 权限的添加时间

    def __repr__(self):
        return '<Auth {0}>'.format(self.id)


class Role(db.Model):
    '''
    权限角色
    id  --》角色的id编号
    name    --》角色的名称
    auths   --》角色的列表
    addtime --》角色的添加时间
    '''
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)  # 角色的id编号
    name = db.Column(db.String(100), unique=True)  # 角色的名称并且设置唯一
    auths = db.Column(db.String(800))  # 角色的列表
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 角色的添加时间
    admin = db.relationship('Admin', backref='role')  # 和admin角色进行模型绑定

    def __repr__(self):
        return '<Role {0}>'.format(self.id)


class Admin(db.Model):
    '''
    管理员模型
    id  --》管理员id编号
    name    --》管理员名称
    pwd --》管理员密码
    is_super    --》是否是超级管理员
    role_id --》权限角色
    addtime --》添加时间
    '''
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)  # 管理员的id编号
    name = db.Column(db.String(100), unique=True)  # 管理员的名称
    pwd = db.Column(db.String(600))  # 管理员的密码
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员，0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 管理员的所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 管理员的添加时间
    adminlog = db.relationship('AdminLog', backref='admin')  # 登陆日志和管理员进行绑定
    oplog = db.relationship('OpLog', backref='admin')  # 操作日志和管理员进行绑定

    def __repr__(self):
        return '<Admin {0}>'.format(self.name)

    # 验证密码
    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        #
        return check_password_hash(self.pwd, pwd)


class AdminLog(db.Model):
    '''
    管理员登陆日志模型：
    id  --》编号
    user_id --》关联管理员id
    ip  --》登陆IP
    addtime --》登陆时间
    '''
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号并且设置为主键
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 登陆的管理员
    ip = db.Column(db.String(100))  # 登陆IP
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 登陆时间

    def __repr__(self):
        return '<AdminLog {0}>'.format(self.id)


class OpLog(db.Model):
    '''
    管理员操作日志模型：
    id  --》编号
    user_id --》关联管理员id
    ip  --》操作IP
    reason --》操作原因
    addtime --》操作时间
    '''
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)  # 编号并且设置为主键
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 操作的管理员
    ip = db.Column(db.String(100))  # 操作IP
    reason = db.Column(db.String(600))  # 操作原因
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 操作时间

    def __repr__(self):
        return '<OpLog {0}>'.format(self.id)


if __name__ == "__main__":
    # 把Model插入数据库
    # db.create_all()
    # # # 定义管理员账号密码
    # from werkzeug.security import generate_password_hash  # 导入加密工具
    #
    # # 实例化角色
    # role = Role(
    #     name="admin",
    #     auths="0"
    # )
    # db.session.add(role)
    # db.session.commit()
    #
    # # 实例化管理员
    # admin = Admin(
    #     name="admin",
    #     pwd=generate_password_hash("admin888"),
    #     is_super=0,
    #     role_id=1
    # )
    #
    # # 插入数据
    # db.session.add(admin)
    #
    # # 保存数据
    # db.session.commit()
    pass
