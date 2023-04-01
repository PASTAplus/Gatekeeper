#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: manager

:Synopsis:

:Author:
    pasta

:Created:
    3/28/23
"""
import daiquiri
import httpx
from starlette.requests import Request
import starlette.status as status

from auth.exceptions import AuthenticationException, ExpiredTokenException, InvalidTokenException
from auth.pasta_token import PastaToken
import auth.pasta_crypto as pasta_crypto
from config import Config


logger = daiquiri.getLogger(__name__)


async def authenticate(request: Request) -> PastaToken:
    pt = PastaToken()
    if "authorization" in request.headers:
        basic_auth = request.headers["authorization"]
        external_token = await _authenticate(basic_auth)
        pt.from_auth_token(external_token)
    else:
        external_token = request.cookies.get("auth-token")
        if external_token is not None:
            try:
                pasta_crypto.verify_authtoken(Config.PUBLIC_KEY, external_token)
            except Exception as ex:
                msg = f"Invalid authentication token"
                raise InvalidTokenException(msg, status.HTTP_400_BAD_REQUEST)
            pt.from_auth_token(external_token)
            if not pt.is_valid_ttl():
                msg = f"Expired authentication token"
                raise ExpiredTokenException(msg, status.HTTP_401_UNAUTHORIZED)
        else:
            pt.uid = Config.PUBLIC
            pt.system = Config.SYSTEM
    return pt


async def _authenticate(credentials: str) -> str:
    client = httpx.AsyncClient(base_url=Config.AUTH)
    headers = {"authorization": credentials}
    path = "/auth/login/pasta"
    req = client.build_request("GET", path, headers=headers)
    resp = await client.send(req)
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
        msg = "Unrecognized error occurred - response status code: {s}"
    logger.error(msg)
    raise AuthenticationException(msg, resp.status_code)
