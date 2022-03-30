from datetime import datetime

import db
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .user_group import user_group


class Group(db.Base):
    """
    Groupテーブル

    id            : 主キー
    created_at    : レコード作成時刻
    update_at     : レコード更新時刻
    line_group_id : line group id
    users         : 所属しているユーザー
    """
    __tablename__ = 'group'
    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    created_at = Column('created_at', DateTime, default=datetime.now(), nullable=False)
    updated_at = Column('updated_at', DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    line_group_id = Column(String(256))
    # True: 会計処理中  False: 通常時
    is_accounting = Column(Boolean, default=False)

    user = relationship("User", secondary=user_group, back_populates="group")

    def get_or_create(line_group_id):
        group = db.session.query(Group).filter(Group.line_group_id==line_group_id).first()
        if not group:
            group = Group(line_group_id=line_group_id)
            db.session.add(group)
            db.session.commit()
            # db.session.close()
            print('_____create_group_____')

        return group
