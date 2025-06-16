# analyza_voleb_arsen.py
# Autor: Arsen Aloyan
# Email: aloyanarsen3@gmail.com

import sys
import csv
import requests
from bs4 import BeautifulSoup

ZKRATKY_STRAN = {
    "Občanská demokratická strana": "ODS",
    "Česká str.sociálně demokrat.": "ČSSD",
    "Komunistická str.Čech a Moravy": "KSČM",
    "ANO 2011": "ANO 2011",
    "Svob.a př.dem.-T.Okamura (SPD)": "SPD",
    "Česká pirátská strana": "Piráti",
    "CESTA ODPOVĚDNÉ SPOLEČNOSTI": "COS",
    "Radostné Česko": "Rado. Č.",
    "STAROSTOVÉ A NEZÁVISLÍ": "STAN",
    "Strana zelených": "Zelený",
    "ROZUMNÍ-stop migraci,diktát.EU": "ROZUMNÍ",
    "Strana svobodných občanů": "SSO",
    "Blok proti islam.-Obran.domova": "BPI",
    "Občanská demokratická aliance": "ODA",
    "Referendum o Evropské unii": "EU referendum",
    "TOP 09": "TOP 09",
    "Dobrá volba 2016": "DB 2016",
    "SPR-Republ.str.Čsl. M.Sládka": "SPR",
    "Křesť.demokr.unie-Čs.str.lid.": "Křesťaní",
    "Česká strana národně sociální": "ČSNS",
    "REALISTÉ": "REALIST",
    "SPORTOVCI": "SPORT",
    "Dělnic.str.sociální spravedl.": "DSSS",
    "Strana Práv Občanů": "SPO"
}

def nacti_obce(url):
    base_url = "https://volby.cz/pls/ps2017nss/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    obce = []
    for radek in soup.select("tr"):
        odkaz = radek.select_one("td.cislo a")
        nazev = radek.select_one("td.overflow_name")
        if odkaz and nazev:
            kod = odkaz.text.strip()
            jmeno = nazev.text.strip()
            detail = base_url + odkaz["href"]
            obce.append((kod, jmeno, detail))
    return obce

def zpracuj_obec(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    vysledky = {zkr: "0" for zkr in ZKRATKY_STRAN.values()}
    volici = soup.find("td", headers="sa2").text.strip().replace("\xa0", "")
    obalky = soup.find("td", headers="sa3").text.strip().replace("\xa0", "")
    platne = soup.find("td", headers="sa6").text.strip().replace("\xa0", "")

    strany = soup.select("td.overflow_name")
    hlasy = soup.select("td[headers*=t1sa2]")
    for strana, hlas in zip(strany, hlasy):
        jmeno = strana.text.strip()
        if jmeno in ZKRATKY_STRAN:
            vysledky[ZKRATKY_STRAN[jmeno]] = hlas.text.strip().replace("\xa0", "")

    return volici, obalky, platne, vysledky

def main():
    if len(sys.argv) != 3:
        print("Použití: python analyza_voleb_arsen.py <URL> <výstupní_soubor.csv>")
        return

    url = sys.argv[1]
    vystup = sys.argv[2]
    print("Načítání obcí...")
    seznam = nacti_obce(url)
    print(f"Nalezeno {len(seznam)} obcí.")

    hlavicky = list(ZKRATKY_STRAN.values())
    data = []

    for kod, jmeno, obec_url in seznam:
        volici, obalky, platne, hlasy = zpracuj_obec(obec_url)
        radek = [kod, jmeno, volici, obalky, platne] + [hlasy[zkr] for zkr in hlavicky]
        data.append(radek)

    with open(vystup, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"] + hlavicky)
        writer.writerows(data)
    print(f"Výstup uložen do: {vystup}")

if __name__ == "__main__":
    main()
