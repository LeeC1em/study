from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, Email
from .models import User
from werkzeug.security import check_password_hash
from app.auth.models import UserGender


class LoginForm(FlaskForm):
    """登录表单"""

    def qs_username(username):
        # 对该字段进行在传递之前处理
        u = f'{username}123456'
        print(u)
        return username

    username = StringField(
        'username',
        validators=[DataRequired(message='用户名不能为空'), Length(max=32, message='用户名不符合字数要求')],
        filters=(qs_username,)
    )

    password = PasswordField(
        'password',
        validators=[DataRequired(message='密码不能为空'), Length(max=32, message='密码不符合字数要求')]
    )

    def validate_username(form, field):
        user = User.query.filter_by(username=field.data).first()
        if user is None:
            error = '该用户不存在！'
            raise ValidationError(error)
        elif not check_password_hash(user.password, form.password.data):
            error = '密码不正确！'
            raise ValidationError(error)


class RegisterForm(FlaskForm):
    """注册表单"""

    username = StringField(
        'username',
        validators=[DataRequired(message='用户名不能为空'), Length(min=2, max=32, message='用户名超过字数限制')]
    )

    password = PasswordField(
        'password',
        validators=[DataRequired(message='密码不能为空'),
                    Length(min=2, max=32, message='密码超过字数限制'),
                    EqualTo('password1', message='两次密码输入不一致')]
    )

    password1 = PasswordField('password1')

    def validate_username(form, field):
        user = User.query.filter_by(username=field.data).first()
        if user is not None:
            error = '用户名已存在'
            raise ValidationError(error)


class InfoForm(FlaskForm):
    """用户信息表单"""

    signature = StringField(
        '个性签名',
        validators=[
            Length(max=30, message='字数不符合要求')
        ]
    )
    gender = RadioField(
        '性别',
        choices=(UserGender.male.name, UserGender.female.name),
        default=UserGender.male.name
    )
    email = EmailField(
        '邮箱',
        validators=[
            Email(message='请输入正确的邮箱地址'),
            Length(max=20, message='字数不符合要求')
        ]
    )
    profile = TextAreaField(
        '个人简介',
        validators=[
            Length(max=128, message='字数不符合要求')
        ]
    )
