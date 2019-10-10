#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019-04-29 15:53
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : tasks.py
# @Software: PyCharm


from abc import ABCMeta


class Task(metaclass=ABCMeta):
    def __init__(self, software):
        self._software = software

    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ;{software} --version'.format(
            repr=self.__repr__(),

            software=self._software
        )

    def __repr__(self):
        return "Task()"

    def __str__(self):
        return "Abstract class Task"


def main():
    pass


if __name__ == '__main__':
    main()
