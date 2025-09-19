"""
Simple Authentication API
Login and logout endpoints with dummy user data
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
from fastapi import HTTPException, status
import secrets

# Dummy user database
DUMMY_USERS = {
    "admin": {
        "id": 1,
        "username": "admin",
        "password": "admin123",  # In real apps, this would be hashed
        "email": "admin@example.com",
        "full_name": "Admin User"
    },
    "user": {
        "id": 2,
        "username": "user",
        "password": "user123",
        "email": "user@example.com",
        "full_name": "Regular User"
    },
    "demo": {
        "id": 3,
        "username": "demo",
        "password": "demo123",
        "email": "demo@example.com",
        "full_name": "Demo User"
    }
}

# Active sessions storage (in real apps, use Redis or database)
ACTIVE_SESSIONS: Dict[str, Dict] = {}


def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """
    Authenticate user with username and password

    Args:
        username: User's username
        password: User's password

    Returns:
        User data if authentication successful, None otherwise
    """
    user = DUMMY_USERS.get(username)
    if user and user["password"] == password:
        return user
    return None


def create_session(user_data: Dict) -> str:
    """
    Create a new session for authenticated user

    Args:
        user_data: User information

    Returns:
        Session token
    """
    # Generate random session token
    session_token = secrets.token_urlsafe(32)

    # Store session data
    ACTIVE_SESSIONS[session_token] = {
        "user_id": user_data["id"],
        "username": user_data["username"],
        "email": user_data["email"],
        "full_name": user_data["full_name"],
        "login_time": datetime.now(),
        "expires_at": datetime.now() + timedelta(hours=24)
    }

    return session_token


def get_session(session_token: str) -> Optional[Dict]:
    """
    Get session data by token

    Args:
        session_token: Session token

    Returns:
        Session data if valid, None otherwise
    """
    session = ACTIVE_SESSIONS.get(session_token)
    if not session:
        return None

    # Check if session expired
    if datetime.now() > session["expires_at"]:
        # Remove expired session
        del ACTIVE_SESSIONS[session_token]
        return None

    return session


def revoke_session(session_token: str) -> bool:
    """
    Revoke/logout a session

    Args:
        session_token: Session token to revoke

    Returns:
        True if session was revoked, False if not found
    """
    if session_token in ACTIVE_SESSIONS:
        del ACTIVE_SESSIONS[session_token]
        return True
    return False


def get_active_sessions_count() -> int:
    """Get count of active sessions"""
    # Clean expired sessions first
    current_time = datetime.now()
    expired_tokens = [
        token for token, session in ACTIVE_SESSIONS.items()
        if current_time > session["expires_at"]
    ]

    for token in expired_tokens:
        del ACTIVE_SESSIONS[token]

    return len(ACTIVE_SESSIONS)


def verify_session_token(token: str) -> Dict:
    """
    Verify session token and return user data

    Args:
        token: Session token to verify

    Returns:
        User session data

    Raises:
        HTTPException: If token is invalid or expired
    """
    session = get_session(token)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return session