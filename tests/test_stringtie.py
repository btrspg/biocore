#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) MIT License
# @Time    : 14/10/2019 12:47 PM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : test_stringtie
# @Software: PyCharm
from unittest import TestCase
from biocores.softwares.stringtie import Stringtie
from biocores.softwares.default import *


class TestStringtie(TestCase):
    def setUp(self):
        self.stringtie=Stringtie('stringtie',stringtieDefault)

    def test_cmd_version(self):
        self.assertIsInstance(self.stringtie.cmd_version(), str, msg='is str for command')

    def test_cmd_assemble_transcript(self):
        bam='bamfile'
        bams=['bam1','bam2','bam3']
        outgtf='outgtf'
        annogtf='annotation.gtf'
        self.assertIsInstance(self.stringtie.cmd_assemble_transcript(bams,outgtf,annogtf),str,msg='is str for command')
        self.assertIsInstance(self.stringtie.cmd_assemble_transcript(bam, outgtf, annogtf), str,
                              msg='is str for command')

    def test_cmd_merge_gtf(self):
        gtf='1.gtf'
        gtfs=['1.gtf','2.gtf','3.gtf']
        output='/path/to/output.gtf'
        self.assertIsInstance(self.stringtie.cmd_merge_gtf(self,gtf,output))
        self.assertIsInstance(self.stringtie.cmd_merge_gtf(self, gtfs, output))
