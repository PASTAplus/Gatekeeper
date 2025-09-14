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
from iam_lib.api.edi_token import EdiTokenClient
from iam_lib.exceptions import IAMResponseError, IAMInvalidToken
import ssl
from starlette.requests import Request
import starlette.status as status

from auth.exceptions import AuthenticationException, InvalidTokenException
from auth.pasta_token import PastaToken
from config import Config


logger = daiquiri.getLogger(__name__)


async def authenticate(request: Request) -> tuple:
    auth_token = _get_token_from_cookie(request, "auth-token")
    edi_token = _get_token_from_cookie(request, "edi-token")

    pasta_token = PastaToken()
    edi_token_client = EdiTokenClient(
        scheme=Config.AUTH_SCHEME,
        host=Config.AUTH_HOST,
        accept=Config.ACCEPT_TYPE,
        public_key_path=Config.AUTH_PUBLIC_KEY,
        algorithm=Config.JWT_ALGORITHM,
        token=None,
        truststore=Config.CA_FILE
    )

    if ((auth_token is None) and (edi_token is not None)) or ((auth_token is not None) and (edi_token is None)):
        msg = "EDI token and PASTA token must be present together"
        raise InvalidTokenException(msg, status.HTTP_400_BAD_REQUEST)
    elif auth_token is None and edi_token is None:
        if "authorization" in request.headers:
            basic_auth = request.headers["authorization"]
            auth_token, edi_token = await ldap_authenticate(basic_auth)
            pasta_token.from_auth_token(auth_token)
        else:
            pasta_token.uid = Config.PUBLIC
            pasta_token.system = Config.SYSTEM
            edi_token_response = edi_token_client.create_token(profile_edi_identifier=Config.PUBLIC_ID, key=Config.AUTH_KEY)
            edi_token = edi_token_response["token"]
    else:
        try:
            edi_token_client.token = edi_token
            edi_token_response = edi_token_client.refresh_token(auth_token=auth_token, edi_token=edi_token)
            auth_token = edi_token_response["pasta-token"]
            pasta_token.from_auth_token(auth_token)
            edi_token = edi_token_response["edi-token"]
        except (IAMInvalidToken, IAMResponseError) as ex:  # Reset edi-token and pasta-token to PUBLIC user
            logger.error(ex)
            edi_token_client.token = None
            edi_token_response = edi_token_client.create_token(profile_edi_identifier=Config.PUBLIC_ID, key=Config.AUTH_KEY)
            edi_token = edi_token_response["token"]
            pasta_token.uid = Config.PUBLIC
            pasta_token.system = Config.SYSTEM

    return pasta_token, edi_token


async def ldap_authenticate(credentials: str) -> tuple:
    verify = True
    if Path(str(Config.CA_FILE)).exists() and Path(str(Config.CA_FILE)).is_file():
        # Create local SSL CA context if Config.CA_FILE is valid path
        verify = ssl.create_default_context(cafile=Config.CA_FILE)
    else:
        msg = f"Truststore file '{Config.CA_FILE}' does not exist"
        logger.warning(msg)
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
        auth_token = cookies["auth-token"]
        edi_token = cookies["edi-token"]
        return auth_token, edi_token
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


def _get_token_from_cookie(request: Request, token_name: str) -> str | None:
    token = None
    if token_name in request.cookies:
        token = request.cookies[token_name]
    return token
