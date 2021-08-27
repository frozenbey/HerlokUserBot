

from texera import TEMP_AYAR
from texera.cmdhelp import CmdHelp

from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command(['info'], ['!','.','/']) & filters.me)
async def info(c:Client, m:Message):
    if m.reply_to_message is not None:
        user_id = m.reply_to_message.from_user.id
        user_username = m.reply_to_message.from_user.username
        user_status = m.reply_to_message.from_user.status 
        user_name = m.reply_to_message.from_user.mention 
        user_dc = m.reply_to_message.from_user.dc_id
        
        chat_id = m.chat.id
        chat_username = m.chat.username
        chat_name = str(m.chat.first_name) +" "+ str(m.chat.last_name)
        
        
        
        
        
        
        await c.send_message(m.chat.id,  chat_id )
        await c.send_message(m.chat.id,  chat_username )
        await c.send_message(m.chat.id,  chat_name )
        
        
        await m.edit(f"""
                **USER**
        **İsim:**          {user_name}
        **Id:**            {user_id}
        **Kullanıcı Adı:** @{user_username}
        **Son Görülme:**   {user_status}
        **DC:**            {user_dc}
        
                **CHAT**
        **İsim:**          {chat_name}` 
        **Id:**            {chat_id}
        **Kullanıcı Adı:** @{chat_username}
        """)
        
    else:
        try:
            user = m.command[1]
        except IndexError:
            await m.edit("`Bir kullanıcının mesajını yanıtla veya kullanıcı id yada kullanıcı adı gir.`")
            return
        
        try:
            user = await c.get_users(user)
        except:
            await m.edit("`Yanlış Kullanım !`")
            return
        user_id = user.id
        user_username = user.username
        user_status = user.status
        user_name = user.mention
        user_dc = user.dc_id
        
        await m.edit(f"""
                **USER**
        **İsim:**          {user_name}
        **Id:**            {user_id}
        **Kullanıcı Adı:** @{user_username}
        **Son Görülme:**   {user_status}
        **DC:**            {user_dc}
        """)
        

CmdHelp("info").add_command("info", "|id| veya |kullanıcı adı|", "Bilgilerini almak için bir kullanıcının mesajını yanıtlayın veya .info @sherlock_exe şeklinde kulanın.").add()
