from linebot.models import ButtonsTemplate, PostbackAction, TemplateSendMessage


def confirm_input(username, payment):
    confirm_input_message = TemplateSendMessage(
        alt_text='確認',
        template=ButtonsTemplate(
            title='確認画面',
            text=f'{username}さんが{payment}円支払いました',
            actions=[
                PostbackAction(
                    label='入力を取り消す',
                    display_text='入力を取り消す',
                    data='record_id'
                ),
            ]
        )
    )

    return confirm_input_message
