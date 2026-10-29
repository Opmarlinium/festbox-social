#!/usr/bin/env bash
# Einrichtung für die Cloud-Routinen (Post- und Reel-Agent). Lokal nicht nötig.
# Legt eine eigene Python-Umgebung an (/tmp/fbvenv), installiert dort Playwright mit Chromium, Pillow und
# imageio-ffmpeg, sorgt für ffmpeg und prüft, dass festbox-website neben diesem Repo liegt.
# Der Python-Aufruf für die Werkzeuge steht danach in werkzeug/.python (nicht im Git).
set -e
cd "$(dirname "$0")/.."
VENV=/tmp/fbvenv
PY=python3
if [ -x "$VENV/bin/python" ] || python3 -m venv "$VENV" >/dev/null 2>&1 || { python3 -m venv --without-pip "$VENV" >/dev/null 2>&1 && curl -sS https://bootstrap.pypa.io/get-pip.py | "$VENV/bin/python" - -q >/dev/null 2>&1; }; then
  PY="$VENV/bin/python"
fi
"$PY" -m pip install -q --disable-pip-version-check playwright pillow imageio-ffmpeg 2>&1 | grep -v -i "running pip as the 'root'" || true
"$PY" -m playwright install --with-deps chromium >/dev/null 2>&1 || "$PY" -m playwright install chromium >/dev/null
if ! command -v ffmpeg >/dev/null 2>&1; then
  (apt-get install -y -qq ffmpeg >/dev/null 2>&1 || sudo -n apt-get install -y -qq ffmpeg >/dev/null 2>&1) || true
fi
if ! command -v ffmpeg >/dev/null 2>&1; then
  ff=$("$PY" -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
  ln -sf "$ff" /usr/local/bin/ffmpeg 2>/dev/null || { mkdir -p "$HOME/.local/bin" && ln -sf "$ff" "$HOME/.local/bin/ffmpeg"; echo "Hinweis: ffmpeg liegt in ~/.local/bin, vor ffmpeg-Befehlen export PATH=\$HOME/.local/bin:\$PATH"; }
fi
"$PY" -c "import PIL.Image, playwright; import sys; sys.path.insert(0, 'werkzeug'); import umgebung; print('Python:', sys.version.split()[0], sys.executable); print('festbox-website:', umgebung.FESTBOX); print('ffmpeg:', umgebung.FFMPEG)"
echo "$PY" > werkzeug/.python
command -v ffprobe >/dev/null 2>&1 && echo "ffprobe: ja" || echo "ffprobe: nein (Dauer und Grösse mit ffmpeg -i bzw. ls prüfen)"
echo "Bereit. Python für die Werkzeuge: $PY (steht in werkzeug/.python)"
