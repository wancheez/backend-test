from strawberry.fastapi import BaseContext

from backend_test.data_sources.data_source import DataSource


class Context(BaseContext):
    ds: DataSource

    def __init__(self, ds: DataSource) -> None:
        self.ds = ds