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

from auth.token_manager import TokenManager

router = fastapi.APIRouter()

client = httpx.AsyncClient(base_url=f'http://localhost:8080/audit/')


@router.get("/audit/{path:path}")
async def rp_get(request: Request, path: str):
    tm = TokenManager(request=request)
    req = client.build_request("GET", path, cookies={"auth-token": tm.token})
    resp = await client.send(req, stream=True)
    return StreamingResponse(
        resp.aiter_raw(),
        background=BackgroundTask(resp.aclose),
    )
