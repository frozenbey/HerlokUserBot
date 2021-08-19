import os
import time
from texera import BOT_VER
from random import choice
from texera import StartTime
from texera.cmdhelp import CmdHelp
from pyrogram import Client, filters
from pyrogram.types import Message

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = [" Saniye", " Dakika", " Saat", " Gün"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += " ".join(time_list)

    return ping_time    
# ----------------------------------------------------------------------------------
    
    
FOTO = "https://telegra.ph/file/00efe339a87c53f1fe963.jpg"    
ALIVE_MESSAGE = """
⚙️ **TEXERA UserBot** __Sahibi İçin Çalışıyor. __⚙️


✨**Bot Version:**  `{}`
✨**Çalışma Süresi:**  `{}`
✨**Plugin Sayısı:**  `{}`
"""


@Client.on_message(filters.command(['alive'], ['!','.','/']) & filters.me)
async def komut(client:Client, message:Message):
    uptime = get_readable_time((time.time() - StartTime))
    
    tum_eklentiler = []
    for dosya in os.listdir("./texera/plugins/"):
        if not dosya.endswith(".py") or dosya.startswith("_"):
            continue
        tum_eklentiler.append(dosya.replace('.py',''))
    pluginsayi = len(tum_eklentiler)
    
    await message.delete()
    try:
        await client.send_photo(message.chat.id,FOTO,caption=ALIVE_MESSAGE.format(BOT_VER,uptime,pluginsayi))
    except:
        await client.send_message(message.chat.id,ALIVE_MESSAGE.format(BOT_VER,uptime,pluginsayi))
    
    
    
CmdHelp("alive").add_command("alive", None, "Botun çalışıp çalışmadığını kontrol eder.").add()
