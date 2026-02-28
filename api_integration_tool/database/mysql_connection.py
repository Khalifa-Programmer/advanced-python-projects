import mysql.connector
from config.db_config import DB_CONFIG

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    # حذف الجدول إذا كان موجودًا
    cursor.execute("DROP TABLE IF EXISTS users")
    # إنشاء الجدول بنوع id الصحيح
    cursor.execute("""
    CREATE TABLE users (
        id VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255)
    )
    """)
    conn.commit()
    conn.close()
