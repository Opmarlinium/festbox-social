"""Wo die Werkzeuge laufen: lokal auf Marlins PC oder in der Cloud (Claude-Routine).

- FESTBOX: Checkout von festbox-website (Bilder, Schriften, Logos). Lokal C:/Dev/Festbox, in der Cloud der Ordner
  festbox-website neben diesem Repo. Mit der Umgebungsvariable FESTBOX_WEBSITE lässt sich ein anderer Pfad setzen.
- FFMPEG: ffmpeg aus dem PATH, sonst das von imageio-ffmpeg mitgelieferte.
- browser(pw): lokal das installierte Chrome, in der Cloud das Chromium von Playwright.
"""
import os, pathlib, shutil

HIER = pathlib.Path(__file__).resolve().parent
REPO = HIER.parent


def _festbox():
    kandidaten = [os.environ.get("FESTBOX_WEBSITE"), "C:/Dev/Festbox", REPO.parent / "festbox-website", REPO / "festbox-website"]
    for k in kandidaten:
        if k and (pathlib.Path(k) / "public/assets/images").is_dir():
            return pathlib.Path(k)
    raise SystemExit("festbox-website nicht gefunden (C:/Dev/Festbox oder ../festbox-website); in der Cloud zuerst werkzeug/cloud-setup.sh")


def _ffmpeg():
    pfad = shutil.which("ffmpeg")
    if pfad:
        return pfad
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        raise SystemExit("ffmpeg fehlt: in der Cloud zuerst werkzeug/cloud-setup.sh")


FESTBOX = _festbox()
FFMPEG = _ffmpeg()


def browser(pw):
    try:
        return pw.chromium.launch(channel="chrome")
    except Exception:
        return pw.chromium.launch()
