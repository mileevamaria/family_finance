SQL_SCRIPT_STARTUP = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER,
        first_name VARCHAR(64),
        last_name VARCHAR(64),
        username VARCHAR(64)
    );

    CREATE INDEX idx_telegram_id
    ON users (telegram_id);

    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER,
        user ?,
        data ?,
        text TEXT
    );

    CREATE TABLE IF NOT EXISTS updates (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER,
        message ?,
    );
"""
