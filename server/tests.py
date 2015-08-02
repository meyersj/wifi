#!env/bin/python

import os
import unittest
import json

import requests
from flask import Flask

from app import app
from app import db


class WebAPITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_pings_mac(self):
        rv = self.app.get(
            '/api/pings',
            data=dict(
        	    mac="18:22:7e:ea:56:ef",
            ),
            follow_redirects=True
        )
        #data = json.loads(rv.data)
        #for row in data["data"]:
        #    print row


    def test_pings_unique(self):
        rv = self.app.get(
            '/api/pings',
            data=dict(
                unique=True
            ),
            follow_redirects=True
        )
        data = json.loads(rv.data)
        for row in data["data"]:
            print row


if __name__ == '__main__':
    unittest.main()
