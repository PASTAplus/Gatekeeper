#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: __init__

:Synopsis:
    Initialize robot_patterns list at package load.

:Author:
    servilla

:Created:
    4/3/23
"""
from config import Config

with open(Config.ROBOTS, "r") as f:
    robot_patterns = f.readlines()
