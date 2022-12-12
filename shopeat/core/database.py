import logging

from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from shopeat.core.config import Config
from shopeat.settings import SHOPEAT_DATABASE_URL

LOGGER = logging.getLogger(__name__)


class DBModel(DeclarativeBase):
    ...


class Database:
    def __init__(
        self,
        database_url: str,
        create_database: bool = True,
        create_schemas: bool = True,
    ):
        self.uri = make_url(database_url)
        self.engine = create_async_engine(database_url, echo=True)
        self.session = async_sessionmaker(bind=self.engine)

        self.__create_database = create_database
        self.__create_schemas = create_schemas

    async def create_all(self):
        create_db_exception = None

        if self.__create_database:
            try:
                await self.create_database()
            except Exception as exception:
                create_db_exception = exception

        if self.__create_schemas:
            async with self.engine.begin() as connection:
                try:
                    await connection.run_sync(DBModel.metadata.create_all)
                except Exception as error:
                    # re-raised here to include create db exception if schema creation fails
                    raise error from create_db_exception

    async def drop_all(self):
        async with self.engine.begin() as connection:
            await connection.run_sync(DBModel.metadata.drop_all)

    async def create_schemas(self):
        async with self.engine.begin() as connection:
            await connection.run_sync(DBModel.metadata.create_all)

    async def create_database(self):
        if self.uri.database:
            uri_without_database = self.uri.set(database="")
            async with create_async_engine(
                uri_without_database
            ).connect() as connection:
                await connection.execute(text("COMMIT"))
                await connection.execute(text(f'CREATE DATABASE "{self.uri.database}"'))
            LOGGER.info("Database %s successfully created!", self.uri.database)
        else:
            LOGGER.info("No database name specified... Skipping database creation.")

    @classmethod
    def from_config(cls):
        return cls(database_url=Config.get(SHOPEAT_DATABASE_URL))


DATABASE = Database.from_config()
