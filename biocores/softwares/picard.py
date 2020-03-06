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
    def __init__(self, software, fd):
        super(Picard, self).__init__(software)
        self._default = fd

    def cmd_version(self):
        return 'echo {repr};echo NOVERSION '.format(
            repr=self.__repr__()
        )

    @utils.special_tmp
    def cmd_collect_alignment_summary_metrics(self, bam, reference, qc_prefix, tmp='/tmp/'):
        '''

        :param bam:
        :param reference:
        :param qc_prefix:
        :param tmp:
        :return:
        '''

        return r'''
{software} -Djava.io.tmpdir={tmp} CollectAlignmentSummaryMetrics \
          R={reference} \
          I={bam} \
          O={qc_prefix}.CollectAlignmentSummaryMetrics.txt
        '''.format(
            software=self._software,
            tmp=tmp,
            reference=reference,
            bam=bam,
            qc_prefix=qc_prefix
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
        return r'''
{software} -Djava.io.tmpdir={tmp}  CollectGcBiasMetrics \
      I={bam_file} \
      O={qc_prefix}.gc_bias_metrics.txt \
      CHART={qc_prefix}.gc_bias_metrics.pdf \
      S={qc_prefix}.summary_metrics.txt \
      R={reference}
        '''.format(
            software=self._software,
            tmp=tmp,
            bam_file=bam_file,
            qc_prefix=qc_prefix,
            reference=reference
        )

    @utils.special_tmp
    def cmd_collect_hs_metrics(self, bam_file, qc_prefix, reference, bait_interval,
                               target_interval, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param reference:
        :param bait_interval:
        :param target_interval:
        :param tmp:
        :return:
        '''

        return r'''
{software} -Djava.io.tmpdir={tmp} CollectHsMetrics \
      I={bam_file} \
      O={qc_prefix}.hs_metrics.txt \
      R={reference} \
      BAIT_INTERVALS={bait_interval} \
      TARGET_INTERVALS={target_interval}
        '''.format(
            software=self._software,
            bam_file=bam_file,
            qc_prefix=qc_prefix,
            reference=reference,
            bait_interval=bait_interval,
            target_interval=target_interval,
            tmp=tmp
        )

    @utils.special_tmp
    def cmd_collect_insert_size_metrics(self, rawbam, qc_prefix, tmp):
        '''

        :param rawbam:
        :param qc_prefix:
        :param tmp:
        :return:
        '''
        return r'''
{software} -Djava.io.tmpdir={tmp}  CollectInsertSizeMetrics \
      I={bam} \
      O={qc_prefix}.insert_size_metrics.txt \
      H={qc_prefix}.insert_size_histogram.pdf \
      M=0.5
        '''.format(

            software=self._software,
            tmp=tmp,
            bam=rawbam,
            qc_prefix=qc_prefix
        )

    @utils.special_tmp
    def cmd_collect_oxoG_metrics(self, bam_file, qc_prefix, reference, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param reference:
        :param tmp:
        :return:
        '''
        return r'''
{software} -Djava.io.tmpdir={tmp}  CollectOxoGMetrics \
      I={bam_file} \
      O={qc_prefix}.oxoG_metrics.txt \
      R={reference}
        '''.format(
            software=self._software,
            tmp=tmp,
            bam_file=bam_file,
            qc_prefix=qc_prefix,
            reference=reference
        )

    @utils.special_tmp
    def cmd_collect_raw_wgs_metrics(self, bam_file, qc_prefix, reference, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param reference:
        :param tmp:
        :return:
        '''

        return '''
{software} -Djava.io.tmpdir={tmp}  CollectRawWgsMetrics \
          I={bam_file} \
          O={qc_prefix}.raw_wgs_metrics.txt \
          R={reference} \
          INCLUDE_BQ_HISTOGRAM=true
            '''.format(
            software=self._software,
            tmp=tmp,
            bam_file=bam_file,
            qc_prefix=qc_prefix,
            reference=reference
        )

    @utils.special_tmp
    def cmd_collect_targeted_pcr_metrics(self, bam_file, qc_prefix, reference, amplicon_intervals,
                                         target_intervals, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param reference:
        :param tmp:
        :return:
        '''
        return r'''
{software} -Djava.io.tmpdir={tmp}  CollectTargetedPcrMetrics \
           I={bam_file} \
           O={qc_prefix}.pcr_metrics.txt \
           R={reference} \
           AMPLICON_INTERVALS={amplicon_intervals} \
           TARGET_INTERVALS={target_intervals}
            '''.format(
            software=self._software,
            bam_file=bam_file,
            tmp=tmp,
            qc_prefix=qc_prefix,
            reference=reference,
            amplicon_intervals=amplicon_intervals,
            target_intervals=target_intervals
        )

    @utils.special_tmp
    def cmd_collect_rna_seq_metrics(self, bam_file, qc_prefix, ref_flat, ribosomal_intervals, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param ref_flat:
        :param ribosomal_intervals:
        :param tmp:
        :return:
        '''
        return r'''
{software} -Djava.io.tmpdir={tmp}  CollectRnaSeqMetrics \
          I={bam_file} \
          O={qc_prefix}.RNA_Metrics \
          REF_FLAT={ref_flat} \
          STRAND=None \
          RIBOSOMAL_INTERVALS={ribosomal_intervals}
            '''.format(
            software=self._software,
            tmp=tmp,
            bam_file=bam_file,
            qc_prefix=qc_prefix,
            ref_flat=ref_flat,
            ribosomal_intervals=ribosomal_intervals
        )

    @utils.special_tmp
    def cmd_collect_rrbs_metrics(self, bam_file, qc_prefix, reference, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param tmp:
        :return:
        '''
        return r'''
{software} -Djava.io.tmpdir={tmp}  CollectRrbsMetrics \
          R={reference} \
          I={bam_file} \
          M={qc_prefix}.rrbs
            '''.format(
            software=self._software,
            tmp=tmp,
            qc_prefix=qc_prefix,
            bam_file=bam_file,
            reference=reference
        )

    @utils.special_tmp
    def cmd_collect_sequencing_artifact_metrics(self, bam_file, qc_prefix, reference, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param reference:
        :param amplicon_interval_list:
        :param targets_interval_list:
        :param tmp:
        :return:
        '''
        return r'''
{software}  -Djava.io.tmpdir={tmp}  CollectSequencingArtifactMetrics \
         I={bam_file} \
         O={qc_prefix}artifact_metrics.txt \
         R={reference}
            '''.format(
            software=self._software,
            tmp=tmp,
            bam_file=bam_file,
            qc_prefix=qc_prefix,
            reference=reference
        )

    @utils.special_tmp
    def cmd_collect_wgs_metrics(self, bam_file, qc_prefix, reference, tmp):
        '''

        :param bam_file:
        :param qc_prefix:
        :param reference:
        :param tmp:
        :return:
        '''

        return r'''
{software}  -Djava.io.tmpdir={tmp}  CollectWgsMetrics \
           I={bam_file} \
           O={qc_prefix}.collect_wgs_metrics.txt \
           R={reference}
            '''.format(
            software=self._software,
            bam_file=bam_file,
            tmp=tmp,
            qc_prefix=qc_prefix,
            reference=reference
        )

    @utils.special_tmp
    def cmd_create_sequence_dictionary(self, reference, reference_dict, tmp):
        '''

        :param reference:
        :param reference_dict:
        :param tmp:
        :return:
        '''
        return r'''
{software} -Djava.io.tmpdir={tmp}  CreateSequenceDictionary \ 
          R={reference} \ 
          O={reference_dict}  
            '''.format(
            reference=reference,
            software=self._software,
            reference_dict=reference_dict,
            tmp=tmp,
        )

    @utils.special_tmp
    def cmd_mark_duplicates(self, bam_file, marked_bam, qc_prefix, tmp):
        '''

        :param bam_file:
        :param marked_bam:
        :param qc_prefix:
        :param tmp:
        :return:
        '''
        return r'''
{software} -Djava.io.tmpdir={tmp}   MarkDuplicates \
          I={bam_file} \
          O={marked_bam}\
          M={qc_prefix}marked_dup_metrics.txt
            '''.format(
            tmp=tmp,
            software=self._software,
            bam_file=bam_file,
            qc_prefix=qc_prefix,
            marked_bam=marked_bam
        )

    def __repr__(self):
        return 'picard:' + self._software

    def __str__(self):
        return 'A set of command line tools (in Java) for manipulating high-throughput ' \
               'sequencing (HTS) data and formats such as SAM/BAM/CRAM and VCF'


def test():
    pass


def main():
    test()


if __name__ == '__main__':
    main()
