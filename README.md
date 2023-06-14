# Třetí projekt do ENGETO Python akademie
## Popis projektu:
Projekt slouží k načtení výsledků voleb z roku 2017, který vytáhne data přímo z webu pro všechny obce z vybraného okresu z adresy https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ
## Instalace knihoven:
Seznam veškerých použitých knihoven je v souboru requirements.txt
Lze je jednoduše nainstalovat příkazem 
-  ```pip install -r requirements.txt```
Před instalací je doporučeno vytvořit a aktivovat virtuální prostředí pro tento projekt

## Spuštění projektu:
Pro spuštění projektu je vyžadováno zadání dvou argumentů - první je odkaz na požadovaný územní celek a druhý je jméno výstupního csv souboru.

## Ukázka spuštění
Vybraný územní celek: Prostějov, výstupní soubor: vysledky_prostejov.csv
- ``` python projekt3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_prostejov.csv" ```

## Ukázka výstupu:
code,location,registered,envelopes,valid,Občanská demokratická strana... 
506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
589268,Bedihošť,834,527,524,51,0,0,28,1,13,123,2,2,14,1,0,34,0,6,140,0,0,26,0,0,0,0,82,1
...
