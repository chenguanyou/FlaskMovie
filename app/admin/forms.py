#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 12:00
# @User    : zhunishengrikuaile
# @File    : forms.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: TheMovie
from flask_wtf import FlaskForm
from flask import session
from wtforms import StringField  # 验证字符串
from wtforms import PasswordField  # 验证密码
from wtforms import FileField  # 验证URL
from wtforms import TextAreaField  # 验证文本框
from wtforms import SelectField  # 用来验证下拉选择框
from wtforms import SubmitField  # 提交表单
from wtforms import SelectMultipleField  # 多选验证
from wtforms.validators import DataRequired  # 导入验证器
from wtforms.validators import ValidationError  # 验证信息错误，通过他来进行抛出
from app.models import Admin  # 管理员数据模型
from app.models import Tag  # 导入电影标签
from app.models import Auth  # 导入权限列表

tags = Tag.query.all()

auth_list = Auth.query.all()


# 管理员登陆表单验证
class LoginForm(FlaskForm):
    account = StringField(
        # 标签
        label='账号',
        # 验证器
        validators=[
            DataRequired("请输入账号")
        ],
        # 描述
        description="账号",
        # 附加的选项
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！",
            # 必填项
            "required": "required"
        }
    )

    pwd = PasswordField(
        # 标签
        label='密码',
        # 验证器
        validators=[
            DataRequired("请输入密码")
        ],
        # 描述
        description="密码",
        # 附加选项
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            "required": "required",
        }
    )

    submit = SubmitField(
        # 标签
        '登陆',
        # 附加选项
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    # 验证账号
    def validate_account(self, field):
        accound = field.data
        admin = Admin.query.filter_by(name=accound).count()
        if admin == 0:
            raise ValidationError("账号不存在")


# 标签的表单验证
class TagForm(FlaskForm):
    name = StringField(
        label="标签",
        validators=[
            DataRequired("请输入标签")
        ],
        description="标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称！",
            "required": "required"
        }
    )

    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 电影的表单验证
class MovieForm(FlaskForm):
    title = StringField(
        label="片名",
        validators=[
            DataRequired("请输入片名")
        ],
        description="片名",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入片名！",
            "required": "required",
        }
    )

    url = FileField(
        label='文件',
        validators=[
            DataRequired("请上传文件！")
        ],
        description="文件",
    )

    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介！")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "rows": "10",
            "id": "input_info",
            "required": "required",
        }
    )

    logo = FileField(
        label="封面",
        validators=[
            DataRequired("请上传封面！")
        ],
        description="封面",
    )

    star = SelectField(
        label="星级",
        validators=[
            DataRequired("请选择星级！")
        ],
        coerce=int,
        choices=[(1, "一星"), (2, "二星"), (3, "三星"), (4, "四星"), (5, "五星")],
        description="星级",
        render_kw={
            "class": "form-control",
            "required": "required"
        }
    )

    tag_id = SelectField(
        label="标签",
        validators=[
            DataRequired("请选择标签")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in tags],
        description="标签",
        render_kw={
            "class": "form-control",
            "required": "required"
        }
    )

    arga = StringField(
        label="上映地区",
        validators=[
            DataRequired("请输入上映地区！")
        ],
        description="上映地区",
        render_kw={
            "class": "form-control",
            "id": "input_area",
            "placeholder": "请输入地区！",
            "required": "required"
        }
    )

    length = StringField(
        label="播放时间",
        validators=[
            DataRequired("请输入播放时间！")
        ],
        description="播放时间",
        render_kw={
            "class": "form-control",
            "id": "input_length",
            "placeholder": "请输入片长!",
            "required": "required"

        }
    )

    release_time = StringField(
        label="上映时间",
        validators=[
            DataRequired("请选择上映时间！")
        ],
        description="上映时间",
        render_kw={
            "class": "form-control",
            "id": "input_release_time",
            "placeholder": "请选择上映时间!",
            "required": "required"
        }
    )

    submit = SubmitField(
        label="编辑",
        render_kw={
            "class": "btn btn-primary",
            "required": "required"
        }
    )


# 预告片的表单验证
class PreViewForm(FlaskForm):
    # 验证预告片的名称
    title = StringField(
        label="名称",
        validators=[
            DataRequired("请输入预告片名称！")
        ],
        description="名称",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入预告标题!",
            "required": "required",
        }
    )

    # 验证预告片的封面
    logo = FileField(
        label="封面",
        validators=[
            DataRequired("请上传封面！")
        ],
        description="封面",
    )

    # 进行提交
    submit = SubmitField(
        label="编辑",
        render_kw={
            "class": "btn btn-primary",
            "required": "required"
        }
    )


# 修改密码
class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码！")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "id": "input_pwd",
            "placeholder": "请输入旧密码!",
            "required": "flase",
        },
    )

    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码！")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "id": "input_newpwd",
            "placeholder": "请输入新密码!",
            "required": "flase",
        }
    )

    submit = SubmitField(
        label="编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )

    # 验证账号是否存在
    def validate_old_pwd(self, field):
        pwd = field.data
        name = session.get("admin")
        admin = Admin.query.filter_by(name=name).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码错误")


# 添加权限表单
class AuthForm(FlaskForm):
    name = StringField(
        label='权限名称',
        validators=[
            DataRequired("请输入权限名称！")
        ],
        description="权限名称",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入权限名称！"
        }
    )

    url = StringField(
        label="权限地址",
        validators=[
            DataRequired("请输入权限地址！")
        ],
        description="权限地址",
        render_kw={
            "class": "form-control",
            "id": "input_url",
            "placeholder": "请输入权限地址!"
        }
    )

    submit = SubmitField(
        label="编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 权限角色的表单验证
class RoleForm(FlaskForm):
    name = StringField(
        label="角色名称",
        validators=[
            DataRequired("请输入角色名称！")
        ],
        description="角色名称",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入角色名称!"
        }
    )

    auths = SelectMultipleField(
        label="操作权限",
        validators=[
            DataRequired("请选择操作权限！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in auth_list],
        description="操作权限",
        render_kw={
            "type": "checkbox",
            "placeholder": "操作权限!"
        }
    )

    submit = SubmitField(
        label="编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 添加管理员表单验证
class AdminForm(FlaskForm):
    name = StringField(
        # 标签
        label='管理员名称',
        # 验证器
        validators=[
            DataRequired("请输入管理员名称")
        ],
        # 描述
        description="管理员名称",
        # 附加的选项
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入管理员名称!"
        }
    )

    pwd = PasswordField(
        # 标签
        label='密码',
        # 验证器
        validators=[
            DataRequired("请输入密码")
        ],
        # 描述
        description="密码",
        # 附加选项
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            "id": "input_pwd",
            "required": "required",
        }
    )

    re_pwd = PasswordField(
        # 标签
        label='重复密码',
        # 验证器
        validators=[
            DataRequired("请输入管理员重复密码")
        ],
        # 描述
        description="重复密码",
        # 附加选项
        render_kw={
            "class": "form-control",
            "id": "input_re_pwd",
            "placeholder": "请输入管理员重复密码！",
            "required": "required",
        }
    )

    role_id = SelectField(
        label="所属角色",
        validators=[
            DataRequired("请选择角色"),
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in auth_list],
        description="所属角色",
        render_kw={
            "class": "form-control",
            "id": "input_role_id"
        }
    )

    submit = SubmitField(
        # 标签
        label='编辑',
        # 附加选项
        render_kw={
            "class": "btn btn-primary",
        }
    )

    # 验证账号
    def validate_name(self, field):
        name = field.data
        admin = Admin.query.filter_by(name=name).count()
        if admin != 0:
            raise ValidationError("账号已经存在")

    # 验证密码
    def validate_pwd(self, field):
        if self.re_pwd.data != self.pwd.data:
            raise ValidationError("密码不一致")
