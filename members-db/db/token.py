import logging
import datetime as dt

from sqlalchemy.future import select

from db.tables import Token


async def create_token(db_session, token_type, valid_period):

    uid = None

    now = dt.datetime.utcnow()

    token = Token(
        token_type=token_type,
        created_at=now,
        valid_until=now + valid_period,
        is_active=True,
    )

    async with db_session() as session:
        session.add(token)
        await session.flush()
        uid = token.uid
        await session.commit()

    logging.info('create_token(%s, %s, %s) -> %s', token_type, now, valid_period, uid)
    return uid


async def create_state_token(db_session):
    uid = await create_token(db_session, 'state', dt.timedelta(minutes=2))
    return str(uid)


async def create_nonce_token(db_session):
    uid = await create_token(db_session, 'nonce', dt.timedelta(minutes=2))
    return str(uid)


async def is_token_valid(db_session, token_uid, token_type):

    is_valid = False

    async with db_session() as session:
        result = await session.execute(select(Token).where(Token.uid == token_uid))
        token = result.scalars().first()

        if bool(token):
            now = dt.datetime.utcnow()
            logging.info('>>> >>> >>> >>> >>> >>>')
            logging.info('token.valid_until < now (%s, %s, %s)', now, token.valid_until, now < token.valid_until)
            logging.info('token.token_type == token_type (%s, %s, %s)', token.token_type, token_type, token.token_type == token_type)
            logging.info('token.is_active (%s)', token.is_active)
            if now < token.valid_until and token.token_type == token_type and token.is_active:
                is_valid = True

    logging.info('is_token_valid(%s, %s) --> %s', token_uid, token_type, is_valid)
    return is_valid
