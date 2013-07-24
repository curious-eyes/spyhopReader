#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.api import urlfetch
from xml.dom import minidom
from models.rss.rss_parse.rss_parse_rss import RssParseRss
from models.rss.rss_parse.rss_parse_atom import RssParseAtom


def parsefeed(url):
    dict_return = {}
    dict_return['url'] = url
    feedinput = urlfetch.fetch(url)
    if feedinput.status_code == 200:
        rss_parsed = minidom.parseString(feedinput.content)
        xmllink = rss_parsed.getElementsByTagName("link")[0]
        if (xmllink.getAttribute('href')):
            # atom 1.0
            objARP = RssParseAtom(rss_parsed)
        else:
            # rss 2.0
            objARP = RssParseRss(rss_parsed)
    dict_return['title'] = objARP.title()
    dict_return['upday'] = objARP.lastbuilddate()
    dict_return['key_name'] = objARP.base_link()
    return dict_return


def get_textnode(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc
