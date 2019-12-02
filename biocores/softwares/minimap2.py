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


class Minimap2(Task):
    def __init__(self, software, fd):
        super(Minimap2, self).__init__(software)
        self._default = fd

    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;echo $({software} --version)'.format(
            repr=self.__repr__(),
            software=self._software
        )

    def cmd_align(self, reference, fq_fa, output, preset_options=' -x splice:hq'):
        '''

        :param reference:
        :param fq_fa:
        :param output:
        :param preset_options:
        :return:
        '''

        return r'''
{minimap2} {preset_options} {align_default} {reference} {fq_fa} -o {output}
        '''.format(
            minimap2=self._software,
            align_default=self._default.default,
            preset_options=preset_options,
            reference=reference,
            fq_fa=fq_fa if isinstance(fq_fa, str) else ' '.join(fq_fa),
            output=output

        )

    def __repr__(self):
        return 'minimap2:' + self._software

    def __str__(self):
        return 'Mapping and alignment between collections of DNA sequences'


def main():
    pass


if __name__ == '__main__':
    main()
