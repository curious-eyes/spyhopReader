#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2
import logging
import jinja2
from spy_setting import *
# from google.appengine.api import urlfetch
# from xml.dom import minidom

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(MODULES_DIR + '/toppage/views/templates'),
    extensions=['jinja2.ext.autoescape'])


class DefaultHandler(webapp2.RequestHandler):
    def get(self, *args, **kwargs):
        template_values = {
            'msg': 'Hello world!!',
        }
        get_values = self.request.get("more")
        logging.info(get_values)
        logging.info(kwargs)
        template = JINJA_ENVIRONMENT.get_template('default.html')
        self.response.write(template.render(template_values))
        """
        feedurl = 'http://www.curious-eyes.com/blog/shuhei/?feed=atom'
        feedinput = urlfetch.fetch(feedurl)
        if feedinput.status_code == 200:
            # self.response.write(feedinput.content)
            rss_parsed = minidom.parseString(feedinput.content)
            xmltitle = rss_parsed.getElementsByTagName("title")[0]
            self.response.write(getText(xmltitle.childNodes))
        """


def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc
