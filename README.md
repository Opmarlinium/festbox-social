# festbox-social

Öffentliche Ablage für Instagram- und Facebook-Bilder von [Festbox](https://festbox.ch).
Metricool lädt die Bilder von hier, wenn ein Post geplant wird.

Nur fertige Post-Bilder ablegen, keine Kundendaten. Ordner: `posts/JJJJ-MM/`.

Der Post-Agent (Anleitung in `AGENT.md`) und der Reel-Agent (Anleitung in `REELS.md`) erstellt hier jede Woche neue Bilder mit `werkzeug/render.py` und legt sie in Metricool als Entwurf ab. Bisherige Posts stehen in `posts/verlauf.json`.
