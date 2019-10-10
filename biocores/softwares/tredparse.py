#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019/6/20 0020 13:21
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : tredparse.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
import os
import sys

from biocores import utils
from biocores.bases.tasks import Task
from biocores.softwares.default import *


class Tredparse(Task):
    def __init__(self, container):
        super(Tredparse, self).__init__(container, 'tred.py')
        self._tredreport = 'tredreport.py'
        self._tredplot = 'tredplot.py'

    def cmd_version(self):
        return 'echo {repr};{environment} {software} --version'.format(
            repr=self.__repr__(),
            environment=self._environment,
            software=self._software
        )

    @utils.special_tmp
    def cmd_call_str_variant(self, bam, workdir,sample_id,final_str):
        '''

        :param bam:
        :param workdir:
        :param sample_id:
        :param final_str:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_dirs(workdir),*utils.dirs_for_file(final_str))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {tredparse_paras} \
            --workdir {workdir} \
            {bam}'
{environment} '{tredreport} {tredreport_paras} \
            --tsv {workdir}/{sample_id}.tsv \
            {workdir}/*.json'
{environment} 'cp {workdir}/{sample_id}.tsv.cases.txt {final_str}'  
        '''.format(
            environment=self._environment,
            software=self._software,
            mkdir_paras=MKDIR_DEFAULT,
            output_dirs=output_dirs,
            tredparse_paras=TREDPARSE_DEFAULT,
            tredreport_paras=TREDREPORT_DEFAULT,
            tredreport=self._tredreport,
            workdir=workdir,
            sample_id=sample_id,
            final_str=final_str,
            bam=bam

        )

    def __repr__(self):
        return 'tredparse:' + self._environment

    def __str__(self):
        return 'TREDPARSE: HLI Short Tandem Repeat (STR) caller'


def main():
    pass


if __name__ == '__main__':
    main()
