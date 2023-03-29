#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: package

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

from auth.token_manager import TokenManager

router = fastapi.APIRouter()

client = httpx.AsyncClient(base_url=f'http://localhost:8080/package/')


@router.get("/package/{path:path}")
async def rp_get(request: Request, path: str):
    tm = TokenManager(request=request)
    cookies = {"auth-token": await tm.token}
    req = client.build_request("GET", path, cookies=cookies)
    resp = await client.send(req, stream=True)
    print(resp.headers)
    return StreamingResponse(
        resp.aiter_raw(),
        background=BackgroundTask(resp.aclose),
    )
