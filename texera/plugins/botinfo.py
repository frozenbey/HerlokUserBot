from texera import SURUM,TEMP_AYAR

from pyrogram import Client, filters,__version__
from pyrogram.types import Message
import os
from texera import BOT_VER
from texera.cmdhelp import CmdHelp
MESAJ = f"""
ㅤㅤㅤ⚒ Texera UserBot ⚒ㅤㅤ
🛠 Sahip: [➽ѕнєяℓοϲκ⟢](https://t.me/sherlock_exe)
⚔️ Geliştiriciler: {TEMP_AYAR['PLUGIN_MSG']['info']['DEVS']}
 
 ┏━━━━━━━━━━━━━━━━━━━━━
 ┣ @TexeraUserBot
 ┣ @TexeraSupport
 ┣ @TexeraSohbet
 ┣ @TexeraPlugin
 ┗━━━━━━━━━━━━━━━━━━━━━
 """

@Client.on_message(filters.command(['boti'], ['!','.','/']) & filters.me)
async def boti(client:Client, message:Message):
    tum_eklentiler = []
    for dosya in os.listdir("./texera/plugins/"):
        if not dosya.endswith(".py") or dosya.startswith("_"):
            continue
        tum_eklentiler.append(dosya.replace('.py',''))
    lama = len(tum_eklentiler)
    acklm = "`Python versiyonu`:  **{}**\n`Pyrogram versiyonu`:  **{}**\n`Bot versiyonu`:  **{}**\n`Eklenti sayınız`:  **{}**\n\n".format(SURUM,__version__,BOT_VER,lama)
    acklm += MESAJ
    await message.edit(acklm)
CmdHelp("botinfo").add_command("boti", None, "Botunuz hakkında bilgi verir.").add()
