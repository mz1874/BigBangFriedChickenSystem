import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'v6%+nT8McT7z'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:v6%+nT8M@192.168.0.60:3306/online_ordering_system?charset=utf8mb4"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:v6%+nT8McT7zvn%@bugcreator.org.cn:3306/online_ordering_system?charset=utf8mb4"

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
