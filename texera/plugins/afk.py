
from texera.cmdhelp import CmdHelp

from texera import TEMP_AYAR, idm

import asyncio
from datetime import datetime
import humanize
from pyrogram import filters, Client
from pyrogram.types import Message

def GetChatID(message: Message):
    return message.chat.id

def ReplyCheck(message: Message):
    reply_id = None
    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id
    elif not message.from_user.is_self:
        reply_id = message.message_id
    return reply_id


AFK = False
AFK_REASON = ""
AFK_TIME = ""
USERS = {}
GROUPS = {}


def subtract_time(start, end):
    """ZAMAN"""
    subtracted = humanize.naturaltime(start - end)
    return str(subtracted)


@Client.on_message(
    ((filters.group & filters.mentioned) | filters.private) & ~filters.me & ~filters.service, group=3
)
async def collect_afk_messages(c:Client, message: Message):
    if AFK:
        last_seen = subtract_time(datetime.now(), AFK_TIME)
        is_group = True if message.chat.type in ["supergroup", "group"] else False
        CHAT_TYPE = GROUPS if is_group else USERS

        if GetChatID(message) not in CHAT_TYPE:
            text = (
                f"`Beep boop. Bu bir otomatik mesajdır.\n"
                f"Şuan müsait değilim.\n"
                f"Son görülme: {last_seen}\n"
                f"Sebep: ```{AFK_REASON.upper()}```\n"
                f"Şuanki işimi bitirdikten sonra sana döneceğim.`"
            )
            await c.send_message(
                chat_id=GetChatID(message),
                text=text,
                reply_to_message_id=ReplyCheck(message),
            )
            CHAT_TYPE[GetChatID(message)] = 1
            return
        elif GetChatID(message) in CHAT_TYPE:
            if CHAT_TYPE[GetChatID(message)] == 50:
                text = (
                    f"`Bu otomatik mesajdır\n"
                    f"Son görülme: {last_seen}\n"
                    f"Bu sana şu anda AFK olduğumu söylediğim 10. sefer.\n"
                    f"Ulaşılabilir olduğumda sana döneceğim.\n"
                    f"Senin için daha fazla otomatik mesaj yok !`"
                )
                await c.send_message(
                    chat_id=GetChatID(message),
                    text=text,
                    reply_to_message_id=ReplyCheck(message),
                )
            elif CHAT_TYPE[GetChatID(message)] > 50:
                return
            elif CHAT_TYPE[GetChatID(message)] % 5 == 0:
                text = (
                    f"`Hey, Hâlâ dönmedim.\n"
                    f"Son görülme: {last_seen}\n"
                    f"Hâlâ meşgul: ```{AFK_REASON.upper()}```\n"
                    f"Biraz sonra tekrardan deneyin.`"
                )
                await c.send_message(
                    chat_id=GetChatID(message),
                    text=text,
                    reply_to_message_id=ReplyCheck(message),
                )

        CHAT_TYPE[GetChatID(message)] += 1


@Client.on_message(filters.command("afk", ".") & filters.me, group=3)
async def afk_set(_, message: Message):
    global AFK_REASON, AFK, AFK_TIME

    cmd = message.command
    afk_text = ""

    if len(cmd) > 1:
        afk_text = " ".join(cmd[1:])

    if isinstance(afk_text, str):
        AFK_REASON = afk_text

    AFK = True
    AFK_TIME = datetime.now()

    await message.delete()


@UserBot.on_message(filters.command("unafk", ".") & filters.me, group=3)
async def afk_unset(_, message: Message):
    global AFK, AFK_TIME, AFK_REASON, USERS, GROUPS

    if AFK:
        last_seen = subtract_time(datetime.now(), AFK_TIME).replace("ago", "").strip()
        await message.edit(
            f"`Siz yokken ({last_seen}'dan beri), {len(USERS) + len(GROUPS)} sohbetten aldın"
            f"{sum(USERS.values()) + sum(GROUPS.values())} mesaj aldın.`"
        )
        AFK = False
        AFK_TIME = ""
        AFK_REASON = ""
        USERS = {}
        GROUPS = {}
        await asyncio.sleep(5)

    await message.delete()


@Client.on_message(filters.me, group=3)
async def auto_afk_unset(_, message: Message):
    global AFK, AFK_TIME, AFK_REASON, USERS, GROUPS

    if AFK:
        last_seen = subtract_time(datetime.now(), AFK_TIME).replace("ago", "").strip()
        reply = await message.reply(
            f"`Siz yokken ({last_seen}'dan beri), {len(USERS) + len(GROUPS)} sohbetten aldın"
            f"{sum(USERS.values()) + sum(GROUPS.values())} mesaj aldın.`"
        )
        AFK = False
        AFK_TIME = ""
        AFK_REASON = ""
        USERS = {}
        GROUPS = {}
        await asyncio.sleep(5)
        await reply.delete()
        

    
CmdHelp("afk").add_command("afk", "<sebep>", "AFK olduğunuzu belirtir.", "afk uyuyor").add_command("unafk", None, "AFK modunu kapatır.").add()
