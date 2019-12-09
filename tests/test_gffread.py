#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) MIT License
# @Time    : 27/11/2019 2:55 PM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : test_gffread
# @Software: PyCharm
from unittest import TestCase
from biocores.softwares.gffread import Gffread
from biocores.softwares.default import *


class TestGffread(TestCase):

    def setUp(self):
        self.gffread = Gffread('gffread', gffreadDefault)

    def test_cmd_version(self):
        self.assertIsInstance(self.gffread.cmd_version(), str, msg='is str for command')

    def test_cmd_gffread(self):
        self.assertIsInstance(self.gffread.cmd_gffread('reference', 'gtf', 'output_fasta'), str,
                              msg='is str for command')


import unittest

if __name__ == '__main__':
    unittest.main()
