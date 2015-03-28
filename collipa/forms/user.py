# coding: utf-8

from ._base import BaseForm
from collipa.libs.tforms import validators
from collipa.libs.tforms.fields import TextField, TextAreaField, PasswordField
from collipa.libs.tforms.validators import ValidationError
from collipa.models import User, Message
from collipa import config

from pony import orm


class MessageForm(BaseForm):
    content = TextAreaField(
        '内容', [
            validators.Required(),
            validators.Length(min=2, max=2000),
        ],
    )

    def save(self, **kargs):
        data = self.data
        data.update(kargs)
        message = Message(**data).save()
        return message


class SignupForm(BaseForm):
    name = TextField(
        '用户名', [
            validators.Required(),
            validators.Length(min=4, max=16),
            validators.Regexp(
                '^[a-zA-Z0-9]+$',
                message='用户名只能包含英文字母和数字',
            ),
        ],
        description='用户名只能包含英文字母和数字'
    )
    email = TextField(
        '邮箱', [
            validators.Required(),
            validators.Length(min=4, max=30),
            validators.Email(),
        ],
        description='邮箱用于管理帐户'
    )
    password = PasswordField(
        '密码', [
            validators.Required(),
            validators.Length(min=6, max=24),
        ],
        description='密码最少 6 字节'
    )
    password2 = PasswordField(
        '密码确认', [
            validators.Required(),
            validators.Length(min=6, max=24),
        ],
    )

    @orm.db_session
    def validate_name(self, field):
        data = field.data.lower()
        if data in config.forbidden_name_list or User.get(name=data):
            raise ValidationError('此用户名已注册')

    @orm.db_session
    def validate_email(self, field):
        data = field.data.lower()
        if User.get(email=data):
            raise ValidationError('此邮箱已注册')

    def validate_password(self, field):
        if field.data != self.password2.data:
            raise ValidationError('密码不匹配')

    def save(self, role=None):
        data = self.data
        data.pop('password2')
        user = User.init(**data)
        if role:
            user.role = role
        user.save()
        return user


class SigninForm(BaseForm):
    account = TextField(
        '邮箱', [
            validators.Required(),
            validators.Length(min=4, max=30),
        ],
    )
    password = PasswordField(
        '密码', [
            validators.Required(),
            validators.Length(min=6, max=24),
        ]
    )
    # permanent = BooleanField('记住我')

    @orm.db_session
    def validate_password(self, field):
        account = self.account.data
        if '@' in account:
            user = User.get(email=account)
        else:
            user = User.get(name=account)

        if not user:
            raise ValidationError('用户名或密码错误')
        if user.check_password(field.data):
            self.user = user
            return user
        raise ValidationError('用户名或密码错误')


class SettingForm(BaseForm):
    @classmethod
    def init(cls, user=None, **kwargs):
        cls.nickname = TextField(
            '昵称', [
                validators.Required(),
                validators.Length(min=4, max=16),
            ],
            description='您还有 %s 次修改昵称的机会' % user.edit_nickname_count
        )
        cls.urlname = TextField(
            '域名', [
                validators.Required(),
                validators.Length(min=4, max=30),
                validators.Regexp(
                    '^[a-zA-Z0-9_]+$',
                    message='域名只能包含英文字母和数字',
                ),
            ],
            description='您还有 %s 次修改域名的机会' % user.edit_urlname_count
        )
        cls.address = TextField(
            '城市', [
                validators.Length(min=0, max=200),
            ],
        )
        cls.website = TextField(
            '网址', [
                validators.Length(min=0, max=200),
            ],
        )
        cls.description = TextAreaField(
            '简介', [
                validators.Length(min=0, max=10000),
            ],
        )
        cls.style = TextAreaField(
            '样式', [
                validators.Length(min=0, max=1000),
            ],
        )
        cls.site_style = TextAreaField(
            '全站样式', [
                validators.Length(min=0, max=1000),
            ],
        )

        if not kwargs and user:
            kwargs = {
                'nickname': [user.nickname],
                'urlname': [user.urlname],
                'address': [user.address],
                'website': [user.website],
                'description': [user.description],
                'style': [user.style],
                'site_style': [user.site_style]
            }

        sf = cls(kwargs)
        if user:
            sf.edit_nickname_count = user.edit_nickname_count
            sf.edit_urlname_count = user.edit_urlname_count
            sf.user = user
        return sf

    def validate_nickname(self, field):
        data = field.data
        if data != self.user.nickname:
            if self.user.edit_nickname_count < 1:
                raise ValidationError('您已经没有修改昵称的机会')

    def validate_urlname(self, field):
        data = field.data
        if data != self.user.urlname:
            if self.user.edit_urlname_count < 1:
                field.data = self.user.urlname
                raise ValidationError('您已经没有修改域名的机会')
            if data in config.forbidden_name_list or User.get(urlname=data):
                raise ValidationError('此域名已经被占用')

    def save(self, user=None):
        data = self.data
        user = user.update(data)
        return user
