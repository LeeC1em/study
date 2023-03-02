import functools
import json

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g, abort
from ..models import User, Info
from RealProject import db
from werkzeug.security import generate_password_hash
from ..forms import LoginForm, RegisterForm
from app.auth.forms import InfoForm


bp = Blueprint('auth', __name__, url_prefix='/auth', static_folder='../static', template_folder='../templates')


# @bp.before_app_request    注册一个在视图函数运行之前的函数，无论访问什么url，都会先运行此函数检查用户ID是否储存在会话中
# 通过这个函数，可以判断用户是否登录，来显示不同的页面信息
@bp.before_app_request
def load_logged_in_user():
    # 每个请求前都会去session中查看user_id获取用户

    # 注册用户即非管理员用户允许登录后查看的url
    urls = ['/auth/']

    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(int(user_id))

        # 权限判断
        if g.user.is_super_user and g.user.is_active:
            g.user.has_perm = 1
        elif not g.user.is_super_user and g.user.is_active and not g.user.is_staff and request.path in urls:
            g.user.has_perm = 1
        else:
            g.user.has_perm = 0


def login_required(view):
    # 限制必须登录才能访问的页面装饰器
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            # 如果没有登录，会先跳转至登录页面
            # redirect_to{request.path}：保存了之前访问的路径，可以让登录视图获取，并实现登录后跳转至之前访问的页面
            redirect_to = f'{url_for("auth.login")}?redirect_to={request.path}'
            return redirect(redirect_to)

        # 登录成功后对权限进行判断处理
        if g.user.has_perm:
            pass
        else:
            # 没有权限的用户访问，直接报404错误
            abort(404)

        return view(**kwargs)
    return wrapped_view


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """登录页视图"""

    # 获取login_required(view)函数返回的请求中的 redirect_to{request.path} 中的路径，以便于实现登录后跳转至之前的页面
    redirect_to = request.args.get('redirect_to')

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        session.clear()
        session['user_id'] = user.id

        if redirect_to is not None:
            return redirect(url_for(redirect_to))
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

    # if request.method == 'POST':
    #     # 获取用户名密码
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #
    #     error = None
    #
    #     user = User.query.filter_by(username=username).first()
    #     if not user:
    #         error = '用户不存在！'
    #     # 判断输入的密码和数据库中该用户的密码是否相同
    #     elif not check_password_hash(user.password, password):
    #         error = '密码不正确！'
    #
    #     if not error:
    #         # 若没有错误信息，则登录成功跳转至首页
    #         session.clear()
    #         session['user_id'] = user.id
    #         return redirect(url_for('index'))
    #     else:
    #         flash(error)
    #
    # return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """注册页视图"""

    form = RegisterForm()
    if form.validate_on_submit():
        # 向数据添加用户
        user = User(username=form.username.data, password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()

        # 使用新的用户自动登录并跳转至首页
        session.clear()
        session['user_id'] = user.id
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

    # if request.method == 'POST':
    #     # 获取用户名和密码
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     password1 = request.form.get('password1')
    #
    #     if password != password1:
    #         flash('两次密码输入不一致！')
    #         # return redirect(url_for('auth.register'))
    #
    #     # 查询数据库中是否已经有用户名为 'username' 的用户
    #     exists_user = User.query.filter_by(username=username).first()
    #
    #     if exists_user:
    #         flash('用户名已存在，请勿重复注册')
    #         return redirect(url_for('auth.register'))
    #     else:
    #         # 注册成功，在数据库添加一条新的用户信息
    #         user = User(username=username, password=generate_password_hash(password))
    #         db.session.add(user)
    #         db.session.commit()
    #
    #         # 使用新的用户建立session
    #         # 自动登录
    #         session.clear()
    #         session['user_id'] = user.id
    #
    #     # 注册成功跳转至登录页
    #     return redirect(url_for('index'))
    #
    # return render_template('register.html')


@bp.route('/logout')
def logout():
    """注销"""
    session.clear()
    return redirect(url_for('index'))


@bp.route('/')
def userinfo():
    """个人中心"""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    user = User.query.get(user_id)
    return render_template('userinfo.html', user=user)


@bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def userinfo_edit(user_id):
    user = User.query.get(user_id)
    # 若用户还没有修改过信息（数据库中不存在此用户信息），则先在数据库中创建一条此用户的数据
    if not user.info:
        add_info = Info(
            user_id=user.id
        )
        db.session.add(add_info)
        db.session.commit()

    info_id = user.info.id
    info = Info.query.get(info_id)
    form = InfoForm(
        signature=info.signature,
        gender=info.gender.value,
        email=info.email,
        profile=info.profile
    )

    if form.validate_on_submit():
        info.signature = form.signature.data
        info.gender = form.gender.data
        info.email = form.email.data
        info.profile = form.profile.data
        db.session.add(info)
        db.session.commit()
        flash('个人信息修改成功')
        return redirect(url_for('auth.userinfo'))
    return render_template('userinfo_form.html', form=form)


@bp.route('/loginfail', methods=['GET', 'POST'])
def loginfail():
    return render_template('loginfail.html')
