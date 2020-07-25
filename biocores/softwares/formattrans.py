#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019-04-29 17:05
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : formattrans.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores import utils
from biocores.bases.tasks import Task


class Formattrans(Task):
    def __init__(self, software, fd):
        super(Formattrans, self).__init__(software)
        self._default = fd
        self._fc2o = 'fc2o'

    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;{software} --version'.format(
            repr=self.__repr__(),
            software=self._fc2o
        )

    @utils.modify_cmd
    def cmd_featurecounts_to_others(self, featurecounts,info,prefix):
        '''
        '''

        return r'''
{software} -f {fcs} {info} {prefix}
        '''.format(
            software=self._fc2o,
            fcs=' '.join(featurecounts) if isinstance(featurecounts,list) else featurecounts,
            info=info,
            prefix=prefix
        )

    def __repr__(self):
        return 'transformats:' + self._software

    def __str__(self):
        return 'My own python package for format transformation.'
