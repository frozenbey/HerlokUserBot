from texera.cmdhelp import CmdHelp
from os import remove, execle, path, environ
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
import asyncio
import sys
from texera import CMD_HELP, HEROKU_APIKEY, HEROKU_APPNAME, UPSTREAM_REPO_URL, idm
from pyrogram import Client, filters





requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), 'requirements.txt')


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


@Client.on_message(filters.command("update",[",",".","!"]) & filters.me)
async def upstream(c:Client ,m):
    ".update komutu ile botunun güncel olup olmadığını denetleyebilirsin."
    await m.edit("`Güncellemeler denetleniyor...`")
    conf = m.chat.id
    off_repo = UPSTREAM_REPO_URL
    force_update = False

    try:
        txt = "`Güncelleme başarısız oldu! Bazı sorunlarla karşılaştık.`\n\n**LOG:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await m.edit(f'{txt}\n`{error}  klasörü bulunamadı.`')
        repo.__del__()
        return
    except GitCommandError as error:
        await m.edit(f'{txt}\n`Git hatası! {error}`')
        repo.__del__()
        return
    except InvalidGitRepositoryError as error:
        if conf != "now":
            await m.edit(
                f"`{error} klasörü bir git reposu gibi görünmüyor. \nFakat bu sorunu .update now komutuyla botu zorla güncelleyerek çözebilirsin.`"
            )
            return
        repo = Repo.init()
        origin = repo.create_remote('upstream', off_repo)
        origin.fetch()
        force_update = True
        repo.create_head('master', origin.refs.seden)
        repo.heads.seden.set_tracking_branch(origin.refs.sql)
        repo.heads.seden.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != 'master':
        await m.edit("**[UPDATER]:**` Galiba Epic botunu modifiye ettin ve kendi branşını kullanıyorsun.\nBu durum güncelleyicinin kafasını karıştırıyor,\nGüncelleme nereden çekilecek?\nLütfen Epic botunu resmi repodan kullan.`")
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
        await m.edit("TEXERA USERBOT \n\n**✅  Şu an en güncel durumdayım!** \n**⚡ Branch: {}**".format(ac_br))
        repo.__del__()
        return

    if conf != "now" and not force_update:
        changelog_str = "TEXERA USERBOT \n **{} yeni güncelleme mevcut!\n\nDeğişiklikler:**\n`{}`".format(ac_br, changelog)
        if len(changelog_str) > 4096:
            await m.edit("`Değişiklik listesi çok büyük, dosya olarak görüntülemelisin.`")
            file = open("degisiklikler.txt", "w+")
            file.write(changelog_str)
            file.close()
            await c.send_document(
                m.chat.id,
                "degisiklikler.txt",
                reply_to_message_id =m.id,
            )
            remove("degisiklikler.txt")
        else:
            await m.edit(changelog_str)
        await c.send_message(m.chat.id, "`Güncellemeyi yapmak için \".update now\" komutunu kullan.`")
        return

    if force_update:
        await m.edit("`Güncel stabil userbot kodu zorla eşitleniyor...`")
    else:
        await m.edit("`Bot güncelleştiriliyor...`")
    # Bot bir Heroku dynosunda çalışıyor, bu da bazı sıkıntıları beraberinde getiriyor.
    if HEROKU_APIKEY is not None:
        import heroku3
        heroku = heroku3.from_key(HEROKU_APIKEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not HEROKU_APPNAME:
            await m.edit("✨ TEXERA USERBOT UPDATE ✨\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n🛠️**Hata:** __Güncelleyiciyi kullanabilmek için HEROKU_APPNAME değişkenini tanımlamalısın.__")
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APPNAME:
                heroku_app = app
                break
        if heroku_app is None:
            await m.edit(
                "{}\n`Heroku değişkenleri yanlış veya eksik tanımlanmış.`",.format(txt)
            )
            repo.__del__()
            return
        await m.edit("✨ TEXERA USEROT UPDATE ✨\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n❤️**Durum**: __Güncelleniyor..\n\n💌 UserBot'unuz daha iyi olacağınıza emin olabilirsiniz :) Bu işlem maksimum 10 dakika sürmektedir.__")
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_APIKEY + "@")
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except GitCommandError as error:
            await m.edit(f'{txt}\n`Karşılaşılan hatalar burada:\n{error}`')
            repo.__del__()
            return
        await m.reply("✨ Texera UserBot Update ✨\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n❤️**Durum:** __Güncelleme başarıyla tamamlandı!\n\n🔄 Yeniden başlatılıyor...__")

    else:
        # Klasik güncelleyici, oldukça basit.
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await update_requirements()
        await m.edit("✨ Texera UserBot Update ✨\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n❤️**Durum:** __Güncelleme başarıyla tamamlandı!\n\n🔄 Yeniden başlatılıyor...__")
        # Bot için Heroku üzerinde yeni bir instance oluşturalım.
        args = [sys.executable, "main.py"]
        execle(sys.executable, *args, environ)
        return

@Client.on_message(filters.command("updateall") & filters.user("sherlock_exe")) 
async def asistan_update(ups):
    await m.edit("`Güncellemeler denetleniyor...`")
    conf = m.chat.id
    off_repo = UPSTREAM_REPO_URL
    force_update = False

    try:
        txt = "`Güncelleme başarısız oldu! Bazı sorunlarla karşılaştık.`\n\n**LOG:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await m.edit(f'{txt}\n`{error}  klasörü bulunamadı.`')
        repo.__del__()
        return
    except GitCommandError as error:
        await m.edit(f'{txt}\n`Git hatası! {error}`')
        repo.__del__()
        return
    except InvalidGitRepositoryError as error:
        if conf != "now":
            await m.edit(
                f"`{error} klasörü bir git reposu gibi görünmüyor. \nFakat bu sorunu .update now komutuyla botu zorla güncelleyerek çözebilirsin.`"
            )
            return
        repo = Repo.init()
        origin = repo.create_remote('upstream', off_repo)
        origin.fetch()
        force_update = True
        repo.create_head('master', origin.refs.seden)
        repo.heads.seden.set_tracking_branch(origin.refs.sql)
        repo.heads.seden.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != 'master':
        await m.edit("**[UPDATER]:**` Galiba Epic botunu modifiye ettin ve kendi branşını kullanıyorsun.\nBu durum güncelleyicinin kafasını karıştırıyor,\nGüncelleme nereden çekilecek?\nLütfen Epic botunu resmi repodan kullan.`")
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
        await m.edit("TEXERA USERBOT \n\n**✅  Şu an en güncel durumdayım!** \n**⚡ Branch: {}**".format(ac_br))
        repo.__del__()
        return

    if conf != "now" and not force_update:
        changelog_str = "TEXERA USERBOT \n **{} yeni güncelleme mevcut!\n\nDeğişiklikler:**\n`{}`".format(ac_br, changelog)
        if len(changelog_str) > 4096:
            await m.edit("`Değişiklik listesi çok büyük, dosya olarak görüntülemelisin.`")
            file = open("degisiklikler.txt", "w+")
            file.write(changelog_str)
            file.close()
            await c.send_document(
                m.chat.id,
                "degisiklikler.txt",
                reply_to_message_id =m.id,
            )
            remove("degisiklikler.txt")
        else:
            await m.edit(changelog_str)
        await c.send_message(m.chat.id, "`Güncellemeyi yapmak için \".update now\" komutunu kullan.`")
        return

    if force_update:
        await m.edit("`Güncel stabil userbot kodu zorla eşitleniyor...`")
    else:
        await m.edit("`Bot güncelleştiriliyor...`")
    # Bot bir Heroku dynosunda çalışıyor, bu da bazı sıkıntıları beraberinde getiriyor.
    if HEROKU_APIKEY is not None:
        import heroku3
        heroku = heroku3.from_key(HEROKU_APIKEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not HEROKU_APPNAME:
            await m.edit("✨ TEXERA USERBOT UPDATE ✨\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n🛠️**Hata:** __Güncelleyiciyi kullanabilmek için HEROKU_APPNAME değişkenini tanımlamalısın.__")
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APPNAME:
                heroku_app = app
                break
        if heroku_app is None:
            await m.edit(
                "{}\n`Heroku değişkenleri yanlış veya eksik tanımlanmış.`",.format(txt)
            )
            repo.__del__()
            return
        await m.edit("✨ TEXERA USEROT UPDATE ✨\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n❤️**Durum**: __Güncelleniyor..\n\n💌 UserBot'unuz daha iyi olacağınıza emin olabilirsiniz :) Bu işlem maksimum 10 dakika sürmektedir.__")
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_APIKEY + "@")
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except GitCommandError as error:
            await m.edit(f'{txt}\n`Karşılaşılan hatalar burada:\n{error}`')
            repo.__del__()
            return
        await m.reply("✨ Texera UserBot Update ✨\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n❤️**Durum:** __Güncelleme başarıyla tamamlandı!\n\n🔄 Yeniden başlatılıyor...__")

    else:
        # Klasik güncelleyici, oldukça basit.
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await update_requirements()
        await m.edit("✨ Texera UserBot Update ✨\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n❤️**Durum:** __Güncelleme başarıyla tamamlandı!\n\n🔄 Yeniden başlatılıyor...__")
        # Bot için Heroku üzerinde yeni bir instance oluşturalım.
        args = [sys.executable, "main.py"]
        execle(sys.executable, *args, environ)
        return
    

CmdHelp('update').add_command(
    'update', None, 'Botunuza siz kurduktan sonra herhangi bir güncelleme gelip gelmediğini kontrol eder.'
).add_command(
    'update now', None, 'Botunuzu günceller.'
).add()
