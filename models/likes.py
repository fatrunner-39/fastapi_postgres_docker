from sqlalchemy import Boolean, Column, ForeignKey, Integer

from db import Base


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id', ondelete='CASCADE'))
    post_id = Column(ForeignKey('posts.id', ondelete='CASCADE'))
    is_like = Column(Boolean, nullable=True)

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'is_like': self.is_like
        }
