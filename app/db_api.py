from app.models import Base, Chat, Channel
from app.config import DATABASE_URL

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBApi:
    def __init__(self):
        engine = create_engine(f'postgresql+psycopg2://{DATABASE_URL}')
        Base.metadata.create_all(engine)
        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)
        self.session = Session()
    

    def get_all_channels(self, chat_id):
        return self.session.query(Channel)\
                              .filter_by(chat_id=chat_id)\
                              .all()


    def get_channel(self, id:str, chat_id: str):
        return self.session.query(Channel)\
                              .filter_by(chat_id=chat_id, channel_id=id)\
                              .first()


    def create_channel(self, id:str, chat_id: str, last_video_id: str):
        channel = Channel(
            channel_id=id,
            chat_id=chat_id,
            last_video_id=last_video_id
        )
        self.session.add(channel)
        self.session.commit()
        return channel


    def delete_channel(self, id:str, chat_id:str):
        channel = self.get_channel(id, chat_id)
        self.session.delete(channel)
        self.session.commit()
        return channel


    def get_or_create_chat(self, chat_id: str):
        chat = self.session.query(Chat).get(str(chat_id))
        if chat:
            return chat
        chat = Chat(id=str(chat_id))
        self.session.add(chat)
        self.session.commit()
        return chat


    def delete_chat(self, chat_id: str):
        chat = self.session.query(Chat).get(str(chat_id))
        self.session.delete(chat)
        self.session.commit()
        return chat


    def get_all_chats(self):
        return self.session.query(Chat).all()


if __name__ == '__main__':
    db = DBApi()
    for chat in db.get_all_chats():
        print(chat)