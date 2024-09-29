from functools import partial

import strawberry
from databases import Database
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from backend_test.context import Context
from backend_test.data_sources.data_source import DataSource
from backend_test.data_sources.postgres_data_source import PostgresDataSource
from backend_test.lifespan import lifespan
from backend_test.queries import Query
from backend_test.settings import Settings


def configure_datasource() -> DataSource:
    CONN_TEMPLATE = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"
    settings = Settings()  # type: ignore

    db = Database(
    CONN_TEMPLATE.format(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            port=settings.DB_PORT,
            host=settings.DB_SERVER,
            name=settings.DB_NAME,
        ),
    )
    data_source = PostgresDataSource(db)
    
    return data_source


schema = strawberry.Schema(query=Query)
ds=configure_datasource()
graphql_app: GraphQLRouter = GraphQLRouter(
    schema,
    context_getter=partial(Context, ds),  
)
app = FastAPI(lifespan=partial(lifespan, ds=ds))
app.include_router(graphql_app, prefix="/graphql")

