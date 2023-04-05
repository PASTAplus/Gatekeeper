#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: paths

:Synopsis:
    Clean URL paths with PASTA conflicting patterns.

:Author:
    servilla

:Created:
    4/2/23
"""
import re


def clean_path(path: str) -> str:
    return re.sub(r'/{2,}', '/', path)