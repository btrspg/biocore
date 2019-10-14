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

    def cmd_align(self,hisat2_idx, fq1, fq2, summary , samtools,samtools_idx,outbam):
        '''

        :param hisat2_idx:
        :param fq1:
        :param fq2:
        :param summary:
        :param samtools:
        :param samtools_idx:
        :param outbam:
        :return:
        '''

        return r'''
{hisat2} {align_paras} -x {hisat2_idx} -1 {fq1} -2 {fq2} --summary-file {summary} | {samtools_sam2bam} | {samtools_sort}
{samtools_index}
 
            '''.format(
            hisat2=self._software,
            align_paras=self._default.align,
            samtools_sam2bam=samtools.cmd_sam2bam(samtools_idx,'-',bamfile=None),
            samtools_sort=samtools.cmd_sort('-',sortbam=outbam),
            samtools_index=samtools.cmd_index(outbam),
            **locals()
            )


    def __repr__(self):
        return 'hisat2:' + self._software

    def __str__(self):
        return 'graph-based alignment of next generation sequencing reads to a population of genomes'




def main():
    pass

if __name__ == '__main__':
    main()
