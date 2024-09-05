#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: pasta_crypto

:Synopsis:
    Perform PASTA-based crytography associated with authentication tokens.

:Author:
    servilla

:Created:
    3/31/23
"""
import base64

from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import daiquiri

from auth.exceptions import InvalidCryptoKeyException, InvalidTokenException

logger = daiquiri.getLogger(__name__)


def import_key(f: str) -> RSA.RsaKey:
    try:
        with open(f, "r") as f:
            key_file = f.read()
        key = RSA.import_key(key_file)
        return key
    except FileNotFoundError as e:
        msg = f"Crypto-key '{f}' not found"
        logger.error(msg)
        logger.error(e)
        raise


def verify_auth_token(public_key: str, auth_token: str):
    """
    Verifies the PASTA+ authentication token, which is a two part string
    separate with a hyphen '-', and each part being base64 encoded:

        base64(token)-base64(md5_signature_of_base64_token)

    The base64 decoded token is a PASTA+ custom string like:

        uid=EDI,o=EDI,dc=edirepository,dc=org*https://pasta.edirepository.org/
        authentication*1558090703946*authenticated

    :param public_key:
    :param auth_token:
    :return: None, if successful
    """
    try:
        key = import_key(public_key)
    except FileNotFoundError as ex:
        msg = "Public signing key not found"
        raise InvalidCryptoKeyException(msg)
    try:
        token, signature = auth_token.split("-")
        h = MD5.new(token.encode("utf-8"))
        signature = base64.b64decode(signature)
        pkcs1_15.new(key).verify(h, signature)
    except ValueError as ex:
        msg = "Authentication token could not be decoded or verified"
        logger.error(msg)
        raise InvalidTokenException(msg)


def create_authtoken(private_key: str, token: str) -> str:
    try:
        key = import_key(private_key)
    except FileNotFoundError:
        msg = "Private signing key not found"
        raise InvalidCryptoKeyException(msg)
    token = base64.b64encode(token.encode("utf-8"))
    h = MD5.new(token)
    signature = base64.b64encode(pkcs1_15.new(key).sign(h))
    auth_token = token.decode("utf-8") + "-" + signature.decode("utf-8")
    logger.debug(auth_token)
    return auth_token
