#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) MIT License
# @Time    : 14/10/2019 12:30 PM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : test_samtools
# @Software: PyCharm
from unittest import TestCase
from subprocess import check_call
from biocores.softwares.samtools import Samtools
from biocores.softwares.default import *


class TestSamtools(TestCase):
    def setUp(self):
        self.samtools = Samtools('samtools', samtoolsDefault)
        self.bamfile = 'tests/test-data/bam/HS.MT.Raw.bam'
        self.samtools_idx = 'tests/test-data/fasta/Homo_sapiens.GRCh38.dna.primary_assembly.chromosomeMT.fa.fai',
        self.samfile = 'tests/test-data/bam/header.sam'
        self.newbam = 'tests/test-data/header.bam'
        self.sortbam = 'tests/test-data/sort.bam'

    def test_cmd_version(self):
        run_ok = False
        self.assertIsInstance(self.samtools.cmd_version(), str, msg='is str for command')
        if check_call(self.samtools.cmd_version(), shell=True):
            run_ok = True
        self.assertTrue(run_ok, msg='command could not run healthily')

    def test_cmd_sam2bam(self):
        run_ok = False
        self.assertIsInstance(self.samtools.cmd_sam2bam(self.samtools_idx, self.samfile, self.newbam), str,
                              msg='is str for command')
        if check_call(self.samtools.cmd_sam2bam(self.samtools_idx, self.samfile, self.newbam), shell=True):
            run_ok = True
        self.assertTrue(run_ok, msg='command could not run healthily')

    def test_cmd_sort(self):
        run_ok = False
        self.assertIsInstance(self.samtools.cmd_sort(self.bamfile, self.sortbam), str, msg='is str for command')
        if check_call(self.samtools.cmd_sort(self.bamfile, self.sortbam), shell=True):
            run_ok = True
        self.assertTrue(run_ok, msg='command could not run healthily')

    def test_cmd_index(self):
        run_ok = False
        self.assertIsInstance(self.samtools.cmd_index(self.newbam), str, msg='is str for command')
        if check_call(self.samtools.cmd_index(self.bamfile), shell=True):
            run_ok = True
        self.assertTrue(run_ok, msg='command could not run healthily')


import unittest

if __name__ == '__main__':
    unittest.main()
