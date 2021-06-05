import logging

from sqlalchemy.future import select

from db.tables import User


async def add_user_info(db_session, email, name, given_name, family_name, avatar):

    async with db_session() as session:
        result = await session.execute(select(User).where(User.email == email))
        current_user = result.scalars().first()

        if bool(current_user):
            current_user.name = name
            current_user.given_name = given_name
            current_user.family_name = family_name
            current_user.picture = picture
        else:
            user = User(
                email=email,
                given_name=given_name,
                family_name=family_name,
                name=name,
                avatar=avatar
            )
            session.add(user)

        await session.flush()
        await session.commit()
