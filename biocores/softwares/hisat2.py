#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019-04-29 17:05
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : fastp.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
import os
from biocores import utils
from biocores.bases.tasks import Task


class Hisat2(Task):
    def __init__(self, software, fd):
        super(Hisat2, self).__init__(software)
        self._default = fd
        if '/' in software:
            bin = os.path.dirname(software) + '/'
        else:
            bin = ''
        self._hisat2_build = bin + 'hisat2-build'
        self._hisat2_extract_snps_haplotypes_UCSC = bin + 'hisat2_extract_snps_haplotypes_UCSC.py'
        self._hisat2_align_l = bin + 'hisat2-align-l'
        self._hisat2_extract_snps_haplotypes_VCF = bin + 'hisat2_extract_snps_haplotypes_VCF.py'
        self._hisat2_align_s = bin + 'hisat2-align-s'
        self._hisat2_extract_splice_sites = bin + 'hisat2_extract_splice_sites.py'
        self._hisat2_inspect = bin + 'hisat2-inspect'
        self._hisat2_build_l = bin + 'hisat2-build-l'
        self._hisat2_inspect_l = bin + 'hisat2-inspect-l'
        self._hisat2_build_s = bin + 'hisat2-build-s'
        self._hisat2_inspect_s = bin + 'hisat2-inspect-s'
        self._hisat2_extract_exons = bin + 'hisat2_extract_exons.py'
        self._hisat2_simulate_reads = bin + 'hisat2_simulate_reads.py'

    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;{software} --version'.format(
            repr=self.__repr__(),
            software=self._software
        )

    @utils.modify_cmd
    def cmd_build_index(self, reference, genome_index_prefix, genome_ss=None, genome_exon=None,
                        genome_genotype=None, genome_snp=None):
        '''

        :param reference:
        :param genome_ss:
        :param genome_exon:
        :param genome_genotype:
        :param genome_snp:
        :param genome_index_prefix:
        :return:
        '''
        option = ''
        if None is not genome_ss:
            option += ' --ss ' + genome_ss
        if None is not genome_exon:
            option += ' --exon ' + genome_exon
        if None is not genome_genotype:
            option += ' --haplotype ' + genome_genotype
        if None is not genome_snp:
            option += ' --genome_snp ' + genome_snp
        return r'''
{hisat_build} -p {nt} {reference} {option} {genome_index_prefix}
        '''.format(
            hisat_build=self._hisat2_build,
            nt=self._default.nt,
            reference=reference,
            option=option,
            genome_index_prefix=genome_index_prefix
        )

    @utils.modify_cmd
    def cmd_prepare_snp_ucsc(self,reference,snp_file,prefix):
        '''

        :param reference:
        :param snp_file:
        :param prefix:
        :return:
        '''
        if None is snp_file:
            return 'echo No snp_file'
        return r'''
awk 'BEGIN{{OFS="\t"}} {{if($2 ~ /^chr/) {{$2 = substr($2, 4)}}; if($2 == "M") {{$2 = "MT"}} print}}' {snp_file} \
    > {prefix}_snp.tmp
{software} {reference} {prefix}_snp.tmp {prefix}        
        '''.format(
            software=self._hisat2_extract_snps_haplotypes_UCSC,
            snp_file=snp_file,
            prefix=prefix,
            reference=reference
        )

    @utils.modify_cmd
    def cmd_prepare_exon_ss(self,gtf_file,prefix):
        '''

        :param gtf_file:
        :param prefix:
        :return:
        '''
        return r'''
{software1} {gtf_file} > {prefix}.ss
{software2} {gtf_file} > {prefix}.exon
        '''.format(
            software1=self._hisat2_extract_splice_sites,
            software2=self._hisat2_extract_exons,
            gtf_file=gtf_file,
            prefix=prefix
        )

    @utils.modify_cmd
    def cmd_align(self, hisat2_idx, fq1, fq2, summary, samtools, samtools_idx, outbam):
        '''

        :param hisat2_idx:
        :param fq1:
        :param fq2:
        :param summary:
        :param samtools:
        :param samtools_idx:
        :param outbam:
        :return:
        '''
        if None is fq2 or fq2 == '':
            return r'''
{hisat2} {align_paras} -x {hisat2_idx} -1 {fq1}  --summary-file {summary} | {samtools_sam2bam} | {samtools_sort}
{samtools_index}
 
            '''.format(
            hisat2=self._software,
            align_paras=self._default.align,
            samtools_sam2bam=samtools.cmd_sam2bam(samtools_idx, '-', bamfile=None),
            samtools_sort=samtools.cmd_sort('-', sortbam=outbam),
            samtools_index=samtools.cmd_index(outbam),
            **locals()
        )
        else:
            return r'''
{hisat2} {align_paras} -x {hisat2_idx} -1 {fq1} -2 {fq2} --summary-file {summary} | {samtools_sam2bam} | {samtools_sort}
{samtools_index}
 
            '''.format(
            hisat2=self._software,
            align_paras=self._default.align,
            samtools_sam2bam=samtools.cmd_sam2bam(samtools_idx, '-', bamfile=None),
            samtools_sort=samtools.cmd_sort('-', sortbam=outbam),
            samtools_index=samtools.cmd_index(outbam),
            **locals()
        )

    def __repr__(self):
        return 'hisat2:' + self._software

    def __str__(self):
        return 'graph-based alignment of next generation sequencing reads to a population of genomes'


def main():
    pass


if __name__ == '__main__':
    main()
