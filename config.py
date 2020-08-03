import os
basedir = os.path.abspath(os.path.dirname("../../"))



class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key_')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DB_USER = "postgres"
    DB_DATABASE = "telegram"
    DB_PASSWORD = "postgres"
    db_url = "127.0.0.1:5432"
    DATABASE_URI = 'postgres://{user}:{pw}@{url}/{db}'.format(
        user=DB_USER, pw=DB_PASSWORD, url=db_url, db=DB_DATABASE)
