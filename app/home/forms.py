#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 12:00
# @User    : zhunishengrikuaile
# @File    : forms.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: TheMovie
import re
from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField

from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

from app.models import User


# 会员注册表单验证
class RegisterForm(FlaskForm):
    name = StringField(
        label="昵称",
        validators=[
            DataRequired("请输入昵称")
        ],
        description="昵称",
        render_kw={
            "autofocus": "autofocus",
            "id": "input_name",
            "class": "form-control input-lg",
            "placeholder": "昵称",
        }
    )

    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱！")
        ],
        description="邮箱",
        render_kw={
            "id": "input_email",
            "class": "form-control input-lg",
            "placeholder": "邮箱",
            "type": "email",
            "autofocus": "autofocus"
        }
    )

    phone = StringField(
        label="手机",
        validators=[
            DataRequired("请输入手机号")
        ],
        description="手机",
        render_kw={
            "id": "input_phone",
            "class": "form-control input-lg",
            "placeholder": "手机",
            "type": "text",
            "autofocus": "autofocus"
        }
    )

    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "id": "input_password",
            "class": "form-control input-lg",
            "placeholder": "密码",
            "type": "password"
        }
    )

    re_pwd = PasswordField(
        label="再次输入密码",
        validators=[
            DataRequired("请再次输入密码！")
        ],
        description="再次输入密码",
        render_kw={
            "id": "input_repassword",
            "class": "form-control input-lg",
            "placeholder": "再次输入密码",
            "type": "password"
        }
    )

    submit = SubmitField(
        label="注册",
        render_kw={
            "class": "btn btn-lg btn-success btn-block",
        }
    )

    # 验证昵称是否存在
    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user != 0:
            raise ValidationError("昵称已经被使用！")

    # 验证邮箱格式是否正确，是否存在
    def validate_email(self, field):
        email = field.data
        if not re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
            raise ValidationError("邮箱格式错误！")

        user = User.query.filter_by(email=email).count()
        if user != 0:
            raise ValidationError("邮箱已经存在")

    # 验证手机号是否正确，是否存在
    def validate_phone(self, field):
        phone = field.data
        if not re.match(r'^1((3[\d])|(4[75])|(5[^3|4])|(66)|(7[013678])|(8[\d])|(9[89]))\d{8}$', phone):
            raise ValidationError("手机号格式错误！")

        user = User.query.filter_by(phone=phone).count()
        if user != 0:
            raise ValidationError("手机号已经存在")

    # 验证密码是否相等
    def validate_pwd(self, field):
        if len(self.pwd.data) < 6:
            raise ValidationError("密码长度不能小于6位")
        if self.pwd.data != self.re_pwd.data:
            raise ValidationError("密码不相等")
