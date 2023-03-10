from sqlalchemy import Column, Integer, VARCHAR, DATE, Identity, BigInteger  # type: ignore
from sqlalchemy.orm import sessionmaker, relationship, selectinload  # type: ignore
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    #Task number
    number = Column('number', VARCHAR(50), unique=False, nullable=False, primary_key=True)
    #Task title
    title = Column('title', VARCHAR(100), unique=False, nullable=False)
    #Task theme
    theme = Column('theme', VARCHAR(300), unique=False, nullable=False)
    #Task difficulty
    diff = Column('diff', Integer, unique=False, nullable=False)
    #Solved
    solved = Column('solved', VARCHAR(100), unique=False, nullable=False)
    #Tasks links
    link = Column('link', VARCHAR(100), unique=False, nullable=False)

    def __repr__(self):
        return "".format(self.code)

