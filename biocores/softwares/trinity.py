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


class Trinity(Task):
    def __init__(self, software, fd):
        super(Trinity, self).__init__(software)
        self._default = fd

    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;{software} 2>&1|grep Version'.format(
            repr=self.__repr__(),
            software=self._software
        )

    def cmd_assemble_transcript(self,fq1,fq2,outdir,memory=None,nt=None):
        '''

        :param bams:
        :param outgtf:
        :param annogtf:
        :return:
        '''
        return r'''
{trinity} {assemble_default} --max_memory {memory} \
    --output {outdir} --CPU {nt}  \
    --left {fq1} \
    --right {fq2}
        '''.format(
            trinity=self._software,
            assemble_default=self._default.default,
            nt=self._default.nt if None==nt else nt,
            memory=self._default.memory if None==memory else memory,
            fq1=fq1 if isinstance(fq1,str) else ','.join(fq1),
            fq2=fq2 if isinstance(fq2,str) else ','.join(fq2),
            **locals()

        )


    def __repr__(self):
        return 'trinity:' + self._software

    def __str__(self):
        return 'Trinity RNA-Seq de novo transcriptome assembly'



def main():
    pass


if __name__ == '__main__':
    main()
