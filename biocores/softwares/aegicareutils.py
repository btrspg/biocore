#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019/6/25 0025 16:20
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : aegicareutils.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
import os
import sys

from biocores import utils
from biocores.bases.tasks import Task
from biocores.softwares.default import *


class AegicareUtils(Task):
    def __init__(self, container):
        super(AegicareUtils, self).__init__(container, 'Aegicare-Seg')
        self._aegicare_qc = 'Aegicare-QC'

    def cmd_version(self):
        return 'echo {repr};{environment} {software} --help '.format(
            repr=self.__repr__(),
            environment=self._environment,
            software=self._software
        )

    def cmd_rm(self,files):
        '''

        :param files:
        :return:
        '''
        return r'''
{environment} 'rm {files}'
        '''.format(
            files=' '.join(files),
            environment=self._environment
        )

    def cmd_fastq_qc(self, qc_config, project, passwd, receivers, sample_id, fastp_json, html, fq1, fq2):
        '''

        :param qc_config:
        :param project:
        :param passwd:
        :param receivers:
        :param sample_id:
        :param fastp_json:
        :param html:
        :param fq1:
        :param fq2:
        :return:
        '''
        if receivers in ['', None]:
            receivers = MAIL_RECEIVERS_DEFAULT
        if fq1 in ['', None]:
            check_fq = ''
        else:
            check_fq = '--fq1 ' + fq1

        if fq2 in ['', None]:
            check_fq = check_fq + ' '
        else:
            check_fq = check_fq + ' --fq2 ' + fq2

        return r'''
{environment} '{aegicare_qc} --config {qc_config} \
            --project {project} \
            --passwd {passwd} \
            --receivers {receivers} \
            --sample-id {sample_id} \
            fastq \
            --fastp-json {fastp_json} \
            --html {html} {check_fq}'        
        '''.format(
            environment=self._environment,
            aegicare_qc=self._aegicare_qc,
            **locals()
        )

    def cmd_bam_qc(self, qc_config, project, passwd, receivers, sample_id, alignment_summary, dup, capture):
        '''

        :param qc_config:
        :param project:
        :param passwd:
        :param receivers:
        :param sample_id:
        :param alignment_summary:
        :param dup:
        :param capture:
        :return:
        '''
        if receivers in ['', None]:
            receivers = MAIL_RECEIVERS_DEFAULT
        if alignment_summary in ['', None]:
            check_paras = ''
        else:
            check_paras = '--alignment-summary ' + alignment_summary

        if dup in ['', None]:
            check_paras = check_paras + ' '
        else:
            check_paras = check_paras + ' --dup ' + dup

        if capture in ['',None]:
            check_paras = check_paras + ' '
        else:
            check_paras = check_paras + ' --capture ' + capture
        return r'''
{environment} '{aegicare_qc} --config {qc_config} \
            --project {project} \
            --passwd {passwd} \
            --receivers {receivers} \
            --sample-id {sample_id} \
            bam {check_paras}' 
        '''.format(
            environment=self._environment,
            aegicare_qc=self._aegicare_qc,
            **locals()
        )

    @utils.special_tmp
    def cmd_segmentation(self, cnr, sv_vcf, output):
        '''

        :param cnr:
        :param sv_vcf:
        :param output:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_file(output))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} \
        --cnr {cnr} --output {output} --sv-vcf {sv_vcf}'       
            '''.format(
            environment=self._environment,
            software=self._software,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    def cmd_merge_segments(self,output,segments):
        '''

        :param output:
        :param segments:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_file(output))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{merge_segments} --output {output} --segments {segment_files}'       
        '''.format(
            environment=self._environment,
            mkdir_paras=MKDIR_DEFAULT,
            segment_files=' '.join(segments),
            **locals()
        )

    def __repr__(self):
        return 'Aegicare Utils:' + self._environment

    def __str__(self):
        return 'Aegicare Utils'


def main():
    pass


if __name__ == '__main__':
    main()
