from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import UserLogin, UserRegister
from app.services import auth_service

router = APIRouter()


@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    """
    Registration endpoint
    
    :param user: Registration request object
    :type user: UserRegister
    :param db: Database session
    :type db: Session
    """
    try:
        u = auth_service.register_user(db, user.username, user.email, user.password)
        return {"id": u.id, "username": u.username}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    """
    Login endpoint
    
    :param data: Login request object
    :type data: UserLogin
    :param db: Database session
    :type db: Session
    """
    token_data = auth_service.authenticate_user(db, data.username_or_email, data.password)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token_data