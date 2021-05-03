import logging

from db.tables import User


async def create_user(db_session, name):

    user = User(
        name=name,
    )

    async with db_session() as session:
        session.add(user)
        await session.flush()
        await session.commit()
