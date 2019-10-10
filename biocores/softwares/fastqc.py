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
    def __init__(self, container):
        super(Fastqc, self).__init__(container,'fastqc')
        # self._environment is exec for docker container



    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;{environment} {software} -v'.format(
            repr=self.__repr__(),
            environment=self._environment,
            software=self._software
        )

    def cmd_fastqc_stat(self, outdir,fq1,fq2=''):
        '''

        :param outdir:
        :param fq:
        :return:
        '''

        output_dirs = utils.string_dirs(' ', *utils.dirs_for_dirs(outdir))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} -o {outdir} {fq1} {fq2}'        
        '''.format(
            environment=self._environment,
            mkdir_paras=MKDIR_DEFAULT,
            software=self._software,
            **locals()
        )

    def __repr__(self):
        return 'fastqc:' + self._environment

    def __str__(self):
        return 'A quality control tool for high throughput sequence data.'



