# coding: utf-8

import logging
from ._base import BaseForm
from collipa.libs.tforms import validators
from collipa.libs.tforms.fields import TextField, TextAreaField, SelectField
from collipa.libs.tforms.validators import ValidationError
from collipa.models import Topic, Node, History
from collipa.helpers import strip_tags, strip_xss_tags
from collipa.libs import ghdiff


class TopicForm(BaseForm):
    def validate_content(self, field):
        """ 为了照顾一图流
        """
        if field.data.find('<img class="upload-topic-image"') == -1 and\
           field.data.find('<embed type="application') == -1:
            data = strip_tags(field.data)
            if len(data) < 3:
                raise ValidationError('内容至少 3 字符')

    @property
    def result(self):
        msg = u'主题创建失败'
        for field in self:
            if field.errors:
                if field.name == 'title':
                    msg = '标题至少 4 字节'
                elif field.name == 'content':
                    msg = '内容至少 3 字节'
                elif field.name == 'node_name':
                    msg = '节点必须选择'

        result = {'status': 'error', 'message': msg}
        return result

    @classmethod
    def init(cls, choices, selected, **kwargs):
        cls.node_name = SelectField(
            '节点', [
                validators.Required(),
            ],
            choices=choices,
        )
        cls.title = TextField(
            '标题', [
                validators.Required(),
                validators.Length(min=4, max=100),
            ],
        )
        cls.content = TextAreaField(
            '内容', [
                validators.Required(),
                validators.Length(min=3, max=1000000),
            ],
        )
        tf = cls(kwargs)
        tf.node_name.data = selected
        return tf

    def __init__(self, *args, **kwargs):
        self.node = None
        super(TopicForm, self).__init__(*args, **kwargs)

    def validate_node_name(self, field):
        node_name = unicode(self.node_name.data)
        node = Node.get(name=node_name)
        if not node:
            raise ValidationError('不存在此节点')
        self.node = node

    def save(self, user, topic=None):
        data = self.data

        node_name = data.pop('node_name', None)
        if not node_name:
            logging.info('no node_name in form data, data: %s', data)

        if not self.node:
            self.node = Node.get(name=node_name)

        if not self.node:
            logging.info('node is None in form instance, self: %s', self)

        content = unicode(data.get('content'))
        data.update({'user_id': user.id, 'node_id': self.node.id,
                     'content': strip_xss_tags(content)})
        if topic:
            category = 'edit'
            pre_node_id = topic.node_id
            pre_title = topic.title
            pre_content = topic.content
            cur_node_id = data.get('node_id')
            cur_title = data.get('title')
            cur_content = data.get('content')
            changed = 0
            if pre_node_id != cur_node_id:
                topic.node.topic_count -= 1
                self.node.topic_count += 1
                diff_content = '主题节点从' + '<a class="node" href="' +\
                    topic.node.url + '">' + topic.node.name +\
                    '</a>移动到<a class="node" href="' + self.node.url + '">' +\
                    self.node.name + '</a>'
                changed = 1
            if pre_title != cur_title or pre_content != cur_content:
                content1 = '<p><h2>' + pre_title + '</h2></p>' + pre_content
                content2 = '<p><h2>' + cur_title + '</h2></p>' + cur_content
                diff_content = ghdiff.diff(content1, content2, css=None)
                changed = 1
            if changed == 1:
                topic.node_id = cur_node_id
                topic.title = cur_title
                topic.content = cur_content
                History(user_id=user.id, content=diff_content,
                        topic_id=topic.id).save()
            else:
                return topic
        else:
            category = 'create'
            topic = Topic(**data)
        return topic.save(category=category)
