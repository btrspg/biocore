#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019/6/4 11:23
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : vep.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
import os
import sys

from biocores import utils
from biocores.bases.tasks import Task
from biocores.softwares.default import *


class Vep(Task):
    def __init__(self, container):
        super(Vep, self).__init__(container, 'vep')

    def cmd_version(self):
        return 'echo {repr};{environment} {software} --help 2>&1 |grep -A 5 Versions:'.format(
            repr=self.__repr__(),
            environment=self._environment,
            software=self._software
        )

    @utils.special_tmp
    def cmd_annotate(self, vcf, vep_vcf, vep_database, reference):
        '''

        :param vcf:
        :param vep_vcf:
        :param vep_database:
        :param reference:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_file(vep_vcf))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software}  {vep_command} \
            --dir_cache {vep_database}  \
            --plugin ExAC,{vep_database}/pdb/ExAC.r0.3.1.sites.vep.vcf.gz,AC,AN \
            --input_file {vcf} \
            --output_file {vep_vcf} \
            --fasta {reference}'         
            '''.format(
            environment=self._environment,
            software=self._software,
            vep_command=VEP_ANNOTATION_DEFAULT,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    def __repr__(self):
        return 'vep:' + self._environment

    def __str__(self):
        return 'Variant Effect Predictor'


def test():
    container = 'practical_davinci'
    vep = Vep(container)
    print(vep.cmd_version())
    print(vep.cmd_annotate('./analysis_result/TMP/sentieon-test/test.vcf',
                           './analysis_result/TMP/sentieon-test/test.vep.vcf',
                           './database/human/hg19/annotations/VEP/',
                           './database/human/hg19/genome/v0/human_g1k_v37.fasta'))


def main():
    test()


if __name__ == '__main__':
    main()
