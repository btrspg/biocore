#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) MIT License
# @Time    : 2/12/2019 12:42 PM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : test_minimap2
# @Software: PyCharm
from unittest import TestCase
from biocores.softwares.minimap2 import Minimap2
from biocores.softwares.default import *


class TestMinimap2(TestCase):
    def setUp(self):
        self.minimap2 = Minimap2('Minimap2', minimap2Default)

    def test_cmd_version(self):
        self.assertIsInstance(self.minimap2.cmd_version(), str, msg='is str for command')

    def test_cmd_align(self):
        self.assertIsInstance(self.minimap2.cmd_align('reference', 'fa_fq', 'output', preset_options=' -x splice:hq'),
                              str, msg='is str for command')
        self.assertIsInstance(
            self.minimap2.cmd_align('reference', ['fa_fq1', 'fq2'], 'output', preset_options=' -x splice:hq'),
            str, msg='is str for command')


import unittest

if __name__ == '__main__':
    unittest.main()
