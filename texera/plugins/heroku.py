
import math, asyncio, os
import heroku3, requests
from texera import HEROKU_APPNAME, HEROKU_APIKEY, HEROKU
from texera.cmdhelp import CmdHelp

if HEROKU.lower() == "true":
    heroku_api = "https://api.heroku.com"
    Heroku = heroku3.from_key(HEROKU_APIKEY)
    app = Heroku.app(HEROKU_APPNAME)
    heroku_var = app.config()

from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command(['dyno'], ['!','.','/']) & filters.me)
async def dyno(client:Client, message:Message):

    if HEROKU.lower() == "true":
        useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/80.0.3987.149 Mobile Safari/537.36'
                    )
        u_id = Heroku.account().id
        headers = {
        'User-Agent': useragent,
        'Authorization': f'Bearer {HEROKU_APIKEY}',
        'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
        }
        path = "/accounts/" + u_id + "/actions/get-quota"
        r = requests.get(heroku_api + path, headers=headers)
        if r.status_code != 200:
            return await message.edit("`Hata: Kötü bir şey oldu.`\n\n"
                                f">.`{r.reason}`\n")
        result = r.json()
        quota = result['account_quota']
        quota_used = result['quota_used']

        remaining_quota = quota - quota_used
        percentage = math.floor(remaining_quota / quota * 100)
        minutes_remaining = remaining_quota / 60
        hours = math.floor(minutes_remaining / 60)
        minutes = math.floor(minutes_remaining % 60)

        App = result['apps']
        try:
            App[0]['quota_used']
        except IndexError:
            AppQuotaUsed = 0
            AppPercentage = 0
        else:
            AppQuotaUsed = App[0]['quota_used'] / 60
            AppPercentage = math.floor(App[0]['quota_used'] * 100 / quota)
        AppHours = math.floor(AppQuotaUsed / 60)
        AppMinutes = math.floor(AppQuotaUsed % 60)

        await asyncio.sleep(1.5)

        return await message.edit("**⚒ Dyno**:\n\n"
                            f" ✍🏻  `Kullanılan dyno süresi`  **({HEROKU_APPNAME})**:\n"
                            f"      `{AppHours}` **saat**  `{AppMinutes}` **dakika**  "
                            f"➿  [`{AppPercentage}` **%**]"
                            "\n\n"
                            " ✍🏻  `Kalan dyno süresi`:\n"
                            f"      `{hours}` **saat**  `{minutes}` **dakika**  "
                            f"➿  [`{percentage}` **%**]"
                            )

@Client.on_message(filters.command(['hlog'], ['!','.','/']) & filters.me)
async def hlog(client:Client, message:Message):


    if HEROKU.lower() == "true":

        try:
            Heroku = heroku3.from_key(HEROKU_APIKEY)
            app = Heroku.app(HEROKU_APPNAME)
        except BaseException:
            return await message.edit(
                "Hata oluştu."
            )
        await message.delete()
        with open("hlog.txt", "w") as log:
            log.write(app.get_log())
        await client.send_document(chat_id=message.chat.id, document="hlog.txt")
        try:
            os.remove("hlog.txt")
        except:
            pass
CmdHelp("heroku").add_command("dyno", None, "Kalan dyno sürenize bakın.").add_command("hlog", None, "Heroku logunuza bakın.").add()
