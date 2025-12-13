import os
import re
from contextlib import asynccontextmanager

import aiosqlite
from fastapi import FastAPI

from app.consts import (
    INLINE_CONFIRM_EXPENSE,
    REPLY_NEED_CATEGORY_EXPENSE,
    REPLY_NEED_MONEY_EXPENSE,
    SUCCESS_EXPENSE,
    WRONG_EXPENSE_FORMAT,
)
from app.pydantic_models import Env, Expense, Message, Update
from app.sql_scripts import (
    SQL_CREATE_EXPENSE,
    SQL_CREATE_MESSAGE,
    SQL_CREATE_TABLE_CATEGORIES,
    SQL_CREATE_TABLE_EXPENSES,
    SQL_CREATE_TABLE_MESSAGES,
    SQL_CREATE_TABLE_UPDATES,
    SQL_CREATE_TABLE_USERS,
    SQL_CREATE_UPDATE,
    SQL_CREATE_USER_IF_NOT_EXISTS,
)
from app.telegram_api import TelegramApi
from app.utils import ParseExpenseError, parse_expense, parse_force_reply


async def create_db_and_tables(env: Env) -> None:
    """Init & connect to database"""

    async with aiosqlite.connect(env.db_file_name) as db:
        await db.executescript(SQL_CREATE_TABLE_USERS)
        await db.executescript(SQL_CREATE_TABLE_MESSAGES)
        await db.execute(SQL_CREATE_TABLE_UPDATES)
        await db.executescript(SQL_CREATE_TABLE_CATEGORIES)
        await db.execute(SQL_CREATE_TABLE_EXPENSES)
        await db.commit()


async def save_telegram_message_in_db(
    env: Env,
    message: Message,
    update: Update,
) -> None:
    """Save Telegram data to the DB"""

    async with aiosqlite.connect(env.db_file_name) as db:
        await db.execute(
            SQL_CREATE_USER_IF_NOT_EXISTS.format(user=message.user))
        await db.execute(SQL_CREATE_MESSAGE.format(message=message))
        await db.execute(
            SQL_CREATE_UPDATE.format(update=update, message=message))
        await db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    """Check and create db and set webhook before start an app"""
    env = Env.from_env(os.getenv)
    await create_db_and_tables(env=env)
    telegram_api = TelegramApi(env=env)
    await telegram_api.set_webhook()
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def get() -> dict:
    return {'Hello': 'World!'}


@app.post('/message/')
async def post(update: Update) -> Update:
    env = Env.from_env(os.getenv)
    telegram_api = TelegramApi(env=env)
    message: Message
    expense: Expense
    text: str = ''
    reply: bool = False
    reply_markup: dict | None = None

    if update.message:
        message = update.message

        # Force Reply (category or money)
        if message.reply_to_message:
            message.text = await parse_force_reply(message=message)

        # Try to parse expense
        expense, error = await parse_expense(message=message)
        if error is None:
            # Expense parsed, create in the DB
            async with aiosqlite.connect(env.db_file_name) as db:
                await db.executescript(
                    SQL_CREATE_EXPENSE.format(expense=expense))
                await db.commit()
            text = SUCCESS_EXPENSE.format(expense=expense)

        elif error == ParseExpenseError.NOT_PRECISE:
            # Force Inline Keyboard
            reply = True
            matched_string = expense.metadata['matched_string']
            text = INLINE_CONFIRM_EXPENSE.format(
                expense=expense, matched_string=matched_string)
            reply_markup = {
                'inline_keyboard': [
                    [
                        {
                            'text': 'Yes, create it',
                            'callback_data': matched_string,
                        }
                    ]
                ]
            }

        elif error == ParseExpenseError.CATEGORY:
            # Force Reply category
            reply = True
            text = REPLY_NEED_CATEGORY_EXPENSE.format(expense=expense)
            reply_markup = {'force_reply': True}

        elif error == ParseExpenseError.MONEY:
            # Force Reply money
            reply = True
            text = REPLY_NEED_MONEY_EXPENSE.format(expense=expense)
            reply_markup = {'force_reply': True}

        else:
            text = WRONG_EXPENSE_FORMAT

    # Inline Choice
    elif update.callback_query:
        message = update.callback_query.message
        message.text = update.callback_query.data
        expense, _ = await parse_expense(message=message)
        text = SUCCESS_EXPENSE.format(expense=expense)

    # Something unexpected
    else:
        raise Exception

    await save_telegram_message_in_db(env=env, message=message, update=update)
    await telegram_api.send_message(
        chat_id=message.chat.telegram_id,
        text=text,
        reply=reply,
        reply_markup=reply_markup,
    )
    return update
