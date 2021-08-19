import time
import logging
from math import ceil
import os, sys, platform
from dotenv import load_dotenv
from pyrogram import Client, __version__


print("TexeraUserBot Başlatılıyor...")

def hata(yazi:str) -> None:
   print("[✗] {}".format(yazi))
def bilgi(yazi:str) -> None:
   print("[*] {}".format(yazi))
def basarili(yazi:str) -> None:
   print("[✓] {}".format(yazi))
def onemli(yazi:str) -> None:
   print("[!] {}".format(yazi))


if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    hata("""En az python 3.6 sürümüne sahip olmanız gerekir.
              Birden fazla özellik buna bağlıdır. Bot kapatılıyor.""")
    quit(1)

if  os.path.exists("ayar.env"):
    load_dotenv("ayar.env")

# Yapılandırmanın önceden kullanılan değişkeni kullanarak düzenlenip düzenlenmediğini kontrol edin.
# Temel olarak, yapılandırma dosyası için kontrol.
AYAR_KONTROL = os.environ.get("___________LUTFEN_______BU_____SATIRI_____SILIN__________", None)

if AYAR_KONTROL:
    hata("\n\tLütfen ayar.env dosyanızı düzenlediğinize emin olun /veya\n\tilk hashtag'de belirtilen satırı kaldırın..\n")
    quit(1)

API_ID          = str(os.environ.get("API_ID", str))
API_HASH        = str(os.environ.get("API_HASH", str))
STRING_SESSION  = str(os.environ.get("STRING_SESSION", str))
SESSION_ADI     = os.environ.get("SESSION_ADI", "TexeraUserbot")
INDIRME_ALANI   = os.environ.get("INDIRME_ALANI", "downloads/")
HEROKU_APPNAME  = os.environ.get("HEROKU_APPNAME", str)
HEROKU_APIKEY   = os.environ.get("HEROKU_APIKEY", str)
HEROKU          = os.environ.get("HEROKU", str)

if not os.path.isdir(INDIRME_ALANI): os.makedirs(INDIRME_ALANI)

if STRING_SESSION.startswith('-') or len(STRING_SESSION) < 351:
    hata("\n\tMuhtemelen String Session Hatalı..!\n")
    quit(1)


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
LOGGER = logging.getLogger("pyrogram").setLevel(logging.WARNING)
StartTime = time.time()

try:
    texera        = Client(
STRING_SESSION,
api_id          = API_ID,
api_hash        = API_HASH,
plugins         = dict(root="texera/plugins")
)
except ValueError:
    print("Lütfen ayar.env dosyanızı DÜZGÜNCE oluşturun!")


TEMP_AYAR = {
"AFK" : "0",
"AFK_MSG": "Şu anda afkyım",
"PLUGIN_MSG" : {
    "info" : {"DEVS" : "[➽ѕнєяℓοϲκ⟢](https://t.me/sherlock_exe)"}
}}

idm = None
PATTERNS = "."
CMD_HELP = {}
CMD_HELP_BOT = {}

tum_eklentiler = []
for dosya in os.listdir("./texera/plugins/"):
    if not dosya.endswith(".py") or dosya.startswith("_"):
        continue
    tum_eklentiler.append(dosya.replace('.py',''))

def baslangic() -> None:   
    texera.start()
      
    me = texera.get_me()
    idm = me.id  
      
    time.sleep(1.5)
    TexeraSohbet = -1001524686970
    TexeraUserBot = -1001560054521
    TexeraPlugin = -1001473944468
    TexeraSupport = -1001513915421

    try:
        texera.join_chat(TexeraSohbet)
    except Exception as E:
      print(E)
    try:
        texera.join_chat(TexeraUserBot)
    except:
        pass
    try:
        texera.join_chat(TexeraPlugin)
    except:
        pass
    try:
        texera.join_chat(TexeraSupport)
    except:
        pass


    surum = f"{str(sys.version_info[0])}.{str(sys.version_info[1])}"
    print(f"@{SESSION_ADI} 🍁 Python: {surum} Pyrogram: {__version__}")
    basarili(f"{SESSION_ADI} {len(tum_eklentiler)} eklentiyle çalışıyor...\n")
    texera.stop()

BOT_VER = "v0.1"
SURUM = f"{str(sys.version_info[0])}.{str(sys.version_info[1])}"
