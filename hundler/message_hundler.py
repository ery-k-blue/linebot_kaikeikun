import db
from message_template import confirm_input_message, kaikeikun_menu_message
from models import PaymentInfo


async def input_payment_info(line_api, reply_token, pay_user, group, text):
    # 支払いレコードを作成
    payment = int(text)
    payment_info = PaymentInfo(payment=payment, user_id=pay_user.id, group_id=group.id)
    db.session.add(payment_info)
    db.session.commit()

    # レコードを作成後、確認メッセージの送信
    await line_api.reply_message_async(reply_token, confirm_input_message(pay_user.username, payment_info))


async def send_menu(line_api, reply_token):
    await line_api.reply_message_async(reply_token, kaikeikun_menu_message())
