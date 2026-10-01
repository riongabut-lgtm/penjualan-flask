import os

class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "penjualan-flask-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
        "connect_args": {
            "connect_timeout": 10
        }
    }
