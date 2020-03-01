#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019/7/26 0026 9:32
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : fastqc.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores import utils
from biocores.bases.tasks import Task
from biocores.softwares.default import *


class Fastqc(Task):
    def __init__(self, software, fd):
        super(Fastqc, self).__init__(software)
        self._default = fd
        # self._environment is exec for docker container

    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;{software} -v'.format(
            repr=self.__repr__(),
            software=self._software
        )

    @utils.modify_cmd
    def cmd_fastqc_stat(self, outdir, fq1, fq2=''):
        '''

        :param outdir:
        :param fq:
        :return:
        '''
        return r'''
{software} -o {outdir} {fq1} {fq2}      
        '''.format(
            mkdir_paras=self._default.default,
            software=self._software,
            **locals()
        )

    def __repr__(self):
        return 'fastqc:' + self._software

    def __str__(self):
        return 'A quality control tool for high throughput sequence data.'
