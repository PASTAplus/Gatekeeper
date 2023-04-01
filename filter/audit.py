#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: audit

:Synopsis:

:Author:
    pasta

:Created:
    3/27/23
"""
import fastapi
import httpx
from starlette.requests import Request
from starlette.responses import StreamingResponse
from starlette.background import BackgroundTask

from auth.authenticate import authenticate
from auth.exceptions import AuthenticationException, ExpiredTokenException, InvalidTokenException
from auth.pasta_crypto import create_authtoken
from auth.pasta_token import PastaToken
from config import Config


router = fastapi.APIRouter()

client = httpx.AsyncClient(base_url=f'http://localhost:8080/audit/')


@router.get("/audit/{path:path}")
async def rp_get(request: Request, path: str):
    try:
        pt: PastaToken = await authenticate(request=request)
    except (AuthenticationException, ExpiredTokenException, InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        return fastapi.responses.PlainTextResponse(f"{status}: {msg}", status_code=status)

    cookies = {"auth-token": pt.to_b64().decode("utf-8")}
    req = client.build_request("GET", path, cookies=cookies)
    resp = await client.send(req, stream=True)

    sr = StreamingResponse(
        resp.aiter_raw(),
        background=BackgroundTask(resp.aclose),
        headers=resp.headers,
        status_code=resp.status_code
    )
    if pt.uid != Config.PUBLIC:
        sr.set_cookie(key="auth-token", value=create_authtoken(Config.PRIVATE_KEY, pt.to_string()))
    return sr
