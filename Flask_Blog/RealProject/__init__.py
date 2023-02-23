from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger

from RealProject.settings import CONFIG_PATH


# 操作数据库
db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    # 创建并配置app
    # instance_relative_config=True 代表开启从文件加载配置，默认为False
    app = Flask(__name__, instance_relative_config=True)

    swagger = Swagger(app)

    # app.config调用的是flask类的config属性，该属性又被设置为了一个Config的类
    # from_mapping是Config类的一个方法，用来更新默认配置，返回值为True
    # app.config.from_mapping(
    #     SECRET_KEY='dev'
    # )

    # 判断是否传入了测试配置
    if test_config is None:
        # 如果没有传入配置，则从settings.py文件加载配置
        # silent=True表示如果文件不存在，程序不会报错并终止运行
        app.config.from_pyfile(CONFIG_PATH, silent=True)
    else:
        # test_config 是一个字典
        app.config.from_mapping(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    # 首页url引入
    from app.blog import views as blog
    from app.auth import views as auth
    from app.admin import views as admin
    app.add_url_rule('/', endpoint='index', view_func=blog.index)
    # 注册蓝图对象
    app.register_blueprint(blog.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)

    # 注册数据库模型
    from app.blog import models
    from app.auth import models

    # 全局上下文
    app.context_processor(inject_category)

    return app


def inject_category():
    # 上下文处理器回调函数
    """
    context_processor上下文处理器在呈现模板之前运行，并且能够将新值注入模板上下文。上下文处理器是返回字典的函数。
    然后，对于应用程序中的所有模板，此字典的键和值将与模板上下文合并：
    """
    from app.blog.models import Category
    categorys = Category.query.limit(6).all()
    return dict(categorys=categorys)
