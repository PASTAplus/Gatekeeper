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


logger = daiquiri.getLogger(__name__)


async def authenticate(request: Request) -> PastaToken:
    pt = PastaToken()
    if "authorization" in request.headers:
        basic_auth = request.headers["authorization"]
        external_token = await ldap_authenticate(basic_auth)
        pt.from_auth_token(external_token)
    else:
        external_token = request.cookies.get("auth-token")
        if external_token is not None:
            try:
                pasta_crypto.verify_auth_token(Config.PUBLIC_KEY, external_token)
            except InvalidCryptoKeyException:
                raise
            except InvalidTokenException as ex:
                raise InvalidTokenException(ex, status.HTTP_400_BAD_REQUEST)
            pt.from_auth_token(external_token)
            if not pt.is_valid_ttl():
                msg = f"Authentication token time-to-live has expired, condolences"
                logger.error(msg)
                raise ExpiredTokenException(msg, status.HTTP_401_UNAUTHORIZED)
        else:
            pt.uid = Config.PUBLIC
            pt.system = Config.SYSTEM
    msg = f"Authentication for user '{pt.to_string()}'"
    logger.debug(msg)
    return pt


async def ldap_authenticate(credentials: str) -> str:
    ctx = True
    if Path(str(Config.CA_FILE)).exists():
        # Create local SSL CA context if Config.CA_FILE is valid path
        ctx = ssl.create_default_context(cafile=Config.CA_FILE)
    client = httpx.AsyncClient(base_url=Config.AUTH, verify=ctx)
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
