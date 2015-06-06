# coding: utf-8

from collipa.libs.tforms import validators
from collipa.libs.tforms.fields import TextField, TextAreaField, SelectMultipleField
from collipa.libs.tforms.validators import ValidationError
from ._base import BaseForm

from collipa.models import Node, NodeNode


class NodeForm(BaseForm):
    @classmethod
    def init(cls, choices, selected):
        cls.parent_name = SelectMultipleField(
            '父节点', [
            ],
            choices=choices,
        )
        cls.name = TextField(
            '节点名', [
                validators.Required(),
                validators.Length(min=1, max=16),
            ],
        )
        cls.urlname = TextField(
            '节点地址', [
                validators.Required(),
                validators.Length(min=2, max=32),
                validators.Regexp(
                    '^[a-zA-Z0-9_]+$',
                    message='节点地址只能包含英文字母和数字',
                ),
            ],
            description='节点地址只能包含英文字母和数字'
        )
        cls.description = TextAreaField(
            '描述', [
                validators.Length(min=0, max=3000),
            ],
            description='节点描述'
        )
        nf = cls()
        nf.parent_name.data = selected
        return nf

    def validate_name(self, field):
        data = field.data.lower()
        if Node.get(name=data):
            raise ValidationError('此节点名已存在')

    def validate_urlname(self, field):
        data = field.data.lower()
        if Node.get(urlname=data):
            raise ValidationError('此节点地址已存在')

    def save(self, user, role=None):
        data = self.data
        try:
            parent_name = data.pop('parent_name')
        except:
            parent_name = None
        data.update({'user_id': user.id})
        node = Node(**data).save()
        if not parent_name:
            if not NodeNode.get(parent_id=1, child_id=node.id):
                NodeNode(parent_id=1, child_id=node.id).save()
        else:
            for name in parent_name:
                parent = Node.get(name=name)
                if parent:
                    if not NodeNode.get(parent_id=parent.id, child_id=node.id):
                        NodeNode(parent_id=parent.id, child_id=node.id).save()
        return node


class NodeEditForm(BaseForm):
    @classmethod
    def init(cls, choices, selected, node=None, **kwargs):
        cls.parent_name = SelectMultipleField(
            '父节点', [
            ],
            choices=choices,
        )
        cls.name = TextField(
            '节点名', [
                validators.Required(),
                validators.Length(min=1, max=16),
            ],
        )
        cls.urlname = TextField(
            '节点地址', [
                validators.Required(),
                validators.Length(min=2, max=32),
                validators.Regexp(
                    '^[a-zA-Z0-9_]+$',
                    message='节点地址只能包含英文字母和数字',
                ),
            ],
            description='节点地址只能包含英文字母和数字'
        )
        cls.description = TextAreaField(
            '描述', [
                validators.Length(min=0, max=3000),
            ],
            description='节点描述'
        )
        cls.style = TextAreaField(
            '样式', [
                validators.Length(min=0, max=1000),
            ],
            description='节点样式'
        )
        nf = cls(kwargs)
        nf.parent_name.data = selected
        nf.node = node
        return nf

    def validate_name(self, field):
        data = field.data.lower()
        node = Node.get(name=data)
        if node and node != self.node:
            raise ValidationError('此节点名已存在')

    def validate_urlname(self, field):
        data = field.data.lower()
        node = Node.get(urlname=data)
        if node and node != self.node:
            raise ValidationError('此节点地址已存在')

    def save(self, user, role=None, node=None):
        data = self.data
        try:
            parent_name = data.pop('parent_name')
        except:
            parent_name = None
        data.update({'user_id': user.id})
        nns = NodeNode.select(lambda rv: rv.child_id == node.id)
        for nn in nns:
            nn.delete()
        if not parent_name:
            if not NodeNode.get(parent_id=1, child_id=node.id):
                NodeNode(parent_id=1, child_id=node.id).save()
        else:
            for name in parent_name:
                parent = Node.get(name=unicode(name))
                if parent:
                    if not NodeNode.get(parent_id=parent.id, child_id=node.id):
                        NodeNode(parent_id=parent.id, child_id=node.id).save()
        node = node.update(data)

        return node
