import os
from asyncio import sleep
from texera.cmdhelp import CmdHelp
from pyrogram import filters, Client
from pyrogram.types import Message


CARBON_LANG = "py"

@Client.on_message(filters.command("carbon", ".") & filters.me)
async def carbon_test(c, message: Message):
    carbon_text = message.text[8:]

    # Write the code to a file cause carbon-now-cli wants a file.
    file = "texera/downloads/carbon.{}".format(get_carbon_lang())
    with open(file, "w+") as f:
        f.write(carbon_text)

    await message.edit_text("Carbon oluşturuluyor...")

    os.system("carbon-now -h -t texera/downloads/carbon {}".format(file))

    await c.send_photo(message.chat.id, "texera/downloads/carbon.png")
    await message.delete()


@Client.on_message(filters.command("carbonlang", ".") & filters.me)
async def update_carbon_lang(_, message: Message):
    global CARBON_LANG
    cmd = message.command

    type_text = ""
    if len(cmd) > 1:
        type_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        type_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("Carbona dönüştürmem için birşeyler ver")
        await sleep(2)
        await message.delete()
        return

    CARBON_LANG = type_text
    await message.edit_text("Carbon türü {}'a dönüştürüldü.".format(type_text))
    await sleep(2)
    await message.delete()


@UserBot.on_message(filters.command("carbonlang", "!") & filters.me)
async def send_carbon_lang(_, message: Message):
    await message.edit_text(get_carbon_lang())
    await sleep(5)
    await message.delete()


def get_carbon_lang():
    return CARBON_LANG


CmdHelp("carbon").add_command("carbon", "|bir mesajı yanıtla veya komutun yanına yaz|", "Metni carbon'a dönüştürür.").add()
