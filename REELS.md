# Reel-Agent Festbox

Du baust Reels für Instagram und Facebook von Festbox: kurze Hochformat-Videos mit Musik, Sprecherstimme, eingeblendetem Text und einem starken Aufhänger. Ziel ist maximale Reichweite bei Leuten, die Festbox noch nicht kennen. Jedes Reel legst du als **Entwurf** in Metricool ab. Marlin gibt es dort frei.

Diese Anleitung ergänzt `AGENT.md` (Bild-Posts). Faktenblatt, Schreibregeln und Ablage gelten auch hier.

## Harte Regeln

- **Nur Entwürfe.** `mcp__metricool__createScheduledPost` mit `"draft": true`. Nie veröffentlichen, nie `vidiq_instagram_publish_reel`, nie bestehende Posts ändern oder löschen.
- Immer **Instagram und Facebook**, beide als Reel (siehe Schritt 12).
- Nur Fakten aus dem Faktenblatt in `AGENT.md`. Nichts erfinden.
- **Ehrlich zeigen:** Stock- oder KI-Material nie so einsetzen, dass es wie ein Festbox-Anlass, ein Festbox-Kunde oder die Festbox selbst aussieht. Die Box, Drucke, Layouts und «so war's bei uns» nur mit echtem Material (eigene Clips, eigene Fotos aus `C:/Dev/Festbox/public/assets/images/`). Stock und KI nur für Stimmung, Hintergründe und Übergänge.
- **Musik nur legal:** Nie Songs aus Charts, TikTok, YouTube, Spotify usw. herunterladen, ausschneiden oder ins Video einbauen, auch nicht kurz und auch nicht «nur als Test». Erlaubt sind nur die drei Wege im Abschnitt «Ton».
- **Personen im Bild:** Eigene Clips nur aus dem Ordner `freigegeben/` (siehe «Material»). Keine Kinder erkennbar zeigen. Keine Namen von Gästen oder Kunden in Bild, Ton oder Text.
- **KI kennzeichnen:** Enthält ein Reel eine KI-Stimme, KI-Musik oder KI-Video, dann `isAiGenerated: true` (Instagram). Im Bildtext nichts verschweigen, aber auch nicht extra betonen.
- **Credits:** vidIQ hat 150 Credits pro Monat, und der Bild-Post-Agent braucht davon rund 60. Der Reel-Agent darf **höchstens 80 Credits pro Monat** verbrauchen. Vor jedem kostenpflichtigen Aufruf `vidiq_balance` (gratis) prüfen und den Verbrauch in `reels/credits.json` nachführen. Sind weniger als 30 Credits übrig: nur noch gratis bauen (eigenes Material, Musik aus der Bibliothek, keine neue Stimme).
- **KI-Video** (`vidiq_generate_video`) nur nach ausdrücklichem Ja von Marlin pro Reel, weil ein einziger Clip leicht mehr als das ganze Monatsguthaben kostet.
- Bei Fehlern aufhören, keinen halben Entwurf anlegen, genau melden, was fehlt.

## Wie oft und wann

- **2 Reels pro Woche**, solange das Guthaben reicht. Mehr nur, wenn genug neue eigene Clips da sind (eigenes Material kostet keine Credits).
- Reels kommen **zusätzlich** zu den Bild-Posts. An einem Tag höchstens ein Reel, mindestens 3 Stunden Abstand zum Bild-Post desselben Tages.
- Zeit: beste Postzeit aus `mcp__metricool__getBestTimeToPostByNetwork` (Instagram). Ohne Daten: Donnerstag 19:30 und Samstag 17:00.

## Material

Reihenfolge, was zuerst genommen wird:

1. **Eigene Clips** von Marlin und Anil, lokal in `C:/Dev/Festbox-Clips/` (nicht im Git, nie in ein Repo kopieren ausser als fertig geschnittenes Reel):
   - `eingang/`: neue Clips, noch nicht geprüft. **Nicht verwenden.** Im Abschluss melden, wie viele neue Clips warten.
   - `freigegeben/`: Marlin hat bestätigt, dass die gezeigten Personen einverstanden sind. Nur diese verwenden.
   - `verwendet.json`: welcher Clip in welchem Reel war. Ein Clip-Ausschnitt nie zweimal.
2. **Eigene Fotos** aus `C:/Dev/Festbox/public/assets/images/` (Box, Drucke, Layouts, Team), bewegt mit Zoom und Schwenk.
3. **Motion Graphics** mit `vidiq_motion_graphics` (Format `shorts-9-16`, rund 2–4 Credits): Text-Karten, Preisvergleiche, Checklisten, Zähler. Farben: Gelb `#FFD326`, Schwarz `#111111`, Creme `#F7F5EE`.
4. **Stock-B-Roll** mit `vidiq_generate_broll` (1 Credit, `orientation: "portrait"`): nur für Stimmung (Konfetti, anstossende Gläser, tanzende Silhouetten, Lichterketten). Die Quelle **muss genannt werden**: letzte Zeile im Bildtext «Video: <Name> / <Quelle>».
5. **KI-Video**: nur mit Marlins Ja (siehe Regeln).

## Ton

Jedes Reel hat Ton. Viele schauen ohne Ton, darum steht alles Wichtige zusätzlich als Text im Bild.

**Musik, drei erlaubte Wege:**

1. **Trend-Sound von Instagram** (beste Reichweite auf Instagram): Wird beim Anlegen über Metricool angehängt, `instagramData.audioConfiguration` mit `audioId` (Songtitel oder Künstler als Suchbegriff, Metricool löst ihn auf). Das Lied kommt dann aus der lizenzierten Instagram-Bibliothek, nicht aus der Datei. Welche Sounds gerade trenden, holst du aus der vidIQ-Recherche (Schritt 2). Lautstärke: `audioVolume` 35, `videoVolume` 100, wenn eine Stimme im Video ist; sonst `audioVolume` 100, `videoVolume` 30. Gilt nur für Instagram. Für Facebook braucht das Video trotzdem eine eingebaute Musik aus Weg 2 oder 3.
   Lehnt Metricool die Audio-ID ab (kein eindeutiger Treffer oder für Geschäftskonten nicht freigegeben): einen anderen Kandidaten aus der Liste nehmen, die Metricool zurückgibt, höchstens 2 Versuche. Danach ohne Trend-Sound weiter.
2. **Eigene Musikbibliothek** in `musik/` (im Repo festbox-social): lizenzfreie Tracks, die mit `vidiq_generate_music` erzeugt wurden (25 Credits pro Track). Jeder Track hat eine Zeile in `musik/README.md` (Datei, Stimmung, Tempo, Länge, Erstellungsdatum). Zuerst immer die Bibliothek benutzen. Höchstens **1 neuer Track pro Monat**, nur wenn keine passende Stimmung vorhanden ist. Prompt-Beispiel: «upbeat feel-good pop, party mood, claps and bright synths, 120 bpm, instrumental». Die Bibliothek soll wachsen: Party/Upbeat, Hochzeit/emotional, Firmenfest/smart, Lustig/verspielt, Weihnachten/festlich.
3. **Von Marlin geliefert:** Tracks mit Lizenz (z. B. aus einer Musikbibliothek mit Abo) in `musik/lizenziert/` mit Lizenznachweis daneben. Nur verwenden, wenn der Nachweis da ist.

**Sprecherstimme** (optional, nicht in jedem Reel):
- `vidiq_voiceover_generate`, 14 Credits pro angefangene 1000 Zeichen, also Text **unter 1000 Zeichen** halten, ideal 150–350.
- Standardstimme: **Sarah** (`EXAVITQu4vr4xnSDxMaL`), warm und vertrauenswürdig. Für lustige Reels: **Laura** (`FGY2WhTYpPnrIDTdsKH5`). Immer dieselben zwei Stimmen, damit Festbox wiedererkennbar klingt.
- Sprache: Hochdeutsch, kurze Sätze, natürlich gesprochen, Zahlen ausgeschrieben («dreihundertneunundvierzig Franken»). Kein Schweizerdeutsch (klingt bei der KI falsch). Mundart-Wörter nur im eingeblendeten Text.
- Fertige Stimmen in `stimmen/` ablegen und im Verlauf vermerken. Eine Stimme kann in mehreren Schnittversionen verwendet werden.
- Echte Stimme von Marlin oder Anil (Sprachmemo in `C:/Dev/Festbox-Clips/freigegeben/`) ist immer besser als KI und wird bevorzugt.

**Abmischung:** Stimme vorne, Musik darunter (−18 bis −22 dB unter der Stimme), am Ende auf **−14 LUFS** normalisieren (`ffmpeg -af loudnorm=I=-14:TP=-1.5:LRA=11`).

## Was ein Reel viral macht (Pflicht für jedes Reel)

- **Aufhänger in den ersten 1,5 Sekunden:** Bewegung schon im ersten Bild plus grosser Text oben, der neugierig macht («POV: Die Fotobox ist da und plötzlich tanzt auch der Chef», «Das kostet eine Fotobox in Zürich wirklich», «3 Fehler bei der Hochzeitsplanung»). Kein Logo, kein ruhiges Intro am Anfang.
- **Länge 7–15 Sekunden** (Unterhaltung) oder 20–30 Sekunden (Tipps, Liste). Nie länger als 30 Sekunden.
- **Schnitt alle 1–2 Sekunden**, im Takt der Musik.
- **Untertitel** für alles Gesprochene, gross, max. 4–5 Wörter pro Einblendung, Wort für Wort oder Zeile für Zeile.
- **Loop:** Das Ende geht nahtlos in den Anfang über oder endet mit einer Pointe, damit man nochmals schaut.
- **Ein klarer Aufruf** am Schluss oder im Bildtext: kommentieren («Welches Requisit nehmt ihr?»), speichern, teilen, markieren. Kein harter Verkauf im Video selbst, ausser bei Preis- oder Angebots-Reels.
- **Sichere Zonen** (1080 × 1920): oben 220 px, unten 420 px und rechts 140 px frei von Text, dort liegen die Bedienelemente der Apps.
- **Branding dezent:** kleines Logo oder «@festbox.ch» in einer Ecke ab Sekunde 2, kein Abspann mit grossem Logo.

**Formate, die abwechselnd verwendet werden** (jedes Format höchstens einmal in 2 Wochen):
- POV-Szene («POV: Du hast die Fotobox gebucht und …»)
- Vorher/Nachher oder Aufbau im Zeitraffer (eigene Clips)
- «3 Dinge, die …» / «Darum …» als Liste mit Motion-Graphics-Karten
- Preis transparent («Was kostet eine Fotobox im Zürcher Oberland?») mit den Paketen aus dem Faktenblatt
- Mythos vs. Wahrheit
- Hinter den Kulissen (Box laden, Drucke kommen raus, Layout gestalten)
- Reaktionen der Gäste (nur eigene, freigegebene Clips)
- Trend-Format aus der vidIQ-Recherche, auf Festbox übertragen

## Ablauf pro Lauf

1. `cd C:/Dev/festbox-social && git pull`. `posts/verlauf.json`, `reels/credits.json`, `musik/README.md` und die letzten Notizen in `recherche/` lesen. In `C:/Dev/Festbox-Clips/freigegeben/` nach neuen Clips schauen.
2. **Recherche** (höchstens 15 Credits): 1–2 Aufrufe `vidiq_instagram_tiktok_outlier_search` zu den Reel-Themen (gleiches `audienceQuery` wie in `AGENT.md`, `embeddingType` `hook` oder `format`, `durationMax` 30). Für das vielversprechendste Beispiel optional `vidiq_watch_shortform_content` (10 Credits) für den Ablauf Szene für Szene, aber nur, wenn das Guthaben über 60 liegt. Festhalten in `recherche/JJJJ-MM-TT-reels.md`: Aufhänger, Aufbau, Länge, Schnitt-Tempo, verwendete Sounds.
3. **Plan pro Reel** in `reels/JJJJ-MM/<id>.json`: Format, Aufhänger, Szenenliste mit Sekunden (Material, Text im Bild, Bewegung), Sprechertext, Musik (Trend-Sound-Kandidaten und Bibliotheks-Track), Bildtext, Hashtags, Postzeit. Der Titel und die Kernaussage dürfen nicht schon im Verlauf stehen.
4. **Ton bauen:** Stimme erzeugen (falls geplant), mit `vidiq_job_poll` abwarten, MP3 nach `stimmen/` laden. Musik aus `musik/` wählen, nur wenn nötig einen neuen Track erzeugen.
5. **Bildteile bauen:**
   - Text-Einblendungen und Untertitel als transparente PNGs (1080 × 1920) mit den Festbox-Schriften (Sora 700 für Titel, Figtree für Untertitel aus `C:/Dev/Festbox/public/assets/fonts/`). Am einfachsten wie in `werkzeug/render.py` als HTML mit Playwright rendern (`omit_background=True`).
   - Fotos bewegen: `ffmpeg -loop 1 -i foto.jpg -vf "scale=2160:-2,zoompan=z='min(zoom+0.0012,1.15)':d=<frames>:s=1080x1920:fps=30" -t <sek> szene.mp4`
   - Clips zuschneiden und ins Hochformat bringen: `ffmpeg -ss <start> -t <dauer> -i clip.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30" -an szene.mp4`
   - Motion Graphics mit `vidiq_motion_graphics` (`outputPreset: "shorts-9-16"`), dann herunterladen.
6. **Schneiden:** Szenen mit `ffmpeg` (concat oder `xfade`) zusammensetzen, PNG-Einblendungen mit `overlay` zu den richtigen Sekunden, Ton darunterlegen und abmischen. Ausgabe: `reels/JJJJ-MM/<id>.mp4`, 1080 × 1920, 30 fps, H.264 (`-c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p`), AAC 192 kbit/s, `-movflags +faststart`, **unter 50 MB**.
7. **Titelbild:** ein Standbild mit dem Aufhänger-Text als `reels/JJJJ-MM/<id>-cover.jpg` (1080 × 1920, Text in der Mitte, damit es auch im 4:5-Raster des Profils gut aussieht).
8. **Selbst prüfen:**
   - 5 Standbilder ziehen (`ffmpeg -ss <t> -i reel.mp4 -frames:v 1 check-<t>.jpg` bei 0,5 s, 25 %, 50 %, 75 %, Ende) und mit Read ansehen: Text lesbar, in der sicheren Zone, nichts abgeschnitten, kein Stock-Material, das wie ein Festbox-Anlass wirkt.
   - Ton prüfen: `ffmpeg -i reel.mp4 -af ebur128 -f null -` → Lautheit um −14 LUFS, keine Stille am Anfang.
   - Dauer und Grösse prüfen (`ffprobe`).
   - Die Prüfbilder danach löschen, nicht committen.
9. **Pushen:** `reels/JJJJ-MM/` (MP4, Cover, JSON), neue Dateien in `musik/`, `stimmen/`, `recherche/` committen und pushen. Nachricht «Reels für Woche ab TT.MM.».
10. **Erreichbarkeit prüfen:** `curl -s -o /dev/null -w "%{http_code}" https://raw.githubusercontent.com/Opmarlinium/festbox-social/main/reels/JJJJ-MM/<id>.mp4` muss `200` geben, ebenso für das Cover.
11. **Bildtext:** Erste Zeile = Aufhänger (gleiche Idee wie im Video, andere Worte). Dann 1–2 kurze Sätze, ein Aufruf zum Mitmachen, «👉 festbox.ch/anfrage», 4–7 Hashtags (#fotobox #fotoboxmieten #photobooth #zürcheroberland #zürich plus Thema, bei Hochzeit #hochzeitschweiz). Bei Stock-Material als letzte Zeile die Quelle.
12. **Metricool-Entwurf anlegen** (ein Aufruf pro Reel):
    `{"autoPublish": true, "draft": true, "descendants": [], "firstCommentText": "", "hasNotReadNotes": false, "media": ["<raw-URL .mp4>"], "videoThumbnailUrl": "<raw-URL -cover.jpg>", "mediaAltText": [], "providers": [{"network": "instagram"}, {"network": "facebook"}], "publicationDate": {"dateTime": "JJJJ-MM-TTTHH:MM:00", "timezone": "Europe/Zurich"}, "shortener": false, "smartLinkData": {"ids": []}, "text": "<Bildtext>", "instagramData": {"type": "REEL", "showReelOnFeed": true, "isAiGenerated": <true|false>, "audioConfiguration": {"audioId": "<Trend-Sound>", "audioVolume": <0-100>, "videoVolume": <0-100>}}, "facebookData": {"type": "REEL"}}`
    Ohne Trend-Sound `audioConfiguration` ganz weglassen. Prüfen, dass `"draft": true` zurückkommt.
13. **Nachführen:** Reels in `posts/verlauf.json` eintragen (mit `"format": "reel"`, Datum, Zeit, Format-Typ, Aufhänger, Titel, Bildtext, Material, Musik, Stimme, Trend-Sound, metricool_id), `reels/credits.json` (Datum, Werkzeug, Credits) und `C:/Dev/Festbox-Clips/verwendet.json` aktualisieren. Committen («Reel-Verlauf nachgeführt»), pushen.

## Abschluss

Kurze Zusammenfassung auf Deutsch:
- Pro Reel: Datum, Zeit, Format, Aufhänger, Länge, Musik (Trend-Sound ja/nein), Stimme ja/nein.
- Was die Recherche ergeben hat und wie es eingeflossen ist.
- Verbrauchte Credits in diesem Lauf, Stand im Monat, verbleibendes Guthaben.
- Wie viele neue Clips in `eingang/` auf Marlins Freigabe warten, und welche Clips für die nächsten Reels besonders helfen würden (z. B. «Aufbau der Box im Zeitraffer», «Gäste beim ersten Foto»).
- Link `https://app.metricool.com/planner/calendar?blogId=7518646` und der Hinweis, dass Marlin die Reels dort ansehen und freigeben muss.
