from message_template import kaikei_confirm_message
from models import PaymentInfo, Group, User
import db

async def kaikei_hundler(line_api, event):
    warikan_member_id_list = []
    total_payment = 0

    line_user_id = event.source.user_id
    line_group_id = event.source.group_id
    mentionees = event.message.mention.mentionees

    warikan_member_id_list.append(line_user_id)
    for mentioonee in mentionees:
        warikan_member_id_list.append(mentioonee.user_id)

    group = db.session.query(Group).filter(Group.line_group_id==line_group_id).first()
    # このグループの合計支払金額は○○円です。
    payment_infos = db.session.query(PaymentInfo).filter(PaymentInfo.group_id==group.id).all()
    for payment_info in payment_infos:
        total_payment += payment_info.payment 

    warikan_users = db.session.query(User).filter(User.line_user_id.in_(warikan_member_id_list)).all()

    await line_api.reply_message_async(event.reply_token, kaikei_confirm_message(total_payment, warikan_users))

    # メンション指定
    # メンションからメンバーIDを取得
    # get_group_member_profileメソッドでユーザーレコードget_or_create
    # メンバーとpaymentレコード情報を元に精算を行う

    # 精算情報をグループに送信する。




    # profile = line_api.get_group_member_profile(line_group_id, line_user_id)