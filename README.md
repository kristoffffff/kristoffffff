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

A `testproject.freykristof.com.conf` fájl példát ad arra, hogyan tehető a Flask
alkalmazás elérhetővé a `testproject.freykristof.com` domainről. Másold ezt a
fájlt az Nginx `sites-available` könyvtárába, majd hozz létre egy szimbolikus
linket a `sites-enabled` mappába, és töltsd újra az Nginx szolgáltatást.

## cPaneles deploy

A gyökérkönyvtárban található `.cpanel.yml` fájl automatikusan a
`/home/kimondta/public_html/testproject.freykristof.com` könyvtárba másolja a
szükséges fájlokat minden `git push` után. A célútvonal a `DEPLOYPATH`
változóban módosítható, ha máshová szeretnéd telepíteni az alkalmazást.

Python‑alapú cPanel környezetben a `passenger_wsgi.py` fájl szolgál belépési
pontként a Flask alkalmazáshoz. A telepítés után ellenőrizd, hogy a cPanel
felületén engedélyezett Python alkalmazás erre a fájlra mutat, különben a
weboldal 403 Forbidden hibát adhat.


## Tesztek futtatása

```bash
pytest
```
