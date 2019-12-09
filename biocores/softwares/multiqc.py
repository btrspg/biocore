#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019-05-07 13:09
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : multiqc.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores import utils
from biocores.bases.tasks import Task
from biocores.softwares.default import *


class Multiqc(Task):
    def __init__(self, container):
        super(Multiqc, self).__init__(container,'multiqc')


    def cmd_version(self):
        return 'echo {repr};{environment} {software} --version'.format(
            repr=self.__repr__(),
            environment=self._environment,
            software=self._software
        )

    @utils.modify_cmd
    def cmd_merge_qc(self, outdir, filename, qc_dir):
        '''

        :param outdir:
        :param filename:
        :param qc_dir:
        :return:
        '''
        output_dirs = utils.string_dirs(' ', *utils.dirs_for_dirs(outdir))

        return r'''
{environment} 'mkdir {mkdir_paras} {output_dirs}'
{environment} '{software} {multiqc_paras} \
                --filename {filename} \
                --outdir {outdir} {qc_dir}'
            '''.format(
            environment=self._environment,
            software=self._software,
            multiqc_paras=MULTIQC_DEFAULT,
            mkdir_paras=MKDIR_DEFAULT,
            **locals()
        )

    def __repr__(self):
        return 'multiqc:' + self._environment

    def __str__(self):
        return 'Aggregate results from bioinformatics ' \
               'analyses across many samples into a single report'


def main():
    pass


if __name__ == '__main__':
    main()
