#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019/11/15 10:11 AM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : cmdtype
# @Software: PyCharm


class Docker:
    def __init__(self, environment,software):
        self._software_type = 'Docker'
        self._environment= environment

    def wrapper_args(self, cmd):
        if "'" in cmd:
            cmd = cmd.replace('\'', '"')
        return '\'' + cmd + '\''

    def __repr__(self):
        return "Docker()"

    def __str__(self):
        return "Abstract class Task"


class Localrun:
    def __init__(self, software):
        self._software_type = 'Localrun'

    def warpper_args(self, cmd):
        return cmd

    def __repr__(self):
        return "Localrun()"

    def __str__(self):
        return "Abstract class Task"
