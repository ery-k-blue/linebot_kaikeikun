from linebot.models import ButtonsTemplate, PostbackAction, TemplateSendMessage, TextSendMessage


def confirm_input_message(username, payment_info):
    confirm_input_message = TemplateSendMessage(
        alt_text='確認',
        template=ButtonsTemplate(
            title='確認画面',
            text=f'{username}さんが{payment_info.payment}円支払いました',
            actions=[
                PostbackAction(
                    label='入力を取り消す',
                    display_text='入力を取り消す',
                    data=f'delete_payment_info_record:{payment_info.id}'
                ),
            ]
        )
    )

    return confirm_input_message

def cancel_input_message(cancel_user, payment_user, payment):
    cancel_input_message = TextSendMessage(text=f'{cancel_user}さんが以下の支払情報を削除しました。\n「{payment_user}さんの{payment}円の支払い」')

    return cancel_input_message

def kaikei_confirm_message(total_payment, warikan_users):
    warikan_user_names = []
    warikan_user_ids = []
    for warikan_user in warikan_users:
        warikan_user_names.append(warikan_user.username)
        print("warikan_user.id:{}".format(warikan_user.id))
        warikan_user_ids.append(str(warikan_user.id))

    kaikei_confirm_message = TemplateSendMessage(
        alt_text='会計確認画面',
        template=ButtonsTemplate(
            title='会計確認画面',
            text=f'合計金額：{total_payment}\n割り勘を行うメンバー:{"、".join(warikan_user_names)}',
            actions=[
                PostbackAction(
                    label='会計を行う',
                    display_text='会計を行う',
                    data=f'act_kaikei:{",".join(warikan_user_ids)}'
                ),
                PostbackAction(
                    label='会計を止める',
                    display_text='まだ、他にも入力を行う',
                    data='cancel_kaikei'
                ),
            ]
        )
    )

    return kaikei_confirm_message

def kaikeikun_menu_message():
    kaikeikun_menu_message = TemplateSendMessage(
        alt_text='会計君menu',
        template=ButtonsTemplate(
            title='会計君menu',
            text='操作を選択してください！',
            actions=[
                PostbackAction(
                    label='会計を行う',
                    display_text='会計を行う',
                    data=f'start_accounting:'
                ),
                PostbackAction(
                    label='使い方を見る',
                    display_text='使い方を見る',
                    data='send_help_message:'
                ),
            ]
        )
    )

    return kaikeikun_menu_message
