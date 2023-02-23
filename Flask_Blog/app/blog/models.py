from datetime import datetime
from enum import IntEnum
from RealProject import db
from sqlalchemy.dialects.mysql import LONGTEXT


class BaseModel(db.Model):
    """基类模型"""

    __abstract__ = True

    add_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    pub_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class PostPublishType(IntEnum):
    """文章发布类型"""
    draft = 1   # 草稿
    show = 2    # 发布


class Category(BaseModel):
    """文章分类模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    icon = db.Column(db.String(128), nullable=True)

    # 文章类别和文章的关系：一 对 多
    # db.relationship：写在“一”方，关联“多”方，“多”方可以通过 backref='category' 访问到其对应的“一”方的对象
    # post = db.relationship('Post', back_populates='category')
    post = db.relationship('Post', backref='category', lazy=True)

    def __repr__(self):
        return '<Category %r>' % self.name


# 文章和文章标签的关系：多 对 多
# 多对多关系帮助器表
tags = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)


class Post(BaseModel):
    """文章模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    content = db.Column(LONGTEXT, nullable=False)
    has_type = db.Column(db.Enum(PostPublishType), server_default='show', nullable=False)

    # db.ForeignKey：写在“多”方，关联“一”方的某一个属性
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    # 多对多关系
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('post', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.title


class Tag(BaseModel):
    """文章标签模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)

    def __repr__(self):
        return '<Tag %r>' % self.name
