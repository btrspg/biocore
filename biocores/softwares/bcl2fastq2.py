#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019-07-13 10:53
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : bcl2fastq2
# @Software: PyCharm


from biocores import utils
from biocores.bases.tasks import Task
from biocores.softwares.default import *


class Bcl2fastq2(Task):
    def __init__(self, container):
        super(Bcl2fastq2, self).__init__(container, 'bcl2fastq')

    def cmd_version(self):
        return 'echo {repr};{environment} {software} '.format(
            repr=self.__repr__(),
            environment=self._environment,
            software=self._software
        )

    @utils.special_tmp
    def cmd_bcl2fastq(self, bcl_root, fastq_root, sample_sheet):
        '''

        :param bcl_root:
        :param fastq_root:
        :param sample_sheet:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_file(fastq_root))

        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {bcl2fastq2_paras} \
            -R {bcl_root} \
            -o {fastq_root} \
            --sample-sheet {sample_sheet}       
        '''.format(
            environment=self._environment,
            software=self._software,
            mkdir_paras=MKDIR_DEFAULT,
            bcl2fastq2_paras=BCL2FASTQ2_DEFAULT,
            **locals()
        )

    def __repr__(self):
        return 'bcl2fastq2:' + self._environment

    def __str__(self):
        return 'Bcl2fastq2 Conversion Software'
