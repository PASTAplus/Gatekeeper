#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    test_iam

:Synopsis:

:Author:
    pasta

:Created:
    7/31/25
"""
import pytest

from config import Config
from edi.iam import IAM


@pytest.mark.asyncio
async def test_create_token():
    iam = IAM()
    edi_token = await iam.create_token(Config.PUBLIC_ID)
    assert edi_token is not None