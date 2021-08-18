from os import execl

from texera import texera

import asyncio, sys
from texera.cmdhelp import CmdHelp

from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command(['kapat'], ['!','.','/']) & filters.me)
async def shutdown(client:Client, message:Message):


    await message.edit("Hoşça Kal!")
    await asyncio.sleep(1.5)
    await message.edit("Bot kapatıldı.")
    try:
        await texera.disconnect()
        await texera.stop()
    except:
        pass
    return

@Client.on_message(filters.command(['restart'], ['!','.','/']) & filters.me)
async def restart(client:Client, message:Message):

    await message.edit("Yeniden Başlatılıyor...")
    try:
        await texera.stop()
    except:
        pass
    execl(sys.executable, sys.executable, *sys.argv)
    return

CmdHelp("misc").add_command("kapat", None, "Botu kapatır.").add_command("restart", None, "Botu yeniden başlatır.")