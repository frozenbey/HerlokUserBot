
from texera.cmdhelp import CmdHelp

from texera import TEMP_AYAR, idm

from pyrogram import Client, filters
from pyrogram.types import Message


YANITLANAN = []
COUNT_PRIV = 0
COUNT_GRUP = 0

@Client.on_message(filters.command(['afk'], ['!','.','/']) & filters.me)
async def afk(client:Client, message:Message):

    girilen_yazi = message.text
    sebep=girilen_yazi[+5:]

    TEMP_AYAR["AFK"] = f"1{sebep}"

    msg = "**Artık AFK'yım!**"
    if sebep != "":
        await message.edit(msg + f"\n`Sebep:` {sebep}")
    else:
        await message.edit(msg)

@Client.on_message(filters.incoming & ~filters.bot & ~filters.private)
async def on_tag(client:Client, message:Message):
    global YANITLANAN
    global COUNT_GRUP
    
    msg = "Şu an AFK'yım!"
    mentioned = message.mentioned
    rep_m = message.reply_to_message

    me = idm
    
    if mentioned or rep_m and rep_m.from_user and rep_m.from_user.id == me:
        COUNT_GRUP += 1
        if message.from_user.id in YANITLANAN:
            pass
        else:
            YANITLANAN.append(message.from_user.id)
            if TEMP_AYAR["AFK"] != "0":
                if TEMP_AYAR["AFK"][+1:] == '':
                    await message.reply(msg)
                else:
                    await message.reply(msg + f"\n`Sebep:` {TEMP_AYAR['AFK'][+1:]}")

@Client.on_message(filters.incoming & ~filters.bot & filters.private)
async def on_pm(client:Client, message:Message):
    global COUNT_PRIV
    
    msg = "**Şu an AFK'yım!**"
    if TEMP_AYAR["AFK"] != "0":
        COUNT_PRIV += 1
        if TEMP_AYAR["AFK"][+1:] == '':
            await message.reply(msg)
        else:
            await message.reply(msg + f"\n`Sebep:` {TEMP_AYAR['AFK'][+1:]}`")

@Client.on_message(filters.command(['unafk'], ['!','.','/']) & filters.me)
async def unafk(client:Client, message:Message):
    global YANITLANAN
    global COUNT_GRUP
    global COUNT_PRIV
    
    YANITLANAN = []
    
    if TEMP_AYAR["AFK"] != "0":
        await message.delete()
        await client.send_message(message.chat.id, f"**Artık AFK değilim!**\n\n**Afk iken:**\n__{COUNT_PRIV} Özel Mesaj\n{COUNT_GRUP} Grup Etiketi Aldınız.__")
        COUNT_GRUP = 0
        COUNT_PRIV = 0
        TEMP_AYAR["AFK"] = "0"
    else:
        await message.delete()
        

    
CmdHelp("afk").add_command("afk", "<İsteğe bağlı sebep>", "AFK olduğunuzu belirtir.", "afk uyuyor").add_command("unafk", None, "AFK modunu kapatır.").add()
