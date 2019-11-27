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


class Gffcompare(Task):
    def __init__(self, software, fd):
        super(Gffcompare, self).__init__(software)
        self._default = fd

    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;echo $({software} --version)'.format(
            repr=self.__repr__(),
            software=self._software
        )

    def cmd_gffcompare(self, gtflist, reference, prefix, extend_para, *gtfs):
        '''

        :param gtflist:
        :param reference:
        :param prefix:
        :param extend_para: -M -N
        :param gtfs:
        :return:
        '''
        cmd = ''
        if None != gtflist:
            cmd = cmd + ' -i ' + gtflist
        else:
            cmd = cmd + ' '.join(gtfs)

        return r'''
{gffcompare} {gffcompare_default} {extend_para} -o {prefix} -r {reference} {cmd} 
        '''.format(
            gffcompare=self._software,
            gffcompare_default=self._default.default,
            prefix=prefix,
            reference=reference,
            cmd=cmd,
            extend_para=extend_para
        )

    def __repr__(self):
        return 'gffcompare:' + self._software

    def __str__(self):
        return 'Program for processing GTF/GFF files'


def main():
    pass


if __name__ == '__main__':
    main()
