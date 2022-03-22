from aiolinebot import AioLineBotApi
from fastapi import BackgroundTasks, FastAPI, Request
from linebot import WebhookParser
from linebot.models import TextSendMessage
import uvicorn

import setting_env
from hundler import message_hundler, postback_hundler
from message_template import cancel_accounting_message, kaikeikun_menu_message
from models.group import Group
from models.user import User

# APIクライアントとパーサーをインスタンス化
line_api = AioLineBotApi(channel_access_token=setting_env.CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(channel_secret=setting_env.CHANNEL_SECRET)

app = FastAPI()

@app.post("/callback")
async def handle_request(request: Request, background_tasks: BackgroundTasks):
    events = parser.parse((await request.body()).decode("utf-8"), request.headers.get("X-Line-Signature", ""))
    background_tasks.add_task(handle_events, events=events)

    return "ok"


async def handle_events(events):
    for ev in events:
        print(ev.type)
        print(ev)

        # eventの情報を取得
        text, postback_data, speaker_line_user_id, line_group_id, mentionees_line_user_info = _get_event_info(ev)  

        print("text:{}".format(text))
        print("postback_data:{}".format(postback_data))
        print("speaker_line_user_id:{}".format(speaker_line_user_id))
        print("line_group_id:{}".format(line_group_id))
        print("mentionees_line_user_info:{}".format(mentionees_line_user_info))

        # 入力が「数字のみ」or「メンション＋数字のみ」or「会計君が含まれている」以外の場合、何もしない
        if not _judg_through_event(ev.type, text, postback_data, mentionees_line_user_info):
            print("___pass")
            return []

        # --- ユーザー・グループを登録 ---
        group = Group.get_or_create(line_group_id)
        profile = line_api.get_group_member_profile(line_group_id, speaker_line_user_id)
        speaker_line_user = User.get_or_create(speaker_line_user_id, profile.display_name, line_group_id)
        mentionee_line_user_list = []
        for user_info in mentionees_line_user_info:
            mentionee_line_user = User.get_or_create(user_info["line_user_id"], user_info["username"], line_group_id)
            mentionee_line_user_list.append(mentionee_line_user)


        # --- 各hundlerへの振り分け ---
        if group.is_accounting:
            if ev.type == "message":
                # メンションのみのメッセージ
                if mentionees_line_user_info and text == "":
                    await message_hundler.selected_warikan_member(line_api, ev.reply_token, group, speaker_line_user, mentionee_line_user_list)
                else:
                    await line_api.reply_message_async(ev.reply_token, cancel_accounting_message(group))
            elif ev.type == "postback":
                if "cancel_accounting" in postback_data:
                    await postback_hundler.canceled_accounting(line_api, ev.reply_token, group)
                    pass
                else:
                    await line_api.reply_message_async(ev.reply_token, cancel_accounting_message(group))

        else:
            if ev.type == "message":
                # 数字のみのメッセージ
                if text.isdigit():
                    if len(mentionees_line_user_info) == 0:
                        await message_hundler.input_payment_info(line_api, ev.reply_token, speaker_line_user, group, text)
                        print("数字のみのメッセージ")
                    elif len(mentionees_line_user_info) == 1:
                        await message_hundler.input_payment_info(line_api, ev.reply_token, mentionee_line_user, group, text)
                        print("メンション＋数字のみのメッセージ")
                    elif len(mentionees_line_user_info) >= 2:
                        print("複数メンション＋数字のみのメッセージ")
                        await line_api.reply_message_async(ev.reply_token, TextSendMessage(text=f"金額を支払った人は1人しか選択できません。"))

                if "会計君" in text:
                    await line_api.reply_message_async(ev.reply_token, kaikeikun_menu_message())
                    print("会計君込みのメッセージ")

            elif ev.type == "postback":
                if "cancel_accounting" in postback_data:
                    await line_api.reply_message_async(ev.reply_token, TextSendMessage(text=f"現在、会計中ではありません。"))

                if "delete_payment_info" in postback_data:
                    await postback_hundler.delete_payment_info(line_api, ev.reply_token, postback_data, speaker_line_user)

                if "start_accounting" in postback_data:
                    await postback_hundler.start_accounting(line_api, ev.reply_token, group)

                if "send_help_message" in postback_data:
                    await line_api.reply_message_async(ev.reply_token, TextSendMessage(text=f"こちらをご確認下さい。\nhttps://github.com/ery-k-blue/linebot_kaikeikun#readme"))

def _get_event_info(ev):
    line_user_id = getattr(ev.source, "user_id", None)
    line_group_id = getattr(ev.source, "group_id", None)

    text = ""
    postback_data = None
    mention = None
    if ev.type == "message":
        text = getattr(ev.message, "text", "")
        mention = getattr(ev.message, "mention", None)
    elif ev.type == "postback":
        postback_data = ev.postback.data

    mentionees_line_user_info = []
    if mention:
        mentionees = mention.mentionees
        
        for mentionee in mentionees:
            mentionee_line_user_id = mentionee.user_id
            profile = line_api.get_group_member_profile(line_group_id, mentionee_line_user_id)
            mentionee_username = profile.display_name
            mentionee_info = {"line_user_id": mentionee_line_user_id, "username": mentionee_username}
            mentionees_line_user_info.append(mentionee_info)

            # メンションをテキストから取り除く　例）「@tanaka 900」→「900」
            text = text.replace("@" + mentionee_username + " ", "")
    
    return text, postback_data, line_user_id, line_group_id, mentionees_line_user_info


def _judg_through_event(event_type, text, postback_data, mentionees_line_user_info):
    if event_type == "message" or event_type == "postback":
        if "会計君" in text:
            return True
        if text.isdigit():
            return True
        if postback_data:
            return True
        if mentionees_line_user_info:
            if text.isdigit() or text == "":
                return True
    return False