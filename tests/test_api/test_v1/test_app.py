#!/usr/bin/python3
'''
Flask API tests
'''
from api.v1 import app
import os
import unittest


class FlaskTestCase(unittest.TestCase):
    '''Tests for Flask api'''

    def setUp(self):
        '''Test setup'''
        self.app = app.app.test_client()
        self.app.testing = True

    def test_status(self):
        '''Test status and return content type'''
        res = self.app.get('/api/v1/status')
        data = res.get_data()
        self.assertEqual(res.status_code, 200)
        self.assertIn(bytes('OK', 'utf-8'), data)
        self.assertEqual('application/json', res.content_type)
