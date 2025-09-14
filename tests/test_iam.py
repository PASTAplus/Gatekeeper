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
from iam_lib.api.edi_token import EdiTokenClient
from iam_lib.token import Token

@pytest.fixture
def edi_token_client():
    return EdiTokenClient(
        scheme="https",
        host="127.0.0.1:5443",
        accept="json",
        public_key_path="/home/pasta/git/iam-lib/tests/data/public_key.pem",
        algorithm="ES256",
        token=None,
        truststore="/etc/ssl/certs/ca-certificates.crt"
    )

@pytest.mark.asyncio
async def test_create_token():
    iam = IAM()
    edi_token = await iam.create_token(Config.PUBLIC_ID)
    assert edi_token is not None

def test_iam_lib_create_token(edi_token_client: EdiTokenClient):
    edi_token_response = edi_token_client.create_token(profile_edi_identifier=Config.PUBLIC_ID, key=Config.AUTH_KEY)
    edi_token = edi_token_response["token"]
    assert edi_token is not None
    token = Token(edi_token_response["token"])
    token.validate(public_key_path=Config.AUTH_PUBLIC_KEY, algorithm=Config.JWT_ALGORITHM),
