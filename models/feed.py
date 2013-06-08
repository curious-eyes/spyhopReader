#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import db


class Feed(db.Model):
    title = db.StringProperty()
    url = db.StringProperty()
    upday = db.DateTimeProperty()
