#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: main

:Synopsis:
    Main driver for the Gatekeeper FastAPI framework

:Author:
    servilla

:Created:
    3/27/23
"""
import logging
import os

import daiquiri
import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from config import Config
from filter import package
from filter import audit
from views import index


cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + "/gatekeeper.log"
daiquiri.setup(level=Config.LEVEL,
               outputs=(daiquiri.output.File(logfile), "stdout",))
logger = daiquiri.getLogger(__name__)


app = fastapi.FastAPI(docs_url=None, redoc_url=None)


def configure(dev_mode: bool):
    configure_routes()


def configure_routes():
    app.mount('/static', StaticFiles(directory='static'), name='static')
    app.include_router(index.router)
    app.include_router(package.router)
    app.include_router(audit.router)


if __name__ == "__main__":
    configure(dev_mode=True)
    uvicorn.run(app, host='127.0.0.1', port=8088)
else:
    configure(dev_mode=False)
