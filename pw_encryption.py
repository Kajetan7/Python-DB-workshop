import hashlib
from random import random
import string


def generate_salt():
    '''
    Generates a 16-character random salt.
    :rtype: str
    :return: str with generated salt
    '''
    salt = ''
    for i in range(0, 16):
        # get a random element from the iterable
        salt += random.choice(string.ascii_letters)
    return salt


def hash_password(password, salt=None):
    '''
    Hashes the password with salt as an optional parameter.

    If salt is not provided, generates random salt.
    If alt is less than 16 chars, fills the string to 16 chars.
    If salt is longer than 16 chars, cuts salt to 16 chars.

    :param str password: password to hash
    :param str salt: salt to hash, default None

    :rtype: str
    :return: hashed password
    '''

    # generate salt if not provided
    if salt is None:
        salt = generate_salt()

    #  fill to 16 chars if too short
    if len(salt) < 16:
        salt += ('a' * (16 - len(salt)))

    #  cut to 16 if too long
    if len(salt) > 16:
        salt = salt[:16]

    #  use sha256 algorithm to generate haintegersh
    t_sha = hashlib.sha256()

    #  encoding salt and password to utf-8 which required by hashlib
    t_sha.update(salt.encode('utf-8') + password.encode('utf-8'))

    #  return salt and hash joined
    return salt + t_sha.hexdigest()
