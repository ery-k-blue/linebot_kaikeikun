from aiolinebot import AioLineBotApi
from fastapi import BackgroundTasks, FastAPI, Request

from hundler import mentioned_message_hundler, message_hundler
from linebot import WebhookParser


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
    for ev in events:
        print(ev.type)
        if ev.type == "join":
            pass
        if ev.type == "leave":
            pass
        if ev.type == "memberJoined":
            pass
        if ev.type == "memberLeft":
            pass
        if ev.type == "message":
            if ev.message.mention:
                await mentioned_message_hundler(line_api, ev)
            else:
                await message_hundler(line_api, ev)


        # await line_api.reply_message_async(ev.reply_token, TextMessage(text=f"You said: {ev.message.text}"))
