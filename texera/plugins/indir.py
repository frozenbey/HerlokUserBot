from texera.cmdhelp import CmdHelp
from pyrogram import Client, filters
from pyrogram.types import Message
from texera.misc._pyrogram.progress import pyro_progress
from texera import INDIRME_ALANI
from time import time
from asyncio import sleep

@Client.on_message(filters.command(['indir'], ['!','.','/']) & filters.me)
async def indir(client:Client, message:Message):

    #------------------------------------------------------------- Başlangıç >

    cevaplanan_mesaj = message.reply_to_message
    if (not cevaplanan_mesaj) or (cevaplanan_mesaj.text):
        await message.edit("`Lütfen indirmek için metin olmayan birşey yanıtlayın`")
        await sleep(3)
        await message.delete()
        return

    try:
        gelen_dosya = await client.download_media(
            message         = cevaplanan_mesaj,
            progress        = pyro_progress,
            file_name       = INDIRME_ALANI,
            progress_args   = ("**__Dosyayı indiriyorum...__**", message, time())
        )
    except Exception as hata:
        print(str(hata))
        return

    dosya = gelen_dosya.split(INDIRME_ALANI)[1]
    
    await message.edit(f"`{dosya}`\n\n__Olarak Kaydettim__")
CmdHelp("indir").add_command("indir", "<Yanıtlanan Mesaj>", "Yanıtlanan mesajı metin **olmaması** halinde indirir.").add()
