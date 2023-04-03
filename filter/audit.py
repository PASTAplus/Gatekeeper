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
from filter.bot_matcher import robot_name
from filter.paths import clean_path


router = fastapi.APIRouter()

client = httpx.AsyncClient(base_url=f'http://localhost:8080/audit/')


@router.get("/audit/{path:path}")
async def audit_get(request: Request, path: str):
    try:
        pt: PastaToken = await authenticate(request=request)
        cookie = f"auth-token={pt.to_b64().decode('utf-8')}"
    except (AuthenticationException, ExpiredTokenException, InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        return fastapi.responses.PlainTextResponse(f"{status}: {msg}", status_code=status)

    headers = request.headers.items()
    headers.append(("cookie", cookie))
    user_agent = request.headers.get("User-Agent")
    if robot_name(user_agent) is not None:
        headers.append(("Robot", user_agent))
    req = client.build_request("GET", clean_path(path), headers=headers)
    resp = await client.send(req, stream=True)

    headers = resp.headers
    if pt.uid != Config.PUBLIC:
        headers["set-cookie"] = f"auth-token={create_authtoken(Config.PRIVATE_KEY, pt.to_string())}"

    return StreamingResponse(
        resp.aiter_raw(),
        background=BackgroundTask(resp.aclose),
        headers=headers,
        status_code=resp.status_code
    )


@router.post("/audit/{path:path}")
async def audit_post(request: Request, path: str):
    try:
        pt: PastaToken = await authenticate(request=request)
        cookie = f"auth-token={pt.to_b64().decode('utf-8')}"
    except (AuthenticationException, ExpiredTokenException, InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        return fastapi.responses.PlainTextResponse(f"{status}: {msg}", status_code=status)

    headers = request.headers.items()
    headers.append(("cookie", cookie))
    user_agent = request.headers.get("User-Agent")
    if robot_name(user_agent) is not None:
        headers.append(("Robot", user_agent))
    body = await request.body()
    content = body.decode("utf-8")
    req = client.build_request("POST", clean_path(path), headers=headers, content=content)
    resp = await client.send(req, stream=True)

    headers = resp.headers
    if pt.uid != Config.PUBLIC:
        headers["set-cookie"] = f"auth-token={create_authtoken(Config.PRIVATE_KEY, pt.to_string())}"

    return StreamingResponse(
        resp.aiter_raw(),
        background=BackgroundTask(resp.aclose),
        headers=headers,
        status_code=resp.status_code
    )


@router.put("/audit/{path:path}")
async def audit_put(request: Request, path: str):
    try:
        pt: PastaToken = await authenticate(request=request)
        cookie = f"auth-token={pt.to_b64().decode('utf-8')}"
    except (AuthenticationException, ExpiredTokenException, InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        return fastapi.responses.PlainTextResponse(f"{status}: {msg}", status_code=status)

    headers = request.headers.items()
    headers.append(("cookie", cookie))
    user_agent = request.headers.get("User-Agent")
    if robot_name(user_agent) is not None:
        headers.append(("Robot", user_agent))
    body = await request.body()
    content = body.decode("utf-8")
    req = client.build_request("PUT", clean_path(path), headers=request, content=content)
    resp = await client.send(req, stream=True)

    headers = resp.headers
    if pt.uid != Config.PUBLIC:
        headers["set-cookie"] = f"auth-token={create_authtoken(Config.PRIVATE_KEY, pt.to_string())}"

    return StreamingResponse(
        resp.aiter_raw(),
        background=BackgroundTask(resp.aclose),
        headers=headers,
        status_code=resp.status_code
    )


@router.delete("/audit/{path:path}")
async def audit_delete(request: Request, path: str):
    try:
        pt: PastaToken = await authenticate(request=request)
        cookie = f"auth-token={pt.to_b64().decode('utf-8')}"
    except (AuthenticationException, ExpiredTokenException, InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        return fastapi.responses.PlainTextResponse(f"{status}: {msg}", status_code=status)

    headers = request.headers.items()
    headers.append(("cookie", cookie))
    user_agent = request.headers.get("User-Agent")
    if robot_name(user_agent) is not None:
        headers.append(("Robot", user_agent))
    req = client.build_request("DELETE", clean_path(path), headers=request.headers)
    resp = await client.send(req, stream=True)

    headers = resp.headers
    if pt.uid != Config.PUBLIC:
        headers["set-cookie"] = f"auth-token={create_authtoken(Config.PRIVATE_KEY, pt.to_string())}"

    return StreamingResponse(
        resp.aiter_raw(),
        background=BackgroundTask(resp.aclose),
        headers=headers,
        status_code=resp.status_code
    )
