from database.db import get_db

def is_admin(tg_id: int) -> bool:
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT tg_id FROM admins WHERE tg_id = ?", (tg_id,))
    result = cursor.fetchone()
    db.close()
    return result is not None
