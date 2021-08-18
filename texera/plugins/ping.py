from pyrogram import Client, filters
from pyrogram.types import Message
import datetime
from texera.cmdhelp import CmdHelp


@Client.on_message(filters.command(['ping'], ['!','.','/']) & filters.me)
async def ping(client:Client, message:Message):

    #------------------------------------------------------------- Başlangıç >

    basla = datetime.datetime.now()

    mesaj = "__Pong!__"

    bitir = datetime.datetime.now()
    sure = (bitir - basla).microseconds
    mesaj += f"\n\n**Tepki Süresi :** `{sure} ms`"

    await message.edit(mesaj)


CmdHelp("ping").add_command("ping", None, "Ping atar.").add()
