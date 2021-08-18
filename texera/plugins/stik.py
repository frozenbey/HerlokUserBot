from texera.cmdhelp import CmdHelp
from pyrogram import Client, filters
from pyrogram.types import  Message
from texera.misc._pyrogram.pyro_yardimcilari import yanitlanan_mesaj
import asyncio, random

@Client.on_message(filters.command("stik", ['!','.','/']) & filters.me)
async def stik(client:Client, message:Message):

    yanit_id  = await yanitlanan_mesaj(message)
    #------------------------------------------------------------- Başlangıç >
    cevaplanan_mesaj = message.reply_to_message

    if cevaplanan_mesaj is None:
        await message.edit("__sticker yapılacak mesajı yanıtlamalısın..__")
        return

    stik_botu = '@QuotLyBot'
    await cevaplanan_mesaj.forward(stik_botu)
    mesaj = await client.get_history(stik_botu, 1)
    await message.edit("`Sticker yapıyorum`")

    stik_mi = False
    bar = 0
    hata_limit = 0

    while not stik_mi:
        try:
            mesaj = await client.get_history(stik_botu, 1)
            _ = mesaj[0]["sticker"]["file_id"]
            stik_mi = True
        except TypeError:
            await asyncio.sleep(0.5)
            bar += random.randint(0, 10)

            try:
                await message.edit(f"**Sticker**\n\n`İşleniyor %{bar}`", parse_mode="md")

            except Exception as hata:
                if hata_limit == 3:
                    break

                print(str(hata))
                await message.edit(f'**Hata Var !**\n\n__{hata}')

                hata_limit += 1

    await message.edit("`Tamamlandı.`", parse_mode="md")
    stik_id = mesaj[0]["sticker"]["file_id"]
    await message.reply_sticker(stik_id, reply_to_message_id=yanit_id)
    await client.read_history(stik_botu)
    await message.delete()

CmdHelp("stik").add_command("stik", "<yanıtlanan mesaj>", "@QuotLyBot kullanarak sticker yapar.").add()