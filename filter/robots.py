#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: robots

:Synopsis:

:Author:
    pasta

:Created:
    4/3/23
"""
import re

from filter import robot_patterns


def robot_name(user_agent: str) -> str:
    rn = None
    for pattern in robot_patterns:
        if re.search(pattern.strip(), user_agent):
            rn = user_agent
            break
    return rn
