from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask import g

load_dotenv()

# connect to database using env variable
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def init_db(app):
  Base.metadata.create_all(engine)
  # Tell flask to run close_db() whenever a context is destroyed
  app.teardown_appcontext(close_db)

# return a new session-connection object
def get_db():
  if 'db' not in g:
    # store db connection in app context
    g.db = Session()
  return g.db

def close_db(e=None):
  # find and remove db from the g object
  db = g.pop('db', None)
  # if db exists then close the connection
  if db is not None:
    db.close()