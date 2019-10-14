#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) MIT License
# @Time    : 14/10/2019 12:19 PM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : test_hisat2
# @Software: PyCharm
from unittest import TestCase
from biocores.softwares.hisat2 import Hisat2
from biocores.softwares.samtools import Samtools
from biocores.softwares.default import *





class TestHisat2(TestCase):
    def setUp(self):
        self.hisat2 = Hisat2('hisat2', hisat2Default)

    def test_cmd_version(self):
        self.assertIsInstance(self.hisat2.cmd_version(), str, msg='is str for command')

    def test_cmd_align(self):
        samtools =Samtools('samtools',samtoolsDefault)
        only_pe=['/path/to/hisat2_idx','r1.fq.gz','r2.fq.gz','summary.txt',samtools,'/path/to/samtools_idx','outbam']
        self.assertIsInstance(self.hisat2.cmd_align(*only_pe), str, msg='is str for command')

