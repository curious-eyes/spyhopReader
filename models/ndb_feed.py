#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


class NdbFeed(ndb.Model):
    title = ndb.TextProperty()
    url = ndb.StringProperty()
    upday = ndb.DateTimeProperty()

    @classmethod
    def gen_key(cls, key_string):
        return ndb.Key(NdbFeed, key_string, parent = ndb.Key('Feed', 'Blogs'))

    @classmethod
    def get_ancestor(cls):
        return ndb.Key('Feed', 'Blogs')

    @classmethod
    def query_feed(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key)
