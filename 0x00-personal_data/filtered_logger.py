#!/usr/bin/env python3
"""The module filtered_logger"""
from typing import List
import logging
import mysql.connector
import os

import re


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
):
    """
    returns the obfuscated log message
    Args:
        fields (List): the fields to obfuscate
        redaction (str): represents by what the fields will be obfuscated
        message (str): the log line
        separator (str): the character separating all fields in the message
    """
    pattern_funcs = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x)
}

    extract = pattern_funcs['extract']
    replace = pattern_funcs['replace']
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """
    this function returns a logging.Logger object when called
    """
    logger = logging.getLogger("user_data")
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.addHandler(streamHandler)
    logger.propagate = False
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    returns a mysql.connector.connection.MySQLConnection object
    """
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_psswd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    connection = mysql.connector(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_psswd,
        database=db_name
    )
    return connection


def main():
    """
    retrieves all rows in the users table then displays each row 
    """
    filtered_fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = filtered_fields.split(',')
    query = f"SELECT {filtered_fields} FROM users;"
    logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(lambda x: f'{x[0]}={x[1]}', zip(columns, row))
            message = "{};".format(';'.join(list(record)))
            args = ("user_data", logging.INFO, None, None, message, None, None)
            logRecord = logging.LogRecord(*args)
            logger.handle(logRecord) 


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes a new class instance
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        filters values in the incoming log records"""
        message = super(RedactingFormatter, self).format(record)
        result = filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR)
        return result
    
    
    if __name__ == '__main__':
        main()
