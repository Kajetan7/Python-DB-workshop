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
        self._hashed_password = password

    def save_to_db(self, cursor):
        if self._id == -1:
            sql = '''INSERT INTO users (username, hashed_password)
                        VALUES (%s, %s) RETURNING id'''
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]
            return True
        return False

#  check: adding new user to database
new_user = User('kajetan', 'kk33')
new_user.save_to_db(cursor)