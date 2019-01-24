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
from wtforms import StringField, PasswordField, SubmitField  # 调用要验证的字段
from wtforms.validators import DataRequired  # 导入验证器
from wtforms.validators import ValidationError  # 验证信息错误，通过他来进行抛出
from app.models import Admin  # 管理员数据模型
from app.models import Tag  # 标签数据模型


class LoginForm(FlaskForm):
    '''
    管理员登陆表单验证
    '''
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

    # 验证密码
    def validate_pwd(self, field):
        pwd = field.data


class TagForm(FlaskForm):
    '''
    标签的表单验证
    '''
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
        '添加',
        render_kw={
            "class": "btn btn-primary"
        }
    )
