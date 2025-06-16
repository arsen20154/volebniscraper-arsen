# Volební scraper

## O co jde v projektu?

Tento skript získá výsledky parlamentních voleb 2017 z [volby.cz](https://volby.cz) pro vybraný okres a uloží je do CSV souboru.

## Jak to spustit?

1. Nainstalujte závislosti:
```bash
pip install -r requirements.txt
```

2. Spusťte skript s parametry:
```bash
python analyza_voleb_arsen.py <URL_na_okres> <vystup.csv>
```

Např.:
```bash
python analyza_voleb_arsen.py https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xokres=10 cheb_volby17.csv
```

## Autor

Arsen Aloyan  
Email: aloyanarsen3@gmail.com
