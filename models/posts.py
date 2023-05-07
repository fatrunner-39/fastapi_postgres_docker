from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    creator_id = Column(ForeignKey('users.id', ondelete='CASCADE'))
    published = Column(DateTime)

    likes = relationship('Like', lazy='subquery')

    def as_dict(self):
        likes = self.likes
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'creator_id': self.creator_id,
            'published': self.published,
            'likes': len([like for like in likes if like.is_like == True]),
            'dislikes': len([like for like in likes if like.is_like == False])
        }

    def as_dict_extra(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'creator_id': self.creator_id,
            'published': self.published
        }
