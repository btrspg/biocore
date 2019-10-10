#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019/6/4 16:13
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : annovar.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
import os
import sys

from biocores import utils
from biocores.bases.tasks import Task
from biocores.softwares.default import *


class Annovar(Task):
    def __init__(self, container):
        super(Annovar, self).__init__(container, 'table_annovar.pl')
        self._table_annovar = self._software
        self._convert2annovar = 'convert2annovar.pl'

    def cmd_version(self):
        return 'echo {repr};{environment} {software} --help  |grep Versions:'.format(
            repr=self.__repr__(),
            environment=self._environment,
            software=self._software
        )

    @utils.special_tmp
    def cmd_annotate(self, vcf, vcfanno, annovardb, tmp='/tmp/annovar'):
        '''

        :param vcf:
        :param vcfanno:
        :param annovardb:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_file(vcfanno), *utils.dirs_for_dirs(tmp))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{convert2annovar} \
        --includeinfo -format vcf4 {vcf} --outfile {tmp}/tmp.avi'
{environment} '{table_annovar} {tmp}/tmp.avi \
        {annovardb} -buildver hg19 \
        -out {vcfanno} \
        {annovar_command}  '       
            '''.format(
            environment=self._environment,
            convert2annovar=self._convert2annovar,
            table_annovar=self._table_annovar,
            annovar_command=ANNOVAR_ANNOTATION_SIMPLE,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    def __repr__(self):
        return 'annovar:' + self._environment

    def __str__(self):
        return 'ANNOVAR is an efficient software tool to utilize update-to-date information to functionally ' \
               'annotate genetic variants detected from diverse genomes'


def test():
    container='determined_sammet'
    annovar=Annovar(container)
    print(annovar.cmd_version())
    print(annovar.cmd_annotate('./analysis_result/TMP/sentieon-test/test.vcf',
                               './analysis_result/TMP/sentieon-test/test.annovar',
                               './database/human/hg19/annotations/humandb/',
                               tmp='./analysis_result/TMP/annovar'))


def main():
    test()


if __name__ == '__main__':
    main()
