import db
from linebot import exceptions
from linebot.models import TextSendMessage
from models import Group, PaymentInfo, User

from .utils import confirm_input


async def create_payment_info_hundler(line_api, event):
    text = event.message.text
    line_user_id = event.source.user_id
    line_group_id = event.source.group_id
    # 入力から「円」or「えん」を取り除く
    if "円" in text:
        text = text.rstrip("円")
    elif "えん" in text:
        text = text.rstrip("えん")
    
    # 入力が正しいかの確認
    try:
        payment = int(text)
    except ValueError:
        await line_api.reply_message_async(event.reply_token, TextSendMessage("「金額のみ。または<金額>+円のみ」を付けて入力してください。\n例）1000、1000円"))
        return []

    # userを取得（作成されていなかったら作成）
    profile = line_api.get_group_member_profile(line_group_id, line_user_id)
    pay_username = profile.display_name
    user = User.get_or_create(line_user_id, pay_username)

    # groupを取得（作成されていなかったら作成）
    group = Group.get_or_create(line_group_id)
    group.user += [user]

    # groupにuserを紐づける（重複は自動でスルーしてくれる）
    db.session.add(group)

    # 支払いレコードを作成
    payment_info = PaymentInfo(payment=payment, user_id=user.id, group_id=group.id)
    db.session.add(payment_info)

    # レコードを作成後、確認メッセージの送信
    await line_api.reply_message_async(event.reply_token, confirm_input(user.username, payment_info.payment))
    db.session.commit()
