"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Michal Henyš
email: henysmichal87@gmail.com
discord: Michal Henys
"""



import requests
from bs4 import BeautifulSoup
import csv
import argparse
import traceback

def hlavni_funkce(url: str, vystupni_soubor: str) -> str:
    """
    Hlavní funkce pro spuštění programu.
    """
    try:
        odpoved = requests.get(url)
        soup = BeautifulSoup(odpoved.text, 'html.parser')
        tabulka = soup.find("div", {"id": "core"})
        vsechny_radky = tabulka.find_all("tr") if tabulka else []

        # Získání volebních výsledků
        vysledky_voleb = ziskat_vysledky_voleb(vsechny_radky)

        # Zápis do CSV
        with open(vystupni_soubor, mode="w", encoding="cp1250", newline='') as soubor_csv:
            if vysledky_voleb:
                hlavicky = vysledky_voleb[0].keys()
                zapisovac = csv.DictWriter(soubor_csv, fieldnames=hlavicky)
                zapisovac.writeheader()
                zapisovac.writerows(vysledky_voleb)
            else:
                return "Žádná data k uložení."
        print(f"Ukládám do souboru: {vystupni_soubor}")
        return "Ukončuji election-scraper"
    except Exception:
        return traceback.format_exc()

def ziskat_vysledky_voleb(radky) -> list:
    """
    Získání volebních výsledků z tabulky na hlavní stránce.
    """
    vysledky = []
    for radek in radky[2:]:
        bunky_na_radku = radek.find_all("td")
        if len(bunky_na_radku) >= 3:
            detailni_url = generovat_url_obce(bunky_na_radku)
            if detailni_url:  # Kontrola, zda URL není prázdná
                vsechny_radky_obce, data_volicu = stahnout_data_obce(detailni_url)
                vysledky_obce = sloucit_vysledky(vsechny_radky_obce, data_volicu, {
                    "Kód": bunky_na_radku[0].get_text(strip=True),
                    "Místo": bunky_na_radku[1].get_text(strip=True),
                })
                vysledky.append(vysledky_obce)
    return vysledky

def generovat_url_obce(bunky_na_radku) -> str:
    """
    Generování URL pro podrobné výsledky obce.
    """
    odkaz = bunky_na_radku[2].find("a")  # Odkaz je na třetí buňce
    if odkaz and 'href' in odkaz.attrs:
        relativni_url = odkaz['href'].replace("&amp;", "&")
        return f"https://www.volby.cz/pls/ps2017nss/{relativni_url}"
    return ""  # Vrací prázdný řetězec, pokud URL neexistuje

def stahnout_data_obce(url: str) -> tuple:
    """
    Stažení podrobností pro konkrétní obec.
    """
    odpoved = requests.get(url)
    soup = BeautifulSoup(odpoved.text, 'html.parser')

    # Najdi hodnoty pro voliče, obálky a platné hlasy
    data_volicu = {
        "Voliči v seznamu": "",
        "Vydané obálky": "",
        "Platné hlasy": ""
    }
    data_volicu["Voliči v seznamu"] = ziskat_text_bezpecne(soup.find("td", {"class": "cislo", "headers": "sa2"}))
    data_volicu["Vydané obálky"] = ziskat_text_bezpecne(soup.find("td", {"class": "cislo", "headers": "sa3"}))
    data_volicu["Platné hlasy"] = ziskat_text_bezpecne(soup.find("td", {"class": "cislo", "headers": "sa6"}))

    # Najdi tabulku s výsledky
    tabulka = soup.find("div", {"id": "core"})
    vsechny_radky = tabulka.find_all("tr") if tabulka else []
    return vsechny_radky, data_volicu

def ziskat_text_bezpecne(element):
    """
    Bezpečně získá text z elementu nebo vrátí prázdný řetězec, pokud element neexistuje.
    """
    return element.get_text(strip=True).replace("\xa0", "") if element else ""

def sloucit_vysledky(radky, data_volicu, kod_a_misto) -> dict:
    """
    Sloučení výsledků pro obec.
    Každé město bude mít jeden řádek, politické strany budou sloupce.
    """
    vysledek = kod_a_misto.copy()
    vysledek.update(data_volicu)
    for radek in radky[2:]:
        bunky_stran = radek.find_all("td", headers=lambda h: 't1sb2' in h or 't2sb2' in h)
        bunky_hlasy = radek.find_all("td", headers=lambda h: 't1sb3' in h or 't2sb3' in h)
        if len(bunky_stran) == len(bunky_hlasy):
            for i in range(len(bunky_stran)):
                strana = bunky_stran[i].get_text(strip=True)
                hlasy = bunky_hlasy[i].get_text(strip=True).replace("\xa0", "")
                vysledek[strana] = hlasy
    return vysledek

if __name__ == "__main__":
    # Nastavení argumentů z příkazového řádku
    parser = argparse.ArgumentParser(description="Stahování volebních výsledků.")
    parser.add_argument("url", type=str, help="URL adresa hlavní stránky.")
    parser.add_argument("vystupni_soubor", type=str, help="Název výstupního CSV souboru.")
    args = parser.parse_args()

    # Kontrola argumentů
    if not args.url or not args.vystupni_soubor:
        print("Nebyly zadány potřebné argumenty! Ujistěte se, že zadáváte URL a název výstupního souboru.")
    else:
        print(f"Stahuji data z vybraného URL: {args.url}")
        # Spuštění hlavní funkce
        vysledky = hlavni_funkce(args.url, args.vystupni_soubor)
        print(vysledky)
