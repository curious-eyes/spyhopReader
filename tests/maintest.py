#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from webtest import TestApp

from google.appengine.ext import testbed

from main import app


class MainTest(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()

        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.setup_env(app_id='curious-eyes-third')
        self.testbed.activate()

        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()

        # create a test server for us to prod
        self.testapp = TestApp(app)

    def tearDown(self):
        self.testbed.deactivate()

    def testFetchRootURL(self):
        result = self.testapp.get("/")
        self.assertEqual(result.status, "200 OK")
