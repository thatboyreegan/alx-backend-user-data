#!/usr/bin/env python3
"""this module implements the encryption of passwords"""

import bcrypt

def hash_password(password: str) -> bytes:
    """
    hashes a given password
    Args:
        password (str): password to be hashed
    Returns:
        bytes: a string of the hashed and salted password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    checks if a hashed_password and a given password match
    Args:
        hashed_password (bytes): a hashed password
        password (str): the password to match
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
