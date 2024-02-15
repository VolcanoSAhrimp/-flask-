from functools import wraps
from flask import redirect, url_for, g


def login_required(func):
    # 保留func的信息
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    return inner
