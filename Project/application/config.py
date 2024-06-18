import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SECRET_KEY = None
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    UPLOAD_FOLDER_PATH = None
    UPLOAD_FOLDER = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "hello world what are you doing ?"
    SQLITE_DB_DIR = os.path.join(basedir, "../database")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "database.sqlite3")
    UPLOAD_FOLDER_PATH = os.path.join(basedir, "../media")
    UPLOAD_FOLDER = {"PICTURE": {"PROFILE":"media/picture/profiles", "BOOK":"media/picture/books",  "SECTION":"media/picture/sections","OTHER":"media/picture"}, "PDF":"media/pdfs"}

    