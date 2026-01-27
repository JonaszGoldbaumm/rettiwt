from sqlalchemy import Text, LargeBinary, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional
from app.db.base import Base


class Post(Base):
    """
    Class representing DB Post table.
    Posts with optional photos. Autogenerates timestamp at creation.
    Contains Mappings for its comments and the author foreign key relationships.
    """
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    media: Mapped[Optional[bytes]] = mapped_column(LargeBinary)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, name="id_user")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="posts")  # type: ignore # noqa: F821
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")  # type: ignore # noqa: F821