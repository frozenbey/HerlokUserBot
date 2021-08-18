
from texera.cmdhelp import CmdHelp

from time import time
import speedtest
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command(['stest'], ['!','.','/']) & filters.me)
async def stest(client:Client, message:Message):
    await message.edit("`Hız testi başlıyor\nLütfen bekleyin...`")
    basla = time()
    a = speedtest.Speedtest()
    a.get_best_server()
    a.download()
    a.upload()
    bitis = time()
    ping = round(bitis - basla, 2)
    b = a.results.share()
    await client.send_photo(message.chat.id,b,caption="**Speedtest** {} saniye içinde tamamlandı.".format(ping))
    await message.delete()

CmdHelp("speedtest").add_command("stest", None, "Botunuzun download ve upload hızını ölçer.").add()