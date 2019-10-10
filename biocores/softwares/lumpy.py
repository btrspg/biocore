#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019-05-15 14:42
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : lumpy.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores import utils
from biocores.bases.tasks import Task
from biocores.softwares.default import *


class Lumpy(Task):
    def __init__(self, container):
        super(Lumpy, self).__init__(container, 'lumpy')
        # lumpyexpress is for simple lumpy running
        self._lumpyexpress = 'lumpyexpress'
        self._extract_split_reads_bwa_mem = 'extractSplitReads_BwaMem'
        self._svtyper = 'svtyper'

    def cmd_version(self):
        return "echo {repr};{environment} {software} lumpy -h 2>&1 |grep Program |awk '{{print $3,$4}}'".format(
            repr=self.__repr__(),
            environment=self._environment,
            software=self._software
        )

    @utils.special_tmp
    def cmd_sv_call(self, bam, name_sort_bam, unsort_bam, split_bam,
                    discordants_bam, sv_vcf, tmp='/tmp/lumpy', exclude_bed=''):
        '''

        :param bam:
        :param name_sort_bam:
        :param unsort_bam:
        :param split_bam:
        :param discordants_bam:
        :param sv_vcf:
        :param tmp:
        :param exclude_bed:
        :return:
        '''
        options = '' if exclude_bed == '' else '-x ' + exclude_bed
        output_dirs = utils.string_dirs(' ',
                                        *utils.dirs_for_file(name_sort_bam, unsort_bam, split_bam,
                                                             discordants_bam, sv_vcf),
                                        *utils.dirs_for_dirs(tmp))

        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} 'samtools sort -n {bam} -o {name_sort_bam}'
{environment} 'samtools view -h {name_sort_bam} | samblaster {samblaster_paras} | \
               samtools view -S -b - -o {unsort_bam}'
{environment} 'samtools view -b -F 1294 {unsort_bam} | samtools sort - -o {discordants_bam}'
{environment} 'samtools view -h {unsort_bam} | {esr_bm} -i stdin | samtools view -Sb - | \
               samtools sort - -o {split_bam}'
{environment} '{lumpyexpress} \
                -B {unsort_bam} \
                -S {split_bam} \
                -D {discordants_bam} \
                -T {tmp} \
                -o {sv_vcf} {options}'        
            '''.format(
            environment=self._environment,
            lumpyexpress=self._lumpyexpress,
            samblaster_paras=SAMBLASTER_DEFAULT,
            esr_bm=self._extract_split_reads_bwa_mem,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    def cmd_genotype_call(self, raw_bam, library_info_json, sv_vcf, reference, sv_genotype_vcf):
        '''

        :param raw_bam:
        :param library_info_json:
        :param sv_vcf:
        :param reference:
        :param sv_genotype_vcf:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_file(library_info_json, sv_genotype_vcf))
        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{svtyper} \
                -i {sv_vcf} \
                -B {raw_bam} \
                -T {reference} \
                -l {library_info_json} \
                -o {sv_genotype_vcf}'        
        '''.format(
            environment=self._environment,
            svtyper=self._svtyper,
            raw_bam=raw_bam,
            sv_vcf=sv_vcf,
            library_info_json=library_info_json,
            sv_genotype_vcf=sv_genotype_vcf,
            reference=reference,
            output_dirs=output_dirs,
            mkdir_paras=MKDIR_DEFAULT,
        )

    def __repr__(self):
        return 'lumpy:' + self._environment

    def __str__(self):
        return 'A probabilistic framework for structural variant discovery'


def main():
    lumpy = Lumpy('lumpy')
    print(lumpy.cmd_version())
    print(lumpy.cmd_sv_call('AS3919.raw.bam', 'AS3919.name-sort.bam',
                            'AS3919.samblaster.bam', 'AS3919.sr.bam', 'AS3919.dc.bam',
                            'AS3919.sv.vcf', tmp='/tmp'))


if __name__ == '__main__':
    main()
