from .utils import confirm_input


async def message_hundler(line_api, event):
    print(event)

    user_id = event.source.user_id
    group_id = event.source.group_id
    message_id = event.message.id
    text = event.message.text

    print(user_id)
    print(group_id)
    print(message_id)
    print(text)

    # userを取得（作成されていなかったら作成）
    pay_username = "yudai"

    # groupを取得（作成されていなかったら作成）

    # 支払いレコードを作成
    # 円、えんで正規表現クリア
    # 数字のみを取り出す。
    # 他の文字が入っている場合はエラーメッセージ
    payment = text

    # レコードを作成後、確認メッセージの送信
    await line_api.reply_message_async(event.reply_token, confirm_input(pay_username, payment))
