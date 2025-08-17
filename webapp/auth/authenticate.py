#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: manager

:Synopsis:
    Perform PASTA-based authentication.

:Author:
    pasta

:Created:
    3/28/23
"""
from pathlib import Path

import daiquiri
import httpx
import ssl
from starlette.requests import Request
import starlette.status as status

from auth.exceptions import (
    AuthenticationException,
    ExpiredTokenException,
    InvalidTokenException,
    InvalidCryptoKeyException
)
from auth.pasta_token import PastaToken
import auth.pasta_crypto as pasta_crypto
from config import Config
from edi.iam import IAM


logger = daiquiri.getLogger(__name__)


async def authenticate(request: Request) -> tuple:
    pasta_token = PastaToken()
    edi_token = None
    is_public = False

    # Old-style PASTA authentication
    if "authorization" in request.headers:
        basic_auth = request.headers["authorization"]
        external_token = await ldap_authenticate(basic_auth)
        pasta_token.from_auth_token(external_token)  # Make internal token
    elif "cookie" in request.headers and request.cookies.get("auth-token"):
        external_token = request.cookies.get("auth-token")
        try:
            pasta_crypto.verify_auth_token(Config.PUBLIC_KEY, external_token)
        except InvalidCryptoKeyException:
            raise
        except InvalidTokenException as ex:
            raise InvalidTokenException(ex, status.HTTP_400_BAD_REQUEST)
        pasta_token.from_auth_token(external_token)  # Make internal token
        if not pasta_token.is_valid_ttl():
            msg = f"Authentication token time-to-live has expired, condolences"
            logger.error(msg)
            raise ExpiredTokenException(msg, status.HTTP_401_UNAUTHORIZED)
    else:
        pasta_token.uid = Config.PUBLIC
        pasta_token.system = Config.SYSTEM
        is_public = True

    msg = f"Authentication for user: '{pasta_token.to_string()}'"
    logger.info(msg)

    # EDI IAM authentication
    if "cookie" in request.headers and request.cookies.get("edi-token"):
        edi_token = request.cookies.get("edi-token")
        msg = f"EDI Token '{edi_token}' exists"
        logger.info(msg)
    elif is_public:
        iam = IAM()
        try:
            edi_token = await iam.create_token(Config.PUBLIC_ID)
        except httpx.HTTPError as ex:
            logger.error(ex)

    return pasta_token, edi_token


async def ldap_authenticate(credentials: str) -> str:
    verify = True
    if Path(str(Config.CA_FILE)).exists() and Path(str(Config.CA_FILE)).is_file():
        # Create local SSL CA context if Config.CA_FILE is valid path
        verify = ssl.create_default_context(cafile=Config.CA_FILE)
    else:
        msg = f"Truststore file '{Config.CA_FILE}' does not exist"
        logger.error(msg)
    client = httpx.AsyncClient(base_url=Config.AUTH, verify=verify)
    headers = {"authorization": credentials}
    path = "/auth/login/pasta"
    req = client.build_request("GET", path, headers=headers)
    try:
        resp = await client.send(req)
    except httpx.ConnectError as ex:
        logger.error(ex)
        msg = f"Internal Server Error - SSL certificate of '{Config.AUTH}' cannot be verified"
        raise AuthenticationException(msg, status.HTTP_500_INTERNAL_SERVER_ERROR)
    if resp.status_code == status.HTTP_200_OK:
        cookies = resp.cookies
        return cookies["auth-token"]
    elif resp.status_code == status.HTTP_400_BAD_REQUEST:
        msg = "Basic Authorization header not sent in request"
    elif resp.status_code == status.HTTP_401_UNAUTHORIZED:
        msg = "User or password is not correct and cannot be authenticated"
    elif resp.status_code == status.HTTP_418_IM_A_TEAPOT:
        msg = "User must accept EDI Data Policy statement"
    else:
        msg = f"Unrecognized error occurred - response status code {resp.status_code}"
    logger.error(msg)
    raise AuthenticationException(msg, resp.status_code)
