#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019-04-29 17:05
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : bowtie2.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores import utils
from biocores.bases.tasks import Task
import os


class Bowtie2(Task):
    def __init__(self, software, fd):
        super(Bowtie2, self).__init__(software)
        self._default = fd
        self._bin = os.path.dirname(self._software)
        if self._bin == '':
            self._bowtie2_build = 'bowtie2-build'
        else:
            self._bowtie2_build = self._bin + '/bowtie2-build'

    def cmd_version(self):
        return 'echo {repr};echo $({software} 2>&1 |grep version)'.format(
            repr=self.__repr__(),
            software=self._software

        )

    @utils.modify_cmd
    def cmd_build_index(self, reference, prefix):
        '''

        :param reference:
        :param prefix:
        :return:
        '''
        return r'''
{software} {parameter} {reference} {prefix}
        '''.format(
            software=self._bowtie2_build,
            reference=reference,
            prefix=prefix,
            parameter=self._default.build_index
        )

    @utils.modify_cmd
    def cmd_mirna_align(self, bowtie2_idx, fq, samtools_idx, bam_file, samtools, sampleid='', lane='L1',
                        platform='Illumina'):
        '''

        :param bwa_idx:
        :param fq:
        :param samtools_idx:
        :param bam_file:
        :param samtools:
        :param sampleid:
        :param lane:
        :param platform:
        :return:
        '''
        return r'''
{software} {bowtie2_mirna_paras} --rg "ID:{lane}\tPL:{platform}\tLB:{sampleid}\tSM:{sampleid}" \
    -x {bowtie2_idx} {fq} \
    |{samtools} view -bSt {samtools_idx} - \
    |{samtools} sort - -o {bam_file}
{samtools} index {bam_file}
                    '''.format(
            software=self._software,
            samtools=samtools,
            bowtie2_mirna_paras=self._default.mirna_align,
            lane=lane,
            platform=platform,
            sampleid=sampleid,
            bowtie2_idx=bowtie2_idx,
            fq=fq,
            bam_file=bam_file,
            samtools_idx=samtools_idx
        )


    def __repr__(self):
        return 'bowtie2:' + self._software

    def __str__(self):
        return 'Fast and sensitive read alignment'
