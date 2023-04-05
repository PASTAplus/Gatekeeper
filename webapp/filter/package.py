#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: package

:Synopsis:
    Reverse proxy service for the PASTA Audit Manager.

:Author:
    servilla

:Created:
    3/27/23
"""
import daiquiri
import fastapi
import httpx
from starlette.requests import Request
from starlette.responses import StreamingResponse
from starlette.background import BackgroundTask

from auth.exceptions import AuthenticationException, ExpiredTokenException, InvalidTokenException
from config import Config
from filter.headers import make_request_headers, make_response_headers
from filter.paths import clean_path


logger = daiquiri.getLogger(__name__)
router = fastapi.APIRouter()
client = httpx.AsyncClient(base_url=Config.PACKAGE)


@router.get("/package/{path:path}")
async def package_get(request: Request, path: str):
    try:
        pasta_token, req_headers = await make_request_headers(request)
    except (AuthenticationException, ExpiredTokenException, InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        logger.error(f"{status}: {msg}")
        return fastapi.responses.PlainTextResponse(f"{status}: {msg}", status_code=status)
    req = client.build_request("GET", clean_path(path), headers=req_headers)
    response = await client.send(req, stream=True)
    resp_headers = make_response_headers(pasta_token, response)
    return StreamingResponse(
        response.aiter_raw(),
        background=BackgroundTask(response.aclose),
        headers=resp_headers,
        status_code=response.status_code
    )


@router.post("/package/{path:path}")
async def package_post(request: Request, path: str):
    try:
        pasta_token, req_headers = await make_request_headers(request)
    except (AuthenticationException, ExpiredTokenException, InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        logger.error(f"{status}: {msg}")
        return fastapi.responses.PlainTextResponse(f"{status}: {msg}", status_code=status)
    body = await request.body()
    content = body.decode("utf-8")
    req = client.build_request("POST", clean_path(path), headers=req_headers, content=content)
    response = await client.send(req, stream=True)
    resp_headers = make_response_headers(pasta_token, response)
    return StreamingResponse(
        response.aiter_raw(),
        background=BackgroundTask(response.aclose),
        headers=resp_headers,
        status_code=response.status_code
    )


@router.put("/package/{path:path}")
async def package_put(request: Request, path: str):
    try:
        pasta_token, req_headers = await make_request_headers(request)
    except (AuthenticationException, ExpiredTokenException, InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        logger.error(f"{status}: {msg}")
        return fastapi.responses.PlainTextResponse(f"{status}: {msg}", status_code=status)
    body = await request.body()
    content = body.decode("utf-8")
    req = client.build_request("PUT", clean_path(path), headers=req_headers, content=content)
    response = await client.send(req, stream=True)
    resp_headers = make_response_headers(pasta_token, response)
    return StreamingResponse(
        response.aiter_raw(),
        background=BackgroundTask(response.aclose),
        headers=resp_headers,
        status_code=response.status_code
    )


@router.delete("/package/{path:path}")
async def package_delete(request: Request, path: str):
    try:
        pasta_token, req_headers = await make_request_headers(request)
    except (AuthenticationException, ExpiredTokenException, InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        logger.error(f"{status}: {msg}")
        return fastapi.responses.PlainTextResponse(f"{status}: {msg}", status_code=status)
    req = client.build_request("DELETE", clean_path(path), headers=req_headers)
    response = await client.send(req, stream=True)
    resp_headers = make_response_headers(pasta_token, response)
    return StreamingResponse(
        response.aiter_raw(),
        background=BackgroundTask(response.aclose),
        headers=resp_headers,
        status_code=response.status_code
    )
