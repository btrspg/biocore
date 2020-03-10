#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2020/3/10 10:36 AM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : cnvkit
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores import utils
from biocores.bases.tasks import Task
from biocores.softwares.default import *


class Cnvkit(Task):
    def __init__(self, software, fd):
        super(Cnvkit, self).__init__(software)
        self._default = fd

    def cmd_version(self):
        return 'echo {repr};echo $({software} version)'.format(
            repr=self.__repr__(),
            software=self._software
        )
    @utils.modify_cmd
    def cmd_infer_gender(self, cnr, gender_out):
        '''
        :param cnr:
        :param gender_out:
        :return:
        '''
        return '''
{software} sex -o {gender_out} {cnr}'
        '''.format(
            software=self._software,
            gender_out=gender_out,
            cnr=cnr
        )

    @utils.modify_cmd
    def cmd_batch_cnv_call(self, t_bam, n_bam, ref_cnn, target_bed, ref_flat, reference, access_bed, outdir):
        '''

        :param t_bam:
        :param n_bam:
        :param ref_cnn:
        :param target_bed:
        :param ref_flat:
        :param reference:
        :param access_bed:
        :param outdir:
        :return:
        '''
        option = ''
        if None is not n_bam:
            option += ' --normal ' + n_bam + ' --output-reference ' + outdir + '/reference.cnn'
        elif None is not ref_cnn:
            option += ' -r ' + ref_cnn
        if None not in [target_bed, reference, ref_flat, access_bed]:
            option += ' --targets {target_bed} --annotate {ref_flat} --fasta {reference} --access {access_bed} '.format(
                target_bed=target_bed,
                ref_flat=ref_flat,
                reference=reference,
                access_bed=access_bed
            )
        return r'''
{software} {batch_paras} {t_bam} {option} \
    --output-dir {outdir}      
        '''.format(
            software=self._software,
            batch_paras=self._default.batch,
            t_bam=t_bam,
            option=option,
            outdir=outdir
        )

    @utils.modify_cmd
    def cmd_segment(self, cnr, output, method):
        '''

        :param cnr:
        :param output:
        :param method:
        :return:
        '''

        return r'''
{software} segment -m {method} -o {output} {cnr}       
        '''.format(
            software=self._software,
            method=method,
            output=output,
            cnr=cnr
        )

    @utils.modify_cmd
    def cmd_call_somatic_copy_number(self, cns, vcf, output, ctype='somatic'):
        '''

        :param cns:
        :param vcf:
        :param output:
        :param ctype:
        :return:
        '''

        return r'''
{software} {call_paras} \
            -o {output} \
            -v {vcf} \
            {cns}'     
            '''.format(
            software=self._software,
            call_paras=self._default.somatic_call if ctype == 'somatic' else self._default.germline_call,
            output=output,
            vcf=vcf,
            cns=cns
        )

    def __repr__(self):
        return 'cnvkit:' + self._software

    def __str__(self):
        return 'Genome-wide copy number from high-throughput sequencing'
