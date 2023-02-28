import sqlite3
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
db_folder = os.path.join(dir_path, "db")
db_file = os.path.join(dir_path, "db", "config.db")

if not os.path.exists(db_folder):
    try:
        os.mkdir(db_folder)
    except:
        pass

def make_tables():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            user_id INTEGER,
            message_timestamp REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config (
            function TEXT,
            value TEXT
        )
    ''')
    cursor.execute('''
    INSERT INTO config (function, value)
    SELECT 'antilinks', 'False'
    WHERE NOT EXISTS (SELECT 1 FROM config WHERE function = 'antilinks');
    ''')
    cursor.execute('''
    INSERT INTO config (function, value)
    SELECT 'antiflood', 'False'
    WHERE NOT EXISTS (SELECT 1 FROM config WHERE function = 'antiflood');
    ''')
    cursor.execute('DELETE FROM messages')        
    conn.commit()
    conn.close()

make_tables()    



def get_antilink():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM config WHERE function=?", ('antilinks',))
    value = cursor.fetchone()[0]
    conn.close()
    return value

def get_antiflood():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM config WHERE function=?", ('antiflood',))
    value = cursor.fetchone()[0]
    conn.close()
    return value

def update_antilink(value):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("UPDATE config SET value = ? WHERE function = ?", (str(value), 'antilinks'))
    conn.commit()
    conn.close()

def update_antiflood(value):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("UPDATE config SET value = ? WHERE function = ?", (str(value), 'antiflood'))
    conn.commit()
    conn.close()

def get_last_messages(author_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()    
    cursor.execute(f'SELECT message_timestamp FROM messages WHERE user_id={author_id} ORDER BY message_timestamp DESC LIMIT 5')
    messages = cursor.fetchall()
    conn.close()
    return messages

def insert_messages(author_id,timestamp):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()     
    cursor.execute(f'INSERT INTO messages (user_id, message_timestamp) VALUES ({author_id}, {timestamp})')
    conn.commit()
    conn.close()

def clear_messages(author_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()     
    cursor.execute(f'DELETE FROM messages WHERE user_id = {author_id}')
    conn.commit()
    conn.close()    

