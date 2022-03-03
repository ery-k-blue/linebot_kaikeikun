from aiolinebot import AioLineBotApi
from fastapi import BackgroundTasks, FastAPI, Request

import setting_env
from hundler import mentioned_message_hundler, kaikei_hundler, create_payment_info_hundler
from linebot import WebhookParser

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
                if "会計君" in ev.message.text:
                    await kaikei_hundler(line_api, ev)
                else:
                    await create_payment_info_hundler(line_api, ev)


        # await line_api.reply_message_async(ev.reply_token, TextMessage(text=f"You said: {ev.message.text}"))
