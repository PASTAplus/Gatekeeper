#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: audit

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
from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.responses import StreamingResponse

from auth.authenticate import authenticate
from auth.exceptions import AuthenticationException, ExpiredTokenException, InvalidTokenException
from config import Config
from filter.headers import make_request_headers, make_response_headers
from filter.paths import clean_path

logger = daiquiri.getLogger(__name__)

router = fastapi.APIRouter()
client = httpx.AsyncClient(base_url=Config.AUDIT, timeout=Config.TIMEOUT)


@router.get("/audit/{path:path}")
async def audit_get(request: Request, path: str):
    try:
        pasta_token = await authenticate(request=request)
    except (AuthenticationException, ExpiredTokenException, InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        logger.error(f"{status}: {msg}")
        return fastapi.responses.PlainTextResponse(content=f"{status}: {msg}", status_code=status)
    req_headers = await make_request_headers(pasta_token, request)
    params = str(request.query_params)
    body = await request.body()
    content = body.decode("utf-8")
    req = client.build_request(
        method="GET",
        url=clean_path(path),
        headers=req_headers,
        params=params,
        content=content
    )
    try:
        response = await client.send(req, stream=True)
        resp_headers = make_response_headers(pasta_token, response)
        return StreamingResponse(
            content=response.aiter_raw(),
            background=BackgroundTask(response.aclose),
            headers=resp_headers,
            status_code=response.status_code
        )
    except httpx.HTTPError as ex:
        logger.error(ex)
        raise ex


@router.post("/audit/{path:path}")
async def audit_post(request: Request, path: str):
    try:
        pasta_token = await authenticate(request=request)
    except (AuthenticationException, ExpiredTokenException, InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        logger.error(f"{status}: {msg}")
        return fastapi.responses.PlainTextResponse(content=f"{status}: {msg}", status_code=status)
    req_headers = await make_request_headers(pasta_token, request)
    params = str(request.query_params)
    body = await request.body()
    content = body.decode("utf-8")
    req = client.build_request(
        method="POST",
        url=clean_path(path),
        headers=req_headers,
        params=params,
        content=content
    )
    try:
        response = await client.send(req, stream=True)
        resp_headers = make_response_headers(pasta_token, response)
        return StreamingResponse(
            content=response.aiter_raw(),
            background=BackgroundTask(response.aclose),
            headers=resp_headers,
            status_code=response.status_code
        )
    except httpx.HTTPError as ex:
        logger.error(ex)
        raise ex


@router.put("/audit/{path:path}")
async def audit_put(request: Request, path: str):
    try:
        pasta_token = await authenticate(request=request)
    except (AuthenticationException, ExpiredTokenException, InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        logger.error(f"{status}: {msg}")
        return fastapi.responses.PlainTextResponse(content=f"{status}: {msg}", status_code=status)
    req_headers = await make_request_headers(pasta_token, request)
    params = str(request.query_params)
    body = await request.body()
    content = body.decode("utf-8")
    req = client.build_request(
        method="PUT",
        url=clean_path(path),
        headers=req_headers,
        params=params,
        content=content
    )
    try:
        response = await client.send(req, stream=True)
        resp_headers = make_response_headers(pasta_token, response)
        return StreamingResponse(
            content=response.aiter_raw(),
            background=BackgroundTask(response.aclose),
            headers=resp_headers,
            status_code=response.status_code
        )
    except httpx.HTTPError as ex:
        logger.error(ex)
        raise ex


@router.delete("/audit/{path:path}")
async def audit_delete(request: Request, path: str):
    try:
        pasta_token = await authenticate(request=request)
    except (AuthenticationException, ExpiredTokenException, InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        logger.error(f"{status}: {msg}")
        return fastapi.responses.PlainTextResponse(content=f"{status}: {msg}", status_code=status)
    req_headers = await make_request_headers(pasta_token, request)
    params = str(request.query_params)
    body = await request.body()
    content = body.decode("utf-8")
    req = client.build_request(
        method="DELETE",
        url=clean_path(path),
        headers=req_headers,
        params=params,
        content=content
    )
    try:
        response = await client.send(req, stream=True)
        resp_headers = make_response_headers(pasta_token, response)
        return StreamingResponse(
            content=response.aiter_raw(),
            background=BackgroundTask(response.aclose),
            headers=resp_headers,
            status_code=response.status_code
        )
    except httpx.HTTPError as ex:
        logger.error(ex)
        raise ex


@router.head("/audit/{path:path}")
async def audit_head(request: Request, path: str):
    try:
        pasta_token = await authenticate(request=request)
    except (AuthenticationException, ExpiredTokenException, InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        logger.error(f"{status}: {msg}")
        return fastapi.responses.PlainTextResponse(content=f"{status}: {msg}", status_code=status)
    req_headers = await make_request_headers(pasta_token, request)
    params = str(request.query_params)
    body = await request.body()
    content = body.decode("utf-8")
    req = client.build_request(
        method="HEAD",
        url=clean_path(path),
        headers=req_headers,
        params=params,
        content=content
    )
    try:
        response = await client.send(req, stream=True)
        resp_headers = make_response_headers(pasta_token, response)
        return StreamingResponse(
            content=response.aiter_raw(),
            background=BackgroundTask(response.aclose),
            headers=resp_headers,
            status_code=response.status_code
        )
    except httpx.HTTPError as ex:
        logger.error(ex)
        raise ex
