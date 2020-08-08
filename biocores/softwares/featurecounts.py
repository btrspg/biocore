#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import absolute_import, unicode_literals

from biocores import utils
from biocores.bases.tasks import Task


class Featurecounts(Task):
    def __init__(self, software, fd):
        super(Featurecounts, self).__init__(software)
        self._default = fd
        

    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;{software} -v'.format(
            repr=self.__repr__(),
            software=self._software
        )

    @utils.modify_cmd
    def cmd_featurecounts(self, bams,gtf,output,tmp,gene_name=True,ignore_dup=True):
        '''
        '''
        return r'''
{software} {paras} {ignore_dup} {gene_name} -a {gtf} -o {output} --tmpDir {tmp} {bam_list} 
        '''.format(
            software=self._software,
            paras=self._default.default,
            ignore_dup=' --ignoreDup ' if ignore_dup else '',
            gene_name= '--extraAttributes gene_name ' if gene_name else '',
            gtf=gtf,
            tmp=tmp,
            output=output,
            bam_list=' '.join(bams) if isinstance(bams,list) else bams,
          
        )

    def __repr__(self):
        return 'featureCounts:' + self._software

    def __str__(self):
        return 'featureCounts for quantity of RNA-seq'
