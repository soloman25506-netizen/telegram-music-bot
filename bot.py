import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

app = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call = PyTgCalls(app)


@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "🎵 Music Bot Online!\n\n"
        "Voice Chat ထဲမှာ music ဖွင့်ဖို့ /play ကိုသုံးပါ။"
    )


@app.on_message(filters.command("help"))
async def help_command(client, message):
    await message.reply_text(
        "🎵 Music Bot Commands\n\n"
        "/play - သီချင်းဖွင့်ရန်\n"
        "/pause - ခဏရပ်ရန်\n"
        "/resume - ပြန်ဖွင့်ရန်\n"
        "/skip - နောက်သီချင်း\n"
        "/stop - Music ရပ်ရန်"
    )


print("🤖 Music Bot Starting...")

app.start()
call.start()

print("🎵 Music Bot Started!")

from pyrogram import idle
idle()

call.stop()
app.stop()
