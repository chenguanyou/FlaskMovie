#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 11:57
# @User    : zhunishengrikuaile
# @File    : __init__.py.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: TheMovie
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:12345678@127.0.0.1:3306/movie"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = uuid.uuid4().hex
db = SQLAlchemy(app)
app.debug = True

from app.admin import admin
from app.home import home

app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(home)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404
