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


class Stringtie(Task):
    def __init__(self, software, fd):
        super(Stringtie, self).__init__(software)
        self._default = fd

    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;{software} 2>&1|grep Version'.format(
            repr=self.__repr__(),
            software=self._software
        )

    def cmd_assemble_transcript(self,bams,outgtf,annogtf):
        '''

        :param bams:
        :param outgtf:
        :param annogtf:
        :return:
        '''
        return r'''
{stringtie} {bams} -o {outgtf} -p {nt} -G {annogtf}        
        '''.format(
            stringtie=self._software,
            bams = bams if isinstance(bams,str) else ' '.join(bams),
            nt=self._default.nt,
            outgtf=outgtf,
            annogtf=annogtf

        )

    def cmd_merge_gtf(self,gtfs,output,nt=None):
        return r'''
{stringtie} {merge_paras} \
    -o {output} \
    -p {nt} \
    {gtfs}     
    '''.format(
            stringtie=self._software,
            gtfs=gtfs if isinstance(gtfs,str) else ' '.join(gtfs),
            merge_paras=self._default.merge,
            nt=self._default.nt if None==nt else nt,
            output=output

        )


    def __repr__(self):
        return 'stringtie:' + self._software

    def __str__(self):
        return 'Transcript assembly and quantification for RNA-Seq'



def main():
    pass


if __name__ == '__main__':
    main()
