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

        await line_api.reply_message_async(reply_token, cancel_input_message(cancel_user.username, payment_user.username, payment_info.payment, payment_info.created_at))


async def start_accounting(line_api, reply_token, group):
    group.is_accounting = True
    db.session.add(group)
    db.session.commit()

    await line_api.reply_message_async(reply_token, TextSendMessage(text=f"割り勘を行うメンバーをメンションで選択してください。（入力者は自動で含まれます）"))
    

async def canceled_accounting(line_api, reply_token, group):
    group.is_accounting = False
    db.session.add(group)
    db.session.commit()

    await line_api.reply_message_async(reply_token, TextSendMessage(text=f"会計を中断しました。\n割り勘を行いたいときは再度会計するボタンを押してください。"))