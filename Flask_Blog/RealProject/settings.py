from pathlib import Path


# 项目路径
BASE_DIR = Path(__file__).resolve().parent.parent

# 配置文件路径，即当前文件 settings.py 的路径
CONFIG_PATH = Path(__file__)

DEBUG = True

# 密钥
SECRET_KEY = 'f0bb90e70e099660809dc8097c8f7102d2e66db8a5c06f8abfee9b56afed996c'

# 数据库配置
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = '123456'
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@127.0.0.1:3306/flaskdb'

# 用于app.config的默认配置更新
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
