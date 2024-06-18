from flask import current_app as app, abort
from application.functions import *
from functools import wraps

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_login'


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.label not in allowed_roles:
                abort(403)  # Forbidden
            return func(*args, **kwargs)
        return wrapper
    return decorator