from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# путь к файлу БД
engine = create_engine("sqlite:///db/artist_bot.db", echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    name = Column(String)
    search = relationship("SearchHistory")


class SearchHistory(Base):
    __tablename__ = 'search'

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('user.id'))
    search = Column(String)
    data = Column(DateTime)

Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
