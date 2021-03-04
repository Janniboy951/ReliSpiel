from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

engine = create_engine('sqlite:///ReliSpiel.db')
Base = declarative_base()
Session = sessionmaker(engine)
