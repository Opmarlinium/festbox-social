"""Rendert Festbox-Posts (1080 x 1350) aus einer JSON-Datei.

Aufruf (mit dem Python aus der Bildwerkstatt, dort ist Playwright installiert):
  C:/Dev/Festbox/tools/bildwerkstatt/.venv/Scripts/python.exe -I werkzeug/render.py posts/2026-11/stapel.json

Schreibt pro Post <ordner>/<id>.jpg und eine Kontrollseite <ordner>/vorschau.html.
Felder pro Post: siehe werkzeug/README.md.
"""
import html, json, pathlib, sys

FESTBOX = pathlib.Path("C:/Dev/Festbox")
BILDER = FESTBOX / "public/assets/images"
FONTS = FESTBOX / "public/assets/fonts"
LOGO_HELL = FESTBOX / "grafiken/social-media/festbox-logo-dunkel-600.png"   # helle Schrift, für dunkle Flächen
LOGO_DUNKEL = FESTBOX / "grafiken/social-media/festbox-logo-hell-600.png"   # dunkle Schrift, für Gelb

CSS = """
@font-face{font-family:Sora;src:url(%(sora)s) format("woff2");font-weight:700}
@font-face{font-family:Figtree;src:url(%(figtree)s) format("woff2");font-weight:300 900}
:root{--y:#FFD326;--ink:#111;--cream:#F7F5EE;--olive:#4A4A1A}
*{box-sizing:border-box;margin:0}
body{background:#888;font-family:Figtree,sans-serif;color:var(--ink)}
.post{width:1080px;height:1350px;position:relative;overflow:hidden;margin:0 0 40px}
h1,h2,.num{font-family:Sora,sans-serif;font-weight:700;letter-spacing:-.055em;line-height:.98}
h1 em{font-style:normal;color:var(--y)}
.logo{position:absolute;top:56px;left:64px;height:56px;z-index:3}
.foot{position:absolute;left:64px;right:64px;bottom:56px;display:flex;justify-content:space-between;font-size:30px;font-weight:600;z-index:3}
.photo{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover}
.tag{display:inline-block;background:var(--y);color:var(--ink);font-weight:800;font-size:30px;padding:12px 22px;border-radius:10px;letter-spacing:.02em}

.foto .shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(17,17,17,.5) 0%%,rgba(17,17,17,0) 18%%,rgba(17,17,17,0) 42%%,rgba(17,17,17,.92) 82%%)}
.foto .txt{position:absolute;left:64px;right:64px;bottom:150px;color:var(--cream)}
.foto h1{font-size:112px;margin:24px 0 26px}
.foto p{font-size:36px;line-height:1.35;color:#E4E2DA;max-width:900px}
.foto .foot{color:var(--cream)}

.panel .photo{height:760px}
.panel .box{position:absolute;left:0;right:0;bottom:0;height:610px;background:var(--y);padding:64px 64px 0}
.panel h1{font-size:104px;margin:22px 0 26px}
.panel h1 em{color:var(--ink);text-decoration:underline;text-decoration-thickness:8px;text-underline-offset:10px}
.panel p{font-size:36px;line-height:1.35;color:var(--olive);max-width:900px}
.panel .tag{background:var(--ink);color:var(--y)}
.panel .polaroid{position:absolute;right:64px;top:430px;width:250px;padding:16px 16px 60px;background:#fff;transform:rotate(6deg);box-shadow:0 18px 40px rgba(0,0,0,.35);z-index:2}
.panel .polaroid img{width:100%%;height:230px;object-fit:cover;display:block}
.panel .polaroid span{position:absolute;bottom:14px;left:0;right:0;text-align:center;font:600 26px Figtree}

.schritte{background:var(--y);padding:200px 64px 0}
.schritte h1{font-size:120px;margin-bottom:70px}
.schritte h1 em{color:var(--ink);text-decoration:underline;text-decoration-thickness:8px;text-underline-offset:10px}
.schritte .step{display:grid;grid-template-columns:150px 1fr;gap:28px;padding:38px 0;border-top:3px solid var(--ink)}
.schritte .num{font-size:96px}
.schritte h2{font-size:52px;letter-spacing:-.04em;margin:6px 0 12px}
.schritte .step p{font-size:32px;line-height:1.35;color:var(--olive)}

.liste{background:var(--ink);color:var(--cream);padding:190px 64px 0}
.liste h1{font-size:120px;margin-bottom:54px}
.liste .row{display:grid;grid-template-columns:110px 1fr auto;align-items:center;gap:30px;padding:34px 36px;border-radius:16px;background:#1f1f1d;margin-bottom:20px}
.liste .row.hot{background:var(--y);color:var(--ink)}
.liste .size{font-family:Sora;font-weight:700;font-size:84px;letter-spacing:-.05em}
.liste .row h2{font-size:44px;letter-spacing:-.03em}
.liste .row p{font-size:28px;color:#C7C9BF;margin-top:6px}
.liste .row.hot p{color:var(--olive)}
.liste .price{font-family:Sora;font-weight:700;font-size:54px;letter-spacing:-.04em;text-align:right}
.liste .price small{display:block;font:600 24px Figtree;letter-spacing:0}
.liste .incl{font-size:29px;line-height:1.4;color:#C7C9BF;margin-top:26px}

.zitat{background:var(--y);padding:220px 64px 0}
.zitat .mark{font-family:Sora;font-weight:700;font-size:180px;line-height:.6;height:90px}
.zitat h1{font-size:96px;margin:30px 0 40px}
.zitat h1 em{color:var(--ink);text-decoration:underline;text-decoration-thickness:8px;text-underline-offset:10px}
.zitat p{font-size:36px;line-height:1.35;color:var(--olive)}
.zitat .photo{position:absolute;inset:auto 64px 150px auto;width:360px;height:360px;border-radius:16px}
"""


def esc(s):
    return html.escape(s or "")


def headline(s):
    # *Wort* wird hervorgehoben (gelb bzw. unterstrichen)
    out, parts = [], esc(s).split("*")
    for i, part in enumerate(parts):
        out.append(f"<em>{part}</em>" if i % 2 else part)
    return "".join(out).replace("\n", "<br>")


def bild(name):
    p = BILDER / name
    if not p.exists():
        raise SystemExit(f"Bild fehlt: {p}")
    return p.as_uri()


def foot(post):
    links, rechts = post.get("fuss", ["festbox.ch", "Zürcher Oberland"])
    return f'<div class="foot"><span>{esc(links)}</span><span>{esc(rechts)}</span></div>'


def render_post(post):
    lay, pid = post["layout"], post["id"]
    tag = f'<span class="tag">{esc(post["tag"])}</span>' if post.get("tag") else ""
    text = f'<p>{esc(post.get("text"))}</p>' if post.get("text") else ""
    pos = post.get("bildposition", "50% 40%")
    if lay == "foto":
        return f'''<section class="post foto" id="{pid}">
  <img class="photo" style="object-position:{pos}" src="{bild(post["bild"])}"><div class="shade"></div>
  <img class="logo" src="{LOGO_HELL.as_uri()}">
  <div class="txt">{tag}<h1>{headline(post["titel"])}</h1>{text}</div>{foot(post)}</section>'''
    if lay == "panel":
        pol = ""
        if post.get("polaroid"):
            pol = f'<div class="polaroid"><img src="{bild(post["polaroid"])}"><span>{esc(post.get("polaroid_text", ""))}</span></div>'
        return f'''<section class="post panel" id="{pid}">
  <img class="photo" style="object-position:{pos}" src="{bild(post["bild"])}">
  <img class="logo" src="{LOGO_HELL.as_uri()}">{pol}
  <div class="box">{tag}<h1>{headline(post["titel"])}</h1>{text}</div>{foot(post)}</section>'''
    if lay == "schritte":
        steps = "".join(
            f'<div class="step"><div class="num">{i:02d}</div><div><h2>{esc(s["titel"])}</h2><p>{esc(s["text"])}</p></div></div>'
            for i, s in enumerate(post["schritte"], 1))
        return f'''<section class="post schritte" id="{pid}">
  <img class="logo" src="{LOGO_DUNKEL.as_uri()}"><h1>{headline(post["titel"])}</h1>{steps}{foot(post)}</section>'''
    if lay == "liste":
        rows = "".join(
            f'<div class="row{" hot" if r.get("hervorheben") else ""}"><div class="size">{esc(r["kurz"])}</div>'
            f'<div><h2>{esc(r["titel"])}</h2><p>{esc(r["text"])}</p></div>'
            f'<div class="price">{esc(r["wert"])}<small>{esc(r.get("einheit", ""))}</small></div></div>'
            for r in post["zeilen"])
        incl = f'<p class="incl">{esc(post.get("text"))}</p>' if post.get("text") else ""
        return f'''<section class="post liste" id="{pid}">
  <img class="logo" src="{LOGO_HELL.as_uri()}"><h1>{headline(post["titel"])}</h1>{rows}{incl}{foot(post)}</section>'''
    if lay == "zitat":
        ph = f'<img class="photo" style="object-position:{pos}" src="{bild(post["bild"])}">' if post.get("bild") else ""
        return f'''<section class="post zitat" id="{pid}">
  <img class="logo" src="{LOGO_DUNKEL.as_uri()}"><div class="mark">«</div>
  <h1>{headline(post["titel"])}</h1>{text}{ph}{foot(post)}</section>'''
    raise SystemExit(f"Unbekanntes Layout: {lay}")


def main():
    spec = pathlib.Path(sys.argv[1]).resolve()
    posts = json.loads(spec.read_text(encoding="utf-8"))["posts"]
    css = CSS % {"sora": (FONTS / "sora-700-latin.woff2").as_uri(), "figtree": (FONTS / "figtree-latin.woff2").as_uri()}
    page = f'<!doctype html><html lang="de-CH"><head><meta charset="utf-8"><style>{css}</style></head><body>' + \
        "".join(render_post(p) for p in posts) + "</body></html>"
    out = spec.parent / "vorschau.html"
    out.write_text(page, encoding="utf-8")

    from playwright.sync_api import sync_playwright
    from PIL import Image
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1080, "height": 1400})
        pg.goto(out.as_uri())
        pg.wait_for_timeout(1000)
        for p in posts:
            png = spec.parent / f'{p["id"]}.png'
            pg.locator(f'#{p["id"]}').screenshot(path=str(png))
            Image.open(png).convert("RGB").save(spec.parent / f'{p["id"]}.jpg', quality=92)
            png.unlink()
        b.close()
    print("ok:", ", ".join(p["id"] + ".jpg" for p in posts))


if __name__ == "__main__":
    main()
