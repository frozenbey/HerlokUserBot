
from texera.cmdhelp import CmdHelp
from pyrogram import Client, filters
from pyrogram.types import Message
import requests
import pytz
from datetime import datetime

@Client.on_message(filters.command(['ezan'], ['!','.','/']) & filters.me)
async def ezan(client:Client, message:Message):

    #------------------------------------------------------------- Başlangıç >
    il = girilen_yazi = message.command[1]

    if len(girilen_yazi) == 1:
        await message.edit("__Arama yapabilmek için `il` girmelisiniz..__")
        return

    try:
        il      = il.replace('İ', "i").lower()
        tr2eng  = str.maketrans(" .,-*/+-ıİüÜöÖçÇşŞğĞ", "________iIuUoOcCsSgG")
        il      = il.lower().translate(tr2eng)

        ezan_api  = f'https://www.sabah.com.tr/json/getpraytimes/{il}'
        json_veri = requests.get(ezan_api).json()['List'][0]

        imsak   = datetime.fromtimestamp(int(json_veri['Imsak'].split('(')[1][:-5]),  pytz.timezone("Turkey")).strftime("%H:%M")
        gunes   = datetime.fromtimestamp(int(json_veri['Gunes'].split('(')[1][:-5]),  pytz.timezone("Turkey")).strftime("%H:%M")
        ogle    = datetime.fromtimestamp(int(json_veri['Ogle'].split('(')[1][:-5]),   pytz.timezone("Turkey")).strftime("%H:%M")
        ikindi  = datetime.fromtimestamp(int(json_veri['Ikindi'].split('(')[1][:-5]), pytz.timezone("Turkey")).strftime("%H:%M")
        aksam   = datetime.fromtimestamp(int(json_veri['Aksam'].split('(')[1][:-5]),  pytz.timezone("Turkey")).strftime("%H:%M")
        yatsi   = datetime.fromtimestamp(int(json_veri['Yatsi'].split('(')[1][:-5]),  pytz.timezone("Turkey")).strftime("%H:%M")
    except IndexError:
        await message.edit(f'`{il}` __diye bir yer bulamadım..__')
        return

    mesaj = f"📍 `{il}` __için Ezan Vakitleri;__\n\n"
    mesaj += f"🏙 **İmsak   :** `{imsak}`\n"
    mesaj += f"🌅 **Güneş   :** `{gunes}`\n"
    mesaj += f"🌇 **Öğle    :** `{ogle}`\n"
    mesaj += f"🌆 **İkindi  :** `{ikindi}`\n"
    mesaj += f"🌃 **Akşam   :** `{aksam}`\n"
    mesaj += f"🌌 **Yatsı   :** `{yatsi}`\n"

    try:
        await message.edit(mesaj)
    except Exception as hata:
        print(str(hata))
        return
CmdHelp("ezanv").add_command("ezan", "<il>", "Girdiğiniz ilin ezan vakitlerini gösterir.").add()