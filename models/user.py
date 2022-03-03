from db import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .user_group import user_group


class User(Base):
    """
    Userテーブル

    id       : 主キー
    username : ユーザネーム
    line_user_d   : ユーザーID

    group: 所属しているグループ
    """
    __tablename__ = 'user'
    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    username = Column(String(256))
    line_user_id = Column(String(256))

    group = relationship("Group", secondary=user_group, back_populates="user")
