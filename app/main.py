import os
from contextlib import asynccontextmanager

import aiosqlite
import requests
from fastapi import FastAPI, status
from pydantic_models import Env, Update
from sql_scripts import (
    SQL_CREATE_MESSAGE,
    SQL_CREATE_TABLE_CATEGORIES,
    SQL_CREATE_TABLE_EXPENSES,
    SQL_CREATE_TABLE_MESSAGES,
    SQL_CREATE_TABLE_UPDATES,
    SQL_CREATE_TABLE_USERS,
    SQL_CREATE_UPDATE,
    SQL_CREATE_USER_IF_NOT_EXISTS,
)


async def create_db_and_tables(env: Env) -> None:
    """Init & connect to database"""

    async with aiosqlite.connect(env.db_file_name) as db:
        await db.executescript(SQL_CREATE_TABLE_USERS)
        await db.executescript(SQL_CREATE_TABLE_MESSAGES)
        await db.execute(SQL_CREATE_TABLE_UPDATES)
        await db.executescript(SQL_CREATE_TABLE_CATEGORIES)
        await db.execute(SQL_CREATE_TABLE_EXPENSES)
        await db.commit()


async def set_telegram_webhook(env: Env) -> None:
    """Set WebHook for Telegram Bot"""

    webhook_api_route = f'https://api.telegram.org/bot{env.tg_bot_token}/setWebhook'
    message_api_method = '/message/'
    message_api_route = env.ngrok_url + message_api_method
    body = {
        'url': message_api_route,
        'drop_pending_updates': False,
    }
    response = requests.post(webhook_api_route, data=body)
    if response.status_code != status.HTTP_200_OK:
        raise Exception


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    """Check and create db and set webhook before start an app"""
    env = Env.from_env(os.getenv)
    await create_db_and_tables(env=env)
    await set_telegram_webhook(env=env)
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def get() -> dict:
    return {'Hello': 'World!'}


@app.post('/message/')
async def post(update: Update) -> Update:
    env = Env.from_env(os.getenv)
    async with aiosqlite.connect(env.db_file_name) as db:
        await db.execute(
            SQL_CREATE_USER_IF_NOT_EXISTS.format(user=update.message.user))
        await db.execute(SQL_CREATE_MESSAGE.format(message=update.message))
        await db.execute(SQL_CREATE_UPDATE.format(update=update))
        await db.commit()
    return update
