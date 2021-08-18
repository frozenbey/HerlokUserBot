

async def okunabilir_byte(boyut: int) -> str:
    if not boyut:
        return ""


    binyirmidort = 2 ** 10

    say = 0
    cikti_sozluk = {0: " ", 1: "K", 2: "M", 3: "G", 4: "T"}

    while boyut > binyirmidort:
        boyut /= binyirmidort
        say += 1

    return str(round(boyut, 2)) + " " + cikti_sozluk[say] + "B"