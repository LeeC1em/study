from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed
from wtforms import StringField, PasswordField, RadioField, SelectField, TextAreaField, \
    SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Length, Email

from app.blog.models import PostPublishType


class CategoryForm(FlaskForm):
    """文章分类表单"""

    name = StringField(
        '分类名称',
        validators=[
            DataRequired(message='文章类别不能为空'),
            Length(max=128, message='不符合字数要求')
        ]
    )
    icon = StringField(
        '分类图标',
        validators=[
            Length(max=256, message='不符合字数要求')
        ]
    )


class PostForm(FlaskForm):
    """文章管理表单"""

    title = StringField(
        '标题',
        validators=[
            DataRequired(message='不能为空'),
            Length(max=128, message='不符合字数要求')
        ]
    )
    desc = StringField(
        '简介',
        validators=[
            DataRequired(message='不能为空'),
            Length(max=200, message='字数不符合要求')
        ]
    )
    has_type = RadioField(
        '发布状态',
        choices=(PostPublishType.draft.name, PostPublishType.show.name),
        default=PostPublishType.show.name
    )
    category_id = SelectField(
        '分类',
        choices=None,
        coerce=int,
        validators=[
            DataRequired(message='不能为空')
        ]
    )
    content = TextAreaField(
        '文章详情',
        validators=[DataRequired(message='不能为空')]
    )
    tags = SelectMultipleField(
        '文章标签',
        choices=None,
        coerce=int
    )


class TagForm(FlaskForm):
    """标签表单"""

    name = StringField(
        '标签',
        validators=[
            DataRequired(message='不能为空'),
            Length(max=128, message='不符合字数要求')
        ]
    )


class CreateUserForm(FlaskForm):
    """用户表单"""

    username = StringField(
        '用户名',
        validators=[
            DataRequired(message='用户名不能为空'),
            Length(max=32, message='字数不符合要求')
        ]
    )
    password = PasswordField(
        '密码',
        validators=[
            # DataRequired(message='密码不能为空'),
            Length(max=32, message='字数不符合要求')
        ]
    )
    avatar = FileField(
        'avatar',
        validators=[
            FileAllowed(['jpg', 'png', 'gif'], message='仅支持jpg/png/gif格式'),
            FileSize(max_size=2048000, message='图片大小不能大于2M')
        ],
        description='图片大小不超过2M，仅支持jpg/png/gif格式， 不选则代表不修改'
    )
    is_super_user = BooleanField('是否为管理员')
    is_active = BooleanField('是否活跃', default=True)
    is_staff = BooleanField('是否锁定')
