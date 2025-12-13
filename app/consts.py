from typing import Final

REPLY_NEED_CATEGORY_EXPENSE: Final[str] = """
    We\'re adding {expense.sum} amount, gimme the category
"""

REPLY_NEED_MONEY_EXPENSE: Final[str] = """
    We\'re adding to "{expense.category.name}" category, gimme the number
"""

INLINE_CONFIRM_EXPENSE: Final[str] = """
    Your expense "{matched_string}", correct?
"""

WRONG_EXPENSE_FORMAT: Final[str] = """
    Can't parse an expense. Allowed formats:
    - <category> <money>
    - <money> <category>
"""

SUCCESS_EXPENSE: Final[str] = (
    'Expense with category "{expense.category.name}" '
    'on {expense.sum} has been added'
)
