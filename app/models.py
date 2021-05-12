from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Chat(Base):
    __tablename__ = 'chat'
    id = Column(String(64), primary_key=True)
    # Посмотреть размер id чатов
    channels = relationship('Channel', backref="chat")


    def __repr__(self):
        return f'<Chat: {self.id}>'


class Channel(Base):
    __tablename__ = 'channel'
    id = Column(String(64), primary_key=True)
    title = Column(String(64))

    videos = relationship('Video', backref="channel")
    chat_id = Column(String(64), ForeignKey('chat.id'))


    def __repr__(self):
        return f'<Channel: {self.id} - {self.title}>'


class Video(Base):
    __tablename__ = 'video'
    id = Column(String(64), primary_key=True)
    url = Column(String)
    datetime = Column(DateTime)
    title = Column(String(128))

    channel_id = Column(String(64), ForeignKey('channel.id'))


    def __repr__(self):
        return f'<Video: {self.title} - {self.datetime}>'
