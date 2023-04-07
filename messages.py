import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password")
parser.add_argument("-l", "--list", help="list all messages", action="store_true")
parser.add_argument("-t", "--to", help="to")
parser.add_argument("-s", "--send", help="text message to send")

args = parser.parse_args()


def print_user_messages(cur, user):
    messages = Message.load_all_messages(cur, user.id)
    for message in messages:
        from_ = User.load_user_by_id(cur, message.from_id)
        print(20 * "-")
        print(f'from: {from_.username}')
        print(f'date: {message.creation_date}')
        print(message.text)
        print(20 * "-")


def send_message(cur, from_id, recipent_name, text):
    if len(text) > 255:
        print("Message is too long!")
        return
    to = User.load_user_by_username(cur, recipient_name)
    if to:
        message = Message(from_id, to.id, text=text)
        message.save_to_db(cur)
        print("Message sent.")
    else:
        print("Recipient does not exists.")


if __name__ == '__main__':
    try:
        cnx = connect(database="workshop", user="postgres", password="coderslab", host="127.0.0.1")
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password:
            user = User.load_user_by_username(cursor, args.username)
            if check_password(args.password, user.hashed_password):
                if args.list:
                    print_user_messages(cursor, user)
                elif args.to and args.send:
                    send_message(cursor, user.id, args.to, args.send)
                else:
                    parser.print_help()
            else:
                print("Incorrect password or User does not exists!")
        else:
            print("username and password are required")
            parser.print_help()
        cnx.close()
    except OperationalError as err:
        print("Connection Error: ", err)
