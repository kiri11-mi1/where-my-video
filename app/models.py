from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Chat(Base):
    __tablename__ = 'chat'
    id = Column(String(64), primary_key=True)
    channels = relationship('Channel', backref="chat")

    def __repr__(self):
        return f'<Chat: {self.id}>'


class Channel(Base):
    __tablename__ = 'channel'
    id = Column(Integer, primary_key=True)
    channel_id = Column(String(64))
    last_video_id = Column(String(64))
    chat_id = Column(String(64), ForeignKey('chat.id'))

    def __repr__(self):
        return f'<Channel: {self.id}>'
