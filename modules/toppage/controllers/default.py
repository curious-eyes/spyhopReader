#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import webapp2
from google.appengine.api import users
from spyframework.router import RouterBaseHandler
from models.ndb_feed import NdbFeed
from models.parsefeed import parsefeed


class DefaultHandler(RouterBaseHandler):
    def get(self, *args, **kwargs):
        # RSSフィード一覧取得
        urlLogout = users.create_logout_url('/')
        urlStoreFeed = webapp2.uri_for('store-feed');
        # logging.info(super(DefaultHandler, self).get_module_name())
        feed_key = NdbFeed.get_ancestor()
        feeds = NdbFeed.query_feed(feed_key)
        template_values = {
            'feeds': feeds,
            'urlLogout': urlLogout,
            'urlStoreFeed': urlStoreFeed,
        }
        template = self.JINJA_ENVIRONMENT.get_template('default.html')
        self.response.write(template.render(template_values))


class StoreHandler(RouterBaseHandler):
    def post(self, *args, **kwargs):
        feedurl = self.request.get("url")
        feedparam = parsefeed(feedurl)
        self.response.write(feedurl)

        feed = NdbFeed(title=feedparam['title'],
                       url=feedparam['url'],
                       upday=feedparam['upday'])
        feed.key = feed.gen_key(feedparam['key_name'])
        feed_key = feed.put()
        logging.info(feed_key)
        return webapp2.redirect('/')
