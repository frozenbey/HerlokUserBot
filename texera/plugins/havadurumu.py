from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from texera.cmdhelp import CmdHelp
import asyncio

@Client.on_message(filters.command(['havad'], ['!','.','/']) & filters.me)
async def havadurumu(client:Client, message:Message):
    sehir = message.command[1]
    site_api = "6fded1e1c5ef3f394283e3013a597879"
    main_url = "https://api.openweathermap.org/data/2.5/weather?"
    url = main_url + "q=" + sehir + "&appid=" + site_api
    ham_veri = requests.get(url)
    await message.edit("⚒Texera UserBot bilgileri arıyor... 🔍.")
    await asyncio.sleep(1.25)
    veri_json = ham_veri.json()
    
    if veri_json["cod"] == "404":
        await message.edit("{} isimli bir şehir bulunmamakta.".format(sehir))
        await asyncio.sleep(1.25)
    else:
        tempature = veri_json["main"]["temp"]
        hissedilen = veri_json["main"]["feels_like"]
        acıklama =  veri_json["weather"][0]["description"]
        country = veri_json["sys"]["country"]
        wind_speed = veri_json["wind"]["speed"]
    csıcaklık = str(float(tempature-273.15))[0:4]
    chis = str(float(hissedilen - 273.15))
    await message.edit("🔆{} şehrinin:\n🌡Sıcaklığı: {}\n🌇Hissedilen sıcaklığı: {}\n🌳Gökyüzünün durumu: {}\n🗺Rüzgar hızı: {}\nŞehrin bulunduğu ülke: {}".format(sehir, csıcaklık, chis, acıklama, wind_speed, country))
    await asyncio.sleep(1.25)
CmdHelp("havadurumu").add_command(".havad", "<dünyadan herhangi bir şehir>", "Girdiğiniz şehrin o günkü hava durumunu getirir.", "havad mersin").add()
