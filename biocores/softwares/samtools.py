#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019-04-29 17:05
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : fastp.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores.bases.tasks import Task
from biocores import utils


class Samtools(Task):
    def __init__(self, software, fd):
        super(Samtools, self).__init__(software)
        self._default = fd

    @utils.modify_cmd
    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;echo $({software} 2>&1 | grep Version)  '.format(
            repr=self.__repr__(),
            software=self._software
        )

    @utils.modify_cmd
    def cmd_faidx(self,reference):
        '''

        :param reference:
        :return:
        '''
        return r'''
{software} faidx {reference}       
        '''.format(
            software=self._software,
            reference=reference
        )

    @utils.modify_cmd
    def cmd_sam2bam(self, samtools_idx, samfile, bamfile=None):
        '''

        :param samtools_idx:
        :param samfile:
        :param bamfile:
        :return:
        '''
        if None is bamfile:
            bamfile = ''
        else:
            bamfile = '-o ' + bamfile
        return r'''
{samtools} {sam2bam_paras} {samtools_idx} {samfile} {bamfile}
            '''.format(
            sam2bam_paras=self._default.sam2bam,
            samtools=self._software,
            **locals())

    @utils.modify_cmd
    def cmd_sort(self, bamfile, sortbam=None):
        '''

        :return:
        '''
        if None == sortbam:
            sortbam = ''
        else:
            sortbam = '-o ' + sortbam
        return r'''
{samtools} {sort_paras} {bamfile} {sortbam}        
        '''.format(
            samtools=self._software,
            sort_paras=self._default.sort,
            **locals())

    @utils.modify_cmd
    def cmd_index(self, bamfile):
        '''

        :param bamfile:
        :return:
        '''
        return r'''
{samtools} {index_paras} {bamfile}        
            '''.format(
            samtools=self._software,
            index_paras=self._default.index,
            **locals())

    def __repr__(self):
        return 'samtools:' + self._software

    def __str__(self):
        return 'SAM Tools provide various utilities for manipulating alignments in the SAM format, ' \
               'including sorting, merging, indexing and generating alignments in a per-position format.'



def main():
    pass


if __name__ == '__main__':
    main()
