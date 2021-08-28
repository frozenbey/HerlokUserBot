from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
from texera.cmdhelp import CmdHelp
import asyncio

def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id


@Client.on_message(filters.command("spam", ".") & filters.me)
async def spam(_, message: Message):
    #--> Mesajı Sil
    await message.delete()

    times = message.command[1]
    to_spam = " ".join(message.command[2:])
    
    #--> Grup spammer
    if message.chat.type in ["supergroup", "group"]:
        for _ in range(int(times)):
            await UserBot.send_message(
                message.chat.id, to_spam, reply_to_message_id=ReplyCheck(message)
            )
            await asyncio.sleep(0.20)

    #--> Priv Spammer
    if message.chat.type == "private":
        for _ in range(int(times)):
            await UserBot.send_message(message.chat.id, to_spam)
            await asyncio.sleep(0.20)

            
CmdHelp("spammer").add_command("spam", "<sayı> <spamlanacak yazı>", "Spam yapar.").add_warning("Sorumluluk kabul etmiyoruz!").add()
