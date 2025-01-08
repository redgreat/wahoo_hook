import asyncio
from typing import Optional

import asyncpg
from fastapi import FastAPI
from utils.config import AppConfig

description = """
This app serves as an base template for internal FastAPI apps
"""


class MyApp(FastAPI):
    def __init__(
        self, *, loop: Optional[asyncio.AbstractEventLoop] = None, config: AppConfig
    ):
        self.loop: asyncio.AbstractEventLoop = (
            loop or asyncio.get_event_loop_policy().get_event_loop()
        )
        super().__init__(
            title="Example Template",
            version="0.1.0",
            description=description,
            loop=self.loop,
            redoc_url="/docs",
            docs_url=None,
        )
        self.config = config
        self.add_event_handler("startup", func=self.startup)
        self.add_event_handler("shutdown", func=self.shutdown)

    @property
    def pool(self) -> asyncpg.Pool:
        return self.state.pool

    async def startup(self) -> None:
        self.state.pool = await asyncpg.create_pool(dsn=self.config["postgres_uri"])

    async def shutdown(self) -> None:
        await self.state.pool.close()
