#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) MIT License
# @Time    : 10/10/2019 1:30 PM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : test_star
# @Software: PyCharm
from unittest import TestCase
from biocores.softwares.star import Star
from biocores.softwares.default import starDefault


class TestStar(TestCase):
    def setUp(self):
        self.star = Star('STAR', starDefault)

    def test_cmd_version(self):
        self.assertIsInstance(self.star.cmd_version(), str, 'is str for command')

    def test_cmd_align(self):
        se = ['/path/to/star_idx', 'fq1', '', '/path/to/prefix', 'gtf',
              'TEST', 'L1', 'Illumina']
        pe = ['/path/to/star_idx', 'fq1', 'fq2', '/path/to/prefix', 'gtf',
              'TEST', 'L1', 'Illumina', 23, 10]
        self.assertIsInstance(self.star.cmd_align(*pe), str, msg='is str for command')
        self.assertIsInstance(self.star.cmd_align(*se), str, msg='is str for command')


import unittest

if __name__ == '__main__':
    unittest.main()
