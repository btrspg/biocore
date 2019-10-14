#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) MIT License
# @Time    : 14/10/2019 1:12 PM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : test_trinity
# @Software: PyCharm
from unittest import TestCase
from biocores.softwares.trinity import Trinity
from biocores.softwares.default import *


class TestTrinity(TestCase):
    def setUp(self):
        self.trinity = Trinity('Trinity', trinityDefault)

    def test_cmd_version(self):
        self.assertIsInstance(self.trinity.cmd_version(), str, msg='is str for command')

    def test_cmd_assemble_transcript(self):
        fq1 = 'fq1.fq.gz'
        fq1s = ['1.fq.gz', '1.1.fq.gz']
        fq2 = 'fq2.fq.gz'
        fq2s = ['2.fq.gz', '2.1.fq.gz']
        outdir = '/path/to/outdir'
        memory = '1G'
        nt = 10
        self.assertIsInstance(self.trinity.cmd_assemble_transcript(fq1, fq2, outdir, memory, nt), str,
                              msg='is str for command')
        self.assertIsInstance(self.trinity.cmd_assemble_transcript(fq1s, fq2s, outdir), str,
                              msg='is str for command')
