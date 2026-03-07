"""
project_3.py : treti projekt z Engeto Online Python Academie
author: Lucia Luptakova
email:lucy.luptakova"gmail.com
"""

import __main__

import requests
from bs4 import BeautifulSoup as bs
import click
import csv

def vycisti_cislo(tag):
    if tag:
        text = tag.get_text(strip=True)
        return int(text.replace("\xa0", ""))
    return 0

def nacti_obsah_stranky(url: str):
    try:
        odpoved = requests.get(url)
        odpoved.raise_for_status()
        return bs(odpoved.text, "html.parser")
    except requests.exceptions.RequestException:
        return None

def ziskej_data_obce(url_obce: str):
    odpoved_obec = requests.get(url_obce)
    soup_obec = bs(odpoved_obec.text, "html.parser")
    vsechny_radky = soup_obec.find_all("tr")
    data = {
        "registred": vycisti_cislo(soup_obec.find("td", {"headers": "sa2"})),
        "envelopes": vycisti_cislo(soup_obec.find("td", {"headers": "sa3"})),
        "valid": vycisti_cislo(soup_obec.find("td", {"headers": "sa6"})),
    }

    for radek in vsechny_radky:
        nazev_tag = radek.find("td", class_="overflow_name")  # Název strany
        hlasy_tag = radek.find(
            "td", {"headers": ["t1sb3", "t2sb3"]}
        )  # Hlasy (vícero možných headers)

        if nazev_tag and hlasy_tag:
            nazev_strany = nazev_tag.get_text(strip=True)
            pocet_hlasu = vycisti_cislo(hlasy_tag)
            # Přidáme stranu do slovníku dat
            data[nazev_strany] = pocet_hlasu

    return data

def ziskej_obce(rozdeleny_text):
    vsechny_obce = []
    vsechny_radky = rozdeleny_text.find_all("tr")
    for radek in vsechny_radky:
        obec_tag = radek.find("td", class_="overflow_name")
        if obec_tag:
            cislo_obce = radek.find("td", class_="cislo").get_text(strip=True)
            nazev_obce = obec_tag.get_text(strip=True)
            odkaz = radek.find("a")["href"]
            url_obce = "https://www.volby.cz/pls/ps2017nss/" + odkaz
            print(f"Stahuji data pro: {nazev_obce}")
            data_z_obce = ziskej_data_obce(url_obce)
            kompletni_radek = {
                "code": cislo_obce,
                "location": nazev_obce,
                **data_z_obce,
            }
            vsechny_obce.append(kompletni_radek)

    return vsechny_obce

def uloz_do_csv(data: list, nazev_souboru: str):
    if not data:
        print("Žádná data k uložení.")
        return

    hlavicka = data[0].keys()
    with open(nazev_souboru, mode="w", newline="", encoding="utf-8-sig") as soubor:
        writer = csv.DictWriter(soubor, fieldnames=hlavicka)
        writer.writeheader()
        writer.writerows(data)


@click.command()
@click.argument('url')
@click.argument('vystup_csv')
def main(url, vystup_csv):
    """
    Elections Scraper - nástroj na sťahovanie výsledkov volieb.
    URL: odkaz na územný celok z volby.cz
    VYSTUP_CSV: názov súboru, do ktorého sa uložia dáta.
    """
    if not url.startswith("https://www.volby.cz/"):
        click.echo("Chyba: Toto nevyzerá ako správna URL z volby.cz")
        return

    click.echo(f"Spracovávam dáta z: {url}")
    # --- TADY SE DĚJE TA MAGIE ---
    obsah_stranky = nacti_obsah_stranky(url)

    if obsah_stranky:
        data = ziskej_obce(obsah_stranky)
        uloz_do_csv(data, vystup_csv)
        click.echo(f"Hotovo! Výsledky sú v {vystup_csv}")
    else:
        click.echo("Chyba: Nepodarilo sa stiahnuť dáta z hlavnej URL.")

if __name__ == "__main__":
    main()
