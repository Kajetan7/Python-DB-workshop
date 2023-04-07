import argparse
from models import User


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