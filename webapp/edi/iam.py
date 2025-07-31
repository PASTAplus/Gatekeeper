#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod:
    iam

:Synopsis:

:Author:
    Mark Servilla

:Created:
    7/31/25
"""
import json
from pathlib import Path

import daiquiri
import httpx
import ssl

from config import Config


logger = daiquiri.getLogger(__name__)



class IAM:

    def __init__(self):
        self.base_url = Config.AUTH

    async def create_token(self, edi_id: str) -> str:
        route = f"/auth/v1/token/{edi_id}"
        url = self.base_url + route
        data = {
            "key": Config.AUTH_KEY
        }

        verify = True
        if Path(str(Config.CA_FILE)).exists() and Path(str(Config.CA_FILE)).is_file():
            # Create local SSL CA context if Config.CA_FILE is valid path
            verify = ssl.create_default_context(cafile=Config.CA_FILE)
        else:
            msg = f"Truststore file '{Config.CA_FILE}' does not exist"
            logger.error(msg)
        try:
            response = httpx.post(url, json=data, verify=verify)
            response.raise_for_status()
        except httpx.HTTPError as ex:
            logger.error(ex)
            raise ex

        payload = response.json()
        try:
            edi_token = payload["token"]
        except KeyError as ex:
            logger.error(ex)
            edi_token = None

        return edi_token
