# Weltzeit-Anzeige — Addon für die Bat Innovations Toolbox

Zeigt die aktuelle Uhrzeit in mehreren Zeitzonen gleichzeitig an, live
aktualisiert (jede Sekunde). Standardmäßig sind Berlin, London, New York,
Los Angeles, Tokio und Sydney eingetragen — weitere Zeitzonen lassen sich
direkt im Addon-Fenster per Dropdown hinzufügen oder entfernen.

Keine externen Abhängigkeiten — nutzt nur die Python-Standardbibliothek
(`zoneinfo`, ab Python 3.9 enthalten).

---

## 1. Auf GitHub veröffentlichen

```bash
cd addon-weltzeit
git init
git add .
git commit -m "Weltzeit-Anzeige Addon"
git branch -M main
git remote add origin https://github.com/DevTheFuture1/Time-addon-BatBox
git push -u origin main
```

Passe davor in `manifest.json` das Feld `"github_url"` und `"author"` an
deine eigenen Angaben an.

---

## 2. In der Bat Innovations Toolbox installieren

1. Toolbox öffnen → **Addon-Manager** oder **Addon-Store**
2. Button **"+ Addon hinzufügen"** bzw. **"+ Aus GitHub laden"** klicken
3. Tab **"GitHub-Repo"** wählen
4. Repository-URL eintragen: `https://github.com/DevTheFuture1/Time-addon-BatBox`
5. **"⬇ Addon hinzufügen"** klicken

Die Toolbox lädt das Repo automatisch als ZIP herunter, prüft die
`manifest.json` und installiert das Addon nach `/addons/weltzeit_anzeige/`.

Danach im Addon-Manager auf **"Aktivieren"** und **"Öffnen"** klicken.

---

## Lokal testen (ohne Toolbox)

```bash
pip install PySide6
python main.py
```

*(Für den lokalen Test brauchst du zusätzlich eine Kopie von
`core/addon_base.py` aus der Haupt-Toolbox im Python-Pfad, da `main.py`
`from core.addon_base import BatAddon` importiert — am einfachsten testest
du direkt innerhalb eines geklonten Toolbox-Projektordners.)*

---

## Eigene Zeitzonen als Standard eintragen

In `main.py` ganz oben:

```python
DEFAULT_CITIES = [
    ("Berlin", "Europe/Berlin"),
    ("London", "Europe/London"),
    # eigene Städte hier ergänzen, z. B.:
    ("Dubai", "Asia/Dubai"),
]
```

Gültige Zeitzonen-Namen findest du in der
[IANA-Zeitzonendatenbank](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
(Spalte "TZ identifier").
