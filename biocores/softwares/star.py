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


class Star(Task):
    def __init__(self, software, fd):
        super(Star, self).__init__(software)
        self._default = fd

    def cmd_version(self):
        return 'echo {repr};{software} --version'.format(
            repr=self.__repr__(),
            software=self._software
        )

    def cmd_align(self, star_idx, fq1, fq2, prefix, gtf, sampleid='TEST',
                  lane='L1', platform='Illumina', readlength=None, threads=None):
        '''

        :param star_idx:
        :param fq1:
        :param fq2:
        :param prefix:
        :param gtf:
        :param sampleid:
        :param tmp:
        :param lane:
        :param platform:
        :return:
        '''
        return r'''
{star} {align_paras} \
    --genomeDir {star_idx} \
    --readFilesIn {fq1} {fq2} \
    --outFileNamePrefix {prefix} \
    --sjdbGTFfile {gtf}  \
    --runThreadN {nt} \
    --sjdbOverhang {rl}
    --outSAMattrRGline "ID:RNA LB:{sampleid} SM:{sampleid} PL:{platform} PU:{platform}"      
            '''.format(
            star=self._software,
            align_paras=self._default.align,
            nt=self._default.nt if None == threads else threads,
            rl=self._default.rl if None == readlength else readlength,
            **locals()
        )

    def __repr__(self):
        return 'star:' + self._software

    def __str__(self):
        return 'Spliced Transcripts Alignment to a Reference'


def main():
    pass


if __name__ == '__main__':
    main()
