#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: auth_exceptions

:Synopsis:
    Authentication related exceptions.

:Author:
    servilla

:Created:
    3/28/23
"""


class AuthenticationException(Exception):
    pass


class ExpiredTokenException(Exception):
    pass


class InvalidTokenException(Exception):
    pass
