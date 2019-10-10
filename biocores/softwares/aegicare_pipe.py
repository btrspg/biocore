#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019/7/29 0029 10:52
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : aegicare_pipe.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores import utils
from biocores.bases.tasks import Task
from biocores.softwares.default import *


class AegicarePipe(Task):
    def __init__(self, container):
        super(AegicarePipe, self).__init__(container,'wes-run')
        # self._environment is exec for docker container
        self._reads_to_alignments='reads_to_alignments'
        self._alignments_to_variants='alignments_to_variants'



    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;{environment} echo pipeline-pipe'.format(
            repr=self.__repr__(),
            environment=self._environment,
            software=self._software
        )

    def cmd_reads2alignments(self, sample_id,fq1,fq2,outdir):
        '''

        :param sample_id:
        :param fq1:
        :param fq2:
        :param outdir:
        :return:
        '''

        output_dirs = utils.string_dirs(' ', *utils.dirs_for_dirs(outdir))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{reads_to_alignments} {sample_id} {fq1} {fq2} {outdir} '        
        '''.format(
            environment=self._environment,
            mkdir_paras=MKDIR_DEFAULT,
            reads_to_alignments=self._reads_to_alignments,
            **locals()
        )

    def cmd_alignments2variants(self,sample_id,outdir):
        '''

        :param sample_id:
        :param outdir:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_dirs(outdir))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{alignments_to_variants} {sample_id} {outdir} '        
        '''.format(
            environment=self._environment,
            alignments_to_variants=self._alignments_to_variants,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    def __repr__(self):
        return 'aegicare-pipe:' + self._environment

    def __str__(self):
        return 'Aegicare core reads to variant pipeline.'


