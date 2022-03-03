from db import Base
from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.mysql import INTEGER


class PaymentInfo(Base):
    """
    Paymentテーブル

    id       : 主キー
    payment  : 支払金額
    user     : 支払ったユーザー
    group    : 支払ったグループ

    """
    __tablename__ = 'payment_info'
    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    payment = Column(INTEGER(unsigned=True))
    is_settled = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    group_id = Column(Integer, ForeignKey("group.id"))
