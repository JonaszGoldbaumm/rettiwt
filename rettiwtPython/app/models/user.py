from sqlalchemy import String, Text, LargeBinary, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional
from app.db.base import Base

class User(Base):
    """
    Class representing DB User table.
    Users of the application with optional descriptions and profile pictures.
    Contains mapping for the constraint on the post.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    profile_pic: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    posts: Mapped[List["Post"]] = relationship(back_populates="user")  # type: ignore # noqa: F821
