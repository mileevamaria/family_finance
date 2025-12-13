import re
from enum import Enum

from app.pydantic_models import Category, Expense, Message


class ParseExpenseError(str, Enum):
    CATEGORY = 'category'
    MONEY = 'money'
    NOT_FORMATTED = 'not_formatted'
    NOT_PRECISE = 'not_precise'


async def parse_expense(
    message: Message,
) -> tuple[Expense, ParseExpenseError | None]:
    pattern_expense = (
        r'[A-Za-z]+\s[1-9][0-9]+((\.|\,)[0-9])?'
        r'|[1-9][0-9]+((\.|\,)[0-9])?\s[A-Za-z]+'
    )
    pattern_money = r'[1-9][0-9]+((\.|\,)[0-9])?'
    pattern_category = r'[A-Za-z]+'
    category_name: str = ''
    money: float = 0
    error: ParseExpenseError | None = None
    metadata: dict = {}

    message_text = message.text.strip().lower()
    message_date = message.date

    # Check if message formatted as "<category> <money>" or "<money> <category>"
    match_obj = re.match(pattern_expense, message_text)
    if match_obj:
        matched_string = match_obj.group().replace(',', '.')
        param1, param2, *_ = message_text.split(' ')
        if re.match(pattern_money, param1):
            category_name, money = param2, float(param1)
        else:
            category_name, money = param1, float(param2)

        # Ask to add as expense matched string (inline keyboard)
        if matched_string != message_text:
            error = ParseExpenseError.NOT_PRECISE
            metadata['matched_string'] = matched_string

    else:
        # Handle incorrect input
        # Received only money (force reply for category)
        money_match = re.fullmatch(pattern_money, message_text)
        if money_match:
            money = float(money_match.group())
            error = ParseExpenseError.CATEGORY

        # Received only category (force reply for money)
        category_match = re.fullmatch(pattern_category, message_text)
        if category_match:
            category_name = category_match.group()
            error = ParseExpenseError.MONEY

        # Wrong format
        if not (money or category_name):
            error = ParseExpenseError.NOT_FORMATTED

    expense = Expense(
        sum=money,
        category=Category(name=category_name),
        date=message_date,
        metadata=metadata,
    )
    return expense, error


async def parse_force_reply(message: Message) -> str:
    message_for_reply = message.reply_to_message.text
    pattern_money = r'\d*\.*\d+'
    pattern_category = r'\"[A-Za-z]+\"'
    try:
        if 'gimme the category' in message.reply_to_message.text:
            needed_part = re.findall(pattern_money, message_for_reply)[0]
        else:
            needed_part = re \
                .findall(pattern_category, message_for_reply)[0] \
                .replace('"', '')
        return f'{message.text} {needed_part}'
    except IndexError as err:
        err_text = 'Error while parsing force reply'
        raise IndexError(err_text) from err
