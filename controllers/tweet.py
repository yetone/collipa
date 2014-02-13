# coding: utf-8

import tornado.web

import config
from ._base import BaseHandler
from pony.orm import *

from models import Tweet
from forms import TweetForm

config = config.rec()


class HomeHandler(BaseHandler):
    @db_session
    def get(self, tweet_id):
        tweet_id = int(tweet_id)
        tweet = Tweet.get(id=tweet_id)
        if not tweet:
            raise tornado.web.HTTPError(404)
        return self.render("tweet/index.html", tweet=tweet)

    @db_session
    def put(self, tweet_id):
        tweet_id = int(tweet_id)
        tweet = Tweet.get(id=tweet_id)
        if not tweet:
            raise tornado.web.HTTPError(404)
        action = self.get_argument('action', None)
        user = self.current_user
        if action and user:
            if action == 'up':
                if tweet.user_id != user.id:
                    result = user.up(tweet_id=tweet.id)
                else:
                    result = {'status': 'info', 'message':
                            '不能为自己的推文投票'}
            if action == 'down':
                if tweet.user_id != user.id:
                    result = user.down(tweet_id=tweet.id)
                else:
                    result = {'status': 'info', 'message':
                            '不能为自己的推文投票'}
            if action == 'collect':
                result = user.collect(tweet_id=tweet.id)
            if action == 'thank':
                result = user.thank(tweet_id=tweet.id)
            if action == 'report':
                result = user.report(tweet_id=tweet.id)
            if self.is_ajax:
                return self.write(result)
            self.flash_message(result)
            return self.redirect_next_url()

    @db_session
    @tornado.web.authenticated
    def delete(self, tweet_id):
        if not self.current_user.is_admin:
            return self.redirect_next_url()
        tweet = Tweet.get(id=tweet_id)
        if not tweet:
            return self.redirect_next_url()
        tweet.remove()
        result = {'status': 'success', 'message': '已成功删除'}
        return self.write(result)


class CreateHandler(BaseHandler):
    @db_session
    @tornado.web.authenticated
    def post(self):
        if not self.has_permission:
            return
        user = self.current_user
        form = TweetForm(self.request.arguments)
        if form.validate():
            tweet = form.save()
            tweet.put_notifier()
            result = {
                        'status'          : 'success',
                        'message'         : '推文创建成功',
                        'content'         : tweet.content,
                        'name'            : tweet.author.name,
                        'nickname'        : tweet.author.nickname,
                        'author_avatar'   : tweet.author.get_avatar(size=48),
                        'author_url'      : tweet.author.url,
                        'author_name'     : tweet.author.name,
                        'author_nickname' : tweet.author.nickname,
                        'tweet_url'       : tweet.url,
                        'created'         : tweet.created,
                        'id'              : tweet.id
                    }
            if self.is_ajax:
                return self.write(result)
            self.flash_message(result)
            return self.redirect(topic.url)
        if self.is_ajax:
            return self.write(form.result)
        self.flash_message(form.result)
        return self.redirect('/timeline')


class EditHandler(BaseHandler):
    @db_session
    @tornado.web.authenticated
    def get(self, tweet_id):
        if not self.has_permission:
            return
        tweet = Tweet.get(id=tweet_id)
        if not tweet or (tweet.author != self.current_user and not self.current_user.is_admin):
            return self.redirect_next_url()
        form = TweetForm(content=tweet.content)
        return self.render("tweet/edit.html", form=form, tweet=tweet)

    @db_session
    @tornado.web.authenticated
    def post(self, tweet_id):
        if not self.has_permission:
            return
        tweet = Tweet.get(id=tweet_id)
        if not tweet or (tweet.author != self.current_user and not self.current_user.is_admin):
            return self.redirect_next_url()
        user = self.current_user
        form = TweetForm(self.request.arguments)
        if form.validate():
            tweet = form.save(user=user, topic=tweet.topic, tweet=tweet)
            tweet.put_notifier()
            result = {
                    'status': 'success',
                    'message': '推文修改成功',
                    'tweet_url': tweet.url
                    }
            if self.is_ajax:
                return self.write(result)
            self.flash_message(result)
            return self.redirect(tweet.url)
        if self.is_ajax:
            return self.write(form.result)
        return self.render("tweet/edit.html", form=form, tweet=tweet)
