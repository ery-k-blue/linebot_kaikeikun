import db
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .user_group import user_group


class Group(db.Base):
    """
    Groupテーブル

    id       : 主キー
    line_group_id : line group id
    users   : 所属しているユーザー
    """
    __tablename__ = 'group'
    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    line_group_id = Column(String(256))

    user = relationship("User", secondary=user_group, back_populates="group")

    def get_or_create(line_group_id):
        group = db.session.query(Group).filter(Group.line_group_id==line_group_id).first()
        if not group:
            group = Group(line_group_id=line_group_id)
            db.session.add(group)
            # HACK: なぜかグループが作成された時のidがとれない
            db.session.commit()

        return group
