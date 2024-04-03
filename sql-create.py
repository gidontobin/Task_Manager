import sqlite3

# Create a SQLite connection
conn = sqlite3.connect('task_manager.db')
cursor = conn.cursor()

# Create tables for users and tasks
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    description TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    completed INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id))''')

conn.commit()
