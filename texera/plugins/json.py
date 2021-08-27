from texera.cmdhelp import CmdHelp
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import MessageTooLong
import os


@Client.on_message(filters.command(['json'], ['!','.','/']) & filters.me)
async def jsn_ver(client:Client, message:Message):
    if message.reply_to_message:
        try:
            await message.edit(f"```{message.reply_to_message}```")
        except MessageTooLong:
            await message.edit("`Mesajın uzunluğu izin verilenden fazla. Dosya olarak gönderiyorum...`")
            text = str(message.reply_to_message)
            with open("json.txt", "w", encoding="utf-8") as dosya:
                dosya.write(text)
            await client.send_document(message.chat.id, "json.txt")
            os.remove("json.txt")
            
    else:
        await message.edit("`Lütfen bir mesajı yanıtlayın`")

CmdHelp("json").add_command("json", "<Yanıtlanan Mesaj>", "Yanıtlanan mesajın ham halini verir.").add()
