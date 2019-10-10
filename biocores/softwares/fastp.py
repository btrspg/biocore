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
from biocores.softwares.default import *


class Fastp(Task):
    def __init__(self, container):
        super(Fastp, self).__init__(container,'fastp')
        # self._environment is exec for docker container
        self._paras = FASTP_DEFAULT
        self._zcat = 'zcat'


    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;{environment} {software} --version|grep version'.format(
            repr=self.__repr__(),
            environment=self._environment,
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

        output_dirs = utils.string_dirs(' ', *utils.dirs_for_file(cfq1, report_prefix))
        if fq2 == '':
            return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {fastp_paras} -i {fq1} -o {cfq1} --html {report_prefix}.fastp.html \
            --json {report_prefix}.fastp.json'   
            '''.format(environment=self._environment,
                       fastp_paras=self._paras,
                       software=self._software,
                       mkdir_paras=MKDIR_DEFAULT,
                       zcat=self._zcat,
                       **locals())
        else:
            return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {fastp_paras} -i {fq1} -I {fq2} -o {cfq1} -O {cfq2} --html {report_prefix}.fastp.html \
            --json {report_prefix}.fastp.json' 
            '''.format(
                environment=self._environment,
                fastp_paras=self._paras,
                software=self._software,
                mkdir_paras=MKDIR_DEFAULT,
                zcat=self._zcat,
                **locals())

    @classmethod
    def get_paras_for_clean_data(cls, paras, config):
        '''
        from paras and config to get special paras
        :param paras:
        :param config:
        :return:
        '''
        if 'fq' in paras.keys() and 'clean_fq' in paras.keys():
            fq1 = paras['fq']
            fq2 = ''
            cfq1 = paras['clean_fq']
            cfq2 = ''
        elif 'fq1' in paras.keys() and 'fq2' in paras.keys() \
                and 'clean_fq1' in paras.keys() and 'clean_fq2' in paras.keys():
            fq1 = paras['fq1']
            fq2 = paras['fq2']
            cfq1 = paras['cfq1']
            cfq2 = paras['cfq2']
        else:
            raise ValueError('Without fq/fq1/fq2 parameters')
        report_prefix = paras['fastp_qc_prefix'] if 'fastp_qc_prefix' in paras.keys() else 'fastp'
        return {
            'fq1': fq1,
            'fq2': fq2,
            'cfq1': cfq1,
            'cfq2': cfq2,
            'report_prefix': report_prefix
        }

    def __repr__(self):
        return 'fastp:' + self._environment

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
