#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2
import jinja2
from spy_setting import *
from models.feed import Feed
from models.parsefeed import parsefeed

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(MODULES_DIR + '/toppage/views/templates'),
    extensions=['jinja2.ext.autoescape'])


class DefaultHandler(webapp2.RequestHandler):
    def get(self, *args, **kwargs):
        # RSSフィード一覧取得
        feeds = Feed.all()
        template_values = {
            'feeds': feeds,
        }
        template = JINJA_ENVIRONMENT.get_template('default.html')
        self.response.write(template.render(template_values))
        """
        feedurl = 'http://www.curious-eyes.com/blog/shuhei/?feed=atom'
        """

    def post(self):
        feedurl = self.request.get("url")
        feedparam = parsefeed(feedurl)
        self.response.write(feedurl)

        feed = Feed(key_name=feedparam['key_name'],
                    title=feedparam['title'],
                    url=feedparam['url'],
                    upday=feedparam['upday'])
        feed.put()
        return webapp2.redirect('/')
