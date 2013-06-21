#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import logging
import webapp2
from spyframework.router import RouterBaseHandler
from models.feed import Feed
from models.parsefeed import parsefeed


class DefaultHandler(RouterBaseHandler):
    def get(self, *args, **kwargs):
        # RSSフィード一覧取得
        # logging.info(super(DefaultHandler, self).get_module_name())
        feeds = Feed.all()
        template_values = {
            'feeds': feeds,
        }
        template = self.JINJA_ENVIRONMENT.get_template('default.html')
        self.response.write(template.render(template_values))

    def post(self, *args, **kwargs):
        feedurl = self.request.get("url")
        feedparam = parsefeed(feedurl)
        self.response.write(feedurl)

        feed = Feed(key_name=feedparam['key_name'],
                    title=feedparam['title'],
                    url=feedparam['url'],
                    upday=feedparam['upday'])
        feed.put()
        return webapp2.redirect('/')
