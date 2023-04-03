#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: __init__

:Synopsis:

:Author:
    pasta

:Created:
    4/3/23
"""
from config import Config

with open(Config.ROBOTS, "r") as f:
    robot_patterns = f.readlines()
