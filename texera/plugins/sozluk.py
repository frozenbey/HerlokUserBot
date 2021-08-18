import requests
import os
from json import loads
from texera.cmdhelp import CmdHelp


from pyrogram import Client, filters
from pyrogram.types import Message


def benzerkelimeleralma(kelime,limit=5):
    benzerler = []
    if not os.path.exists('autocomplete.json'):
        words = requests.get(f'https://sozluk.gov.tr/autocomplete.json')
        open('autocomplete.json', 'a+').write(words.text)
        words = words.json()
    else:
        words = loads(open('autocomplete.json', 'r').read())

    for word in words:
        if word['madde'].startswith(kelime) and not word['madde'] == kelime:
            if len(benzerler) > limit:
                break
            benzerler.append(word['madde'])
    benzerlerStr = ""
    for benzer in benzerler:
        if not benzerlerStr == "":
            benzerlerStr += ", "
        benzerlerStr += f"`{benzer}`"
    return benzerlerStr

@Client.on_message(filters.command(['tdk'], ['!','.','/']) & filters.me)
async def tdk(client:Client, message:Message):
    inp = message.command[1]
    await message.edit("SÖZLÜKTE ARIYORUM...")
    response = requests.get(f'https://sozluk.gov.tr/gts?ara={inp}').json()
    if 'error' in response:
        await message.edit(f'**Kelimeniz({inp}) sözlükte bulunamadı**')
        words = benzerkelimeleralma(inp)
        if not words == '':
            return await message.edit(f'__Kelimeniz({inp}) sözlükte bulunamadı__\n\n**Benzer kelimeler:** {words}')
    else:
        anlamlarStr = ""
        for anlam in response[0]["anlamlarListe"]:
            anlamlarStr += f"\n**{anlam['anlam_sira']}.**"
            if ('ozelliklerListe' in anlam) and ((not anlam["ozelliklerListe"][0]["tam_adi"] == None) or (not anlam["ozelliklerListe"][0]["tam_adi"] == '')):
                anlamlarStr += f"__({anlam['ozelliklerListe'][0]['tam_adi']})__"
            anlamlarStr += f' ```{anlam["anlam"]}```'

            if response[0]["cogul_mu"] == '0':
                cogul = '❌'
            else:
                cogul = '✅'
            
            if response[0]["ozel_mi"] == '0':
                ozel = '❌'
            else:
                ozel = '✅'
        await message.edit(f'**Kelime:** `{inp}`\n\n**Çoğul Mu:** {cogul}\n**Özel Mi:** {ozel}\n\n**Anlamlar:**{anlamlarStr}')
        words = benzerkelimeleralma(inp)
        if not words == '':
            return await message.edit(f'**Kelime:** `{inp}`\n\n**Çoğul Mu:** `{cogul}`\n**Özel Mi:** {ozel}\n\n**Anlamlar:**{anlamlarStr}' + f'\n\n**Benzer Kelimeler:** {words}')

CmdHelp("sozluk").add_command("tdk", "<aranacak kelime>", "Sözlükte arama yapar.").add()