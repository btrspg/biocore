#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) GPL3 License
# @Time    : 2019-04-29 17:05
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : fastp.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores.bases.tasks import Task


class Kallisto(Task):
    def __init__(self, software, fd):
        super(Kallisto, self).__init__(software)
        self._default = fd

    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;echo $({software} --version)'.format(
            repr=self.__repr__(),
            software=self._software
        )

    def cmd_build_index(self, reference, index_dir):
        '''

        :param reference:
        :param outdir:
        :return:
        '''
        return r'''
{kallisto} {index_paras} --index={index_dir} {reference}
        '''.format(
            kallisto=self._software,
            index_dir=index_dir,
            reference=reference,
            index_paras=self._default.index_paras
        )

    def cmd_read_count(self, index_dir, outdir, fq1,fq2,nt=None):
        '''

        :param reference:
        :param gtf:
        :param output_fasta:
        :return:
        '''
        return r'''
{kallisto} {quant_paras} --index={index_dir} --output-dir={outdir} --threads={nt} {fq1} {fq2}  
        '''.format(
            kallisto=self._software,
            quant_paras=self._default.quant_paras,
            index_dir=index_dir,
            outdir=outdir,
            fq1=fq1,
            fq2=fq2,
            nt=self._default.nt if nt is None else nt
        )

    def __repr__(self):
        return 'Kallisto:' + self._software

    def __str__(self):
        return 'kallisto is a program for quantifying abundances of transcripts from bulk and single-cell ' \
               'RNA-Seq data, or more generally of target sequences using high-throughput sequencing reads. '


def main():
    pass


if __name__ == '__main__':
    main()
