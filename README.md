# Documentation of Elections scraper

# 🗳️ Elections Scraper

Tento Python skript slouží k automatizovanému sběru výsledků z parlamentních voleb konaných v roce 2017. Data čerpá z oficiálního serveru [volby.cz](https://www.volby.cz/).

## 🛠️ Instalace a požadavky

Projekt využívá virtuální prostředí a několik externích knihoven. Pro správný chod postupujte následovně:

1. **Klonování projektu nebo stažení souborů.**
2. **Vytvoření a aktivace virtuálního prostředí:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate

3. **Instalace potřebných knihoven:**

    ```powershell
    pip install -r requirements.txt

## 🖥️ Ukázka projektu

Skript se spouští z terminálu a vyžaduje dva argumenty:

- URL adresu konkrétního územního celku (např. okresu Prostějov)
- Název CSV souboru, do kterého se uloží výsledky.


**Příklad spuštění:**

    ```powershell
    python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_prostejov.csv"

Průbeh stahování:

<p>Spracovávam dáta z: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
Stahuji data pro: Alojzov<br>
Stahuji data pro: Bedihošť<br>
Stahuji data pro: Bílovice-Lutotín<br>
...</p>


Částečný výstup se souboru csv:

code,location,registred,envelopes,valid,Občanská demokratická strana, ...
506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
589268,Bedihošť,834,527,524,51,0,0,28,1,13,123,2,2,14,1,0,34,0,6,140,0,0,26,0,0,0,0,82,1

## 📊 Popis výstupu

Výsledné CSV obsahuje pro každou obec tyto údaje:

* Identifikační kód obce
* Název obce
* Počet registrovaných voličů
* Počet vydaných obálek
* Počet platných hlasů
* Výsledky jednotlivých kandidujících stran (hlasy)


### ✍️ Autor
> Vytvořeno jako závěrečný projekt v rámci kurzu Datový analytik s Pythonem.