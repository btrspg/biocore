#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) MIT Lisence
# @Time    : 2019-02-25 14:00
# @Author  : YUELONG.CHEN
# @Mail    : yuelong_chen@yahoo.com
# @File    : bwa.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

import os

from biocores import utils
from biocores.bases.tasks import Task
from biocores.softwares.default import *


class Bwa(Task):
    def __init__(self, container):
        super(Bwa, self).__init__(container, 'bwa')

    def cmd_version(self):
        return 'echo {repr};{environment} {software} 2>&1 |grep Version'.format(
            repr=self.__repr__(),
            environment=self._environment,
            software=self._software
        )
    @utils.modify_cmd
    @utils.special_tmp
    def cmd_align(self, bwa_idx, fq1, fq2, samtools_idx, bam_file, sampleid='', tmp='/tmp/bwa',
                  lane='L1', platform='Illumina'):
        '''

        :param bwa_idx:
        :param fq1:
        :param fq2:
        :param samtools_idx:
        :param bam_file:
        :param tmp:
        :param sampleid:
        :param lane:
        :param platform:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(bam_file))

        if fq2 == '':
            temp_file = os.path.basename(fq1) + '.sai'
            return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {bwa_aln_paras} {bwa_idx} {fq1} > {tmp}/{temp_file} '
{environment} '{software} {bwa_samse_paras} \
        -r "@RG\tID:{sampleid}\tPL:{platform}\tPU:{lane}\tLB:{sampleid}\tSM:{sampleid}" \
        {bwa_idx} {tmp}/{temp_file} {fq1} \
        | samtools view -bSt {samtools_idx} - \
        | samtools sort - -o {bam_file} '
{environment} 'samtools index {bam_file}'
{environment} 'rm {tmp}/{temp_file}'         
            '''.format(
                environment=self._environment,
                software=self._software,
                bwa_aln_paras=BWA_ALN_DEFAULT,
                bwa_samse_paras=BWA_SAMSE_DEFAULT,
                mkdir_paras=MKDIR_DEFAULT,
                **locals()
            )
        else:
            return r'''
{environment} 'mkdir -p {output_dirs}'
{environment} '{software} {bwa_mem_paras} \
        -R "@RG\tID:{lane}\tPL:{platform}\tLB:{sampleid}\tSM:{sampleid}" \
        {bwa_idx} {fq1} {fq2} \
        |samtools view -bSt {samtools_idx} - \
        |samtools sort - -o {bam_file}'
{environment} 'samtools index {bam_file}'
            '''.format(
                environment=self._environment,
                software=self._software,
                bwa_mem_paras=BWA_MEM_DEFAULT,
                **locals()
            )

    def __repr__(self):
        return 'bwa:' + self._environment

    def __str__(self):
        return 'Burrow-Wheeler Aligner for short-read alignment'


def test():
    bwa = Bwa('pipeline')
    print(bwa)
    print(bwa.cmd_version())
    print(bwa.cmd_align('/opt/tmp/test/human_g1k_v37_modified.fasta',
                        '/opt/tmp/test/testpe.clean.1.fq.gz',
                        '/opt/tmp/test/testpe.clean.2.fq.gz',
                        '/opt/tmp/test/human_g1k_v37_modified.fasta.fai',
                        '/opt/tmp/test/test.sort.bam',
                        '/opt/tmp/test/test/tmp',
                        'testpe'))
    print(bwa.cmd_align('/opt/tmp/test/human_g1k_v37_modified.fasta',
                        '/opt/tmp/test/test.clean.1.fq.gz',
                        '',
                        '/opt/tmp/test/human_g1k_v37_modified.fasta.fai',
                        '/opt/tmp/test/test.sort.bam',
                        '/opt/tmp/test/test/',
                        'testse'))


def main():
    test()


if __name__ == '__main__':
    main()
