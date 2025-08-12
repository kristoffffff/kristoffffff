# Projektregisztrációs applikáció

Ez az egyszerű parancssori és webes alkalmazás lehetővé teszi projektek rögzítését a megadott mezőkkel:

- Tervezett kezdés és zárás vagy időtartam
- Célok (bővíthető lista)
- Stakeholderek PMI szerepkörökkel, címkékkel és dedikációval
- Büdzsé és annak jóváhagyása
- Kockázatok valószínűséggel és hatásterülettel
- Feltételezések
- Projekthez tartozó linkek

## Használat

CLI indítása:

```bash
python -m project_registry.cli
```

Webes felület indítása (Flask fejlesztői szerver):

```bash
python -m project_registry.web
```

A rögzített projektek a `projects.json` fájlban kerülnek tárolásra.


## Nginx konfiguráció
A `testproject.freykristof.com.conf` fájl példa arra, hogyan tehető a Flask alkalmazás elérhetővé.

## cPanels deploy
A gyökérkönyvtárban található `.cpanel.yml` fájl automatikusan a `/home/kimondta/public_html/...` mappába másolja a szükséges fájlokat.


## Tesztek futtatása

```bash
pytest
```
