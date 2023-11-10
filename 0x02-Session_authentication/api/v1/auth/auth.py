#!/usr/bin/env python3
"""has the class that manages the API authentication"""

from flask import request
from typing import List, TypeVar
import re
import os


class Auth:
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        if path and excluded_paths:
            for excluded_path in map(lambda x: x.strip(), excluded_paths):
                if excluded_path[-1]  == '*':
                    pattern = f'{excluded_path[0:-1]}.*'
                elif excluded_path[-1] == '/':
                    pattern = f'{excluded_path[0:-1]}/*'
                else:
                    pattern = f'{excluded_path[0:-1]}/*'
                
                if re.match(pattern, path):
                    return False
        return True
    
    def authorization_header(self, request=None) -> str:
        """
        returns the authorization header
        """
        if request:
            return request.headers.get('Authorization', None)
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns the current user
        """
        return None
    
    def session_cookie(self, request=None):
        """
        returns the session name in the request header
        """
        if request is not None:
            cookie = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie)
