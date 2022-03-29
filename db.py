from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import setting_env

Base = declarative_base()
print("setting_env.SQLITE3_PATH:{}".format(setting_env.SQLITE3_PATH))
engine = create_engine(setting_env.SQLITE3_PATH, echo=False)
# engine = create_engine(setting_env.RDB_PATH, echo=False)

Session = sessionmaker(bind=engine)
session = Session()