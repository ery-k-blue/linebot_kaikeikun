from db import Base
from sqlalchemy import Column, ForeignKey, Table

user_group = Table('user_group', Base.metadata, 
                    Column('user_id', ForeignKey('user.id'), primary_key=True),
                    Column('group_id', ForeignKey('group.id'), primary_key=True),
                )