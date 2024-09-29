from abc import ABC, abstractmethod
from typing import List, Optional


class DataSource(ABC):

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.disconnect()
        
    @abstractmethod
    async def fetch_books(self, author_ids: Optional[List[int]], search: Optional[str], limit: Optional[int]):
        pass