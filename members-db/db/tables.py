from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


DB_Base = declarative_base()


class User(DB_Base):
    __tablename__ = "users"

    uid = Column(BIGINT(unsigned=True), default=func.uuid_short(), primary_key=True)
    name = Column(Text, nullable=False)

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}


class Token(DB_Base):
    __tablename__ = "tokens"

    uid = Column(BIGINT(unsigned=True), default=func.uuid_short(), primary_key=True)
    token_type = Column(ENUM('oauth_state'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    valid_until = Column(DateTime, nullable=False)
    is_active = Column(Boolean, nullable=False)

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}


async def init_db(cfg):

    db_engine = create_async_engine(cfg['db']['url'], echo=True, hide_parameters=True)
    async with db_engine.begin() as conn:
        await conn.run_sync(DB_Base.metadata.drop_all)
        await conn.run_sync(DB_Base.metadata.create_all)

    await db_engine.dispose()


async def db_engine_ctx(app):

    app['db_engine'] = create_async_engine(app['cfg']['db']['url'], echo=True, hide_parameters=True)
    app['db_session'] = sessionmaker(app['db_engine'], expire_on_commit=False, class_=AsyncSession)

    yield

    await app['db_engine'].dispose()
