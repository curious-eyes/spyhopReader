#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models.rss.abstract_rss_parse import AbstractRssParse

import datetime
import re


class RssParseAtom(AbstractRssParse):
    def title(self):
        xmltitle = self._parsed.getElementsByTagName("title")[0]
        return self.text_from_textnode(xmltitle.childNodes)

    def base_link(self):
        xmllink = self._parsed.getElementsByTagName("link")[0]
        return xmllink.getAttribute('href')

    def lastbuilddate(self):
        str_updated = self.text_from_textnode(self._parsed.getElementsByTagName("updated")[0].childNodes)
        # erase TimeZone (ISO 8601)
        str_updated = re.sub(r'(\-|\+)[0-9]{2}(|\:)[0-9]{2}$', 'Z', str_updated)
        return datetime.datetime.strptime(str_updated, '%Y-%m-%dT%H:%M:%SZ')
