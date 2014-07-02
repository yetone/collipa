# coding: utf-8

from libs.tforms import validators
from libs.tforms.fields import TextField, TextAreaField, SelectField
from libs.tforms.validators import ValidationError
from ._base import BaseForm
import config

from models import Topic, Node, History
from helpers import strip_tags, strip_xss_tags
from libs import ghdiff

config = config.rec()


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
        result = {'status': 'error', 'message': '主题创建失败'}
        for field in self:
            if field.errors:
                for error in field.errors:
                    if field.name == 'title':
                        prev = '标题至少 4 字节'
                    elif field.name == 'content':
                        prev = '内容至少 3 字节'
                    elif field.name == 'node_name':
                        prev = '节点必须选择'

                    result = {'status': 'error', 'message': prev}
        return result

    @classmethod
    def init(cls, choices, selected, args=None):
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
        if args:
            tf = cls(args)
        else:
            tf = cls()
        tf.node_name.data = selected
        return tf

    def validate_node_name(self, field):
        node_name = unicode(self.node_name.data)
        node = Node.get(name=node_name)
        if not node:
            raise ValidationError('不存在此节点')
        self.node = node
        return node

    def save(self, user, topic=None):
        data = self.data
        try:
            data.pop('node_name')
        except:
            print(data)
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
