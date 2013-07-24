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
        # logging.info(super(DefaultHandler, self).get_module_name())
        feeds = NdbFeed.query()
        template_values = {
            'feeds': feeds,
            'urlLogout': urlLogout,
        }
        template = self.JINJA_ENVIRONMENT.get_template('default.html')
        self.response.write(template.render(template_values))

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
