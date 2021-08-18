from texera.cmdhelp import CmdHelp


from pyrogram import Client, filters
from pyrogram.types import Message

    
@Client.on_message(filters.command(['bio'], ['!','.','/']) & filters.me)
async def bio(client:Client, message:Message):

    #------------------------------------------------------------- Başlangıç >
    girilen_yazi = message.text.split(" ", 1)[1]
    
    if len(girilen_yazi) > 70:
        await message.edit("**70 karakterden az girin**")
    await client.update_profile(bio=girilen_yazi)
    await message.edit("__Bionu güncelledim...__")

@Client.on_message(filters.command(['name'], ['!','.','/']) & filters.me)
async def name(client:Client, message:Message):

    #------------------------------------------------------------- Başlangıç >
    first_na = message.text.split(" ", 2)[1]
    last_na = message.text.split(" ", 2)[2]
    await client.update_profile(first_name=first_na,last_name=last_na)
    await message.edit("__İsmini güncelledim...__")

CmdHelp("profile").add_command("bio", "<yazı>", "Profilinizin Hakkında kısmını değiştirmenizi sağlar.").add_command("name", "<ad> <soyad>", "Profilinizin Ad Soyad kısmını değiştirmenizi sağlar.").add()
