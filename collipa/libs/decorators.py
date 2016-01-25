# coding=utf-8

from functools import wraps

from collipa.models import User


def require_permission(func):
    @wraps(func)
    def wrap(self, *args, **kwargs):
        result = None
        if not self.current_user:
            result = {"status": "error",
                      "message": "请登陆"}
        elif self.current_user.role == User.UNVERIFY:
            result = {"status": "error",
                      "message": "对不起，您的账户尚未激活，请到注册邮箱检查激活邮件"}
        elif self.current_user.role == User.FORBIDDEN:
            result = {"status": "error", "message": "对不起，您没有相关权限"}

        if result is not None:
            return self.send_result(result)
        return func(self, *args, **kwargs)
    return wrap


def require_admin(func):
    @wraps(func)
    def wrap(self, *args, **kwargs):
        if self.current_user and self.current_user.is_admin:
            return func(self, *args, **kwargs)
        result = {"status": "error", "message": "对不起，您没有相关权限"}
        self.send_result(result)
    return wrap


def require_with_roles(includes=None, excludes=None):
    def wrap(func):
        @wraps(func)
        def _wrap(self, *args, **kwargs):
            result = {"status": "error", "message": "对不起，您没有相关权限"}
            if not self.current_user:
                return self.send_result(result)
            if isinstance(includes, list):
                if self.current_user.role in includes:
                    return func(self, *args, **kwargs)
                return self.send_result(result)
            if isinstance(excludes, list):
                if self.current_user.role in excludes:
                    return self.send_result(result)
                return func(self, *args, **kwargs)
            return self.send_result(result)
        return _wrap
    return wrap
