import hashlib
import sqlite3

import bcrypt

from data.User import User


class Data:
    def __init__(self):
        self.cursor = None
        self.conn = None
        self.connect_db()
        self.create_table()

    def connect_db(self):
        self.conn = sqlite3.connect('test.db')
        print('open db successfully')
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS USER (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_name TEXT,
                            hash_password TEXT,
                            first_name TEXT,
                            last_name TEXT,
                            email TEXT,
                            gender BLOB,
                            phone_number TEXT,
                            role BLOB DEFAULT 1
                        )
                    ''')

        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS ATTENDANCE (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            time DATETIME,
                            describe TEXT,
                            FOREIGN KEY (user_id) REFERENCES USER (id)
                        )
                    ''')

        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS IMAGE (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            image TEXT,
                            FOREIGN KEY (user_id) REFERENCES USER (id)
                        )
                    ''')

        self.conn.commit()

    def insert_user(self, user):
        try:
            sql = '''
                INSERT INTO USER (user_name, first_name, last_name, email, gender, phone_number)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            values = (user.username, user.first_name, user.last_name, user.email, user.gender, user.phone_number)

            self.cursor.execute(sql, values)
            self.conn.commit()
        except:
            print('Not success')

    def hash_password(self, password):
        # Use a secure hash function like SHA-256 for password hashing
        return hashlib.sha256(password.encode()).hexdigest()

    def get_user_by_credentials(self, user_name, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        sql = '''
            SELECT * FROM USER WHERE user_name = ? AND hash_password = ?
        '''
        values = (user_name, hashed_password)

        self.cursor.execute(sql, values)
        user_data = self.cursor.fetchone()

        if user_data:
            return User(*user_data)
        else:
            return None

    def close_connection(self):
        self.conn.close()
