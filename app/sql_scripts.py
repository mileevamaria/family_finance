from typing import Final


SQL_CREATE_TABLE_USERS: Final[str] = """
-- =============================================================================
--  `summary` table: Stores users who sent messages to the bot
-- =============================================================================
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY ASC,
        telegram_id INTEGER NOT NULL UNIQUE,
        first_name VARCHAR(64) NOT NULL,
        last_name VARCHAR(64) NOT NULL,
        username VARCHAR(64) NOT NULL UNIQUE
    );

    CREATE INDEX IF NOT EXISTS idx_telegram_user_id
    ON users (telegram_id, username);
"""

SQL_CREATE_TABLE_MESSAGES: Final[str] = """
-- =============================================================================
--  `summary` table: Stores messages which were sent to the bot
-- =============================================================================
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY ASC,
        telegram_id INTEGER NOT NULL UNIQUE,
        user_telegram_id INTEGER NOT NULL,
        date DATETIME NOT NULL,
        text TEXT NOT NULL,
        FOREIGN KEY (user_telegram_id) REFERENCES users(telegram_id)
    );

    CREATE INDEX IF NOT EXISTS idx_telegram_message_id
    ON messages (telegram_id);
"""

SQL_CREATE_TABLE_UPDATES: Final[str] = """
-- =============================================================================
--  `summary` table: Stores updates objects received from the bot
-- =============================================================================
    CREATE TABLE IF NOT EXISTS updates (
        id INTEGER PRIMARY KEY ASC,
        telegram_id INTEGER NOT NULL UNIQUE,
        message_telegram_id INTEGER NOT NULL,
        FOREIGN KEY (message_telegram_id) REFERENCES messages(telegram_id)
    );
"""

SQL_CREATE_TABLE_CATEGORIES: Final[str] = """
-- =============================================================================
--  `summary` table: Stores categories for expenses
-- =============================================================================
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY ASC,
        name VARCHAR(32) NOT NULL UNIQUE
    );

    CREATE INDEX IF NOT EXISTS idx_telegram_category_name
    ON categories (name);
"""

SQL_CREATE_TABLE_EXPENSES: Final[str] = """
-- =============================================================================
--  `summary` table: Stores expenses
-- =============================================================================
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        sum FLOAT(7) NOT NULL,
        category_id INTEGER NOT NULL,
        currency VARCHAR(16) DEFAULT('amd'),
        date DATETIME NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    );
"""

SQL_CREATE_USER_IF_NOT_EXISTS: Final[str] = """
    INSERT INTO users (telegram_id, first_name, last_name, username)
    SELECT
        '{user.telegram_id}',
        '{user.first_name}',
        '{user.last_name}',
        '{user.username}'
    WHERE NOT EXISTS (
        SELECT 1
        FROM users
        WHERE telegram_id = '{user.telegram_id}'
            AND username = '{user.username}'
    );
"""

SQL_CREATE_MESSAGE: Final[str] = """
    INSERT INTO messages (telegram_id, user_telegram_id, date, text)
    VALUES (
        '{message.telegram_id}',
        '{message.user.telegram_id}',
        '{message.date}',
        '{message.text}'
    )
"""

SQL_CREATE_UPDATE: Final[str] = """
    INSERT INTO updates (telegram_id, message_telegram_id)
    VALUES ('{update.telegram_id}', '{update.message.telegram_id}')
"""
