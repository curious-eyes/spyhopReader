#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2
import logging
import jinja2
import datetime
from spy_setting import *
from models.feed import Feed
from google.appengine.api import urlfetch
from xml.dom import minidom

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
        self.response.write(feedurl)
        feedtitle = ''
        key_string = ''
        feedinput = urlfetch.fetch(feedurl)
        if feedinput.status_code == 200:
            # self.response.write(feedinput.content)
            rss_parsed = minidom.parseString(feedinput.content)
            xmltitle = rss_parsed.getElementsByTagName("title")[0]
            feedtitle = getText(xmltitle.childNodes)
            xmllink = rss_parsed.getElementsByTagName("link")[0]
            if (xmllink.getAttribute('href')):
                # atom 1.0
                key_string = xmllink.getAttribute('href')
                str_updated = getText(rss_parsed.getElementsByTagName("updated")[0].childNodes)
                feed_updated = datetime.datetime.strptime(str_updated, '%Y-%m-%dT%H:%M:%SZ')
            else:
                # rss 2.0
                key_string = getText(xmllink.childNodes)
                str_updated = getText(rss_parsed.getElementsByTagName("lastBuildDate")[0].childNodes)
                feed_updated = datetime.datetime.strptime(str_updated, '%a, %d %b %Y %H:%M:%S +0000')
        logging.info(feed_updated)

        feed = Feed(key_name=key_string, title=feedtitle, url=feedurl)
        # feed.upday = datetime.datetime.now().date()
        feed.upday = feed_updated
        feed.put()
        return webapp2.redirect('/')


def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc
