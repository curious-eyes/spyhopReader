#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.api import urlfetch
from email.utils import parsedate
from time import mktime
import datetime
import logging
from xml.dom import minidom


def parsefeed(url):
    dict_return = {}
    dict_return['url'] = url
    feedtitle = ''
    key_string = ''
    feedinput = urlfetch.fetch(url)
    if feedinput.status_code == 200:
        # dict_return[response.write(feedinput.content)
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
            if (rss_parsed.getElementsByTagName("lastBuildDate")):
                str_updated = getText(rss_parsed.getElementsByTagName("lastBuildDate")[0].childNodes)
            else:
                str_updated = getText(rss_parsed.getElementsByTagName("pubDate")[0].childNodes)
            feed_updated = datetime.datetime.fromtimestamp(mktime(parsedate(str_updated)))
    logging.info(feed_updated)
    dict_return['title'] = feedtitle
    dict_return['upday'] = feed_updated
    dict_return['key_name'] = key_string
    return dict_return


def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc
