#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019-04-29 17:05
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : bowtie.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores import utils
from biocores.bases.tasks import Task
import os


class Bowtie(Task):
    def __init__(self, software, fd):
        super(Bowtie, self).__init__(software)
        self._default = fd
        self._bin = os.path.dirname(self._software)
        if self._bin == '':
            self._bowtie_build = 'bowtie-build'
        else:
            self._bowtie_build = self._bin + '/bowtie-build'

    def cmd_version(self):
        return 'echo {repr};echo $({software} 2>&1 |grep Version)'.format(
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
            software=self._bowtie_build,
            reference=reference,
            prefix=prefix,
            parameter=self._default.build_index
        )

    @utils.modify_cmd
    def cmd_mirna_align(self, bowtie_idx, fq, samtools_idx, bam_file, samtools, sampleid='', lane='L1',
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
{software} {bowtie_mirna_paras} --sam-RG "ID:{lane}\tPL:{platform}\tLB:{sampleid}\tSM:{sampleid}" \
    {bowtie_idx} {fq} \
    |{samtools} view -bSt {samtools_idx} - \
    |{samtools} sort - -o {bam_file}
{samtools} index {bam_file}
                    '''.format(
            software=self._software,
            samtools=samtools,
            bowtie_mirna_paras=self._default.mirna_align,
            lane=lane,
            platform=platform,
            sampleid=sampleid,
            bowtie_idx=bowtie_idx,
            fq=fq,
            bam_file=bam_file,
            samtools_idx=samtools_idx
        )


    def __repr__(self):
        return 'bowtie:' + self._software

    def __str__(self):
        return 'An ultrafast memory-efficient short read aligner'
