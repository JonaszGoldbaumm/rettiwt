from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base

class Followed(Base):
    """
    Class representing DB Followed table.
    Relationship between the follower and followed.
    Contains mappings for the foreign keys for both the author and the target.
    """
    __tablename__ = "followed"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True, name="id_user")
    by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True, name="by_user")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(foreign_keys=[user_id])  # type: ignore # noqa: F821
    followed_by: Mapped["User"] = relationship(foreign_keys=[by_user_id])  # type: ignore # noqa: F821
