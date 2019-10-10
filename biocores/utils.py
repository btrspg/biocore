#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019-05-05 16:43
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : utils.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

import os
import random
import string
from functools import wraps


def random_string(number=8):
    '''

    :param number:
    :return:
    '''
    return ''.join(random.sample(string.ascii_letters +
                                 string.digits, number))


def _check_str(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if all(map(lambda x: isinstance(x, str), args)):
            return func(*args, **kwargs)
        else:
            raise TypeError('Not str')

    return wrapper


def special_tmp(func):
    '''
    不同软件的tmp目录需要区分开
    :param func:
    :return:
    '''

    @wraps(func)
    def wrapper(*args, **kwargs):
        for i in kwargs.keys():
            if i == 'tmp':
                kwargs[i] = kwargs[i] + '/' + random_string(8)
        return func(*args, **kwargs)

    return wrapper


@_check_str
def dirs_for_file(*files):
    '''
    因为此方法主要服务于mkdir -p xxxxxx，所以即便有 ''（空），也不会影响程序操作
    :param files:
    :return:
    '''
    return list(map(lambda x: os.path.dirname(x), files))


@_check_str
def dirs_for_dirs(*dirs):
    '''

    :param dirs:
    :return:
    '''
    return dirs


@_check_str
def string_dirs(sep=' ', *dirs):
    '''

    :param sep:
    :param dirs:
    :return:
    '''
    return sep.join(dirs)


def main():
    print(dirs_for_dirs('/tmp/test', '/tmp/test2'))
    print(dirs_for_file('/tmp/file1/file', '/tmp/file2/file'))
    print(string_dirs(' ', *dirs_for_dirs('/tmp/test', '/tmp/test2'),
                      *dirs_for_file('/tmp/file1/file', '/tmp/file2/file')))


if __name__ == '__main__':
    main()
