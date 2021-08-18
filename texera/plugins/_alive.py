
from texera.cmdhelp import CmdHelp
from pyrogram import Client, filters
from pyrogram.types import Message
from random import choice
    
ALIVE_MESSAGES = ["Emirlerine hazırım sahibim. 👑","__Her zamanki gibi çalışıyorum.__ ⚡️","**Texera UserBot** 🔨"]
@Client.on_message(filters.command(['alive'], ['!','.','/']) & filters.me)
async def komut(client:Client, message:Message):

    await message.edit(choice(ALIVE_MESSAGES))
CmdHelp("alive").add_command("alive", None, "Botun çalışıp çalışmadığını kontrol eder.").add()