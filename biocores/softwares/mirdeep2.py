#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2020/2/18 4:28 PM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : mirdeep2
# @Software: PyCharm

import os
from biocores import utils
from biocores.bases.tasks import Task


class Mirdeep2(Task):
    def __init__(self, software, fd):
        super(Mirdeep2, self).__init__(software)
        self._default = fd
        if '/' in software:
            bin = os.path.dirname(software) + '/'
        else:
            bin = ''
        self._mapper = bin + 'mapper.pl'

    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;echo $({software} 2>&1 | grep "# miRDeep2")  '.format(
            repr=self.__repr__(),
            software=self._software
        )

    @utils.modify_cmd
    def cmd_mirdeep2(self,input_fasta,genome_fasta,mapped_reads,
                     miRNAs_ref=None, miRNAs_other=None, precursors=None):
        '''

        :param input_fasta:
        :param genome_fasta:
        :param mapped_reads:
        :param miRNAs_ref:
        :param miRNAs_other:
        :param precursors:
        :return:
        '''
        option = ''
        if miRNAs_ref is None:
            option += ' none '
        else:
            option += ' ' + miRNAs_ref
        if miRNAs_other is None:
            option += ' none '
        else:
            option += ' ' + miRNAs_other
        if precursors is None:
            option += ' none '
        else:
            option += ' ' + precursors
        return r'''
{miRDeep2} {input_fasta} {genome_fasta} {mapped_reads} {option}         
        '''.format(
            miRDeep2=self._software,
            input_fasta=input_fasta,
            genome_fasta=genome_fasta,
            mapped_reads=mapped_reads,
            option=option
        )

    @utils.modify_cmd
    def cmd_align(self, fastq, bowtie_index, reads_collapsed, mapped_reads):
        '''

        :param fastq:
        :param bowtie_index:
        :param reads_collapsed:
        :param mapped_reads:
        :return:
        '''
        return r'''
{mapper} {fastq} \
    {align_parameters}  \
    -p {bowtie_index} \
    -s {reads_collapsed} \
    -t {mapped_reads}     
        '''.format(
            mapper=self._mapper,
            fastq=fastq,
            align_parameters=self._default.align_paras,
            bowtie_index=bowtie_index,
            reads_collapsed=reads_collapsed,
            mapped_reads=mapped_reads
        )

    def __repr__(self):
        return 'mirdeep2:' + self._software

    def __str__(self):
        return 'miRDeep2 is a software package for identification ' \
               'of novel and known miRNAs in deep sequencing data. '
