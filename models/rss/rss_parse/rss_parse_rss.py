#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models.rss.abstract_rss_parse import AbstractRssParse

from email.utils import parsedate
from time import mktime
import datetime


class RssParseRss(AbstractRssParse):
    def title(self):
        xmltitle = self._parsed.getElementsByTagName("title")[0]
        return self.text_from_textnode(xmltitle.childNodes)

    def base_link(self):
        xmllink = self._parsed.getElementsByTagName("link")[0]
        return self.text_from_textnode(xmllink.childNodes)

    def lastbuilddate(self):
        if (self._parsed.getElementsByTagName("lastBuildDate")):
            str_updated = self.text_from_textnode(self._parsed.getElementsByTagName("lastBuildDate")[0].childNodes)
        else:
            str_updated = self.text_from_textnode(self._parsed.getElementsByTagName("pubDate")[0].childNodes)
        return datetime.datetime.fromtimestamp(mktime(parsedate(str_updated)))
