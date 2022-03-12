import db
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from models.group import Group

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

    def get_or_create(line_user_id, username, line_group_id):
        user = db.session.query(User).filter(User.line_user_id==line_user_id).first()
        if not user:
            print("_____create_user_____")
            user = User(username=username, line_user_id=line_user_id)
            db.session.add(user)
        group = db.session.query(Group).filter(Group.line_group_id==line_group_id).first()
        group.user += [user]
        db.session.add(group)
        db.session.commit()
        print("_____connect_group_user_____")
        return user
