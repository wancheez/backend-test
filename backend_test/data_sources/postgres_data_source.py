from typing import List, Optional

from databases import Database

from backend_test.data_sources.data_source import DataSource
from backend_test.schema import Author, Book  # Импортируйте ваши модели
from backend_test.settings import Settings

CONN_TEMPLATE = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"
settings = Settings()  # type: ignore

class PostgresDataSource(DataSource):
    def __init__(self, db: Database):
        self.db = db

    async def connect(self):
        await self.db.connect()

    async def disconnect(self):
        await self.db.disconnect()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.disconnect()

    async def fetch_books(self, author_ids: Optional[List[int]], search: Optional[str], limit: Optional[int]):
        query, values = self._generate_books_query(author_ids, search, limit)
        rows = await self.db.fetch_all(query, values=values)

        return [
            Book(title=row["title"], author=Author(name=row["author_name"]))
            for row in rows
        ]

    def _generate_books_query(self, author_ids=None, search=None, limit=None):
        query = """
            SELECT books.title, authors.id as author_id, authors.name as author_name
            FROM books
            JOIN authors ON books.author_id = authors.id
        """
        values = {}
        conditions = []

        if author_ids:
            conditions.append("books.author_id = ANY(:author_ids)")
            values["author_ids"] = author_ids

        if search:
            conditions.append("books.title ILIKE :search")
            values["search"] = f"%{search}%"

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        if limit:
            query += " LIMIT :limit"
            values["limit"] = limit

        return query, values