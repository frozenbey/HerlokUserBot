from pyrogram import Client
print("""  
 _______                      
|__   __|                     
   | | _____  _____ _ __ __ _ 
   | |/ _ \ \/ / _ \ '__/ _` |
   | |  __/>  <  __/ | | (_| |
   |_|\___/_/\_\___|_|  \__,_|                                              
 ___  ___  ___ ___ _  ___  _ __  
/ __|/ _ \/ __/ __| |/ _ \| '_ \ 
\__ \  __/\__ \__ \ | (_) | | | |
|___/\___||___/___/_|\___/|_| |_|
       _ 
  __ _| |_  ___ _ 
 / _` | | |/ __| |
| (_| | | | (__| |
 \__,_|_|_|\___|_|

""")
phone = input("Lütfen numaranızı ülke kodu ile beraber yazınız\n ➜")

app = Client(':memory:',api_id="4150176",api_hash="cc60c01e601ee9cd77fe5ec6a6129882",app_version='TexeraUserBot',device_model='Texera',system_version='1.0',lang_code='tr',phone_number=phone)
with app:
    self = app.get_me()
    session = app.export_session_string()
    out = f'''<b>SESSION:</b> <code>{session}</code>\n<b>NOT: Bu bilgiyi kurulum dışında hiçbir yere/kimseye vermeyiniz!</b>'''
    print(f"\n\n{session}\nNOT: Bu bilgiyi kurulum dışında hiçbir yere/kimseye vermeyiniz!\n")
    app.send_message('me', out, parse_mode="html")