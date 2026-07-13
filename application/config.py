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
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_temporary_local_fallback_key')
    SQLITE_DB_DIR = os.path.join(basedir, "../database")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "database.sqlite3")
    UPLOAD_FOLDER_PATH = os.path.join(basedir, "..", "../media")
    UPLOAD_FOLDER = {
        "PICTURE": {
            "PROFILE" : os.path.join(basedir, "..", "media/picture/profiles"), 
            "BOOK" : os.path.join(basedir, "..", "media/picture/books"),
            "SECTION" : os.path.join(basedir, "..", "media/picture/sections"),
            "OTHER" : os.path.join(basedir, "..", "media/picture")
            },
        "PDF" : os.path.join(basedir, "..", "media/pdfs")
        }

    