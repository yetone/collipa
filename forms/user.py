# coding: utf-8

from libs.tforms import validators
from libs.tforms.fields import TextField, TextAreaField, PasswordField, BooleanField
from libs.tforms.validators import ValidationError
from ._base import BaseForm
import config

from models import User, Message
from pony.orm import *

config = config.rec()

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

    @db_session
    def validate_name(self, field):
        data = field.data.lower()
        if data in config.forbidden_name_list or User.get(name=data):
            raise ValidationError('此用户名已注册')

    @db_session
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
    #permanent = BooleanField('记住我')

    @db_session
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
    nickname = TextField(
        '昵称', [
            validators.Required(),
            validators.Length(min=4, max=16),
        ],
    )
    urlname = TextField(
        '域名', [
            validators.Required(),
            validators.Length(min=4, max=30),
            validators.Regexp(
                '^[a-zA-Z0-9_]+$',
                message='域名只能包含英文字母和数字',
            ),
        ],
        description='让您的域名具有个性'
    )
    address = TextField(
        '城市', [
            validators.Length(min=0, max=200),
        ],
    )
    website = TextField(
        '网址', [
            validators.Length(min=1, max=200),
        ],
    )
    description = TextAreaField(
        '简介', [
            validators.Length(min=1, max=10000),
        ],
    )
    style = TextAreaField(
        '样式', [
            validators.Length(min=0, max=1000),
        ],
    )

    @staticmethod
    def init(user=None, args=None):
        nickname = TextField(
            '昵称', [
                validators.Required(),
                validators.Length(min=4, max=16),
            ],
            description='您还有 %s 次修改昵称的机会' % user.edit_nickname_count
        )
        urlname = TextField(
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
        address = TextField(
            '城市', [
                validators.Length(min=0, max=200),
            ],
        )
        website = TextField(
            '网址', [
                validators.Length(min=0, max=200),
            ],
        )
        description = TextAreaField(
            '简介', [
                validators.Length(min=0, max=10000),
            ],
        )
        style = TextAreaField(
            '样式', [
                validators.Length(min=0, max=1000),
            ],
        )
        SettingForm.nickname = nickname
        SettingForm.urlname = urlname
        SettingForm.address = address
        SettingForm.website = website
        SettingForm.description = description
        SettingForm.style = style

        if not args:
            if user:
                args = {'nickname': [user.nickname], 'urlname': [user.urlname],
                        'address': [user.address], 'website': [user.website],
                        'description': [user.description],
                        'style': [user.style]}
                sf = SettingForm(args)
                sf.edit_nickname_count = user.edit_nickname_count
                sf.edit_urlname_count = user.edit_urlname_count
                sf.user = user
            else:
                sf = SettingForm()
        else:
            if user:
                sf = SettingForm(args)
                sf.edit_nickname_count = user.edit_nickname_count
                sf.edit_urlname_count = user.edit_urlname_count
                sf.user = user
            else:
                sf = SettingForm(args)
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
