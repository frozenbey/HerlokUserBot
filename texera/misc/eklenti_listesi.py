from os import listdir

def eklentilerim() -> str:
    eklentiler = []

    for dosya in listdir("./texera/plugins/"):
        if not dosya.endswith(".py") or dosya.startswith("_"):
            continue
        eklentiler.append(dosya.replace('.py',''))

    string = ""
    sayfa = [sorted(list(eklentiler))[i:i + 5] for i in range(0, len(sorted(list(eklentiler))), 5)]
        
    for i in sayfa:
        string += '⚔️ '
        for sira, a in enumerate(i):
            string += "`" + str(a)
            if sira == i.index(i[-1]):
                string += "`"
            else:
                string += "`, "
        string += "\n"
    return string
