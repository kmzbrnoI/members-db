import logging

from sqlalchemy.future import select

from db.tables import AllowedAccount


async def is_account_allowed(db_session, email):

    allowed = False

    async with db_session() as session:
        result = await session.execute(select(AllowedAccount).where(AllowedAccount.email == email))
        account = result.scalars().first()

        if bool(account):
            if account.is_active:
                allowed = True

        return allowed


async def allow_account(db_session, email):

    async with db_session() as session:
        result = await session.execute(select(AllowedAccount).where(AllowedAccount.email == email))
        current_account = result.scalars().first()

        if bool(current_account):
            current_account.is_active = True
        else:
            account = AllowedAccount(email=email, is_active=True)
            session.add(account)

        await session.flush()
        await session.commit()
