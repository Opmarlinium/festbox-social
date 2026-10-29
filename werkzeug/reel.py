"""Baut ein Festbox-Reel (1080 x 1920, 30 fps, H.264/AAC) aus Fotos, Text-Einblendungen, Stimme und Musik.

Aufruf lokal:
  C:/Dev/Festbox/tools/bildwerkstatt/.venv/Scripts/python.exe -I werkzeug/reel.py reels/2026-10/<id>.json
In der Cloud nach werkzeug/cloud-setup.sh: python3 werkzeug/reel.py reels/2026-10/<id>.json

Schreibt <ordner>/<id>.mp4 und <ordner>/<id>-cover.jpg. Zwischendateien landen in <ordner>/_arbeit/ (nicht committen).
Felder: siehe werkzeug/README.md, Abschnitt «Reels».
"""
import html, json, pathlib, shutil, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from umgebung import FESTBOX, FFMPEG, browser  # lokal C:/Dev/Festbox, in der Cloud ../festbox-website
BILDER = FESTBOX / "public/assets/images"
FONTS = FESTBOX / "public/assets/fonts"
LOGO = FESTBOX / "grafiken/social-media/festbox-logo-dunkel-600.png"
W, H, FPS = 1080, 1920, 30

CSS = """
@font-face{font-family:Sora;src:url(SORA) format("woff2");font-weight:700}
@font-face{font-family:Figtree;src:url(FIGTREE) format("woff2");font-weight:300 900}
*{box-sizing:border-box;margin:0}
html,body{background:transparent}
.f{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Figtree,sans-serif;color:#F7F5EE}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(17,17,17,.55) 0%,rgba(17,17,17,0) 30%,rgba(17,17,17,0) 45%,rgba(17,17,17,.75) 75%,rgba(17,17,17,.85) 100%)}
.oben{position:absolute;top:250px;left:80px;right:160px;font-family:Sora;font-weight:700;font-size:78px;line-height:1.02;letter-spacing:-.04em;text-shadow:0 4px 24px rgba(0,0,0,.45)}
.oben em,.gross em{font-style:normal;color:#FFD326}
.mitte{position:absolute;left:80px;right:160px;bottom:520px}
.marke{display:inline-block;background:#FFD326;color:#111;font-weight:800;font-size:40px;padding:10px 22px;border-radius:12px;letter-spacing:.02em}
.gross{font-family:Sora;font-weight:700;font-size:150px;line-height:.95;letter-spacing:-.05em;margin:22px 0 18px;color:#FFD326}
.klein{font-size:50px;font-weight:600;line-height:1.2;color:#F7F5EE}
.logo{position:absolute;top:120px;right:150px;height:52px;opacity:.95}
.unten{position:absolute;left:80px;right:160px;bottom:430px;font-size:44px;font-weight:700}
"""


def esc_em(s):
    out, parts = [], html.escape(s or "").split("*")
    for i, p in enumerate(parts):
        out.append(f"<em>{p}</em>" if i % 2 else p)
    return "".join(out).replace("\n", "<br>")


def overlay_html(sz, logo):
    teile = ['<div class="shade"></div>']
    if logo:
        teile.append(f'<img class="logo" src="{LOGO.as_uri()}">')
    if sz.get("oben"):
        teile.append(f'<div class="oben">{esc_em(sz["oben"])}</div>')
    mitte = ""
    if sz.get("marke"):
        mitte += f'<span class="marke">{html.escape(sz["marke"])}</span>'
    if sz.get("gross"):
        mitte += f'<div class="gross">{esc_em(sz["gross"])}</div>'
    if sz.get("klein"):
        mitte += f'<div class="klein">{esc_em(sz["klein"])}</div>'
    if mitte:
        teile.append(f'<div class="mitte">{mitte}</div>')
    if sz.get("unten"):
        teile.append(f'<div class="unten">{esc_em(sz["unten"])}</div>')
    return f'<div class="f">{"".join(teile)}</div>'


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"Fehler bei: {' '.join(map(str, cmd))}\n{r.stderr[-2000:]}")
    return r.stdout


def bewegung(art, n):
    # Ausdruck für ffmpeg zoompan, Bild vorher auf 2160 x 3840 gebracht
    if art == "zoom-out":
        return f"z='1.18-0.18*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    if art == "pan-links":
        return f"z='1.15':x='(iw-iw/zoom)*(1-on/{n})':y='ih/2-(ih/zoom/2)'"
    if art == "pan-rechts":
        return f"z='1.15':x='(iw-iw/zoom)*on/{n}':y='ih/2-(ih/zoom/2)'"
    return f"z='1+0.18*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"  # zoom-in


def main():
    spec_pfad = pathlib.Path(sys.argv[1]).resolve()
    spec = json.loads(spec_pfad.read_text(encoding="utf-8"))
    ordner, rid = spec_pfad.parent, spec["id"]
    arbeit = ordner / "_arbeit" / rid
    if arbeit.exists():
        shutil.rmtree(arbeit)
    arbeit.mkdir(parents=True)
    szenen = spec["szenen"]

    # 1) Text-Einblendungen als transparente PNGs
    css = CSS.replace("SORA", (FONTS / "sora-700-latin.woff2").as_uri()).replace("FIGTREE", (FONTS / "figtree-latin.woff2").as_uri())
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = browser(pw)
        pg = b.new_page(viewport={"width": W, "height": H})
        for i, sz in enumerate(szenen):
            seite = arbeit / f"o{i}.html"
            seite.write_text(f'<!doctype html><meta charset="utf-8"><style>{css}</style>{overlay_html(sz, i > 0 and spec.get("logo", True))}', encoding="utf-8")
            pg.goto(seite.as_uri())
            pg.wait_for_timeout(300)
            pg.screenshot(path=str(arbeit / f"o{i}.png"), omit_background=True)
        b.close()

    # 2) Szenen: Foto bewegen oder Clip zuschneiden, Einblendung darüber
    teile = []
    for i, sz in enumerate(szenen):
        n = round(sz["dauer"] * FPS)
        out = arbeit / f"s{i}.mp4"
        if sz.get("clip"):
            # Video-Clip: Pfad relativ zur JSON-Datei oder absolut; Ton des Clips wird verworfen
            clip = (ordner / sz["clip"]).resolve()
            if not clip.exists():
                raise SystemExit(f"Clip fehlt: {clip}")
            tempo = sz.get("tempo", 1.0)  # 0.5 = Zeitlupe, 2 = doppelt so schnell
            vf = (f"[0:v]setpts=PTS/{tempo},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                  f"fps={FPS},setsar=1,tpad=stop_mode=clone:stop_duration={sz['dauer']}[bg];"
                  f"[bg][1:v]overlay=0:0,format=yuv420p[v]")
            run([FFMPEG, "-y", "-ss", str(sz.get("start", 0)), "-i", str(clip), "-i", str(arbeit / f"o{i}.png"),
                 "-filter_complex", vf, "-map", "[v]", "-frames:v", str(n), "-an",
                 "-c:v", "libx264", "-preset", "medium", "-crf", "18", str(out)])
        else:
            bild = BILDER / sz["bild"]
            if not bild.exists():
                raise SystemExit(f"Bild fehlt: {bild}")
            vf = (f"[0:v]scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
                  f"zoompan={bewegung(sz.get('bewegung', 'zoom-in'), n)}:d={n}:s={W}x{H}:fps={FPS},setsar=1[bg];"
                  f"[bg][1:v]overlay=0:0,format=yuv420p[v]")
            run([FFMPEG, "-y", "-loop", "1", "-i", str(bild), "-i", str(arbeit / f"o{i}.png"),
                 "-filter_complex", vf, "-map", "[v]", "-frames:v", str(n), "-r", str(FPS),
                 "-c:v", "libx264", "-preset", "medium", "-crf", "18", str(out)])
        teile.append(out)

    # 3) Szenen aneinanderhängen (harte Schnitte im Takt)
    liste = arbeit / "liste.txt"
    liste.write_text("".join(f"file '{p.as_posix()}'\n" for p in teile), encoding="utf-8")
    stumm = arbeit / "stumm.mp4"
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(liste), "-c", "copy", str(stumm)])
    dauer = sum(s["dauer"] for s in szenen)

    # 4) Ton: Musik (+ Stimme), Ende ausblenden, auf -14 LUFS
    ein, filt, mix = ["-i", str(stumm)], [], []
    idx = 1
    if spec.get("musik"):
        ein += ["-i", str((ordner / spec["musik"]).resolve())]
        vol = spec.get("musik_db", -18 if spec.get("stimme") else -4)
        filt.append(f"[{idx}:a]atrim=0:{dauer},asetpts=PTS-STARTPTS,volume={vol}dB,afade=t=out:st={dauer - 0.6}:d=0.6[m]")
        mix.append("[m]")
        idx += 1
    if spec.get("stimme"):
        ein += ["-i", str((ordner / spec["stimme"]).resolve())]
        ms = int(spec.get("stimme_start", 0.2) * 1000)
        filt.append(f"[{idx}:a]adelay={ms}|{ms},volume={spec.get('stimme_db', 0)}dB[s]")
        mix.append("[s]")
        idx += 1
    ziel = ordner / f"{rid}.mp4"
    if mix:
        filt.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{dauer},"
                    f"loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]")
        run([FFMPEG, "-y", *ein, "-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[a]",
             "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", str(dauer), str(ziel)])
    else:
        shutil.copy(stumm, ziel)

    # 5) Titelbild: erstes Bild der ersten Szene (mit Aufhänger)
    run([FFMPEG, "-y", "-ss", "0.8", "-i", str(ziel), "-frames:v", "1", "-q:v", "2", str(ordner / f"{rid}-cover.jpg")])
    print(f"ok: {ziel.name} ({dauer:.1f} s)")


if __name__ == "__main__":
    main()
