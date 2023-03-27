#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: index

:Synopsis:

:Author:
    pasta

:Created:
    3/27/23
"""
import fastapi
from starlette.requests import Request


router = fastapi.APIRouter()


@router.get('/')
def index(request: Request):
    return fastapi.responses.PlainTextResponse(content="PASTA Gatekeeper\n")


@router.get('/favicon.ico')
def favicon():
    return fastapi.responses.RedirectResponse(url='/static/images/favicon.png')