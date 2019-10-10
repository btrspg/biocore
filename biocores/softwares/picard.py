#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019-05-05 09:47
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : picard.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores import utils
from biocores.bases.tasks import Task
from biocores.softwares.default import *


class Picard(Task):
    def __init__(self, container):
        super(Picard, self).__init__(container,'picard')
        self._common_paras = JAVA_OPTIONS

    def cmd_version(self):
        return 'echo {repr};{environment} {software} '.format(
            repr=self.__repr__(),
            environment=self._environment,
            software=self._software
        )
    @utils.special_tmp
    def cmd_quality_score_distribution(self, bam_file, qc_prefix, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(qc_prefix))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} {qualityscoredistribution_command} \
            INPUT={bam_file} \
            O={qc_prefix}.qual_score_dist.txt \
            CHART={qc_prefix}.qual_score_dist.pdf ' 
        '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            qualityscoredistribution_command=PICARD_QUALITY_SCORE_DISTRIBUTION_DEFALUT,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_collect_gc_bias_metrics(self, bam_file, qc_prefix, reference, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param reference:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(qc_prefix))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} {collect_gc_bias_command}  \
    I={bam_file} \
    O={qc_prefix}.gc_bias_metrics.txt \
    CHART={qc_prefix}.gc_bias_metrics.pdf \
    S={qc_prefix}.summary_metrics.txt \
    R={reference}    '
        '''.format(
            environment=self._environment,
            software=self._software,
            collect_gc_bias_command=PICARD_COLLECT_GC_BIAS_METRICS_DEFALUT,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals())

    @utils.special_tmp
    def cmd_collect_wgs_metrics(self, bam_file, qc_prefix, reference, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param reference:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(qc_prefix))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} {collect_wgs_metrics_command} \
    I={bam_file} \
    O={qc_prefix}.collect_wgs_metrics.txt \
    R={reference}   '
        '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            collect_wgs_metrics_command=PICARD_COLLECT_WGS_MERTICS,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_markdup(self, rawbam, markdupbam, dupstat, tmp):
        '''

        :param rawbam:
        :param markdupbam:
        :param dupstat:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_file(markdupbam, dupstat),
                                        *utils.dirs_for_dirs(tmp))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} {markdup_command} \
            I={rawbam} O={markdupbam} M={dupstat}'
{environment} 'samtools index {markdupbam}'
        '''.format(
            environment=self._environment,
            software=self._software,
            markdup_command=PICARD_MARKDUP_DEFAULT,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    @utils.special_tmp
    def cmd_estimate_library_complexity(self, bam_file, qc_prefix, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(qc_prefix))
        cmd = '''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} EstimateLibraryComplexity \
    INPUT={bam_file} \
    O={qc_prefix}.est_lib_complex_metrics.txt  '  
        '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals())
        return cmd

    @utils.special_tmp
    def cmd_collect_oxo_g_metrics(self, bam_file, qc_prefix, reference, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param reference:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(qc_prefix))
        cmd = '''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} CollectOxoGMetrics \
    I={bam_file} \
    O={qc_prefix}.oxoG_metrics.txt \
    R={reference}'
        '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals())
        return cmd

    @utils.special_tmp
    def cmd_collect_wgs_metrics_with_non_zero_coverage(self, bam_file, qc_prefix, reference, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param reference:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(qc_prefix))
        cmd = '''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} CollectWgsMetricsWithNonZeroCoverage \
    I={bam_file} \
    O={qc_prefix}.collect_wgs_metrics_with_non_zero_coverage.txt \
    CHART={qc_prefix}.collect_wgs_metrics_with_non_zero_coverage.pdf  \
    R={reference}   '
        '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals())
        return cmd

    @utils.special_tmp
    def cmd_collect_hs_metrics(self, bam_file, qc_prefix, reference, bait_interval_list, target_interval_list, tmp):
        '''

        :param picard:
        :param bam_file:
        :param qc_prefix:
        :param reference:
        :param bait_interval_list:
        :param target_interval_list:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(qc_prefix))
        cmd = '''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} CollectHsMetrics \
    I={bam_file} \
    O={qc_prefix}_hs_metrics.txt \
    R={reference} \
    BAIT_INTERVALS={bait_interval_list} \
    TARGET_INTERVALS={target_interval_list}    '
        '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals())
        return cmd

    @utils.special_tmp
    def cmd_collect_insert_size_metrics(self, bam_file, qc_prefix, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(qc_prefix))
        cmd = '''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} CollectInsertSizeMetrics \
    I={bam_file} \
    O={qc_prefix}.insert_size_metrics.txt \
    H={qc_prefix}.insert_size_histogram.pdf \
    M=0.5    '
        '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals())
        return cmd

    @utils.special_tmp
    def cmd_collect_targeted_pcr_metrics(self, bam_file, qc_prefix, reference, amplicon_interval_list,
                                         targets_interval_list, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param reference:
        :param amplicon_interval_list:
        :param targets_interval_list:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(qc_prefix))
        cmd = '''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} CollectTargetedPcrMetrics \
    I={bam_file} \
    O={qc_prefix}.output_pcr_metrics.txt \
    R={reference} \
    AMPLICON_INTERVALS={amplicon_interval_list} \
    TARGET_INTERVALS={targets_interval_list}'
        '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals())
        return cmd

    @utils.special_tmp
    def cmd_collect_raw_wgs_metrics(self, bam_file, qc_prefix, reference, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param reference:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(qc_prefix))
        cmd = '''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} CollectRawWgsMetrics \
    I={bam_file} \
    O={qc_prefix}.output_raw_wgs_metrics.txt \
    R={reference} \
    INCLUDE_BQ_HISTOGRAM=true    '
        '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals())
        return cmd

    @utils.special_tmp
    def cmd_collect_quality_yield_metrics(self, bam_file, qc_prefix, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(qc_prefix))
        cmd = '''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} CollectQualityYieldMetrics \
    I={bam_file} \
    O={qc_prefix}.quality_yield_metrics.txt'    
        '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals())
        return cmd

    @utils.special_tmp
    def cmd_collect_sequencing_artifact_metrics(self, bam_file, qc_prefix, reference, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param reference:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(qc_prefix))
        cmd = '''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} CollectSequencingArtifactMetrics \
     I={bam_file} \
     O={qc_prefix}.artifact_metrics.txt \
     R={reference}    '
        '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals())
        return cmd

    @utils.special_tmp
    def cmd_mean_quality_by_cycle(self, bam_file, qc_prefix, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(qc_prefix))
        cmd = '''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} MeanQualityByCycle \
    INPUT={bam_file} \
    O={qc_prefix}.mean_qual_by_cycle.txt \
    CHART={qc_prefix}.mean_qual_by_cycle.pdf'
        '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals())
        return cmd

    @utils.special_tmp
    def cmd_collect_base_distribution_by_cycle(self, bam_file, qc_prefix, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(qc_prefix))
        cmd = '''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} CollectBaseDistributionByCycle \
    CHART={qc_prefix}.collect_base_dist_by_cycle.pdf \
    I={bam_file} \
    O={qc_prefix}.collect_base_dist_by_cycle.txt'  
        '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals())
        return cmd

    @utils.special_tmp
    def cmd_collect_alignment_summary_metrics(self, bam_file, qc_prefix, reference, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param reference:
        :param tmp:
        :return:
        '''
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_dirs(tmp),
                                        *utils.dirs_for_file(qc_prefix))
        cmd = '''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {common_paras} -Djava.io.tmpdir={tmp} CollectAlignmentSummaryMetrics \
    R={reference} \
    I={bam_file} \
    O={qc_prefix}.alignment_summary_metrics.txt'    
        '''.format(
            environment=self._environment,
            software=self._software,
            common_paras=self._common_paras,
            mkdir_paras=MKDIR_DEFAULT,
            **locals())
        return cmd

    def __repr__(self):
        return 'picard:' + self._environment

    def __str__(self):
        return 'A set of command line tools (in Java) for manipulating high-throughput ' \
               'sequencing (HTS) data and formats such as SAM/BAM/CRAM and VCF'


def test():
    rawbam = '/opt/tmp/test/test.sort.bam'
    markdupbam = '/opt/tmp/test/test.markdup.bam'
    dupstat = '/opt/tmp/test/dupstate'
    tmp = '/opt/tmp/test/tmp'
    picard = Picard('pipeline')
    print(picard.cmd_version())
    print(picard.cmd_markdup(rawbam, markdupbam, dupstat, tmp=tmp))


def main():
    test()


if __name__ == '__main__':
    main()
