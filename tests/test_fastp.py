#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 10/10/2019 11:18 AM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : test_fastp
# @Software: PyCharm
from unittest import TestCase
from biocores.softwares.fastp import Fastp
from biocores.softwares.default import fastpDefault



class TestFastp(TestCase):
    def setUp(self):
        self.fastp=Fastp('fastp',fastpDefault)

    def test_cmd_version(self):
        self.assertIsInstance(self.fastp.cmd_version(),str,msg='is str for command')


    def test_cmd_clean_data(self):
        se= ['r1.fq.gz','clean.r1.fq.gz','','','prefix']
        pe = ['r1.fq.gz','clean.r1.fq.gz','r2.fq.gz','clean.r2.fq.gz','prefix']
        self.assertIsInstance(self.fastp.cmd_clean_data(*pe),str,msg='is str for command')
        self.assertIsInstance(self.fastp.cmd_clean_data(*se), str, msg='is str for command')

