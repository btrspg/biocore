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


class Fastp(Task):
    def __init__(self, software, fd):
        super(Fastp, self).__init__(software)
        self._default = fd

    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;{software} --version'.format(
            repr=self.__repr__(),
            software=self._software
        )

    @utils.modify_cmd
    def cmd_clean_data(self, fq1, cfq1, fq2, cfq2, report_prefix, adapter_fasta=None):
        '''

        :param fq1:
        :param cfq1:
        :param fq2:
        :param cfq2:
        :param report_prefix:
        :param adapter_fasta:
        :return:
        '''

        if fq2 == '':
            return r'''
{software} {fastp_paras} {se} -i {fq1} -o {cfq1} --html {report_prefix}.fastp.html \
            --json {report_prefix}.fastp.json {adapter_fasta}
            '''.format(
                fastp_paras=self._default.default,
                software=self._software,
                fq1=fq1,
                cfq1=cfq1,
                report_prefix=report_prefix,
                se=self._default.se,
                adapter_fasta='--adapter_fasta ' + adapter_fasta if adapter_fasta is not None else ''
            )
        else:
            return r'''
{software} {fastp_paras}  {pe} -i {fq1} -I {fq2} -o {cfq1} -O {cfq2} --html {report_prefix}.fastp.html \
            --json {report_prefix}.fastp.json 
            '''.format(

                fastp_paras=self._default.default,
                software=self._software,
                pe=self._default.pe,
                **locals())

    def __repr__(self):
        return 'fastp:' + self._software

    def __str__(self):
        return 'A tool designed to provide fast all-in-one preprocessing for FastQ files. This tool is developed ' \
               'in C++ with multithreading supported to afford high performance.'
