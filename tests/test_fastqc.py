#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 10/10/2019 11:56 AM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : test_fastqc
# @Software: PyCharm
from unittest import TestCase
from biocores.softwares.fastqc import Fastqc
from biocores.softwares.default import fastqcDefault


class TestFastqc(TestCase):
    def setUp(self):
        self.fastqc = Fastqc('fastqc', fastqcDefault)

    def test_cmd_version(self):
        self.assertIsInstance(self.fastqc.cmd_version(), str, msg='is str for command')

    def test_cmd_fastqc_stat(self):
        se = ['/path/to/outdir', 'r1.fq.gz']
        pe = ['/path/to/outdir', 'r1.fq.gz', 'r2.fq.gz']
        self.assertIsInstance(self.fastqc.cmd_fastqc_stat(*pe), str, msg='is str for command')
        self.assertIsInstance(self.fastqc.cmd_fastqc_stat(*se), str, msg='is str for command')
