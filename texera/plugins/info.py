

from texera import TEMP_AYAR
from texera.cmdhelp import CmdHelp

from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command(['info'], ['!','.','/']) & filters.me)
async def hakkbilgi(client:Client, message:Message):
    
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
    await message.edit(MESAJ,disable_web_page_preview=True)

CmdHelp("info").add_command("info", None, "Botun sahipleri, geliştiriciler ve USERBOT kanalları hakkında bilgi verir.").add()
