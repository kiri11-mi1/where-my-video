from config import DATABASE_FILE
from models import Base, Chat, Channel

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(f'sqlite:///{DATABASE_FILE}')
Base.metadata.create_all(engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()


def create_new_chat(id: str):
    chat = Chat(id=id)
    session.add(chat)
    session.commit()


def create_new_channel(id: str, chat: object):
    channel = Channel(id=id, chat_id=chat.id)
    session.add(channel)
    session.commit()



chat = session.query(Chat).first()
print(chat)


create_new_channel(id='48446ssddcdas56', chat=chat)

for c in session.query(Channel).all():
    print(c)