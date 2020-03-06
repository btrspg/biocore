#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2020/3/1 10:53 AM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : gatk4
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores import utils
from biocores.bases.tasks import Task



class Gatk4(Task):
    def __init__(self, software, fd):
        super(Gatk4, self).__init__(software)
        self._default = fd

    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ; echo {software}'.format(
            repr=self.__repr__(),
            software=self._software
        )

    @utils.special_tmp
    @utils.modify_cmd
    def cmd_call_somatic_mutation(self, t_id, n_id, t_bam, n_bam, reference, intervals, pon, genomad,
                                  common, outdir, tmp=utils.get_tempfile()):

        control = ''
        gr = ''
        ponfile = ''

        if None is not n_id and None is not n_bam:
            control = ' -I ' + n_bam + ' -normal ' + n_id
        if None is not pon:
            ponfile = ' -pon ' + pon
        if None is not genomad:
            gr = '-germline-resource ' + genomad
        return r'''
{software} Mutect2 --tmp-dir {tmp} --java-options {java_options} \
    -I {t_bam} {control}
    -O {outdir}/{t_id}.unfiltered.vcf \
    -R {reference} \
    -L {intervals} \
    {ponfile} {gr}
    --f1r2-tar-gz {outdir}/{t_id}.f1r2.tar.gz
    
{software} LearnReadOrientationModel --tmp-dir {tmp} --java-options {java_options} \
    -I {outdir}/{t_id}.f1r2.tar.gz \
    -O {outdir}/{t_id}.read-orientation-model.tar.gz

{software} GetPileupSummaries --tmp-dir {tmp} --java-options {java_options} \
    -I {t_bam} \
    -V {common} \
    -L {common} \
    -O {outdir}/{t_id}.getpileupsummaries.table
    
{software} CalculateContamination --tmp-dir {tmp} --java-options {java_options} \
    -I {outdir}/{t_id}.getpileupsummaries.table \
    -tumor-segmentation {outdir}/{t_id}.segments.table \
    -O {outdir}/{t_id}.contamination.table


{software} FilterMutectCalls --tmp-dir {tmp} --java-options {java_options} \
    -V {outdir}/{t_id}.unfiltered.vcf \
    --tumor-segmentation {outdir}/{t_id}.segments.table \
    --contamination-table {outdir}/{t_id}.contamination.table \
    --ob-priors {outdir}/{t_id}.read-orientation-model.tar.gz \
    -O {outdir}/{t_id}.somatic.vcf \
    -R {reference}
        '''.format(
            software=self._software,
            outdir=outdir,
            t_id=t_id,
            reference=reference,
            common=common,
            control=control,
            gr=gr,
            ponfile=ponfile,
            intervals=intervals,
            t_bam=t_bam,
            tmp=tmp,
            java_options=self._default.java_options

        )

    def __repr__(self):
        return 'fastp:' + self._software

    def __str__(self):
        return 'A tool designed to provide fast all-in-one preprocessing for FastQ files. This tool is developed ' \
               'in C++ with multithreading supported to afford high performance.'
