import strawberry
from strawberry.types import Info

from backend_test.context import Context
from backend_test.schema import Book


@strawberry.type
class Query:

    @strawberry.field
    async def books(
        self,
        info: Info[Context, None],
        author_ids: list[int] | None = [],
        search: str | None = None,
        limit: int | None = None,
    ) -> list[Book]:
        return await info.context.ds.fetch_books(author_ids, search, limit)

