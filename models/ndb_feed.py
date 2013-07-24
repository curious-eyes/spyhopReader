#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


class NdbFeed(ndb.Model):
    title = ndb.TextProperty()
    url = ndb.StringProperty()
    upday = ndb.DateTimeProperty()

    @classmethod
    def gen_key(cls, key_string):
        return ndb.Key(NdbFeed, key_string)
