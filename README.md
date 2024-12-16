# Projekt_3
Třetí projekt v engeto project má za cíl stáhnout výsledky voleb za územní celky u vybrané obce.
Pro tuto ukázku jsem zvolil Jihočeský kraj, okres České Budějovice.
Prázdné řádky v tabulce jsou u toho města, které má více volebních okrsků viz. ČB - 90

# Výsledky hlasování - první argument:
URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3101

# Výsledný soubor - druhý argument:
Soubor: vysledky_cb.scv

# Spuštění programu: 
python scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3101" "vysledky_cb.csv"

# Průběh stahování - program zobrazí informace o průběhu stahování 
Stahuji data z vybraného URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3101
Ukládám do souboru: vysledky_cb.csv
Ukončuji election-scraper

# Částečný výstup - po úspěšném spuštění program uloží data ve formátu CSV. Například:
Kód,Město,Voliči v seznamu,Vydané obálky,....
535826,Adamov,682,474,472,91,0,2,37,0,36,40,4,3,13,0,1,43,0,23,126,0,0,12,0,3,1,0,36,1,-
536156,Bečice,82,63,63,3,0,0,1,0,5,3,0,1,1,0,0,8,0,5,17,0,0,10,0,0,0,0,9,0,-

# Instalační knihovny:
Pro spuštění je nutné instalovat tyto knihovny:
- pip install beautifulsoup4
- pip install requests

# Vytvoření requirements s použitými knihovnami:
pip freeze > requirements.txt

