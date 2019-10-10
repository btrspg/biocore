#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019-04-29 17:05
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : fastp.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores import utils
from biocores.bases.tasks import Task


class Hisat2(Task):
    def __init__(self, software, fd):
        super(Hisat2, self).__init__(software)
        self._default = fd

    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;{software} 2>&1|grep Version'.format(
            repr=self.__repr__(),
            software=self._software
        )

    def cmd_clean_data(self,hisat2_idx, fq1, fq2, summary , samtools,samtools_idx):
        '''

        :param fq1:
        :param cfq1:
        :param fq2:
        :param cfq2:
        :param report_prefix:
        :return:
        '''

        return r'''
{hisat2} {align_paras} -x {hisat2_idx} -1 {fq1} -2 {fq2} --summary-file {summary} | {samtools_sam2bam} | {samtools_sort}
{samtools_index}
 
            '''.format(
                align_paras=self._default.align,
                hisat2=self._software,




            )


    def __repr__(self):
        return 'fastp:' + self._software

    def __str__(self):
        return 'graph-based alignment of next generation sequencing reads to a population of genomes'


def test():
    fastp = Fastp('pipeline')
    print(fastp.cmd_version())
    print(fastp.cmd_clean_data('/opt/tmp/test/AS2818.clean.1.fq.gz',
                               '/opt/tmp/test/testpe.clean.1.fq.gz',
                               '/opt/tmp/test/AS2818.clean.2.fq.gz',
                               '/opt/tmp/test/testpe.clean.2.fq.gz',
                               '/opt/tmp/test/testpe'))
    print(fastp.cmd_clean_data('/opt/tmp/test/AS2818.clean.1.fq.gz',
                               '/opt/tmp/test/testse.clean.1.fq.gz',
                               '',
                               '',
                               '/opt/tmp/test/test-se'))


def main():
    test()


if __name__ == '__main__':
    main()
