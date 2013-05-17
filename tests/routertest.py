#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from spyframework.router import parse_handler_template


class RouterTest(unittest.TestCase):

    def testParseHandlerTemplate(self):
        # ルートアクセス時のDefaultHandler
        request_path = '/'
        str_handler = parse_handler_template(request_path)
        self.assertEqual(str_handler, "modules.toppage.controllers.default.DefaultHandler")

        # Moduleのみ指定アクセス時
        request_path = '/'
        str_handler = parse_handler_template(request_path)
        self.assertEqual(str_handler, "modules.toppage.controllers.default.DefaultHandler")

        # Module,Controller指定アクセス時
        request_path = '/toppage/default'
        str_handler = parse_handler_template(request_path)
        self.assertEqual(str_handler, "modules.toppage.controllers.default.DefaultHandler")

        # Module,Controller,Action指定アクセス時
        request_path = '/toppage/default/default'
        str_handler = parse_handler_template(request_path)
        self.assertEqual(str_handler, "modules.toppage.controllers.default.DefaultHandler")

        # Module,Controller指定アクセス時
        request_path = '/toppage/default'
        str_handler = parse_handler_template(request_path)
        self.assertEqual(str_handler, "modules.toppage.controllers.default.DefaultHandler")
