#!/usr/bin/en python3
"""implements the BasicAuth class"""

from api.v1.auth.auth import Auth
import base64
import binascii
import re
from typing import TypeVar
from models.user import User

class BasicAuth(Auth):
    """An implementation of basic authorization"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        returns a Base64 part of the authorization header for a
        basic authentication
        Args:
            authorization_header (str): the value to encode
        """
        if authorization_header:
            if type(authorization_header ) == str:
                if authorization_header[0:6] == f'Basic ':
                    return authorization_header[6:-1]
        return None
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        decodes the value of the authorization header
        Args:
            base64_authorization_header (str): a Base64 string
        Returns:
            a decoded string
        """
        if base64_authorization_header:
            if type(base64_authorization_header) == str:
                try:
                    res = base64.b64decode(base64_authorization_header, validate=True)
                    res.decode('utf-8')
                except (binascii.Error, UnicodeDecodeError):
                    return None
        return None
    
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        extracts he user email and password from the base64 decoded value
        """
        if type(decoded_base64_authorization_header) == str:
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            match = re.fullmatch(pattern, decoded_base64_authorization_header.strip())
            if match:
                user = match.group('user')
                passwd =  match.group('password')
                return user, passwd
            return None, None
        
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        finds the user based on the users email and password
        Args:
            user_email (str): email of the user
            user_pwd (str): passwd associated with the user
        Returns:
            the user associated with the email and password
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                user = User.search({'email': user_email})
            except Exception:
                return None
            
            if len(user) <= 0:
                return None
            if user[0].is_valid_password(user_pwd):
                return user[0]
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads the Auth and retrieves a User instance for a request
        Args:
            request (default=None): request for a user
        Returns:
            a User instance
        """
        auth_header = self.authorization_header(request)
        base64_auth = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(base64_auth)
        email, passwd = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, passwd)