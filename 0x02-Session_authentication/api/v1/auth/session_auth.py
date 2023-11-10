#!/usr/bin/env python3
"""Implements the class SessionAuth"""

from .auth import Auth
from uuid import uuid4
from models.user import User

class SessionAuth(Auth):
    """
    an implementation of the class SessionAuth
    """
    user_id_by_session_id = {}
    
    def create_session(self, user_id: str = None) -> str:
        """
        creates a session ID for a user_id
        """
        if user_id is not None and type(user_id) == str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None
        
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a user ID based on a session ID
        """
        if session_id is not None and type(session_id) == str:
            return self.user_id_by_session_id.get(session_id)
    
    def current_user(self, request=None) -> User:
         """"
         that returns a User instance based on a cookie value
         """
         user = self.user_id_for_session_id(self.session_cookie(request))
         return user
     
    def destroy_session(self, request=None):
        """
        destroys an authenticated session
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
    