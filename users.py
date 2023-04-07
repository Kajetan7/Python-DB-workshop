import argparse
from models import User
from psycopg2.errors import UniqueViolation
from pw_encryption import check_password


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")

args = parser.parse_args()


def list_users(cur):
    users = User.load_all_users(cur)
    for user in users:
        print(user.username)


def create_user(cur, username, password):
    if len(password) < 8:
        print('Password is too short. It should have minimum 8 characters.')
    else:
        try:
            user = User(username=username, password=password)
            user.save_to_db(cur)
            print('User created')
        except UniqueViolation as e:
            print("User already exists. ", e)


def delete_user(cur, username, password):
    user = User.load_user_by_username(cur, username)
    if not user:
        print("User does not exist!")
    elif check_password(password, user.hashed_password):
        user.delete(cur)
        print("User deleted.")
    else:
        print("Incorrect password!")


def edit_user(cur, username, password, new_pass):
    user = User.load_user_by_username(cur, username)
    if not user:
        print("User does not exist!")
    elif check_password(password, user.hashed_password):
        if len(new_pass) < 8:
            print("Password is too short. It should have minimum 8 characters.")
        else:
            user.hashed_password = new_pass
            user.save_to_db(cur)
            print("Password changed.")
    else:
        print("Incorrect password.")

