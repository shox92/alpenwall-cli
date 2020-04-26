#!/usr/bin/env python

import unittest
import time
import subprocess

#unittest.main(warnings='ignore')

class MistbornCLITest(unittest.TestCase):
    config = {}

    def setUp(self):
        pass        

    def tearDown(self):
        pass
    
    def test_dummy(self):
        self.assertTrue(True)

    def test_ping(self):
        result = subprocess.check_output('mistborn-cli ping', shell=True)
        self.assertIn("pong", result.decode('utf-8'))
