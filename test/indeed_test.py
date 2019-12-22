#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 00:12:11 2019

@author: barjan
"""

import unittest.test
import legendary_eureka

class IndeedTest(unittest.TestCase):
    def setUp(self) -> None:
        self.indeed = legendary_eureka.Indeed()
        
    def tearDown(self) -> None:
        self.indeed = None
    
    def test_get_jobs(self):
        
        def correct_what_where():
            return self.assertIsInstance(
                    self.indeed.get_jobs("student software","israel"),
                    dict
            )
        def correct_what():
            return self.assertIsNone(
                    self.indeed.get_jobs("student software","israael")
            )
        def correct_where():
            return self.assertIsNone(
                    self.indeed.get_jobs("studensr","israel")
            )
        def only_what():
            return self.assertIsInstance(
                    self.indeed.get_jobs("student software",""),
                    dict
            )
        def only_where():
            return self.assertIsNone(
                    self.indeed.get_jobs("","israel")
            )
        def broken_link():
            return self.assertIsNone(
                    self.indeed.get_jobs("https://","")
            )

        correct_what_where()                
        correct_what()
        correct_where()
        only_what()
        only_where()
        broken_link()
        
if __name__ == '__main__':
    unittest.main()