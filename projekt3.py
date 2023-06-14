import requests
from bs4 import BeautifulSoup
import csv
import sys
import os


if len(sys.argv) == 1:
    print("Je potřeba zadat vstupní parametry")
    exit()


# Kontrola argumentů
def input_check():
    if len(sys.argv) != 3:
        print("Nebyly zadány požadované argumenty")
        exit()

    if "volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=" not in sys.argv[1]:
        print("Zadejte správnou URL a zkuste znovu...")
        exit()

    if ".csv" not in sys.argv[2]:
        print("zadejte správný název souboru *.csv")
        exit()
    if os.path.isfile(sys.argv[2]):
        decision = input("Soubor již existuje, přepsat? Y/N ")
        if decision.capitalize() != "Y":
            exit()
        else:
            print("OK...downloading...")
    print("Zadání OK, downloading...")


# Funce na zpracování odkazů - defaultní hodnota je použita pro výchozí stránku ze zadání
def zpracuj_odkaz(odkaz=sys.argv[1]):
    odpoved = requests.get(odkaz)
    soup = BeautifulSoup(odpoved.text, "html.parser")
    return soup


# Získá čísla/kódy obcí
def cisla_obci():
    cisla_obci = []
    web_element = zpracuj_odkaz().find_all("td", {"class": "cislo"})
    for cislo in web_element:
        cisla_obci.append(cislo.get_text())
    return cisla_obci


# Získá jména obcí
def jmena_obci():
    jmena_obci = []
    web_element = zpracuj_odkaz().find_all("td", {"class": "overflow_name"})
    for jmeno in web_element:
        jmena_obci.append(jmeno.get_text())
    return jmena_obci


# Získá odkazy jednotlivých obcí
def odkazy_obci():
    seznam_odkazu = []
    zacatek_odkazu = "https://volby.cz/pls/ps2017nss/"
    web_element = zpracuj_odkaz().find_all("td", {"class": "cislo"})

    for odkaz in web_element:
        seznam_odkazu.append((zacatek_odkazu) + (odkaz.find("a")["href"]))
    return seznam_odkazu


# Získá počet registrovaných voličů
def volici():
    pocet_volicu = []
    for odkaz in odkazy_obci():
        web_element = (
            zpracuj_odkaz(odkaz).find("td", {"class": "cislo"}, headers="sa2")
        ).get_text()
        pocet_volicu.append((web_element.replace("\xa0", "")))

    return pocet_volicu


# Získá počet vydaných obálek
def obalky():
    pocet_obalek = []
    for odkaz in odkazy_obci():
        web_element = (
            zpracuj_odkaz(odkaz).find("td", {"class": "cislo"}, headers="sa3")
        ).get_text()
        pocet_obalek.append((web_element.replace("\xa0", "")))

    return pocet_obalek


# Získá počet platných hlasů
def platne_hlasy():
    pocet_platnych_hlasu = []
    for odkaz in odkazy_obci():
        web_element = (
            zpracuj_odkaz(odkaz).find("td", {"class": "cislo"}, headers="sa6")
        ).get_text()
        pocet_platnych_hlasu.append((web_element.replace("\xa0", "")))

    return pocet_platnych_hlasu


# Získá názvy všech volitelných stran
def strany():
    odkazy = odkazy_obci()
    web_element = zpracuj_odkaz(odkazy[0]).find_all("td", {"class": "overflow_name"})
    seznam_stran = []
    for strana in web_element:
        seznam_stran.append(strana.get_text())

    return seznam_stran


# Získá seznam všech hlasů pro volené strany
def vsechny_hlasy():
    seznam_hlasu = []
    for url in odkazy_obci():
        soup = zpracuj_odkaz(url)
        votes_elements = soup.find_all(
            "td", {"class": "cislo"}, headers=["t1sb3", "t2sb3"]
        )
        get_votes = []
        for votes in votes_elements:
            get_votes.append(int((votes.get_text().replace("\xa0", ""))))
        seznam_hlasu.append(get_votes)
    return seznam_hlasu


# Zapíše výsledné *.csv
def csv_write():
    zacatek = ["code", "location", "registered", "envelopes", "valid"] + strany()
    data = []

    code = cisla_obci()
    location = jmena_obci()
    registered = volici()
    envelopes = obalky()
    valid = platne_hlasy()
    hlasy_stran = vsechny_hlasy()

    for i in range(len(code)):
        radek = [
            code[i],
            location[i],
            registered[i],
            envelopes[i],
            valid[i],
        ] + hlasy_stran[i]
        data.append(radek)

    f = open(sys.argv[2], "w", newline="")
    f_writer = csv.writer(f)
    f_writer.writerow(zacatek)
    f_writer.writerows(data)
    f.close()
    print(f"Dokončeno, uloženo do souboru {sys.argv[2]}")


if __name__ == "__main__":
    input_check()
    csv_write()
