from __future__ import annotations

from typing import TYPE_CHECKING

import asyncpg
from fastapi import Request
from starlette.datastructures import State

if TYPE_CHECKING:
    from app.core import MyApp


class AppState(State):
    pool: asyncpg.Pool


class AppRequest(Request):
    app: MyApp
