from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import auth_service

router = APIRouter()

@router.post("/register")
def register(username:str, email:str, password:str, db:Session = Depends(get_db)):
    try:
        user = auth_service.register_user(db, username, email, password)
        return {"id": user.id, "username": user.username}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login")
def login(username_or_email:str, password:str, db:Session = Depends(get_db)):
    token_data = auth_service.authenticate_user(db, username_or_email, password)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token_data