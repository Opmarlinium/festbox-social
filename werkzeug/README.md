# Render-Werkzeug

`render.py` macht aus einer JSON-Datei fertige Post-Bilder (1080 × 1350, JPG) im Festbox-Stil.
Schriften, Logos und Fotos kommen aus der Website (lokal `C:/Dev/Festbox`, in der Cloud `../festbox-website`, nur lesen; siehe `umgebung.py`). In der Cloud zuerst `bash werkzeug/cloud-setup.sh`, dann `python3` statt des Bildwerkstatt-Pythons.

```
C:/Dev/Festbox/tools/bildwerkstatt/.venv/Scripts/python.exe -I werkzeug/render.py posts/2026-11/2026-11-02.json
```

## Felder für alle Layouts

- `id`: Dateiname ohne Endung, nur Kleinbuchstaben, Zahlen und Bindestriche.
- `layout`: `foto`, `panel`, `schritte`, `liste` oder `zitat`.
- `titel`: Überschrift. `*Wort*` hebt hervor (gelb auf Foto/Dunkel, unterstrichen auf Gelb). `\n` erzwingt einen Zeilenumbruch.
- `text`: Untertitel (optional).
- `fuss`: zwei Texte unten links und rechts, Standard `["festbox.ch", "Zürcher Oberland"]`.

## Layouts

| Layout | Wofür | Eigene Felder |
|---|---|---|
| `foto` | Stimmung, Anlässe: Foto über die ganze Fläche, Text unten | `bild`, `bildposition` (CSS, z. B. `"50% 30%"`), `tag` |
| `panel` | Foto oben, gelbes Feld unten | `bild`, `bildposition`, `tag`, optional `polaroid` (2. Bild) und `polaroid_text` |
| `schritte` | Ablauf, Tipps, Checklisten: Gelb mit 3 nummerierten Punkten | `schritte`: Liste mit `titel` und `text` |
| `liste` | Pakete, Zusätze, Vergleiche: Dunkel mit Zeilen | `zeilen`: Liste mit `kurz`, `titel`, `text`, `wert`, `einheit`, `hervorheben` |
| `zitat` | Frage oder Spruch auf Gelb, kleines Foto unten rechts | `bild` (optional), `bildposition` |

Längen als Richtwert: Titel bis ca. 40 Zeichen (`foto`, `panel`), Untertitel bis ca. 110 Zeichen, bei `schritte` pro Punkt-Text bis ca. 70 Zeichen.

## Reels (`reel.py`)

```
C:/Dev/Festbox/tools/bildwerkstatt/.venv/Scripts/python.exe -I werkzeug/reel.py reels/2026-10/<id>.json
```

Oberste Felder: `id`, `musik` und `stimme` (Pfade relativ zur JSON-Datei, beide optional), `stimme_start` (Sekunden, Standard 0.2), `musik_db` (Standard −18 mit Stimme, −4 ohne), `stimme_db`, `logo` (true: kleines Logo ab Szene 2), `szenen`.

Pro Szene: entweder `bild` (aus `C:/Dev/Festbox/public/assets/images/`) mit `bewegung` (`zoom-in`, `zoom-out`, `pan-links`, `pan-rechts`), oder `clip` (Videodatei, Pfad relativ zur JSON-Datei oder absolut) mit `start` (Sekunde im Clip) und optional `tempo` (0.5 = Zeitlupe, 2 = doppelt so schnell). Dazu `dauer` (Sekunden) und Text: `oben` (Aufhänger oben), `marke` (gelbes Schild), `gross` (grosse gelbe Zahl oder Wort), `klein` (Zeilen darunter, `\n` für neue Zeile), `unten` (z. B. Link). `*Wort*` hebt gelb hervor.

Ausgabe: `<id>.mp4` (1080 × 1920, 30 fps, H.264, AAC, −14 LUFS) und `<id>-cover.jpg`. Zwischendateien in `_arbeit/` (wird nicht committet).
