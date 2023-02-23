import os
import uuid
import click
from flask import Flask

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from RealProject.settings import BASE_DIR
from app.auth.models import User
from RealProject import db


def _file_path(directory_name):
    """判断路径是否存在，若不存在则新建并返回路径"""
    file_path = BASE_DIR / f'app/admin/static/{directory_name}'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    return file_path


def update_filename(f):
    """修改文件名称"""
    names = list(os.path.splitext(secure_filename(f.filename)))     # secure_filename() 将文件名中的中文剔除
    names[0] = ''.join(str(uuid.uuid4()).split('-'))
    return ''.join(names)


def upload_file_path(direcotory_name, f):
    file_path = _file_path(direcotory_name)
    filename = update_filename(f)
    return file_path / filename, filename


def init_script(app: Flask):
    """自定义命令"""

    @app.cli.command()
    @click.option('--username', prompt=True, help='请输入用户名！')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='请输入密码！')
    def createsuperuser(username, password):
        user = User(username=username, passowrd=generate_password_hash(password), is_super_user=True)
        db.session.add(user)
        db.session.commit()
        click.echo(f'超级管理员{username}创建成功')
