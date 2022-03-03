import db
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .user_group import user_group


class User(db.Base):
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

    def get_or_create(line_user_id, username):
        user = db.session.query(User).filter(User.line_user_id==line_user_id).first()
        if not user:
            print("_____create_user_____")
            user = User(username=username, line_user_id=line_user_id)
            db.session.add(user)

        return user
