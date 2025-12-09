from pydantic import BaseModel, Field


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
    message: Message | None
