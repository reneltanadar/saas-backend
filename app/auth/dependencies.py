from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth.jwt import decode_access_token

bearer_scheme=HTTPBearer()

def get_current_user(
        credentials:HTTPAuthorizationCredentials=Depends(bearer_scheme),
        db:Session=Depends(get_db),
)->User:
    credential_exceptions= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials",
                                         headers={"WWW-Authenticate":"Bearer"},
                                         )
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise credential_exceptions
    
    user_id=payload.get("sub")
    if user_id is None:
        raise credential_exceptions
    
    user=db.query(User).filter(User.id==int(user_id)).first()
    if user is None:
        raise HTTPException
    return user