#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

# Auth
from auth.account import AccountDocument

from base import conn

conn.register([
    # Auth
    AccountDocument,

])
