# coding: utf-8

import tornado.web


class Page(tornado.web.UIModule):
    def render(self, url, page, page_count):
        return self.render_string("modules/page.html", url=url, page=page,
                                  page_count=page_count)


class NotificationList(tornado.web.UIModule):
    def render(self, notifications):
        return self.render_string("modules/notification_list.html",
                                  notifications=notifications)


class MessageBoxList(tornado.web.UIModule):
    def render(self, message_boxes):
        return self.render_string("modules/message_box_list.html",
                                  message_boxes=message_boxes)


class MessageList(tornado.web.UIModule):
    def render(self, messages):
        return self.render_string("modules/message_list.html",
                                  messages=messages)


class MessageForm(tornado.web.UIModule):
    def render(self, user, form, action=None, button="发送"):
        return self.render_string("modules/message_form.html", form=form,
                                  action='/message/create?user_id=%s' % user.id,
                                  user_id=user.id,
                                  button=button)


class NodeForm(tornado.web.UIModule):
    def render(self, form, action=None, button="创建"):
        return self.render_string("modules/node_form.html", form=form, action=action,
                                  button=button)


class TopicForm(tornado.web.UIModule):
    def render(self, form, action=None, button="创建"):
        return self.render_string("modules/topic_form.html", form=form, action=action,
                                  button=button)


class ReplyForm(tornado.web.UIModule):
    def render(self, form, topic, action=None, page=1, button="创建"):
        return self.render_string("modules/reply_form.html", form=form,
                                  topic=topic,
                                  action=action,
                                  page=page,
                                  button=button)


class SettingForm(tornado.web.UIModule):
    def render(self, form, action=None, button="确定"):
        return self.render_string("modules/setting_form.html", form=form, action=action,
                                  button=button)


class Form(tornado.web.UIModule):
    def render(self, form, action=None, button="确定"):
        return self.render_string("modules/form.html", form=form, action=action,
                                  button=button)


class FormContent(tornado.web.UIModule):
    def render(self, form):
        return self.render_string("modules/form_content.html", form=form)


class UserList(tornado.web.UIModule):
    def render(self, users):
        return self.render_string("modules/user_list.html", users=users)


class NodeList(tornado.web.UIModule):
    def render(self, nodes):
        return self.render_string("modules/node_list.html", nodes=nodes)


class HistoryList(tornado.web.UIModule):
    def render(self, histories):
        return self.render_string("modules/history_list.html",
                                  histories=histories)


class TopicWrap(tornado.web.UIModule):
    def render(self, topic, classes=[], key=None):
        return self.render_string("modules/topic_wrap.html", topic=topic,
                                  classes=classes, key=key)


class TopicList(tornado.web.UIModule):
    def render(self, topics):
        return self.render_string("modules/topic_list.html", topics=topics)


class TopicList2(tornado.web.UIModule):
    def render(self, topics):
        return self.render_string("modules/topic_list2.html", topics=topics)


class ReplyList(tornado.web.UIModule):
    def render(self, replies):
        return self.render_string("modules/reply_list.html", replies=replies)


class ReplyList2(tornado.web.UIModule):
    def render(self, replies):
        return self.render_string("modules/reply_list2.html", replies=replies)


class SiteHead(tornado.web.UIModule):
    def render(self):
        return self.render_string("modules/site_head.html")


class UserHead(tornado.web.UIModule):
    def render(self, user):
        return self.render_string("modules/user_head.html", user=user)


class TopicHead(tornado.web.UIModule):
    def render(self):
        return self.render_string("modules/topic_head.html")


class NodeHead(tornado.web.UIModule):
    def render(self):
        return self.render_string("modules/node_head.html")
