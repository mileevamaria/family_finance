from collections.abc import Callable
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
    last_name: str
    username: str


class Message(BaseModel):
    telegram_id: int = Field(..., alias='message_id')
    user: User = Field(..., alias='from')
    date: int
    text: str


class Update(BaseModel):
    telegram_id: int = Field(..., alias='update_id')
    message: Message
