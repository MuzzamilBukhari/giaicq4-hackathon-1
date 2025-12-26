from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .security import verify_token
from .crud import get_session_by_token
from sqlalchemy.orm import Session
from ..db.connection import SessionLocal


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme."
                )
            token = credentials.credentials
            if not self.verify_jwt(token, request):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token or expired token."
                )
            return token
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code."
            )

    def verify_jwt(self, token: str, request: Request) -> bool:
        """Verify the JWT token and check if the session is valid."""
        from rag_backend.auth.crud import get_session_by_token
        from rag_backend.db.connection import SessionLocal

        # Verify the token structure and signature
        token_data = verify_token(token)
        if token_data is None:
            return False

        # Check if the session exists in the database
        db: Session = SessionLocal()
        try:
            session = get_session_by_token(db, token)
            return session is not None
        finally:
            db.close()


def get_current_user_id(request: Request) -> str:
    """Extract the current user ID from the request if authenticated."""
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        return None

    token = authorization.split(" ")[1]
    token_data = verify_token(token)
    if token_data:
        return token_data.user_id
    return None