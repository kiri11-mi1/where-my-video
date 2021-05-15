from app.models import Base, Chat, Channel
from app.config import DATABASE_FILE

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBApi:
    def __init__(self, db_filename):
        engine = create_engine(f'sqlite:///{db_filename}')
        Base.metadata.create_all(engine)
        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)
        self.session = Session()
    

    def get_channel(self, id:str, chat_id: str):
        return self.session.query(Channel)\
                              .filter_by(chat_id=chat_id, id=id)\
                              .first()


    def create_channel(self, id:str, chat_id: str, last_video_id: str):
        channel = Channel(
            id=id,
            chat_id=chat_id,
            last_video_id=last_video_id
        )
        self.session.add(channel)
        self.session.commit()
        return channel


    def get_or_create_chat(self, chat_id: str):
        chat = self.session.query(Chat).get(chat_id)
        if chat:
            return chat
        chat = Chat(id=chat_id)
        self.session.add(chat)
        self.session.commit()
        return chat


    def create_new_chat(id: str):
        chat = Chat(id=id)
        session.add(chat)
        session.commit()


    def create_new_channel(id: str, chat: object):
        channel = Channel(id=id, chat_id=chat.id)
        session.add(channel)
        session.commit()



if __name__ == '__main__':
    db = DBApi(DATABASE_FILE)
    db.get_or_create_chat('545454')
    db.get_or_create_chat('787878')
    # channel = Channel(id = '15748', chat_id='545454', last_video_id='717171')
    # db.session.add(channel)
    # db.session.commit()
    # channel = Channel(id = '44745', chat_id='545454', last_video_id='121212')
    # db.session.add(channel)
    # db.session.commit()
    result = db.session.query(Channel).filter_by(chat_id='545454', id='15748').first()
    print(result)