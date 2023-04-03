#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: test_bot_matcher

:Synopsis:

:Author:
    pasta

:Created:
    4/3/23
"""
import pytest

from filter.bot_matcher import robot_name


def test_robot_name():
    assert robot_name("nojoybot") is not None
    assert robot_name("google") is None
    assert robot_name("python") is None
