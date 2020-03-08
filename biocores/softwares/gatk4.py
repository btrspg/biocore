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
    def cmd_select_vcf(self, raw_vcf, snp_vcf, indel_vcf, reference, tmp):
        return r'''
{software} SelectVariants --tmp-dir {tmp} --java-options {java_options} \
    --disable_auto_index_creation_and_locking_when_reading_rods \
    -R {reference} \
    --variant {raw_vcf} \
    -o {snp_vcf} \
    -selectType SNP -selectType MNP
{software} SelectVariants --tmp-dir {tmp} --java-options {java_options} \
    --disable_auto_index_creation_and_locking_when_reading_rods \
    -R {reference} \
    --variant {raw_vcf} \
    -o {indel_vcf} \
    -selectType INDEL
        '''.format(
            software=self._software,
            tmp=tmp,
            reference=reference,
            raw_vcf=raw_vcf,
            snp_vcf=snp_vcf,
            indel_vcf=indel_vcf,
            java_options=self._default.java_options
        )

    @utils.special_tmp
    @utils.modify_cmd
    def cmd_base_recalibrator(self, bam_file, out_bam, reference, known_sites, qc_prefix, tmp='/tmp'):
        '''

        :param bam:
        :param out_bam:
        :param reference:
        :param known_sites:
        :param qc_prefix:
        :param tmp:
        :return:
        '''
        if isinstance(known_sites, str):
            ks = ' --known-sites ' + known_sites
        elif isinstance(known_sites, list):
            ks = ' '.join(['--known-sites {}'.format(i) for i in known_sites])
        else:
            raise TypeError('known-sites should be specific')
        return r'''
{software} BaseRecalibrator --tmp-dir {tmp} --java-options {java_options} \
   -I {bam_file} \
   -R {reference} \
   {ks} \
   -O {qc_prefix}.recal_data.table   
{software} ApplyBQSR --tmp-dir {tmp} --java-options {java_options} \
   -R {reference} \
   -I {bam_file} \
   --bqsr-recal-file {qc_prefix}.recal_data.table  \
   -O {out_bam}     
        '''.format(
            software=self._software,
            tmp=tmp,
            java_options=self._default.java_options,
            reference=reference,
            ks=ks,
            qc_prefix=qc_prefix,
            bam_file=bam_file,
            out_bam=out_bam
        )

    @utils.special_tmp
    @utils.modify_cmd
    def cmd_call_germline_mutation(self, bam_file, reference, target_interval, raw_vcf, tmp='/tmp'):
        '''

        :param bam_file:
        :param reference:
        :param target_interval:
        :param raw_vcf:
        :param tmp:
        :return:
        '''
        return r'''
{software} HaplotypeCaller --tmp-dir {tmp} --java-options {java_options} \
    -R {reference} \
    -I {bam_file} \
    -L {target_interval} \
    -O {raw_vcf} \
    -ERC GVCF -stand-call-conf 10      
        '''.format(
            software=self._software,
            reference=reference,
            tmp=tmp,
            target_interval=target_interval,
            raw_vcf=raw_vcf,
            bam_file=bam_file,
            java_options=self._default.java_options

        )

    @utils.special_tmp
    @utils.modify_cmd
    def cmd_genotype_vcf(self, in_vcf, reference, out_vcf, tmp):
        '''

        :param in_vcf:
        :param reference:
        :param out_vcf:
        :param tmp:
        :return:
        '''
        return r'''
{software} GenotypeGVCFs --tmp-dir {tmp} --java-options {java_options}  \
    -R {reference} \
    -V {in_vcf} \
    -O {out_vcf}     
        '''.format(
            software=self._software,
            tmp=tmp,
            java_options=self._default.java_options,
            in_vcf=in_vcf,
            out_vcf=out_vcf,
            reference=reference
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
    {ponfile} {gr} \
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
        return 'gatk:' + self._software

    def __str__(self):
        return 'Genome Analysis Toolkit'
