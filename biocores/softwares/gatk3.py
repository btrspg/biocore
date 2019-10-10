#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019-05-05 10:28
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : gatk3.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores import utils
from biocores.bases.tasks import Task
from biocores.softwares.default import *


class Gatk3(Task):
    def __init__(self, container):
        super(Gatk3, self).__init__(container, 'gatk3')
        self._common_paras = JAVA_OPTIONS

    def cmd_version(self):
        return 'echo {repr};{environment} {software} '.format(
            repr=self.__repr__(),
            environment=self._environment,
            software=self._software
        )

    @utils.special_tmp
    def cmd_vqsr_pre(self, reference, vcf, var_type,
                     qc_dir, *resources, tmp='/tmp/gatk'):
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

        if var_type == 'SNP':
            annotation = GATK_VQSR_PRE_SNP_AN
        elif var_type == 'INDEL':
            annotation = GATK_VQSR_PRE_INDEL_AN
        else:
            raise TypeError('var_type can only in [SNP,INDEL]')

        rs = ' '.join(map(lambda x: ' -resource:{1} {0} '.format(*x.split(':')), resources))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} {vqsr_pre_paras} \
            -R {reference} \
            -input {vcf} \
            {annotation} \
            -mode {var_type} \
            {rs} \
            -recalFile {qc_dir}/{var_type}.vcf_recal_data.txt \
            -tranchesFile {qc_dir}/{var_type}.tranches.txt \
            -rscriptFile {qc_dir}/{var_type}.txt'
        '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            vqsr_pre_paras=GATK_VQSR_PRE_DEFAULT,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_vqsr(self, reference, vcf, qc_dir, var_type, snp_indel_prefix, tmp='/tmp/gatk3'):
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
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} {vqsr_paras} \
            -R {reference} \
            -input {vcf} \
            -mode {var_type} \
            -recalFile {qc_dir}/{var_type}.vcf_recal_data.txt \
            -tranchesFile {qc_dir}/{var_type}.tranches.txt \
            -o {snp_indel_prefix}.{var_type}.vcf.gz'
            '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            vqsr_paras=GATK_VQSR_DEFAULT,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_indel_realign(self, reference, bam, out_bam, known_indel, intervals, tmp='/tmp/gatk'):
        '''

        :param reference:
        :param bam:
        :param out_bam:
        :param known_indel:
        :param intervals:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_file(out_bam),
                                        *utils.dirs_for_dirs(tmp))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} {indelrealigner_command} \
            -R {reference} \
            -I {bam} \
            -known {known_indel} \
            -targetIntervals {intervals} \
            -o {out_bam}'     
        '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            indelrealigner_command=GATK_INDEL_REALIGN_DEFAULT,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_bqsr(self, markdupbam, recalbam, reference, recal_data_table, gatk_intervals,
                 *knownsites, tmp='/tmp/bqsr'):
        '''

        :param markdupbam:
        :param recalbam:
        :param reference:
        :param recal_data_table:
        :param gatk_intervals:
        :param tmp:
        :param knownsites:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_file(recalbam, recal_data_table),
                                        *utils.dirs_for_dirs(tmp))

        ks = ' '.join(map(lambda x: ' -knownSites {} '.format(x), knownsites))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} {baserecal_command} \
        -R {reference} -I {markdupbam} -o {recal_data_table} \
        {ks} \
        -L {gatk_intervals}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} {applybaserecal_command} \
        -R {reference} -I {markdupbam} -BQSR {recal_data_table}\
        -o {recalbam}'
{environment} 'samtools index {recalbam}'
        '''.format(
            environment=self._environment,
            software=self._software,
            baserecal_command=GATK_BASERECAL_DEFAULT,
            common_paras=self._common_paras,
            applybaserecal_command=GATK_APPLY_BASERECAL_DEFAULT,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_hc_call(self, reference, finalbam, rawvcf, gatk_intervals,
                    bamout='', tmp='/tmp/gatk_hc'):
        '''

        :param reference:
        :param finalbam:
        :param rawvcf:
        :param gatk_intervals:
        :param tmp:
        :param bamout:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_file(rawvcf, bamout),
                                        *utils.dirs_for_dirs(tmp))
        options = '-bamout ' + bamout if bamout != '' else ''
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} {hc_command} \
        -R {reference}  -I {finalbam} \
        -o {rawvcf} -L {gatk_intervals} {options}'
        '''.format(
            environment=self._environment,
            software=self._software,
            hc_command=GATK_HC_DEFAULT,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_genotype_gvcf(self, reference, rawvcf, genotype_vcf, tmp):
        '''

        :param reference:
        :param rawvcf:
        :param tmp:
        :param genotype_vcf:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_file(genotype_vcf),
                                        *utils.dirs_for_dirs(tmp))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} {genotype_gvcf_command} \
        -R {reference}  --variant {rawvcf} \
        -o {genotype_vcf} '
                '''.format(
            environment=self._environment,
            software=self._software,
            genotype_gvcf_command=GATK_GENOTYPE_GVCF_DEFAULT,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_vcf_filter(self, reference, snpvcf, indelvcf,
                       snpfiltervcf, indelfiltervcf, indel_1kg, tmp):
        '''

        :param reference:
        :param snpvcf:
        :param indelvcf:
        :param snpfiltervcf:
        :param indelfiltervcf:
        :param indel_1kg:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_file(snpvcf, indelvcf, snpfiltervcf, indelfiltervcf),
                                        *utils.dirs_for_dirs(tmp))

        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp}  {gatk_indelfilter_command} \
        -R {reference} --mask {indel_1kg} --maskName INDEL_Mills_1KG -o {indelfiltervcf} --variant {indelvcf} '
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp}  {gatk_snpfilter_command} \
        -R {reference} -o {snpfiltervcf} --variant {snpvcf} --mask {indelfiltervcf} --maskName "INDEL" '
        '''.format(
            environment=self._environment,
            software=self._software,
            gatk_indelfilter_command=GATK_INDEL_FILTER_DEFAULT,
            gatk_snpfilter_command=GATK_SNP_FILTER_DEFAULT,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_variant_select(self, reference, rawvcf, snpvcf, indelvcf, tmp):
        '''

        :param reference:
        :param rawvcf:
        :param snpvcf:
        :param indelvcf:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_file(snpvcf, indelvcf),
                                        *utils.dirs_for_dirs(tmp))

        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp}  {gatk_select_command} \
        -R {reference} --variant {rawvcf} -o {snpvcf} -selectType SNP -selectType MNP'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp}  {gatk_select_command} \
        -R {reference} --variant {rawvcf} -o {indelvcf} -selectType INDEL'
            '''.format(
            environment=self._environment,
            software=self._software,
            gatk_select_command=GATK_SELECT_DEFAULT,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_variant_merge(self, reference, snpfiltervcf, indelfiltervcf, finalvcf, tmp):
        '''

        :param reference:
        :param tmp:
        :param rawvcf:
        :param snpvcf:
        :param indelvcf:
        :param snpfiltervcf:
        :param indelfiltervcf:
        :param finalvcf:
        :param indel_1kg:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_file(finalvcf),
                                        *utils.dirs_for_dirs(tmp))

        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp}  {gatk_combinevcf_command} \
        --variant:SNP {snpfiltervcf} \
        --variant:INDEL {indelfiltervcf} \
        -R {reference} -o {finalvcf}'
            '''.format(
            environment=self._environment,
            software=self._software,
            gatk_combinevcf_command=GATK_COMBINEVCF_DEFAULT,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_vcf_split(self, reference, finalvcf, chromosome, splitvcf, tmp):
        '''

        :param reference:
        :param tmp:
        :param finalvcf:
        :param chromosome:
        :param splitvcf:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_file(splitvcf),
                                        *utils.dirs_for_dirs(tmp))

        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp}  {gatk_select_command} \
        -R {reference} --variant {finalvcf} -o {splitvcf} -L {chromosome} '
        '''.format(
            environment=self._environment,
            software=self._software,
            gatk_select_command=GATK_SELECT_DEFAULT,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_contest(self, tumor_bam, normal_bam, reference, pf, gatk_intervals, contest_out,
                    popfile, tmp='/tmp/gatk'):
        '''

        :param tumor_bam:
        :param normal_bam:
        :param reference:
        :param pf:
        :param gatk_intervals:
        :param contest_out:
        :param popfile:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_file(contest_out),
                                        *utils.dirs_for_dirs(tmp))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} {gatk_contest_command} \
        -R {reference} -I:eval {tumor_bam} -I:genotype {normal_bam} \
        -L {gatk_intervals} \
        --popfile {popfile} \ 
        -o {contest_out}'        
        '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            gatk_contest_command=GATK_CONTEST_DEFAULT,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    def cmd_somatic_filter(self):
        pass

    @utils.special_tmp
    def cmd_somatic_variant(self, tumor_bam, normal_bam, reference, rawvcf, gatk_intervals, contamination=0.1,
                            bamout='', tmp='/tmp/gatk_hc'):
        '''

        :param tumor_bam:
        :param normal_bam:
        :param reference:
        :param rawvcf:
        :param gatk_intervals:
        :param contamination:
        :param bamout:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(rawvcf))
        if normal_bam is None:
            control = ''
        else:
            control = '-I:normal {normal_bam}'.format(normal_bam=normal_bam)

        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} {gatk_mutect_command} \
        -R {reference} \
        -I:tumor {tumor_bam} {control} \
        --contamination_fraction_to_filter {contamination} \
        -o {rawvcf}'
        '''.format(
            environment=self._environment,
            software=self._software,
            mkdir_paras=MKDIR_DEFAULT,
            common_paras=self._common_paras,
            gatk_mutect_command=GATK_MUTECT2_DEFAULT,
            **locals()
        )

    def __repr__(self):
        return 'gatk3:' + self._environment

    def __str__(self):
        return 'Genome Analysis Toolkit:' \
               'Variant Discovery in High-Throughput Sequencing Data'


def test():
    markdupbam = '/opt/tmp/test/test.markdup.bam'
    recalbam = '/opt/tmp/test/test.recal.bam'
    reference = '/aegicare/database/human/hg19/genome/v0/human_g1k_v37.fasta'
    recal_data_table = '/opt/tmp/test/test.recal_data_table'
    gatk_intervals = '/opt/tmp/test/test.intervals'
    tmp = '/aegicare/analysis_result/TMP/sentieon-test/tmp'
    rawvcf = '/opt/tmp/test/test.raw.vcf'
    snp = '/opt/tmp/test/test.snp.vcf'
    indel = '/opt/tmp/test/test.indel.vcf'
    snpfilter = '/opt/tmp/test/test.snp.filter.vcf'
    indelfilter = '/opt/tmp/test/test.indel.filter.vcf'
    finalvcf = '/opt/tmp/test/test.final.vcf'
    splitvcf = '/opt/tmp/test/test.final.chromosome1.vcf'
    knowsite = '/opt/tmp/test/Mills_and_1000G_gold_standard.nochr.indels.hg19.sites.vcf'

    gatk3 = Gatk3('wgs-test')
    # print(gatk3.cmd_version())
    # print(gatk3.cmd_bqsr(markdupbam, recalbam, reference,
    #                      recal_data_table, gatk_intervals, knowsite, tmp=tmp))
    # print(gatk3.cmd_hc_call(reference, recalbam, rawvcf, gatk_intervals, tmp=tmp))
    # print(gatk3.cmd_vcf_filter(reference, snp, indel, snpfilter, indelfilter, knowsite, tmp=tmp))
    # print(gatk3.cmd_vcf_split(reference, finalvcf, 1, splitvcf, tmp=tmp))

    vcf = '/aegicare/analysis_result/TMP/sentieon-test/genotyper.vcf.gz'
    snp = '/aegicare/analysis_result/TMP/sentieon-test/snp.vcf.gz'
    indel = '/aegicare/analysis_result/TMP/sentieon-test/indel.vcf.gz'
    # print(gatk3.cmd_variant_select(reference, vcf, snp, indel, tmp=tmp))
    filter_snp = '/aegicare/analysis_result/TMP/sentieon-test/snp_indel.SNP.vcf.gz'
    filter_indel = '/aegicare/analysis_result/TMP/sentieon-test/snp_indel.INDEL.vcf.gz'
    final_vcf = '/aegicare/analysis_result/TMP/sentieon-test/final.vcf'
    # print(gatk3.cmd_variant_merge(reference, filter_snp, filter_indel, final_vcf, tmp=tmp))
    bam = '/aegicare/analysis_result/TMP/sentieon-test/dedup.bam'
    out_bam = '/aegicare/analysis_result/TMP/sentieon-test/gatk.realign.bam'
    known_indel = '/aegicare/database/human/hg19/annotations/Mills_and_1000G_gold_standard.indels.b37.vcf'
    intervals = '/aegicare/database//human/hg19/enrichments/wgs/list.interval_list'
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
    qc_dir = '/aegicare/analysis_result/TMP/sentieon-test/qc'
    snp_indel_prefix = '/aegicare/analysis_result/TMP/sentieon-test/snp_indel-gatk'
    # print(gatk3.cmd_indel_realign(reference, bam, out_bam, known_indel, intervals, tmp=tmp))
    print(gatk3.cmd_vqsr_pre(reference, snp, 'SNP', qc_dir, *snp_resources, tmp=tmp))
    print(gatk3.cmd_vqsr_pre(reference, indel, 'INDEL', qc_dir, *indel_resources, tmp=tmp))
    print(gatk3.cmd_vqsr(reference, snp, qc_dir, 'SNP', snp_indel_prefix, tmp=tmp))
    print(gatk3.cmd_vqsr(reference, indel, qc_dir, 'INDEL', snp_indel_prefix, tmp=tmp))


def main():
    test()


if __name__ == '__main__':
    main()
