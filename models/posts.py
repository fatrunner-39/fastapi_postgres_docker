from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from db import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    creator_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    published = Column(
        DateTime,
        server_default=func.timezone("UTC", func.current_timestamp()),
    )

    likes = relationship("Like", lazy="subquery")

    @property
    def like(self):
        return len([like for like in self.likes if like.is_like == True])

    @property
    def dislike(self):
        return len([like for like in self.likes if like.is_like == False])
