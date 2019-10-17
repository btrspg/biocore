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

    def cmd_clean_data(self, fq1, cfq1, fq2, cfq2, report_prefix):
        '''

        :param fq1:
        :param cfq1:
        :param fq2:
        :param cfq2:
        :param report_prefix:
        :return:
        '''
        if fq2 == '':
            return r'''
{software} {fastp_paras} -i {fq1} -o {cfq1} --html {report_prefix}.fastp.html \
            --json {report_prefix}.fastp.json   
            '''.format(
                fastp_paras=self._default.default,
                software=self._software,
                fq1=fq1,
                cfq1=cfq1,
                report_prefix=report_prefix
            )
        else:
            return r'''
{software} {fastp_paras} -i {fq1} -I {fq2} -o {cfq1} -O {cfq2} --html {report_prefix}.fastp.html \
            --json {report_prefix}.fastp.json 
            '''.format(

                fastp_paras=self._default.default,
                software=self._software,
                **locals())

    def __repr__(self):
        return 'fastp:' + self._software

    def __str__(self):
        return 'A tool designed to provide fast all-in-one preprocessing for FastQ files. This tool is developed ' \
               'in C++ with multithreading supported to afford high performance.'


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
