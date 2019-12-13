#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) MIT License
# @Time    : 2/12/2019 12:42 PM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : test_minimap2
# @Software: PyCharm
import unittest
from unittest import TestCase
from subprocess import run
from biocores.softwares.minimap2 import Minimap2
from biocores.softwares.default import *


class TestMinimap2(TestCase):
    def setUp(self):
        self.minimap2 = Minimap2('minimap2', minimap2Default)
        self.fastafile1 = './tests/test-data/fasta/MT.read1.fasta'
        self.fastafile2 = './tests/test-data/fasta/MT.read2.fasta'
        self.reference = './tests/test-data/fasta/Homo_sapiens.GRCh38.dna.primary_assembly.chromosomeMT.fa'
        self.out = './tests/test-data/minimap2.out'

    def test_cmd_version(self):
        self.assertIsInstance(self.minimap2.cmd_version(), str, msg='is str for command')
        run_ok = run(self.minimap2.cmd_version(), shell=True)
        self.assertEqual(run_ok.returncode, 0, msg='command could not run healthily')

    def test_cmd_align(self):
        self.assertIsInstance(self.minimap2.cmd_align('reference', 'fa_fq', 'output', preset_options=' -x splice:hq'),
                              str, msg='is str for command')
        self.assertIsInstance(
            self.minimap2.cmd_align('reference', ['fa_fq1', 'fq2'], 'output', preset_options=' -x splice:hq'),
            str, msg='is str for command')
        run_ok = run(self.minimap2.cmd_align(self.reference, self.fastafile1, self.out + '1.out'), shell=True)
        self.assertEqual(run_ok.returncode, 0, msg='command could not run healthily')
        run_ok = run(self.minimap2.cmd_align(self.reference, [self.fastafile1, self.fastafile2], self.out + '2.out'),
                     shell=True)
        self.assertEqual(run_ok.returncode, 0, msg='command could not run healthily')


if __name__ == '__main__':
    unittest.main()
