#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: test_robots

:Synopsis:

:Author:
    pasta

:Created:
    4/3/23
"""
from webapp.filter.robots import robot_name


def test_robot_name():
    assert robot_name("nojoybot") is not None
    assert robot_name("google") is None
    assert robot_name("python") is None
    assert robot_name(None) is not None
