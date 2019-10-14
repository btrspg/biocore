#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) MIT License
# @Time    : 14/10/2019 12:30 PM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : test_samtools
# @Software: PyCharm
from unittest import TestCase
from biocores.softwares.samtools import Samtools
from biocores.softwares.default import *


class TestSamtools(TestCase):
    def setUp(self):
        self.samtools = Samtools('samtools', samtoolsDefault)
        self.bamfile = 'bamfile'
        self.samtools_idx = 'samtools_idx',
        self.samfile = 'samfile'
        self.sortbam = 'sortbam'

    def test_cmd_version(self):
        self.assertIsInstance(self.samtools.cmd_version(), str, msg='is str for command')

    def test_cmd_sam2bam(self):
        self.assertIsInstance(self.samtools.cmd_sam2bam(self.samtools_idx, self.samfile, self.bamfile), str,
                              msg='is str for command')

    def test_cmd_sort(self):
        self.assertIsInstance(self.samtools.cmd_sort(self.bamfile, self.sortbam), str, msg='is str for command')

    def test_cmd_index(self):
        self.assertIsInstance(self.samtools.cmd_index(self.bamfile), str, msg='is str for command')
