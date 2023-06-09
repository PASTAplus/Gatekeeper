#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: robots

:Synopsis:
    Detect and log robot requests.

:Author:
    servilla

:Created:
    4/3/23
"""
import re

import daiquiri

from filter import robot_patterns


logger = daiquiri.getLogger(__name__)


def robot_name(user_agent: str | None) -> str:
    rn = None
    for pattern in robot_patterns:
        if user_agent is None or re.search(pattern.strip(), user_agent):
            rn = "Empty User-Agent" if user_agent is None else user_agent
            msg = f"The following HTTP User-Agent was identified as robot: {rn}"
            logger.info(msg)
            break
    return rn
