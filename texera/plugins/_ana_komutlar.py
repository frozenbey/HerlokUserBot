from texera import API_ID, API_HASH, STRING_SESSION, SESSION_ADI, CMD_HELP
from texera.misc.eklenti_listesi import eklentilerim
from texera.misc._pyrogram.pyro_yardimcilari import yanitlanan_mesaj, kullanici

from pyrogram import Client, filters
from pyrogram.types import Message



@Client.on_message(filters.command(['texera'], ['!','.','/']) & filters.me)
async def destek(client:Client, message:Message):

    girilen_yazi = message.text.split()

    if len(girilen_yazi) == 1:
        mesaj = "**Nasıl kullanacağını öğrenmek için modül adı girmelisin!**\nÖrnek: `.texera afk`\n\n"

        mesaj += "**💫 Yüklü Pluginler:**\n\n\n"
        mesaj += eklentilerim()

        await message.edit(mesaj)
        return

    await message.edit(CMD_HELP[girilen_yazi[1]])


@Client.on_message(filters.command(['log'], ['!','.','/']) & filters.me)
async def logsalla(client:Client, message:Message):
    
    yanit_id = await yanitlanan_mesaj(message)
    await message.delete()
    await client.send_document(chat_id=message.chat.id, document= f"@{SESSION_ADI}.log", caption="**TexeraUserBot Log**", reply_to_message_id=yanit_id)

@Client.on_message(filters.command(['env'], ['!','.','/']) & filters.me)
async def envsalla(client:Client, message:Message):

    #------------------------------------------------------------- Başlangıç >

    kullanici_adi, kullanici_id = await kullanici(message)

    env_bilgileri = f"""__İşte {kullanici_adi} » {SESSION_ADI} Bilgileri;__
**API_ID :**
`{API_ID}`
**API_HASH :**
`{API_HASH}`
**STRING_SESSION :**
`{STRING_SESSION}`
**KİMSEYLE PAYLAŞMAYINIZ!!**
"""

    await client.send_message(kullanici_id, env_bilgileri)

    await message.edit(f"**{kullanici_adi} !**\n\n`ayar.env` **için gerekli olan bilgilerini kaydettim..**\n\n__Kayıtlı Mesajlarına Bakabilirsin..__")
