import os
from contextlib import asynccontextmanager

import aiosqlite
import requests
from fastapi import FastAPI, status
from pydantic_models import Update
from sql_scripts import SQL_SCRIPT_STARTUP


async def create_db_and_tables() -> None:
    """Init & connect to database"""

    sqlite_file_name = "database.db"
    async with aiosqlite.connect(sqlite_file_name) as db:
        await db.executescript(SQL_SCRIPT_STARTUP)

async def set_telegram_webhook() -> None:
    """Set WebHook for Telegram Bot"""

    bot_token = os.getenv('TG_BOT_TOKEN')
    webhook_api_route = f'https://api.telegram.org/bot{bot_token}/'
    webhook_api_method = 'setWebhook'
    request_url = f'{webhook_api_route}{webhook_api_method}'
    public_url = os.getenv('NGROK_URL')
    if not public_url:
        raise ValueError('public_url is not set')
    message_api_method = '/message/'
    message_api_route = public_url + message_api_method
    body = {
        'url': message_api_route,
        'drop_pending_updates': False,
    }
    response = requests.post(request_url, data=body)
    if response.status_code != status.HTTP_200_OK:
        raise Exception


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    """Check and create db and set webhook before start an app"""

    await create_db_and_tables()
    await set_telegram_webhook()
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def get() -> dict:
    return {'Hello': 'World!'}


@app.post('/message/')
async def post(update: Update) -> Update:
    return update
