from tokenize import group
from fastapi import FastAPI, Request, BackgroundTasks
from linebot import WebhookParser
from linebot.models import TextMessage
from aiolinebot import AioLineBotApi


# APIクライアントとパーサーをインスタンス化
line_api = AioLineBotApi(channel_access_token="fiB0OtMSnuig6C16lTCLOTOGa6E9FsALfDtN5vgQ2nb7+ok5TMLTu5kmThngNoryoIoPvHbH1dgzKL5LMLtcuD+lXdCPOGswQA1IsK3a2JVO3Jqp4OYTdqABBPyBmHgDK/m4xTxPZRBABNwMvcrG+gdB04t89/1O/w1cDnyilFU=")
parser = WebhookParser(channel_secret="7c1699bff03feb2bc7b06750304eea92")

app = FastAPI()

@app.post("/callback")
async def handle_request(request: Request, background_tasks: BackgroundTasks):
    events = parser.parse((await request.body()).decode("utf-8"), request.headers.get("X-Line-Signature", ""))
    background_tasks.add_task(handle_events, events=events)

    return "ok"

async def handle_events(events):
    group_id = "C029695106bd4f5ec16b8b2aae20d8292"
    member_ids_res = line_api.get_group_member_ids(group_id)

    print(member_ids_res.member_ids)
    print(member_ids_res.next)


    for ev in events:
        print(ev)
        try:
            await line_api.reply_message_async(
                ev.reply_token,
                TextMessage(text=f"You said: {ev.message.text}"))
        except Exception:
            pass
