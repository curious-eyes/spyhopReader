#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from google.appengine.api import urlfetch
from xml.dom import minidom


class GaeUrlFetch:
    __metaclass__ = ABCMeta

    def __init__(self, location):
        self._content = None
        self._url = urlfetch.fetch(location)

    def header(self):
        return dict(self._url.headers.items())

    def get(self):
        if self._content is None:
            self._content = minidom.parseString(self._url.content)
        return self._content


class AbstractRssParse:
    __metaclass__ = ABCMeta

    def __init__(self, str_parsed):
        self._parsed = str_parsed

    def text_from_textnode(self, nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc

    @abstractmethod
    def title(self):
        pass

    @abstractmethod
    def base_link(self):
        pass

    @abstractmethod
    def lastbuilddate(self):
        pass
