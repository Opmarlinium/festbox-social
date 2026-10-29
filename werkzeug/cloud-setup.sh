#!/usr/bin/env bash
# Einrichtung für die Cloud-Routinen (Post- und Reel-Agent). Lokal nicht nötig.
# Installiert Playwright mit Chromium, Pillow und ffmpeg und prüft, dass festbox-website neben diesem Repo liegt.
# ffmpeg: zuerst über apt (mit ffprobe), sonst das von imageio-ffmpeg mitgelieferte (ohne ffprobe).
set -e
cd "$(dirname "$0")/.."
python3 -m pip install -q --disable-pip-version-check playwright pillow imageio-ffmpeg
python3 -m playwright install --with-deps chromium >/dev/null 2>&1 || python3 -m playwright install chromium >/dev/null
if ! command -v ffmpeg >/dev/null 2>&1; then
  (apt-get install -y -qq ffmpeg >/dev/null 2>&1 || sudo -n apt-get install -y -qq ffmpeg >/dev/null 2>&1) || true
fi
if ! command -v ffmpeg >/dev/null 2>&1; then
  ff=$(python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
  ln -sf "$ff" /usr/local/bin/ffmpeg 2>/dev/null || { mkdir -p "$HOME/.local/bin" && ln -sf "$ff" "$HOME/.local/bin/ffmpeg"; echo "Hinweis: ffmpeg liegt in ~/.local/bin, vor ffmpeg-Befehlen export PATH=\$HOME/.local/bin:\$PATH"; }
fi
python3 -c "import sys; sys.path.insert(0, 'werkzeug'); import umgebung; print('festbox-website:', umgebung.FESTBOX); print('ffmpeg:', umgebung.FFMPEG)"
command -v ffprobe >/dev/null 2>&1 && echo "ffprobe: ja" || echo "ffprobe: nein (Dauer und Grösse mit ffmpeg -i bzw. ls prüfen)"
echo "Bereit. Python für die Werkzeuge: python3"
