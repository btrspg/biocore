#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019-05-22 16:30
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : sentieon.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores import utils
from biocores.bases.tasks import Task
from biocores.softwares.default import *


class Sentieon(Task):
    def __init__(self, container):
        super(Sentieon, self).__init__(container, 'sentieon')

    def cmd_version(self):
        return 'echo {repr};{environment} {software} '.format(
            repr=self.__repr__(),
            environment=self._environment,
            software=self._software
        )

    @utils.special_tmp
    def cmd_align(self, reference, fq1, fq2, bam_file, sampleid='', tmp='/tmp/bwa',
                  lane='L1', platform='Illumina'):
        '''

        :param reference:
        :param fq1:
        :param fq2:
        :param bam_file:
        :param sampleid:
        :param tmp:
        :param lane:
        :param platform:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(bam_file))

        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {bwa_mem_paras} {nt_paras}  \
        -R "@RG\tID:{sampleid}\tPL:{platform}\tPU:{lane}\tLB:{sampleid}\tSM:{sampleid}" \
        {reference} \
        {fq1} {fq2} | \
        {software} {sort_paras} {nt_paras} -r {reference} \
        -o {bam_file} \
        -i - '      
        '''.format(
            environment=self._environment,
            software=self._software,
            bwa_mem_paras=SENTIEON_BWA_MEM_DEFAULT,
            sort_paras=SENTIEON_SORT_DEFAULT,
            nt_paras=SENTIEON_NT_DEFAULT,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_deduplication(self, bam, qc_prefix, dedup_bam, tmp='/tmp/sentieon'):
        '''

        :param bam:
        :param qc_prefix:
        :param dedup_bam:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(qc_prefix, dedup_bam))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} driver {nt_paras} --temp_dir {tmp} \
            -i {bam} \
            --algo LocusCollector --fun score_info \
            {qc_prefix}.score.txt'
{environment} '{software} driver {nt_paras} --temp_dir {tmp} \
            -i {bam} \
            --algo Dedup --rmdup --score_info {qc_prefix}.score.txt \
            --metrics {qc_prefix}.dedup_metrics.txt {dedup_bam} '       
        '''.format(
            environment=self._environment,
            software=self._software,
            nt_paras=SENTIEON_NT_DEFAULT,
            tmp=tmp,
            bam=bam,
            qc_prefix=qc_prefix,
            dedup_bam=dedup_bam,
            output_dirs=output_dirs,
            mkdir_paras=MKDIR_DEFAULT,
        )

    @utils.special_tmp
    def cmd_hc_call(self, reference, bam, raw_vcf, intervals, tmp='/tmp/sentieon'):
        '''

        :param reference:
        :param bam:
        :param raw_vcf:
        :param intervals:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_file(raw_vcf),
                                        *utils.dirs_for_dirs(tmp))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} driver -r {reference} {nt_paras} \
        --temp_dir {tmp} \
        --interval {intervals} \
        -i {bam} \
        --algo Haplotyper  \
        --emit_mode gvcf \
        --min_base_qual 10 \
        {raw_vcf} '       
        '''.format(
            environment=self._environment,
            software=self._software,
            nt_paras=SENTIEON_NT_DEFAULT,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_indel_realign(self, bam, reference, known_mills_indels, realigned_bam, tmp='/tmp/sentieon'):
        '''

        :param bam:
        :param reference:
        :param known_Mills_indels:
        :param realigned_bam:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(realigned_bam))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} driver -r {reference} {nt_paras} -i {bam} --temp_dir {tmp} \
       --algo Realigner -k {known_mills_indels} \
       {realigned_bam}'        
        '''.format(
            environment=self._environment,
            software=self._software,
            reference=reference,
            tmp=tmp,
            output_dirs=output_dirs,
            known_mills_indels=known_mills_indels,
            realigned_bam=realigned_bam,
            bam=bam,
            nt_paras=SENTIEON_NT_DEFAULT,
            mkdir_paras=MKDIR_DEFAULT,
        )

    @utils.special_tmp
    def cmd_somatic_TNhaplotyper_call(self, pair_bam, tumor_name, normal_name, out_vcf, tmp='/tmp/sentieon'):
        '''

        :param pair_bam:
        :param tumor_name:
        :param normal_name:
        :param out_vcf:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(out_vcf))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} driver -r {reference} {nt_paras} -i {pair_bam} --temp_dir {tmp} \
        --algo TNhaplotyper --tumor_sample {tumor_name} \
        --normal_sample {normal_name} {out_vcf}
        '''.format(
            environment=self._environment,
            mkdir_paras=MKDIR_DEFAULT,
            software=self._software,
            nt_paras=SENTIEON_NT_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_somatic_TNhaplotyper2_call(self, pair_bam, tumor_name, normal_name, reference, out_vcf,
                                       tmp='/tmp/sentieon'):
        '''

        :param pair_bam:
        :param tumor_name:
        :param normal_name:
        :param reference:
        :param out_vcf:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(out_vcf))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} driver -r {reference} {nt_paras} -i {pair_bam} --temp_dir {tmp} \
        --algo TNhaplotyper2 --tumor_sample {tumor_name} \
        --normal_sample {normal_name} {tmp}/tnhaplotyper2.vcf'
{environment} '{software} tnhapfilter --tumor_sample {tumor_name} \
   --normal_sample {normal_name} -v {tmp}/tnhaplotyper2.vcf {out_vcf}'        
        '''.format(
            environment=self._environment,
            software=self._software,
            nt_paras=SENTIEON_NT_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_gvcf_typer(self, raw_vcf, genotyper_vcf, reference, tmp='/tmp/sentieon'):
        '''

        :param raw_vcf:
        :param genotyper_vcf:
        :param reference:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(genotyper_vcf))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} driver -r {reference} {nt_paras} \
            --temp_dir {tmp} \
            --algo GVCFtyper \
            -v {raw_vcf} \
            {genotyper_vcf}'
        '''.format(
            environment=self._environment,
            software=self._software,
            nt_paras=SENTIEON_NT_DEFAULT,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_bqsr(self, reference, bam, recal_bam, qc_prefix, *knownsites, tmp='/tmp/sentieon'):
        '''

        :param reference:
        :param bam:
        :param recal_bam:
        :param qc_prefix:
        :param knownsites:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_file(recal_bam, qc_prefix),
                                        *utils.dirs_for_dirs(tmp))
        ks = ' '.join(map(lambda x: '-k {} '.format(x), knownsites))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} driver -r {reference} \
        {nt_paras} --temp_dir {tmp} \
        -i {bam} \
        --algo QualCal \
        {ks} \
        {qc_prefix}.recal_data.table'
{environment} '{software} driver -r {reference} \
        {nt_paras} --temp_dir {tmp} \
        -i {bam} \
        -q {qc_prefix}.recal_data.table \
        --algo QualCal \
        {ks} \
        {qc_prefix}.recal_data.table.post '
{environment} '{software} driver \
        {nt_paras} --temp_dir {tmp} \
        --algo QualCal --plot \
        --before {qc_prefix}.recal_data.table \
        --after {qc_prefix}.recal_data.table.post \
        {qc_prefix}.recal.csv'
{environment} '{software} plot QualCal -o {qc_prefix}.recal_plots.pdf \
       {qc_prefix}.recal.csv'
{environment} '{software} driver -r {reference} \
        {nt_paras} --temp_dir {tmp} \
        -i {bam} \
        -q {qc_prefix}.recal_data.table \
        --algo ReadWriter \
        {recal_bam}'
        '''.format(
            environment=self._environment,
            software=self._software,
            qc_prefix=qc_prefix,
            reference=reference,
            nt_paras=SENTIEON_NT_DEFAULT,
            bam=bam,
            recal_bam=recal_bam,
            ks=ks,
            tmp=tmp,
            output_dirs=output_dirs,
            mkdir_paras=MKDIR_DEFAULT,
        )

    @utils.special_tmp
    def cmd_vqsr_pre(self, reference, vcf, var_type,
                     qc_dir, *resources, tmp='/tmp/sentieon'):
        '''

        :param reference:
        :param vcf:
        :param var_type:
        :param qc_dir:
        :param resources:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_dirs(tmp, qc_dir))
        rs = ' '.join(map(lambda x: ' --resource {} --resource_param {} '.format(*x.split(':')), resources))

        if var_type == 'SNP':
            annotation = '--annotation QD --annotation MQ --annotation MQRankSum ' \
                         '--annotation ReadPosRankSum --annotation FS --annotation SOR --annotation DP'
        elif var_type == 'INDEL':
            annotation = '--annotation QD --annotation DP --annotation FS --annotation SOR ' \
                         '--annotation ReadPosRankSum --annotation MQRankSum'
        else:
            raise TypeError('var_type can only in [SNP,INDEL]')

        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} driver -r {reference} {nt_paras} \
            --temp_dir {tmp} \
            --algo VarCal \
            -v {vcf} \
            --tranches_file {qc_dir}/{var_type}.tranches.txt \
            --var_type {var_type}  \
            --plot_file {qc_dir}/{var_type}.txt \
            {rs} \
            {annotation} \
            {qc_dir}/{var_type}.vcf_recal_data.txt'
        '''.format(
            environment=self._environment,
            software=self._software,
            nt_paras=SENTIEON_NT_DEFAULT,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_vqsr(self, reference, vcf, qc_dir, var_type, snp_indel_prefix, tmp='/tmp/sentieon'):
        '''

        :param reference:
        :param vcf:
        :param qc_dir:
        :param var_type:
        :param snp_indel_prefix:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_dirs(tmp, qc_dir),
                                        *utils.dirs_for_file(snp_indel_prefix))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} driver -r {reference} {nt_paras} \
            --temp_dir {tmp} \
            --algo ApplyVarCal \
            -v {vcf} \
            --tranches_file {qc_dir}/{var_type}.tranches.txt \
            --var_type {var_type}  \
            --recal {qc_dir}/{var_type}.vcf_recal_data.txt \
            --sensitivity 99.9 \
            {snp_indel_prefix}.{var_type}.vcf.gz  '
        '''.format(
            environment=self._environment,
            software=self._software,
            nt_paras=SENTIEON_NT_DEFAULT,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_bam_qc(self, reference, bam, algo, qc_dir, tmp='/tmp/sentieon'):
        '''

        :param reference:
        :param bam:
        :param algo:
        :param qc_dir:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_dirs(tmp, qc_dir))
        common_cmd = r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} driver -r {reference} {nt_paras} \
            -i {bam} --temp_dir {tmp} \
            {special_command}
        '''
        plot_cmd = r'''
{environment} '{software} plot {algo} -o {qc}/{algo}.pdf {qc}/{algo}_metrics.txt'        
        '''
        if algo in ['MeanQualityByCycle', 'QualDistribution', 'InsertSizeMetricAlgo', 'WgsMetricsAlgo']:
            cmd = common_cmd.format(
                environment=self._environment,
                software=self._software,
                reference=reference,
                nt_paras=SENTIEON_NT_DEFAULT,
                bam=bam,
                tmp=tmp,
                mkdir_paras=MKDIR_DEFAULT,
                output_dirs=output_dirs,
                special_command='--algo {algo} {qc}/{algo}_metrics.txt'.format(
                    algo=algo,
                    qc=qc_dir
                ) + "'"
            )
            if algo != 'WgsMetricsAlgo':
                cmd = cmd + '\n' + plot_cmd.format(
                    environment=self._environment,
                    software=self._software,
                    qc=qc_dir,
                    algo=algo
                )
        elif algo in ['GCBias']:
            cmd = common_cmd.format(
                environment=self._environment,
                software=self._software,
                reference=reference,
                nt_paras=SENTIEON_NT_DEFAULT,
                bam=bam,
                tmp=tmp,
                output_dirs=output_dirs,
                special_command='--algo {algo} --summary {qc}/{algo}_summary.txt {qc}/{algo}_metrics.txt'.format(
                    algo=algo,
                    qc=qc_dir
                ) + "'"
            )
            cmd = cmd + '\n' + plot_cmd.format(
                environment=self._environment,
                software=self._software,
                qc=qc_dir,
                algo=algo
            )
        else:
            cmd = 'echo test'
        return cmd

    def __repr__(self):
        return 'sentieon:' + self._environment

    def __str__(self):
        return 'Sentieon provides complete solutions for secondary DNA analysis. ' \
               'Our software improves upon BWA, GATK, HaplotypeCaller, Mutect, ' \
               'and Mutect2 based pipelines and is deployable on any generic-CPU-based' \
               ' computing system.'


def main():
    container = 'sentieon-test'
    sentieon = Sentieon(container)
    fq1 = '/aegicare/analysis_result/MEDICAL/COMMERCIAL/GENETIC/WGS/results/AS4036/cleanData/AS4036.clean.1.fq.gz'
    fq2 = '/aegicare/analysis_result/MEDICAL/COMMERCIAL/GENETIC/WGS/results/AS4036/cleanData/AS4036.clean.2.fq.gz'
    bam = '/aegicare/analysis_result/TMP/sentieon-test/raw.bam'
    dedup_bam = '/aegicare/analysis_result/TMP/sentieon-test/dedup.bam'
    realigned_bam = '/aegicare/analysis_result/TMP/sentieon-test/realigned.bam'
    recal_bam = '/aegicare/analysis_result/TMP/sentieon-test/recal.bam'
    vcf = '/aegicare/analysis_result/TMP/sentieon-test/hc.vcf.gz'
    snp = '/aegicare/analysis_result/TMP/sentieon-test/snp.vcf.gz'
    indel = '/aegicare/analysis_result/TMP/sentieon-test/indel.vcf.gz'
    reference = '/aegicare/database/human/hg19/genome/v0/human_g1k_v37.fasta'
    intervals = '/aegicare/database//human/hg19/enrichments/wgs/list.interval_list'
    tmp = '/aegicare/analysis_result/TMP/sentieon-test/tmp'
    genotyper_vcf = '/aegicare/analysis_result/TMP/sentieon-test/genotyper.vcf.gz'
    qc_dir = '/aegicare/analysis_result/TMP/sentieon-test/qc'
    qc_prefix = '/aegicare/analysis_result/TMP/sentieon-test/qc/test'
    snp_indel_prefix = '/aegicare/analysis_result/TMP/sentieon-test/snp_indel'
    snp_resources = ['/aegicare/database/human/hg19/annotations/hapmap_3.3.b37.vcf'
                     ':hapmap,known=false,training=true,truth=true,prior=15.0',
                     '/aegicare/database/human/hg19/annotations/1000G_omni2.5.b37.vcf'
                     ':omni,known=false,training=true,truth=true,prior=12.0',
                     '/aegicare/database/human/hg19/annotations/1000G_phase1.snps.high_confidence.b37.vcf'
                     ':1000G,known=false,training=true,truth=false,prior=10.0',
                     '/aegicare/database/human/hg19/annotations/dbsnp_138.b37.vcf'
                     ':dbsnp,known=true,training=false,truth=false,prior=2.0']
    indel_resources = ['/aegicare/database/human/hg19/annotations/Mills_and_1000G_gold_standard.indels.b37.vcf'
                       ':mills,known=false,training=true,truth=true,prior=12.0',
                       '/aegicare/database/human/hg19/annotations/dbsnp_138.b37.vcf'
                       ':dbsnp,known=true,training=false,truth=false,prior=2.0']
    knownsites = ['/aegicare/database/human/hg19/annotations/hapmap_3.3.b37.vcf',
                  '/aegicare/database/human/hg19/annotations/1000G_omni2.5.b37.vcf',
                  '/aegicare/database/human/hg19/annotations/1000G_phase1.snps.high_confidence.b37.vcf',
                  '/aegicare/database/human/hg19/annotations/dbsnp_138.b37.vcf',
                  '/aegicare/database/human/hg19/annotations/Mills_and_1000G_gold_standard.indels.b37.vcf']
    known_mills_indels = '/aegicare/database/human/hg19/annotations/Mills_and_1000G_gold_standard.indels.b37.vcf'

    # print(sentieon.cmd_vqsr_pre(reference, snp, 'SNP', qc_dir, *snp_resources, tmp=tmp))
    # print(sentieon.cmd_vqsr_pre(reference, indel, 'INDEL', qc_dir, *indel_resources, tmp=tmp))
    # print(sentieon.cmd_vqsr(reference, snp, qc_dir, 'SNP', snp_indel_prefix, tmp=tmp))
    # print(sentieon.cmd_vqsr(reference, indel, qc_dir, 'INDEL', snp_indel_prefix, tmp=tmp))
    # print(sentieon.cmd_align(reference, fq1, fq2, bam, 'test', tmp=tmp))
    # print(sentieon.cmd_deduplication(bam, qc_prefix, dedup_bam, tmp=tmp))
    # print(sentieon.cmd_indel_realign(dedup_bam, reference, known_mills_indels, realigned_bam, tmp=tmp))
    # print(sentieon.cmd_bqsr(reference, realigned_bam, recal_bam, qc_prefix, *knownsites, tmp=tmp))
    # print(sentieon.cmd_hc_call(reference, recal_bam, vcf, intervals, tmp=tmp))
    # print(sentieon.cmd_gvcf_typer(vcf, genotyper_vcf, reference, tmp=tmp))
    # print(sentieon.cmd_vqsr_pre(reference, snp, 'SNP',qc_dir, *snp_resources, tmp=tmp))
    # print(sentieon.cmd_vqsr_pre(reference, indel, 'INDEL', qc_dir, *indel_resources, tmp=tmp))
    # print(sentieon.cmd_vqsr(reference, snp, qc_dir, 'SNP', snp_indel_prefix, tmp=tmp))
    # print(sentieon.cmd_vqsr(reference, indel, qc_dir, 'INDEL', snp_indel_prefix, tmp=tmp))
    # print(sentieon.cmd_version())
    algo = ['MeanQualityByCycle', 'QualDistribution', 'InsertSizeMetricAlgo', 'GCBias', 'WgsMetricsAlgo']
    for i in algo:
        print(sentieon.cmd_bam_qc(reference, bam, i, qc_dir, tmp=tmp))


if __name__ == '__main__':
    main()
