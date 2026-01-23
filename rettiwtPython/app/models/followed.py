from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.schema import PrimaryKeyConstraint
from datetime import datetime
from app.db.base import Base

class Followed(Base):
    __tablename__ = "followed"

    user_id = Column(Integer, ForeignKey("users.id"))
    by_user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "by_user_id"),
    )

    user = relationship("User", foreign_keys=[user_id])
    followed_by = relationship("User", foreign_keys=[by_user_id])