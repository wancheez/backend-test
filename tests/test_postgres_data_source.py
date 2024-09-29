import pytest
from unittest.mock import AsyncMock
from backend_test.data_sources.postgres_data_source import PostgresDataSource
from backend_test.schema import Book, Author

@pytest.mark.asyncio
async def test_fetch_books_with_author_ids():
    mock_db = AsyncMock()
    ds = PostgresDataSource(mock_db)
    
    mock_db.fetch_all.return_value = [
        {"title": "Book 1", "author_name": "Author 1"},
        {"title": "Book 2", "author_name": "Author 2"},
    ]
    
    books = await ds.fetch_books(author_ids=[1, 2], search=None, limit=None)
    
    assert len(books) == 2
    assert books[0] == Book(title="Book 1", author=Author(name="Author 1"))
    assert books[1] == Book(title="Book 2", author=Author(name="Author 2"))
    
    mock_db.fetch_all.assert_called_once()
    assert "WHERE books.author_id = ANY(:author_ids)" in mock_db.fetch_all.call_args[0][0]

@pytest.mark.asyncio
async def test_fetch_books_with_search():
    mock_db = AsyncMock()
    ds = PostgresDataSource(mock_db)

    mock_db.fetch_all.return_value = [
        {"title": "Book 1", "author_name": "Author 1"}
    ]

    books = await ds.fetch_books(author_ids=None, search="Book", limit=None)

    assert len(books) == 1
    assert books[0] == Book(title="Book 1", author=Author(name="Author 1"))

    mock_db.fetch_all.assert_called_once()
    assert "books.title ILIKE :search" in mock_db.fetch_all.call_args[0][0]

@pytest.mark.asyncio
async def test_fetch_books_with_limit():
    mock_db = AsyncMock()
    ds = PostgresDataSource(mock_db)

    mock_db.fetch_all.return_value = [
        {"title": "Book 1", "author_name": "Author 1"}
    ]

    books = await ds.fetch_books(author_ids=None, search=None, limit=1)

    assert len(books) == 1
    assert books[0] == Book(title="Book 1", author=Author(name="Author 1"))

    mock_db.fetch_all.assert_called_once()
    assert "LIMIT :limit" in mock_db.fetch_all.call_args[0][0]
