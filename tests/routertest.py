#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import webapp2
from spyframework.router import parse_handler_template


class RouterTest(unittest.TestCase):

    def setUp(self):
        self.testhandler = 'modules.{module}.controllers.{controller}.{action}Handler'

    def testParseHandlerTemplate(self):
        # ルートアクセス時のDefaultHandler
        request_path = '/'
        obj_request = webapp2.Request.blank(request_path)
        str_handler = parse_handler_template(obj_request, self.testhandler, [], {})
        self.assertEqual(str_handler[0], "modules.toppage.controllers.default.DefaultHandler")

        # Moduleのみ指定アクセス時
        request_path = '/toppage'
        obj_request = webapp2.Request.blank(request_path)
        str_handler = parse_handler_template(obj_request, self.testhandler, [], {})
        self.assertEqual(str_handler[0], "modules.toppage.controllers.default.DefaultHandler")

        # Module,Controller指定アクセス時
        request_path = '/toppage/default'
        obj_request = webapp2.Request.blank(request_path)
        str_handler = parse_handler_template(obj_request, self.testhandler, [], {})
        self.assertEqual(str_handler[0], "modules.toppage.controllers.default.DefaultHandler")

        # Module,Controller,Action指定アクセス時
        request_path = '/toppage/default/default'
        obj_request = webapp2.Request.blank(request_path)
        str_handler = parse_handler_template(obj_request, self.testhandler, [], {})
        self.assertEqual(str_handler[0], "modules.toppage.controllers.default.DefaultHandler")

        # Module,Controller,Action,その他パラメータ指定アクセス時
        request_path = '/toppage/default/default/hoge/fuga/aaa/bbb/?ccc=ddd'
        obj_request = webapp2.Request.blank(request_path)
        str_handler = parse_handler_template(obj_request, self.testhandler, [], {})
        self.assertEqual(str_handler[0], "modules.toppage.controllers.default.DefaultHandler")
        self.assertEqual(obj_request.get('hoge'), "fuga")
        self.assertEqual(obj_request.get('aaa'), "bbb")
        self.assertEqual(obj_request.get('ccc'), "ddd")
