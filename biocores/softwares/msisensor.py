#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2020/3/9 7:16 PM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : msisenser
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores.bases.tasks import Task
from biocores import utils

class Msisenser(Task):
    def __init__(self, software, fd):
        super(Msisenser, self).__init__(software)
        self._default = fd

    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;echo $({software} 2>&1 |grep Version)'.format(
            repr=self.__repr__(),
            software=self._software
        )
    @utils.modify_cmd
    def cmd_scan_reference(self, reference, msi_list):
        '''

        :param reference:
        :param msi_list:
        :return:
        '''
        return r'''
{software} scan -d {reference} -o {msi_list}
        '''.format(
            software=self._software,
            reference=reference,
            msi_list=msi_list
        )

    @utils.modify_cmd
    def cmd_call_msi(self,t_bam,c_bam,msi_list,output):
        '''

        :param t_bam:
        :param c_bam:
        :param msi_list:
        :param output:
        :return:
        '''
        return r'''
{software} msi {default} \
        -d {msi_list} \
        -t {t_bam} \
        -n {c_bam} \
        -o {output}
        '''.format(
            software=self._software,
            msi_list=msi_list,
            t_bam=t_bam,
            c_bam=c_bam,
            output=output,
            default=self._default.msi
        )

    def __repr__(self):
        return 'msisensor:' + self._software

    def __str__(self):
        return 'microsatellite instability detection using tumor only or paired tumor-normal data'

