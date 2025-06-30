#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: headers

:Synopsis:
    Generate request and response headers.

:Author:
    servilla

:Created:
    4/3/23
"""
import daiquiri
from httpx import Response
from starlette.requests import Request

from auth.authenticate import authenticate
from auth.pasta_crypto import create_authtoken
from auth.pasta_token import PastaToken
from config import Config
from filter.robots import robot_name


logger = daiquiri.getLogger(__name__)


async def make_request_headers(pasta_token: PastaToken, edi_token: str, request: Request) -> list:
    headers = []
    for header in request.headers:
        if header.lower() != "cookie":
            headers.append((header, request.headers.get(header)))

    # Add internal pasta authentication token
    cookie = f"auth-token={pasta_token.to_b64().decode('utf-8')}"

    # Add new JWT token
    if edi_token is not None:
        cookie += f";edi-token={edi_token}"
    headers.append(("cookie", cookie))

    user_agent = request.headers.get("User-Agent")
    rn = robot_name(user_agent)
    if rn is not None:
        headers.append(("Robot", rn))
    logger.debug(f"Request - {headers}")
    return headers


def make_response_headers(pasta_token: PastaToken, response: Response) -> dict:
    headers = response.headers
    if pasta_token.uid != Config.PUBLIC:
        auth_token = create_authtoken(Config.PRIVATE_KEY, pasta_token.to_string())
        headers["set-cookie"] = f"auth-token={auth_token}"
    logger.debug(f"Response - {headers}")
    return headers

