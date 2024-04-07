from functools import wraps
from flask import redirect, url_for, g, abort


def login_required(func):
    # 保留func的信息
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))

    return inner


def check_permission(permission_level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not g.user:
                # 用户未登录，返回403 Forbidden
                abort(403)
            elif g.user.admin < permission_level:
                # 用户权限不符，返回403 Forbidden
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# 定义各个权限级别的装饰器
check_guest = check_permission(0)  # 未登录用户
check_user = check_permission(1)  # 普通用户
check_admin = check_permission(2)  # 管理员用户
check_root = check_permission(3)  # root用户
