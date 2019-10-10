#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019-05-10 10:50
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : cnvkit.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores import utils
from biocores.bases.tasks import Task
from biocores.softwares.default import *


class Cnvkit(Task):
    def __init__(self, container):
        super(Cnvkit, self).__init__(container, 'cnvkit.py')

    def cmd_version(self):
        return 'echo {repr};{environment} {software} version'.format(
            repr=self.__repr__(),
            environment=self._environment,
            software=self._software
        )

    # TODO: 加入性别判断
    def cmd_infer_gender(self,cnr,gender_out):
        '''

        :param cnr:
        :param gender_out:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_file(gender_out))
        return '''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} sex -o {gender_out} {cnr}'
        '''.format(
            environment=self._environment,
            software=self._software,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    # TODO: 这一版CNV极其简略，需要进行丰富，目前只做到可以使用而已。
    def cmd_cnv_call(self, bam, outdir, method, cnn, sampleid, vcf,
                     segment_method='cbs'):
        '''

        :param bam:
        :param outdir:
        :param method:
        :param cnn:
        :param sampleid:
        :param vcf:
        :param segment_method:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_dirs(outdir))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {batch_paras} \
            -m {method} \
            -d {outdir} \
            --reference {cnn} \
            {bam}'  
{environment} '{software} {segment_paras} \
            -o {outdir}/{sampleid}.{segment_method}.cns \
            -v {vcf} \
            {outdir}/{sampleid}.cnr'
{environment} '{software} {call_paras} \
            -o {outdir}/{sampleid}.{segment_method}.call.cns \
            -v {vcf} \
            {outdir}/{sampleid}.{segment_method}.cns'     
            '''.format(
            environment=self._environment,
            software=self._software,
            batch_paras=CNVKIT_BATCH_DEFAULT,
            segment_paras=CNVKIT_SEGMENT_DEFAULT,
            call_paras=CNVKIT_CALL_DEFAULT,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    def cmd_batch_cnv_call(self,bam,ref_cnn,outdir):
        '''

        :param bam:
        :param ref_cnn:
        :param outdir:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',*utils.dirs_for_dirs(outdir))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} batch {bam} -r {ref_cnn} -d {outdir}'       
        '''.format(
            environment=self._environment,
            software=self._software,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    def cmd_segment(self,cnr,prefix,method):
        '''

        :param cnr:
        :param prefix:
        :param method:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',*utils.dirs_for_file(prefix))
        methods = ['cbs','hmm','haar']
        if method not in methods:
            raise TypeError('{method} is not in {methods}'.format(method=method,methods=str(methods)))

        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} segment -m {method} -o {prefix}.{method}.cns {cnr}'        
        '''.format(
            environment=self._environment,
            mkdir_paras=MKDIR_DEFAULT,
            software=self._software,
            **locals()
        )



    def cmd_copy_number_call(self, cns, vcf, output):
        '''

        :param cns:
        :param vcf:
        :param output:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_file(output))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {call_paras} \
            -o {output} \
            -v {vcf} \
            {cns}'     
            '''.format(
            environment=self._environment,
            software=self._software,
            call_paras=CNVKIT_CALL_DEFAULT,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
)

    def __repr__(self):
        return 'cnvkit:' + self._environment

    def __str__(self):
        return 'Genome-wide copy number from high-throughput sequencing'


def main():
    cnvkit = Cnvkit('wgs')
    print(cnvkit.cmd_cnv_call('bam', 'reference', 'outdir', 'wgs', 'reference.cnn', 'target.bed'))


if __name__ == '__main__':
    main()
