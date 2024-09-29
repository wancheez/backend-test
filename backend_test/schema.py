import strawberry


@strawberry.type
class Author:
    name: str


@strawberry.type
class Book:
    title: str
    author: Author