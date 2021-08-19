import time
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
    
    
ALIVE_MESSAGES = ["Emirlerine hazırım sahibim. 👑","__Her zamanki gibi çalışıyorum.__ ⚡️","**Texera UserBot** 🔨"]
@Client.on_message(filters.command(['alive'], ['!','.','/']) & filters.me)
async def komut(client:Client, message:Message):
    uptime = get_readable_time((time.time() - StartTime))

    await message.edit(str(uptime))
    
    
CmdHelp("alive").add_command("alive", None, "Botun çalışıp çalışmadığını kontrol eder.").add()
