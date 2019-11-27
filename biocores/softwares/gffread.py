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


class Gffread(Task):
    def __init__(self, software, fd):
        super(Gffread, self).__init__(software)
        self._default = fd

    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;echo $({software} --version)'.format(
            repr=self.__repr__(),
            software=self._software
        )

    def cmd_gffread(self, reference,gtf,output_fasta):
        '''

        :param reference:
        :param gtf:
        :param output_fasta:
        :return:
        '''
        return r'''
{gffread} -w {output_fasta} -g {reference} {gtf}
        '''.format(
            gffread=self._software,
            gffcompare_default=self._default.default,
            gtf=gtf,
            output_fasta=output_fasta,
            reference=reference
        )

    def __repr__(self):
        return 'gffread:' + self._software

    def __str__(self):
        return 'FASTA sequence extraction and more'


def main():
    pass


if __name__ == '__main__':
    main()
