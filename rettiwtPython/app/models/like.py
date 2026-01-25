from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base

class Like(Base):
    __tablename__ = "likes"

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), primary_key=True, name="id_post")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True, name="id_user")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    post: Mapped["Post"] = relationship()  # type: ignore # noqa: F821
    user: Mapped["User"] = relationship()  # type: ignore # noqa: F821
