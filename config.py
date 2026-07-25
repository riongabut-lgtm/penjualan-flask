import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "penjualan-flask-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:@localhost/penjualan_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False