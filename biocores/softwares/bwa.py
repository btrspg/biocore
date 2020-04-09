#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019-04-29 17:05
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : bwa.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores import utils
from biocores.bases.tasks import Task


class Bwa(Task):
    def __init__(self, software, fd):
        super(Bwa, self).__init__(software)
        self._default = fd

    def cmd_version(self):
        return 'echo {repr};echo $({software} 2>&1 |grep Version)'.format(
            repr=self.__repr__(),
            software=self._software

        )

    @utils.modify_cmd
    def cmd_build_index(self,reference):
        '''

        :param reference:
        :return:
        '''
        return r'''
{software} {index_paras} {reference}        
        '''.format(
            software=self._software,
            index_paras=self._default.index,
            reference=reference
        )

    @utils.modify_cmd
    def cmd_mirna_align(self, bwa_idx, fq, samtools_idx, bam_file, samtools, sampleid='', lane='L1',
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
{software} {bwa_mirna_paras} \
    {bwa_idx} {fq} > {bam_file}.tmp.sai
{software} samse -r "@RG\tID:{lane}\tPL:{platform}\tLB:{sampleid}\tSM:{sampleid}" \
    {bwa_idx} {bam_file}.tmp.sai {fq} \
    |{samtools} view -bSt {samtools_idx} - \
    |{samtools} sort - -o {bam_file}
{samtools} index {bam_file}
                    '''.format(
            software=self._software,
            samtools=samtools,
            bwa_mirna_paras=self._default.mirna_align,
            lane=lane,
            platform=platform,
            sampleid=sampleid,
            bwa_idx=bwa_idx,
            fq=fq,
            bam_file=bam_file,
            samtools_idx=samtools_idx

        )

    @utils.modify_cmd
    def cmd_align(self, bwa_idx, fq1, fq2, samtools_idx, bam_file, samtools, sampleid='',
                  lane='L1', platform='Illumina'):
        '''

        :param bwa_idx:
        :param fq1:
        :param fq2:
        :param samtools_idx:
        :param bam_file:
        :param samtools:
        :param sampleid:
        :param lane:
        :param platform:
        :return:
        '''

        return r'''
{software} {bwa_mem_paras} \
    -R "@RG\tID:{lane}\tPL:{platform}\tLB:{sampleid}\tSM:{sampleid}" \
    {bwa_idx} {fq1} {fq2} \
    |{samtools} view -bSt {samtools_idx} - \
    |{samtools} sort - -o {bam_file}
{samtools} index {bam_file}
            '''.format(
            software=self._software,
            samtools=samtools,
            bwa_mem_paras=self._default.mem,
            lane=lane,
            platform=platform,
            sampleid=sampleid,
            bwa_idx=bwa_idx,
            fq1=fq1,
            fq2=fq2,
            bam_file=bam_file,
            samtools_idx=samtools_idx

        )

    def __repr__(self):
        return 'bwa:' + self._software

    def __str__(self):
        return 'Burrow-Wheeler Aligner for short-read alignment'
