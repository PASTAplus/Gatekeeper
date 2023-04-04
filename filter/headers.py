#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: headers

:Synopsis:

:Author:
    pasta

:Created:
    4/3/23
"""
from httpx import Response
from starlette.requests import Request

from auth.authenticate import authenticate
from auth.pasta_crypto import create_authtoken
from auth.pasta_token import PastaToken
from config import Config
from filter.robots import robot_name


async def make_request_headers(request: Request) -> tuple:
    pt: PastaToken = await authenticate(request=request)
    headers = request.headers.items()
    cookie = f"auth-token={pt.to_b64().decode('utf-8')}"
    headers.append(("cookie", cookie))
    user_agent = request.headers.get("User-Agent")
    if robot_name(user_agent) is not None:
        headers.append(("Robot", user_agent))
    return pt, headers


def make_response_headers(pasta_token: PastaToken, response: Response) -> dict:
    headers = response.headers
    if pasta_token.uid != Config.PUBLIC:
        auth_token = create_authtoken(Config.PRIVATE_KEY, pasta_token.to_string())
        headers["set-cookie"] = f"auth-token={auth_token}"
    return headers

