from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_token
from app.repositories import user_repo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    payload= decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(payload["sub"])
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

