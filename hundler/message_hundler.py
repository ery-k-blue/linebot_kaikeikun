import db
import pandas as pd
from linebot.models import TextSendMessage
from message_template import confirm_input_message
from models import PaymentInfo, User
from sqlalchemy import func


async def input_payment_info(line_api, reply_token, pay_user, group, text):
    # 支払いレコードを作成
    payment = int(text)
    payment_info = PaymentInfo(payment=payment, user_id=pay_user.id, group_id=group.id)
    db.session.add(payment_info)
    db.session.commit()

    # レコードを作成後、確認メッセージの送信
    await line_api.reply_message_async(reply_token, confirm_input_message(pay_user.username, payment_info))
    

async def selected_warikan_member(line_api, reply_token, group, speaker_line_user, mentionee_line_user_list):
    total_payment = 0
    # 合計金額を計算
    total_payment_by_user = db.session.query(PaymentInfo.user_id, func.sum(PaymentInfo.payment)).filter(
        PaymentInfo.group_id == group.id,
        PaymentInfo.is_deleted == False,
        PaymentInfo.is_settled == False,
        ).group_by(PaymentInfo.user_id).all()

    # 割り勘メンバー一覧表
    df = pd.DataFrame({"UserId": [speaker_line_user.id], "UserName": [speaker_line_user.username], "payment":[0]})
    for _user in mentionee_line_user_list:
        df = df.append({"UserId": _user.id, "UserName": _user.username, "payment":0}, ignore_index=True)
    
    # 支払情報を表に入れる
    for user_id, payment in total_payment_by_user:
        _user = db.session.query(User).filter(User.id==user_id).first()
        df = df.append({"UserId": _user.id, "UserName": _user.username, "payment":payment}, ignore_index=True)
        total_payment += payment
        
    # メンバーでまとめる
    gm_df = df.groupby(["UserId", "UserName"])["payment"].sum().reset_index()

    # 1人あたりの支払い金額を求める
    average_payment = int(total_payment / len(gm_df["UserId"]))
    gm_df["payment"] -= average_payment

    # --- 割り勘メンバーのお金が±0になるまで繰り返す ---
    warikan_info = "--支払情報--\n(払う人→もらう人: 金額)\n\n"
    wi_df = pd.DataFrame(columns=["giver", "taker", "payment"])

    _count = 0
    while(1):
        _count += 1
        # 全員の決済が終わっているかの確認
        _df_bool = (gm_df == 0)
        accounted_user_num = _df_bool["payment"].sum()
        if len(gm_df["UserId"]) == accounted_user_num:
            break
        # 無限ループに入ることがあった時のケア
        if _count >= 999:
            break

        # +が最も大きい人を抽出: もらう人
        take_colm_index = gm_df["payment"].idxmax()
        taker_payment = gm_df.at[take_colm_index, "payment"]
        # -が最も大きい人を抽出: 払う人
        give_colm_index = gm_df["payment"].idxmin()
        giver_payment = gm_df.at[give_colm_index, "payment"]
        
        if giver_payment + taker_payment >= 0:
            gm_df.at[give_colm_index, "payment"] = 0
            gm_df.at[take_colm_index, "payment"] += giver_payment
            wi_df = wi_df.append({"giver": gm_df.at[give_colm_index, "UserName"], "taker": gm_df.at[take_colm_index, "UserName"], "payment":-giver_payment}, ignore_index=True)
        else:
            gm_df.at[give_colm_index, "payment"] = giver_payment + taker_payment
            gm_df.at[take_colm_index, "payment"] = 0
            wi_df = wi_df.append({"giver": gm_df.at[give_colm_index, "UserName"], "taker": gm_df.at[take_colm_index, "UserName"], "payment": taker_payment}, ignore_index=True)

    wi_df = wi_df.sort_values(["giver", "taker"])
    for col in wi_df.itertuples():
        warikan_info += f"{col.giver}→{col.taker}: {col.payment}円\n"

    if warikan_info == "--支払情報--\n(払う人→もらう人: 金額)\n\n" and _count == 1:
        warikan_info = "割り勘を行う必要はありません。\n"
    
    warikan_info += "※\nこれまでの入力情報は削除されます。"
    await line_api.reply_message_async(reply_token, TextSendMessage(warikan_info))

    # 支払情報、グループの状態を会計中から通常に変更
    payment_info = db.session.query(PaymentInfo).filter(
        PaymentInfo.group_id == group.id,
        PaymentInfo.is_deleted == False,
        PaymentInfo.is_settled == False,
        ).all()
    for p in payment_info:
        p.is_settled = True

    group.is_accounting = False
    db.session.add(group)
    db.session.commit()

