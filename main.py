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
    """
    Očistí text z HTML tagu od nezlomitelných mezer a převede jej na celé číslo.
    """
    if tag:
        text = tag.get_text(strip=True)
        return int(text.replace("\xa0", ""))
    return 0


def nacti_obsah_stranky(url: str):
    """
    Odešle požadavek na URL a vrátí objekt bs, pokud je odpověď úspěšná.
    """
    try:
        odpoved = requests.get(url)
        odpoved.raise_for_status()
        return bs(odpoved.text, "html.parser")
    except requests.exceptions.RequestException:
        return None


def ziskej_data_obce(url_obce: str):
    """
    Stáhne a zpracuje volební výsledky pro konkrétní obec.

    Args:
        url_obce (str): Úplná URL adresa na detailní stránku obce.

    Returns:
        dict: Slovník, kde klíče jsou názvy (voliči, strany)
        a hodnoty jsou počty hlasů.

    Example:
        Return: {"registred": 450, "envelopes": 400,
                    "valid": 390, "Strana X": 150...}
    """
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
            data[nazev_strany] = pocet_hlasu

    return data


def ziskej_obce(rozdeleny_text):
    """
    Projde hlavní tabulku územního celku, extrahuje základní info 
    o obcích a pro každou spustí hloubkový scraping dat.
    """
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
    """
    Uloží spracované dáta o voľbách do súboru formátu CSV.

    Funkcia vytvorí hlavičku súboru dynamicky na základe kľúčov
    prvého slovníka v zozname. Používa kódovanie 'utf-8-sig',
    aby sa súbor správne zobrazoval v programe Microsoft Excel
    vrátane českej diakritiky.

    Args:
        data (list): Zoznam slovníkov,
                    kde každý slovník obsahuje dáta za jednu obec.
        nazev_souboru (str): Názov alebo cesta k výslednému CSV súboru.

    Returns:
        None: Funkcia nič nevracia, priamo zapisuje do súboru na disk.

    Example:
        >>> data_ukazka = [
        ... {"code": "589268", "location": "Alojzov", "registered": 205,
                "envelopes": 145, "valid": 144, "Strana A": 50},
        ... {"code": "589276", "location": "Bedihošť", "registered": 834,
                "envelopes": 520, "valid": 515, "Strana A": 120}
        ... ]
        >>> uloz_do_csv(data_ukazka, "vysledky.csv")
        # Vytvorí súbor 'vysledky.csv' s hlavičkou a dvoma riadkami dát.
    """
    if not data:
        print("Žádná data k uložení.")
        return

    hlavicka = data[0].keys()
    with open(
        nazev_souboru, mode="w", newline="", encoding="utf-8-sig"
    ) as soubor:
        writer = csv.DictWriter(soubor, fieldnames=hlavicka)
        writer.writeheader()
        writer.writerows(data)


@click.command()
@click.argument("url")
@click.argument("vystup_csv")
def main(url, vystup_csv):
    """
    Elections Scraper - nástroj na sťahovanie výsledkov volieb.
    URL: odkaz na územný celok z volby.cz
    VYSTUP_CSV: názov súboru, do ktorého sa uložia dáta.
    """
    if not url.startswith("https://www.volby.cz/pls/ps2017nss/"):
        click.echo("CHYBA: Neplatná URL adresa.")
        return

    # 2. Kontrola, zda odkaz vede na správný typ výsledků (územní celek)
    if "ps32" not in url:
        click.echo(
            "CHYBA: Nesprávný odkaz. Vyberte odkaz ze sloupce 'Výběr obce' (ps32)."
        )
        return

    if not vystup_csv.endswith(".csv"):
        click.echo("CHYBA: Výstupní soubor musí mít příponu .csv")
        return

    click.echo(f"Spracovávam dáta z: {url}")

    obsah_stranky = nacti_obsah_stranky(url)

    if obsah_stranky:
        data = ziskej_obce(obsah_stranky)
        uloz_do_csv(data, vystup_csv)
        click.echo(f"Hotovo! Výsledky sú v {vystup_csv}")
    else:
        click.echo(
            "CHYBA: Nepodarilo sa stiahnuť dáta. Skontrolujte pripojenie alebo URL."
        )

if __name__ == "__main__":
    main()
