#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) MIT License
# @Time    : 27/11/2019 10:23 AM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : test_gffcompare
# @Software: PyCharm
from unittest import TestCase
from biocores.softwares.gffcompare import Gffcompare
from biocores.softwares.default import *


class TestGffcompare(TestCase):

    def setUp(self):
        self.gffcompare = Gffcompare('gffcompare', gffcompareDefault)

    def test_cmd_version(self):
        self.assertIsInstance(self.gffcompare.cmd_version(), str, msg='is str for command')

    def test_cmd_gffcompare(self):
        forlist = ['gfflist', 'reference', 'prefix']
        forgtfs = [None, 'reference', 'prefix', 'gtf1', 'gtf2']
        self.assertIsInstance(self.gffcompare.cmd_gffcompare(forlist), str, msg='is str for command')
        self.assertIsInstance(self.gffcompare.cmd_gffcompare(forgtfs), str, msg='is str for command')
