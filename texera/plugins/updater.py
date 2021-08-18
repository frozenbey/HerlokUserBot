from texera.cmdhelp import CmdHelp

from os import path, environ, remove, execle
import sys
import asyncio
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError




requirements_path = path.join(path.dirname(path.dirname(path.dirname(__file__))), 'requirements.txt')

async def gen_chlog(repo, diff):
    ch_log = ''
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += f'•[{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n'
    return ch_log


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            ' '.join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)

from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("update",".") & filters.me)
async def ustream(client:Client, message:Message):
    ".update komutu ile botunun güncel olup olmadığını denetleyebilirsin."

    await message.edit("`Güncellemeler denetleniyor...`")
    conF = message.text.split(" ")
    if len(conF) == 1:
        conf = ""
    elif len(conF) == 2:
        if conF[1] == "now":
            conf = "now"
        if conF[1] == "force":
            conf = "force"
    else:
        conf = ""
    off_repo = "https://github.com/sherlock-exe/TexeraUserBot"
    if conf == "force":
        force_update = True
    else:
        force_update = False

    try:
        txt = "`Güncelleme başarısız oldu! Bazı sorunlarla karşılaştım.`\n\n**LOG:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        repo = Repo()
        await message.edit(f'{txt}\n`{error} klasörü bulunamadı.`')
        repo.__del__()
        return
    except GitCommandError as error:
        await message.edit(f'{txt}\n`⚠️ Git hatası ⚠️ {error}`')
        repo = Repo()
        repo.__del__()
        return
    except InvalidGitRepositoryError as error:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("main", origin.refs.main)
        repo.heads.main.set_tracking_branch(origin.refs.main)
        repo.heads.main.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != 'main':
        await message.edit("**[UPDATER]:**` Galiba Texera'yı modifiye ettin ve kendi branşını kullanıyorsun.\nBu durum güncelleyicinin kafasını karıştırıyor\nLütfen Thor botunu resmi repodan kullan.`")
        repo.__del__()
        return

    try:
        repo.create_remote('upstream', off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote('upstream')
    ups_rem.fetch(ac_br)

    changelog = await gen_chlog(repo, f'HEAD..upstream/{ac_br}')

    if not changelog and not force_update:
        await message.edit("**✅  Şu an en güncel durumdayım!** \n**📡 Branch: {}**".format(ac_br))
        repo.__del__()
        return

    if conf != "now" and not force_update:
        changelog_str = "**{} için yeni güncelleme mevcut!\n\nDeğişiklikler:**\n`{}`".format(ac_br, changelog)
        if len(changelog_str) > 4096:
            await message.edit("`Değişiklik listesi çok büyük, dosya olarak görüntülemelisin.`")
            file = open("degisiklikler.txt", "w+")
            file.write(changelog_str)
            file.close()
            await client.send_document(
                message.chat_id,
                "degisiklikler.txt",
                reply_to_message_id=message.id,
            )
            remove("degisiklikler.txt")
        else:
            await message.edit(changelog_str)
        await client.send_message(message.chat.id, "`Güncellemeyi yapmak için \".update now\" komutunu kullan.`")
        return

    if force_update:
        await message.edit("`Güncel userbot kodu zorla eşitleniyor...`")
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await update_requirements()
        await message.edit("`Güncel userbot kodu zorla eşitlendi`")
        args = [sys.executable, "tex.py"]
        execle(sys.executable, *args, environ)
        return
    else:
        await message.edit("❤️**Durum**: __Güncelleniyor..\n\n💌 UserBot'unuz daha iyi olacağınıza emin olabilirsiniz :) Bu işlem maksimum 10 dakika sürmektedir.__")
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await update_requirements()
    await message.edit("❤️**Durum:** __Güncelleme başarıyla tamamlandı!\n\n🔄 Yeniden başlatılıyor...__")
    args = [sys.executable, "tex.py"]
    execle(sys.executable, *args, environ)
    return
    
CmdHelp("updater").add_command("update", None, "Botunuza siz kurduktan sonra herhangi bir güncelleme gelip gelmediğini kontrol eder.").add_command("update now", None, "Botunuzu günceller.").add_command("update force", None, "Eğer güncelleme olduğuna eminseniz fakat bot güncelleme olmadığını söylüyorsa bu komut ile botu zorla güncelleyebilirsiniz.").add()
