from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend_test.data_sources.data_source import DataSource


@asynccontextmanager
async def lifespan(app: FastAPI, ds: DataSource):
    async with ds:
        yield
    await ds.disconnect()