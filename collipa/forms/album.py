# coding: utf-8

from ._base import BaseForm
from collipa.libs.tforms import validators
from collipa.libs.tforms.fields import TextAreaField
from collipa.helpers import strip_xss_tags

from collipa.models import Album


class AlbumForm(BaseForm):
    name = TextAreaField(
        '名字', [
            validators.Required(),
            validators.Length(min=1, max=10),
        ],
    )

    @property
    def result(self):
        msg = u'专辑创建失败'
        for field in self:
            if field.errors:
                if field.name == 'content':
                    msg = u'名字至少 3 字节'
        result = {'status': 'error', 'message': msg}
        return result

    def save(self, user):
        data = self.data
        name = unicode(data.get('name'))
        data.update({'user_id': user.id, 'name': strip_xss_tags(name)})
        album = Album(**data)
        return album.save()
