from collections.abc import Callable
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Env(BaseModel):
    tg_bot_token: str
    db_file_name: str
    accepted_users_id: list[str]
    timezone_name: str
    ngrok_url: str

    @staticmethod
    def from_env(getenv: Callable[[str, str], str]) -> 'Env':
        return Env(
            tg_bot_token=getenv('TG_BOT_TOKEN', ''),
            db_file_name=getenv('DB_FILE_NAME', ''),
            accepted_users_id=getenv('ACCEPTED_USERS_ID', '').split(','),
            timezone_name=getenv('TIMEZONE_NAME', ''),
            ngrok_url=getenv('NGROK_URL', ''),
        )


class User(BaseModel):
    telegram_id: int = Field(..., alias='id')
    first_name: str
    last_name: str | None = None
    username: str | None = None


class Chat(BaseModel):
    telegram_id: int = Field(..., alias='id')
    chat_type: str = Field(..., alias='type')


class Message(BaseModel):
    telegram_id: int = Field(..., alias='message_id')
    user: User = Field(..., alias='from')
    date: datetime
    text: str
    chat: Chat
    reply_markup: dict | None = None
    reply_to_message: 'Message | None' = None


class CallbackQuery(BaseModel):
    telegram_id: int = Field(..., alias='id')
    user: User = Field(..., alias='from')
    message: Message
    chat_instance: int
    data: str


class Update(BaseModel):
    telegram_id: int = Field(..., alias='update_id')
    message: Message | None = None
    callback_query: CallbackQuery | None = None


class Category(BaseModel):
    name: str


class CurrencyEnum(str, Enum):
    AMD = 'amd'
    USD = 'usd'
    RUB = 'rub'


class Expense(BaseModel):
    category: Category
    sum: float
    currency: CurrencyEnum = CurrencyEnum.AMD
    date: datetime
    metadata: dict
