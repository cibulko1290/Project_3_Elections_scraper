'''
project_3.py : third project from Engeto Online Python Academy
author: Lucia Luptakova
email:lucy.luptakova"gmail.com
'''
import requests
from bs4 import BeautifulSoup as bs

def nacti_obsah_stranky (url: str):
  try:
    odpoved = requests.get(url)
    odpoved.raise_for_status()
    soup = bs(odpoved.text, 'html.parser')
    return soup
  except requests.exceptions.RequestException:
    return None

def ziskej_cenu_zlata (rozdeleny_text):
  element_ceny = rozdeleny_text.find('span', class_='price-section__current-value')
  if element_ceny:
    return element_ceny.get_text()
  else:
    return None

def main():
  url = 'https://markets.businessinsider.com/commodities/gold-price'

  objekt_soup = nacti_obsah_stranky(url)
  if objekt_soup is None:
    print("Nedostupný HTML objekt")
    vysledek = None
  else:
    CENA_ZLATA = ziskej_cenu_zlata(objekt_soup)
    if CENA_ZLATA is None:
      print("Nedostupná cena" )
      vysledek = None
    else:
      print(f"Aktuální cena zlata $: {CENA_ZLATA}")

main()