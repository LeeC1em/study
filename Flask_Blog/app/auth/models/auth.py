from datetime import datetime
from RealProject import db
from enum import IntEnum


class BaseModel(db.Model):
    """基类模型"""

    # Flask-SQLAlchemy创建table时,如何声明基类（这个类不会创建表,可以被继承）
    # 方法就是把__abstract__这个属性设置为True,这个类为基类，不会被创建为表！
    __abstract__ = True

    add_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


class UserGender(IntEnum):
    """性别"""
    male = 1        # 男
    female = 2      # 女


class User(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(200), nullable=True)                       # 头像
    is_super_user = db.Column(db.Boolean, nullable=True, default=False)     # 超级管理员标识
    is_active = db.Column(db.Boolean, nullable=True, default=True)          # 活跃用户标识
    is_staff = db.Column(db.Boolean, nullable=True, default=False)          # 员工标识

    # uselist=False：声明一对一关系时使用，在查找 Info 表时，查找到第一个数据时就停止；若为True则会查找表中全部数据
    info = db.relationship('Info', backref='user', uselist=False)

    def __repr__(self):
        return '<Category %r>' % self.username


class Info(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    signature = db.Column(db.String(30), nullable=True)
    gender = db.Column(db.Enum(UserGender), server_default='male', nullable=True)
    email = db.Column(db.String(20), nullable=True)
    profile = db.Column(db.String(128), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return 'Category %r' % self.id



