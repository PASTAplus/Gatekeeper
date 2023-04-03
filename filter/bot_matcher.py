#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: bot_matcher

:Synopsis:

:Author:
    pasta

:Created:
    4/3/23
"""
import re

from filter import robot_patterns


def robot_name(user_agent: str) -> str:
    robot = None
    for pattern in robot_patterns:
        if re.search(pattern.strip(), user_agent):
            robot = user_agent
            break
    return robot
