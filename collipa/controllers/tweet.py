# coding: utf-8

import tornado.web

from ._base import BaseHandler
from pony import orm

from collipa.models import Tweet, Image
from collipa.helpers import strip_xss_tags, strip_tags, require_permission


class HomeHandler(BaseHandler):
    @orm.db_session
    def get(self, tweet_id):
        tweet_id = int(tweet_id)
        tweet = Tweet.get(id=tweet_id)
        if not tweet:
            raise tornado.web.HTTPError(404)
        return self.render("tweet/index.html", tweet=tweet)

    @orm.db_session
    @tornado.web.authenticated
    def put(self, tweet_id):
        tweet_id = int(tweet_id)
        tweet = Tweet.get(id=tweet_id)
        if not tweet:
            raise tornado.web.HTTPError(404)
        action = self.get_argument('action', None)
        user = self.current_user
        if not action:
            result = {'status': 'error', 'message':
                      '缺少参数'}
            return self.send_result(result)
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
        return self.send_result(result)

    @orm.db_session
    @tornado.web.authenticated
    def delete(self, tweet_id):
        if not self.current_user.is_admin:
            return self.redirect_next_url()
        tweet = Tweet.get(id=tweet_id)
        if not tweet:
            return self.redirect_next_url()
        tweet.delete()
        result = {'status': 'success', 'message': '已成功删除'}
        return self.send_result(result)


class CreateHandler(BaseHandler):
    @orm.db_session
    @tornado.web.authenticated
    @require_permission
    def post(self):
        user = self.current_user
        content = self.get_argument('content', None)
        image_ids = self.get_argument('image_ids', None)
        images = []
        if not (content and len(strip_tags(content)) >= 3):
            result = {
                'status': 'error',
                'message': '推文内容至少 3 字符'
            }
            return self.send_result(result, '/timeline')
        tweet = Tweet(content=strip_xss_tags(content), user_id=user.id).save()
        tweet.put_notifier()
        if image_ids:
            image_ids = image_ids.split(',')
            for image_id in image_ids:
                image_id = int(image_id)
                image = Image.get(id=image_id)
                if not image:
                    continue
                image.tweet_id = tweet.id
                images.append({
                    'id': image.id,
                    'path': image.path,
                    'width': image.width,
                    'height': image.height,
                })
        if images:
            tweet.has_img = 'true'
        result = {
            'status': 'success',
            'message': '推文创建成功',
            'content': tweet.content,
            'name': tweet.author.name,
            'nickname': tweet.author.nickname,
            'author_avatar': tweet.author.get_avatar(size=48),
            'author_url': tweet.author.url,
            'author_name': tweet.author.name,
            'author_nickname': tweet.author.nickname,
            'tweet_url': tweet.url,
            'created': tweet.created,
            'id': tweet.id,
            'images': images,
        }
        return self.send_result(result, '/timeline')
