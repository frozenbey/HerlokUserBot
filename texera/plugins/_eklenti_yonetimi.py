
from texera import texera
import importlib

from texera.misc._pyrogram.pyro_yardimcilari import yanitlanan_mesaj
from texera import SESSION_ADI
from texera.misc.eklenti_listesi import eklentilerim
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio, os, sys


@Client.on_message(filters.command(['plist'], ['!','.','/']) & filters.me)
async def eklenti_list(client:Client, message:Message):
    """
    Yüklü olan Pluginleri Listeler.
    """
    

    mesaj = "**✨ Yüklü Pluginler:**\n\n\n"
    mesaj += eklentilerim()

    try:
        await message.edit(mesaj)
    except Exception as hata:
        print(str(hata))

@Client.on_message(filters.command(['pget'], ['!','.','/']) & filters.me)
async def eklenti_ver(client:Client, message:Message):

    
    yanit_id  = await yanitlanan_mesaj(message)
    #------------------------------------------------------------- Başlangıç >
    girilen_yazi = message.text

    if len(girilen_yazi.split()) == 1:
        await message.edit("`Dosya Adı` **Girmelisin!**")
        return

    dosya = " ".join(girilen_yazi.split()[1:2])

    if f"{dosya}.py" in os.listdir("texera/plugins"):
        await message.delete()

        await message.reply_document(
            document                = f"./texera/plugins/{dosya}.py",
            caption                 = f"__{SESSION_ADI}__ `{dosya}` __eklentisi..__",
            disable_notification    = True,
            reply_to_message_id     = yanit_id
            )

    else:
        await message.edit('**Dosya Bulunamadı!**')

@Client.on_message(filters.command(['pinstall'], ['!','.','/']) & filters.me)
async def eklenti_al(client:Client, message:Message):

    
    #------------------------------------------------------------- Başlangıç >
    cevaplanan_mesaj = message.reply_to_message
    if not message.reply_to_message:
        await message.edit("Plugin kurmak için bir plugin **dosyası** yanıtlamalısın.")
        return
    if len(message.command) == 1 and cevaplanan_mesaj.document:
        if cevaplanan_mesaj.document.file_name.split(".")[-1] != "py":
            await message.edit("`Yalnızca python dosyası yükleyebilirsiniz..`")
            return
        eklenti_dizini = f"./texera/plugins/{cevaplanan_mesaj.document.file_name}"
        await message.edit("`Plugin Yükleniyor...`")

        if os.path.exists(eklenti_dizini):
            await message.edit(f"`{cevaplanan_mesaj.document.file_name}` plugini zaten mevcut!__")
            return

        try:
            await client.download_media(message=cevaplanan_mesaj, file_name=eklenti_dizini)
            await asyncio.sleep(2)
            try:
              spec = importlib.util.spec_from_file_location(eklenti_dizini, eklenti_dizini)
              mod = importlib.util.module_from_spec(spec)
              spec.loader.exec_module(mod)
            except Exception as e:
              await message.edit(f"**Yükleme başarısız!**  `Plugin hatalı. ❌`\n\nHata: {e}")
              os.remove(eklenti_dizini)
              return
            await message.edit(f"**Plugin Yüklendi:** `{cevaplanan_mesaj.document.file_name}`\n__Bot yeniden başlatılıyor 🔄__")
            try:
                await texera.stop()
            except:
                pass
            os.execl(sys.executable, sys.executable, *sys.argv)
            return

        except Exception as hata:
            print(str(hata))
            return

    await message.edit('__Python betiği yanıtlamanız gerekmekte__')

@Client.on_message(filters.command(['pdel'], ['!','.','/']) & filters.me)
async def eklenti_sil(client:Client, message:Message):

    
    #------------------------------------------------------------- Başlangıç >
    silmesene = ["afk","all","carbon","ezanv","gizli","heroku","indir","info","json","komut","misc","ping","profile","sozluk","spammer","stik","updater","whois","admin","botinfo","debug","plugyardım","speedtest"]
        
    if len(message.command) == 2:
        config = message.command[1]
        if config in silmesene:
            await message.edit("**Bu bir yerel modüldür bu yüzden silemezsin!**")
            return
        eklenti_dizini = f"./texera/plugins/{message.command[1]}.py"
        
        if os.path.exists(eklenti_dizini):
            os.remove(eklenti_dizini)
            await asyncio.sleep(2)
            await message.edit(f"**Plugin Silindi:** `{message.command[1]}`\n__Bot yeniden başlatılıyor 🔄__")
            try:
                await texera.stop()
            except:
                pass
            os.execl(sys.executable, sys.executable, *sys.argv)
            return

        await message.edit("`Böyle bir plugin yok`")
        return

    await message.edit("`Geçerli bir plugin adı girin!`")
