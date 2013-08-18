#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


class NdbItem(ndb.Model):
    title = ndb.TextProperty()
    summary= ndb.StringProperty()
    upday = ndb.DateTimeProperty()

    @classmethod
    def gen_key(cls, key_string):
        return ndb.Key(NdbItem, key_string, parent = ndb.Key('Feed', 'Items'))

    @classmethod
    def get_ancestor(cls):
        return ndb.Key('Feed', 'Items')

    @classmethod
    def query_feed(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key)
