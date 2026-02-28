from database.mysql_connection import connect_db

def insert_data(data):
    conn = connect_db()
    cursor = conn.cursor()
    for user in data:
        uuid = user['login']['uuid']
        name = user['name']['first'] + ' ' + user['name']['last']
        email = user['email']
        cursor.execute("""
        INSERT INTO users (id, name, email)
        VALUES (%s, %s, %s)
        """, (uuid, name, email))
    conn.commit()
    conn.close()
