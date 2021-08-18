from texera.cmdhelp import CmdHelp
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command(['json'], ['!','.','/']) & filters.me)
async def jsn_ver(client:Client, message:Message):
    if message.reply_to_message:
        await message.edit(f"```{message.reply_to_message}```")
    else:
        await message.edit("`Lütfen bir mesajı yanıtlayın`")

CmdHelp("json").add_command("json", "<Yanıtlanan Mesaj>", "Yanıtlanan mesajın ham halini verir.").add()