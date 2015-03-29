# coding: utf-8

import tornado.web

from ._base import BaseHandler
from pony import orm

from collipa.models import Album, User, Tweet
from collipa.helpers import strip_tags, require_permission


class HomeHandler(BaseHandler):
    @orm.db_session
    def get(self, album_id):
        album_id = int(album_id)
        album = Album.get(id=album_id)
        if not album:
            raise tornado.web.HTTPError(404)
        return self.render("album/index.html", album=album, page=self.page)

    @orm.db_session
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
            self.flash_message(**result)
            return self.redirect_next_url()

    @orm.db_session
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
    @orm.db_session
    @require_permission
    @tornado.web.authenticated
    def post(self):
        if not self.has_permission:
            return
        user = self.current_user
        name = self.get_argument('name', None)
        name = strip_tags(name)
        if not name:
            return self.send_error_result(msg=u'没有填写专辑名')

        if len(name) >= 10:
            return self.send_error_result(msg=u'专辑名不能超过 10 个字符')

        album = Album(name=name, user_id=user.id).save()
        return self.send_success_result(**album.to_dict())


class ListHandler(BaseHandler):
    @orm.db_session
    def get(self):
        user = self.current_user
        user_id = self.get_int('user_id', None)
        if user_id:
            user = User.get(id=user_id)
        if not user:
            return self.send_error_result(msg=u'没有指定用户 id')
        albums = user.get_albums(page=None)
        object_list = [album.to_simple_dict() for album in albums]
        data = {
            'object_list': object_list,
        }
        return self.send_success_result(**data)
