from datetime import datetime

from db import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship, backref


class PaymentInfo(Base):
    """
    Paymentテーブル

    id        : 主キー
    created_at:レコード作成時刻
    update_at : レコード更新時刻
    payment   : 支払金額
    user      : 支払ったユーザー
    group     : 支払ったグループ

    """
    __tablename__ = 'payment_info'
    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    created_at = Column('created_at', DateTime, default=datetime.now(), nullable=False)
    updated_at = Column('updated_at', DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    payment = Column(INTEGER(unsigned=True))
    is_settled = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    user_id = Column(ForeignKey("user.id"))
    group_id = Column(ForeignKey("group.id"))

    user = relationship("User", backref=backref('payment_info', order_by=id))
    group = relationship("Group", backref=backref('payment_info', order_by=id))
