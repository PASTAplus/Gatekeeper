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

from auth.authenticate import authenticate
from auth.exceptions import AuthenticationException, ExpiredTokenException, InvalidTokenException
from config import Config
from filter.headers import make_request_headers, make_response_headers

logger = daiquiri.getLogger(__name__)
router = fastapi.APIRouter()
client = httpx.AsyncClient(timeout=Config.TIMEOUT)


@router.get("/package/{path:path}")
@router.post("/package/{path:path}")
@router.put("/package/{path:path}")
@router.delete("/package/{path:path}")
@router.head("/package/{path:path}")
async def package_filter(request: Request):
    try:
        pasta_token, edi_token = await authenticate(request=request)
    except (AuthenticationException, ExpiredTokenException, InvalidTokenException) as ex:
        status = ex.args[1]
        msg = ex.args[0]
        logger.error(f"{status}: {msg}")
        return fastapi.responses.PlainTextResponse(content=f"{status}: {msg}", status_code=status)
    req_headers = await make_request_headers(pasta_token, edi_token, request)
    params = str(request.query_params)
    raw_path = request.scope.get('raw_path')
    url = httpx.URL(path=Config.PACKAGE).join(raw_path.decode("latin-1"))
    async def request_body_iterator():
        async for chunk in request.stream():
            yield chunk
    req = client.build_request(
        method=request.method,
        url=url,
        headers=req_headers,
        params=params,
        content=request_body_iterator()
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
