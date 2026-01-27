from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.profile import UserProfileOut
from app.schemas.profile_update import DescriptionUpdate, PasswordUpdate, UsernameUpdate
from app.schemas.user import UserSummary
from app.services import profile_service, follow_service
from app.repositories import user_repo, followed_repo
from app.api.deps import get_current_user
from app.models.user import User
from app.core.security import verify_passwd
import imghdr

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/{user_id}", response_model=UserProfileOut)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    """
    Profile information endpoint
    
    :param user_id: Users id
    :type user_id: int
    :param db: Description
    :type db: Session
    """
    try:
        return profile_service.get_user_profile(db, user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/me/profile", response_model=UserSummary)
def user_info(current_user: User = Depends(get_current_user)):
    """
    Basic currently logged users information endpoint
    
    :param current_user: Description
    :type current_user: User
    """
    return {"id":current_user.id, "username":current_user.username}

@router.get("/{user_id}/photo")
def get_profile_photo(user_id:int, db:Session = Depends(get_db)):
    """
    Specific users profile picture endpoint.
    
    :param user_id: Users id
    :type user_id: int
    :param db: Description
    :type db: Session
    """
    user= user_repo.get_by_id(db, user_id)
    if not user or not user.profile_pic:
        raise HTTPException(status_code=404, detail="Profile photo not found")
    
    img_type = imghdr.what(None, h=user.profile_pic)
    if not img_type:
        raise HTTPException(status_code=400, detail="Invalid image data")
    
    return Response(content=user.profile_pic, media_type=f"image/{img_type}")

@router.patch("/me/username")
def change_username(data: UsernameUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Changing currently logged in users username endpoint.
    
    :param data: Request body
    :type data: UsernameUpdate
    :param db: Description
    :type db: Session
    :param current_user: Description
    :type current_user: User
    """
    if user_repo.get_by_username(db, data.new_username):
        raise HTTPException(status_code=409, detail="Username already taken")
    updated = user_repo.update_username(db, current_user.id, data.new_username)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Username updated", "username": updated.username}

@router.patch("/me/password")
def change_password(
    data: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Changing currently logged in users password endpoint
    
    :param data: Request body
    :type data: PasswordUpdate
    :param db: Description
    :type db: Session
    :param current_user: Description
    :type current_user: User
    """
    if not verify_passwd(data.old_password, current_user.password):
        raise HTTPException(status_code=401, detail="Old password is incorrect")

    user_repo.update_password(db, current_user.id, data.new_password)

    return {"message": "Password updated"}

@router.patch("/me/description")
def change_description(data: DescriptionUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Changing currently logged in users description endpoint
    
    :param data: Request body
    :type data: DescriptionUpdate
    :param db: Description
    :type db: Session
    :param current_user: Description
    :type current_user: User
    """
    user_repo.update_description(db, current_user.id, data.description)
    return {"message": "Description updated"}

@router.patch("/me/profile-pic")
async def change_profile_pic(
    pic: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Changing currently logged in users profile picture endpoint
    
    :param pic: Profile picture sent in the for of multipart/form-body
    :type pic: UploadFile | None
    :param db: Description
    :type db: Session
    :param current_user: Description
    """
    pic_bytes: bytes | None = None
    if pic:
        if pic.content_type not in ["image/jpeg", "image/png", "image/webp"]:
            raise HTTPException(status_code=400, detail="Invalid image type")
        pic_bytes = await pic.read()
    
    user_repo.update_profile_pic(db, current_user.id, pic_bytes)
    return {"message": "Profile picture updated"}


@router.get("/{user_id}/followers", response_model=list[UserSummary])
def get_followers(user_id: int, db: Session = Depends(get_db)):
    """
    Followers of specific users endpoint
    
    :param user_id: Users id
    :type user_id: int
    :param db: Description
    :type db: Session
    """
    links = followed_repo.get_followers(db, user_id)
    return [
        {"id": f.followed_by.id, "username": f.followed_by.username}
        for f in links
    ]


@router.get("/{user_id}/followed", response_model=list[UserSummary])
def get_followed(user_id: int, db: Session = Depends(get_db)):
    """
    Specific users followed accounts endpoint
    
    :param user_id: Users id
    :type user_id: int
    :param db: Description
    :type db: Session
    """
    links = followed_repo.get_followed_users(db, user_id)
    return [
        {"id": f.user.id, "username": f.user.username}
        for f in links
    ]



@router.post("/{user_id}/follow")
def toggle_follow(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Follow/unfollow endpoint
    
    :param user_id: Users id
    :type user_id: int
    :param db: Description
    :type db: Session
    :param current_user: Description
    """
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    following = follow_service.toggle_follow_user(db, user_id, current_user.id)
    return {"following": following}

@router.get("/{user_id}/isfollow")
def check_following(
    user_id: int,
    db: Session = Depends(get_db),
    current_user:UserSummary = Depends(get_current_user)
):
    """
    Checking if currently logged in user follows another specific user endpoint
    
    :param user_id: Users id
    :type user_id: int
    :param db: Database session
    :type db: Session
    :param current_user: Authentication
    :type current_user: UserSummary
    """
    if current_user.id == user_id:
        return {"following": False}

    following = follow_service.is_following(db, user_id, current_user.id)
    return {"following": following}