from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker


try:
    db_string=create_engine('sqlite:///database.db')
    Session=sessionmaker(bind=db_string)
    base = declarative_base()
except Exception as err:
    raise Exception(err)

