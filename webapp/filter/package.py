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
from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.responses import StreamingResponse

from auth.exceptions import AuthenticationException, ExpiredTokenException, \
    InvalidTokenException
from config import Config
from filter.headers import make_request_headers, make_response_headers
from filter.paths import clean_path

logger = daiquiri.getLogger(__name__)
router = fastapi.APIRouter()
client = httpx.AsyncClient(base_url=Config.PACKAGE, timeout=Config.TIMEOUT)


@router.get("/package/{path:path}")
async def package_get(request: Request, path: str):
    try:
        pasta_token, req_headers = await make_request_headers(request)
    except (AuthenticationException, ExpiredTokenException,
            InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        logger.error(f"{status}: {msg}")
        return fastapi.responses.PlainTextResponse(f"{status}: {msg}",
                                                   status_code=status)
    params = str(request.query_params)
    body = await request.body()
    content = body.decode("utf-8")
    req = client.build_request("GET", clean_path(path), headers=req_headers,
                               params=params, content=content)
    try:
        response = await client.send(req, stream=True)
        resp_headers = make_response_headers(pasta_token, response)
        return StreamingResponse(
            response.aiter_raw(),
            background=BackgroundTask(response.aclose),
            headers=resp_headers,
            status_code=response.status_code
        )
    except httpx.HTTPError as ex:
        logger.error(ex)
        raise ex


@router.post("/package/{path:path}")
async def package_post(request: Request, path: str):
    try:
        pasta_token, req_headers = await make_request_headers(request)
    except (AuthenticationException, ExpiredTokenException,
            InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        logger.error(f"{status}: {msg}")
        return fastapi.responses.PlainTextResponse(f"{status}: {msg}",
                                                   status_code=status)
    params = str(request.query_params)
    body = await request.body()
    content = body.decode("utf-8")
    req = client.build_request("POST", clean_path(path), headers=req_headers,
                               params=params, content=content)
    try:
        response = await client.send(req, stream=True)
        resp_headers = make_response_headers(pasta_token, response)
        return StreamingResponse(
            response.aiter_raw(),
            background=BackgroundTask(response.aclose),
            headers=resp_headers,
            status_code=response.status_code
        )
    except httpx.HTTPError as ex:
        logger.error(ex)
        raise ex


@router.put("/package/{path:path}")
async def package_put(request: Request, path: str):
    try:
        pasta_token, req_headers = await make_request_headers(request)
    except (AuthenticationException, ExpiredTokenException,
            InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        logger.error(f"{status}: {msg}")
        return fastapi.responses.PlainTextResponse(f"{status}: {msg}",
                                                   status_code=status)
    params = str(request.query_params)
    body = await request.body()
    content = body.decode("utf-8")
    req = client.build_request("PUT", clean_path(path), headers=req_headers,
                               params=params, content=content)
    try:
        response = await client.send(req, stream=True)
        resp_headers = make_response_headers(pasta_token, response)
        return StreamingResponse(
            response.aiter_raw(),
            background=BackgroundTask(response.aclose),
            headers=resp_headers,
            status_code=response.status_code
        )
    except httpx.HTTPError as ex:
        logger.error(ex)
        raise ex


@router.delete("/package/{path:path}")
async def package_delete(request: Request, path: str):
    try:
        pasta_token, req_headers = await make_request_headers(request)
    except (AuthenticationException, ExpiredTokenException,
            InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        logger.error(f"{status}: {msg}")
        return fastapi.responses.PlainTextResponse(f"{status}: {msg}",
                                                   status_code=status)
    params = str(request.query_params)
    body = await request.body()
    content = body.decode("utf-8")
    req = client.build_request("DELETE", clean_path(path), headers=req_headers,
                               params=params, content=content)
    try:
        response = await client.send(req, stream=True)
        resp_headers = make_response_headers(pasta_token, response)
        return StreamingResponse(
            response.aiter_raw(),
            background=BackgroundTask(response.aclose),
            headers=resp_headers,
            status_code=response.status_code
        )
    except httpx.HTTPError as ex:
        logger.error(ex)
        raise ex


@router.head("/package/{path:path}")
async def package_head(request: Request, path: str):
    try:
        pasta_token, req_headers = await make_request_headers(request)
    except (AuthenticationException, ExpiredTokenException,
            InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        logger.error(f"{status}: {msg}")
        return fastapi.responses.PlainTextResponse(f"{status}: {msg}",
                                                   status_code=status)
    params = str(request.query_params)
    body = await request.body()
    content = body.decode("utf-8")
    req = client.build_request("HEAD", clean_path(path), headers=req_headers,
                               params=params, content=content)
    try:
        response = await client.send(req, stream=True)
        resp_headers = make_response_headers(pasta_token, response)
        return StreamingResponse(
            response.aiter_raw(),
            background=BackgroundTask(response.aclose),
            headers=resp_headers,
            status_code=response.status_code
        )
    except httpx.HTTPError as ex:
        logger.error(ex)
        raise ex
