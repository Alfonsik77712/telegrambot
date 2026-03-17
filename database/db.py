import sqlite3
from config import DB_PATH, ADMIN_ID


def get_db():
    """Открывает соединение с базой."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """Создаёт все таблицы, если их нет."""
    db = get_db()
    cursor = db.cursor()

    # Таблица пользователей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER,
        username TEXT,
        first_seen TEXT
    )
    """)

    # Таблица заказов (добавил username!)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        service TEXT,
        description TEXT,
        price INTEGER,
        status TEXT,
        created_at TEXT
    )
    """)

    # Таблица рекламы
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        duration TEXT,
        pinned INTEGER,
        link TEXT,
        price INTEGER,
        status TEXT,
        created_at TEXT
    )
    """)

    # Таблица приватных подписок
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS private_subs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        expires_at TEXT,
        created_at TEXT
    )
    """)

    # Таблица админов
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER UNIQUE
    )
    """)

    # Таблица логов действий админов
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id INTEGER,
        action TEXT,
        order_id INTEGER,
        created_at TEXT
    )
    """)

    # Добавляем главного админа, если его нет
    cursor.execute("INSERT OR IGNORE INTO admins (tg_id) VALUES (?)", (ADMIN_ID,))

    db.commit()
    db.close()
