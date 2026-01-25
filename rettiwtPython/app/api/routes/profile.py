from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.profile import UserProfileOut
from app.schemas.user import UserSummary
from app.services import profile_service
from app.repositories import user_repo, followed_repo
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/{user_id}", response_model=UserProfileOut)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    try:
        return profile_service.get_user_profile(db, user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")


@router.patch("/me/username")
def change_username(
    new_username: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if user_repo.get_by_username(db, new_username):
        raise HTTPException(status_code=409, detail="Username already taken")

    updated = user_repo.update_username(db, current_user.id, new_username)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Username updated", "username": updated.username}

@router.patch("/me/password")
def change_password(
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_repo.update_password(db, current_user.id, new_password)
    return {"message": "Password updated"}


@router.patch("/me/description")
def change_description(
    description: str | None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_repo.update_description(db, current_user.id, description)
    return {"message": "Description updated"}

@router.patch("/me/profile-pic")
def change_profile_pic(
    pic: bytes | None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_repo.update_profile_pic(db, current_user.id, pic)
    return {"message": "Profile picture updated"}



@router.get("/{user_id}/followers", response_model=list[UserSummary])
def get_followers(user_id: int, db: Session = Depends(get_db)):
    links = followed_repo.get_followers(db, user_id)
    return [
        {"id": f.followed_by.id, "username": f.followed_by.username}
        for f in links
    ]


@router.get("/{user_id}/followed", response_model=list[UserSummary])
def get_followed(user_id: int, db: Session = Depends(get_db)):
    links = followed_repo.get_followed_users(db, user_id)
    return [
        {"id": f.user.id, "username": f.user.username}
        for f in links
    ]

