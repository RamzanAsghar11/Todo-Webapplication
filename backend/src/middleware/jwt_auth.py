"""JWT authentication middleware for FastAPI."""
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from typing import Dict

security = HTTPBearer()

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"


def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, str]:
    """
    Verify JWT token and return decoded payload.

    Raises:
        HTTPException: If token is invalid, expired, or missing.

    Returns:
        Dict containing user_id (sub) and email from token payload.
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email")
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )


def verify_user_access(user_id: str, current_user: Dict[str, str] = Depends(verify_jwt)) -> str:
    """
    Verify that the authenticated user matches the requested user_id.

    Args:
        user_id: The user_id from the URL path
        current_user: The authenticated user from JWT token

    Raises:
        HTTPException: If user_id doesn't match authenticated user.

    Returns:
        The authenticated user_id.
    """
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return current_user["user_id"]
