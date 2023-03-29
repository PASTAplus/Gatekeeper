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
import base64
import daiquiri
import httpx
from starlette.requests import Request
import starlette.status as status

from auth.auth_exceptions import AuthenticationException, ExpiredTokenException, InvalidTokenException
from auth.pasta_token import PastaToken
from config import Config


logger = daiquiri.getLogger(__name__)


class TokenManager:

    def __init__(self, request: Request):
        self._token = None
        if "authorization" in request.headers:
            self._auth = request.headers["authorization"]
        else:
            self._auth = None
        self._cookies = request.cookies.get("auth-token")

    @property
    async def token(self):
        if self._auth is not None:
            self._token = await _authenticate(self._auth)
        elif self._cookies is not None:
            # Test for and validate auth-token
            msg = f"Expired authentication token"
            raise ExpiredTokenException(msg)
            msg = f"Invalid authentication token"
            raise InvalidTokenException(msg)
        else:
            self._token = _make_public_token()
        return self._token


def _make_public_token() -> bytearray:
    token = PastaToken()
    token.uid = Config.PUBLIC
    token.system = Config.SYSTEM
    return token.to_b64().decode()


async def _authenticate(credentials: str) -> str:
    client = httpx.AsyncClient(base_url=Config.AUTH)
    headers = {"authorization": credentials}
    path = "/auth/login/pasta"
    req = client.build_request("GET", path, headers=headers)
    resp = await client.send(req)
    if resp.status_code == status.HTTP_200_OK:
        cookies = resp.cookies
        auth_token = _make_internal_token(cookies["auth-token"])
        return auth_token
    elif resp.status_code == status.HTTP_400_BAD_REQUEST:
        msg = "Basic Authorization header not sent in request"
    elif resp.status_code == status.HTTP_401_UNAUTHORIZED:
        msg = "User or password is not correct and cannot be authenticated"
    elif resp.status_code == status.HTTP_418_IM_A_TEAPOT:
        msg = "User must accept EDI Data Policy statement"
    else:
        msg = "Unrecognized error occurred - response status code: {s}"
    logger.error(msg)
    raise AuthenticationException(msg)


def _make_internal_token(external_token: str) -> str:
    token = PastaToken()
    token.from_auth_token(external_token)
    internal_token = token.to_b64().decode("utf-8")
    return internal_token
