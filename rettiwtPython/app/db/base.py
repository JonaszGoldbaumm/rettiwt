from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like
from app.models.followed import Followed