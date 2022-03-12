import db
from linebot.models import TextSendMessage
from message_template import cancel_input_message
from models import PaymentInfo, User


async def delete_payment_info(line_api, reply_token, postback_data, cancel_user):
    _, payment_info_id = postback_data.split(":")
    payment_info = db.session.query(PaymentInfo).filter(PaymentInfo.id==payment_info_id).first()

    if payment_info.is_deleted:
        await line_api.reply_message_async(reply_token, TextSendMessage("この入力は既に削除されています。"))
    else:
        payment_info.is_deleted = True
        db.session.add(payment_info)
        db.session.commit()
        payment_user = db.session.query(User).filter(User.id==payment_info.user_id).first()

        await line_api.reply_message_async(reply_token, cancel_input_message(cancel_user.username, payment_user.username, payment_info.payment))
