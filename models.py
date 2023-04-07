from pw_encryption import generate_salt, hash_password, check_password
from psycopg2 import connect, sql, OperationalError

try:
    cnx = connect(database="workshop", user='postgres', password='coderslab', host='localhost', port=5432)
    cnx.autocommit = True
    cursor = cnx.cursor()
except OperationalError as e:
    print("Connection Error: ", e)


class User:
    def __init__(self, username='', password='', salt=''):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=''):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = '''INSERT INTO users (username, hashed_password)
                        VALUES (%s, %s) RETURNING id'''
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = '''UPDATE Users SET username=%s, hashed_password=%s
                        WHERE id=%s'''
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_passowrd FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True
#  check: adding new user to database
new_user = User('kajetan', 'kk33')
new_user.save_to_db(cursor)