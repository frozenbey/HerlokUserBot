from texera.cmdhelp import CmdHelp
from pyrogram import Client, filters
from pyrogram.types import  Message
import asyncio
from pyrogram.errors import YouBlockedUser

@Client.on_message(filters.command("byap", ['!','.','/']) & filters.me)
async def  botyap(client:Client, message:Message):
    bot_botu = "@BotFather"
    msg = message.text
    msgsplit = msg.split(" ", 2)
    try:
        cmd1 = msgsplit[1]
        cmd2 = msgsplit[2]
        await message.delete()
    except:
        return
    if cmd1 == "" or cmd2 == "":
        await client.send_message(message.chat.id,"Bilgileri eksik girdiniz tekrar deneyin.")
    try:
        await client.send_message(text="/newbot",chat_id=bot_botu)
        mejas = await client.get_history(chat_id=bot_botu)
        if mejas == """That I cannot do.

You come to me asking for more than 20 bots. But you don't ask with respect. You don't offer friendship. You don't even think to call me Botfather.""":
            await client.send_message(message.chat.id,"Çok fazla botunuz olduğu için bot silmeniz gerekiyor.")
        await asyncio.sleep(1)
        await client.send_message(text=cmd1,chat_id=bot_botu)
        await asyncio.sleep(1)
        await client.send_message(text=cmd2,chat_id=bot_botu)
        mesaj = await client.get_history(chat_id=bot_botu,limit=1)
        if mesaj == "Sorry, the username must end in 'bot'. E.g. 'Tetris_bot' or 'Tetrisbot'":
            await client.send_message(message.chat.id,"Username bot ile bitmeil örneğin TexeraUserBot")
        if mesaj == "Sorry, this username is already taken. Please try something different.":
            await message.edit("Bu username daha önce alınmış lütfen başka bir tane deneyin.")
        await client.send_message("İşlem bitti:\nBotunuzun ismi:{cmd1}\nBotunuzun usernamesi:{cmd2}")
    except YouBlockedUser:
        await client.unblock_user(user_id=bot_botu)
        await message.edit("@BotFather engeli açıldı yeni bot oluşturuluyor...")
        await client.send_message(text="/newbot",chat_id=bot_botu)
        mejas = await client.get_history(chat_id=bot_botu)
        if mejas == """That I cannot do.

You come to me asking for more than 20 bots. But you don't ask with respect. You don't offer friendship. You don't even think to call me Botfather.""":
            await message.edit("Çok fazla botunuz olduğu için bot silmeniz gerekiyor.")
        await asyncio.sleep(1)
        await client.send_message(text=cmd1,chat_id=bot_botu)
        await asyncio.sleep(1)
        await client.send_message(text=cmd2,chat_id=bot_botu)
        mesaj = await client.get_history(chat_id=bot_botu,limit=1)
        if mesaj == "Sorry, this username is invalid.":
            await client.send_message(message.chat.id,"Username bot ile bitmeli örneğin TexeraUserBot")
        if mesaj == "Sorry, this username is already taken. Please try something different.":
            await client.send_message(message.chat.id,"Bu username daha önce alınmış lütfen başka bir tane deneyin.")
        await client.send_message(message.chat.id,"İşlem bitti:\nBotunuzun ismi:{cmd1}\nBotunuzun usernamesi:{cmd2}")
CmdHelp("botyap").add_command("byap", "<bot ismi> <bot usernamesi>", "@BotFather ile yeni bot oluşturur.Bot usernamesi bot ile bitmeli.", "byap texera texerauserbot").add()