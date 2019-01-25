#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 11:43
# @User    : zhunishengrikuaile
# @File    : updata.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: TheMovie
# 上传文件
import os
import time
import uuid

from werkzeug.utils import secure_filename


# 修改上传的文件名称
def change_filename(filename):
    # 使用secure_filename吧filename变成安全的
    filename = secure_filename(filename)
    # 把文件分割成后缀名加前缀
    fileinfo = os.path.splitext(filename)
    # 定义我们的filename
    filename = str(time.time()) + str(uuid.uuid4().hex) + fileinfo[1]
    return filename


if __name__ == "__main__":
    pass
    # print(time.time())
