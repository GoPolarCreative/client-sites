"""Verify a built site before it ships.

    python3 _kit/verify.py sites/<slug>            # all pages, 1440 and 390, screenshots to _src/shots
    python3 _kit/verify.py sites/<slug> --quick    # skip screenshots

Serves the folder over HTTP (fonts fail over file://), drives Chrome with Playwright, and runs
static rules over the source. Exits 1 on any FAIL. Look at the contact sheets afterwards anyway.
"""
from __future__ import annotations

import functools
import http.server
import json
import re
import shutil
import socketserver
import sys
import threading
from pathlib import Path

from PIL import Image

ROOT = Path(sys.argv[1]).resolve()
QUICK = "--quick" in sys.argv
SRC = ROOT / "_src"
SHOTS = SRC / "shots"
CREDIT = "Website by Go Polar Creative"
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF]")
fails, warns = [], []


def fail(m):
    fails.append(m)


def warn(m):
    warns.append(m)


def chrome():
    for p in ("/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"):
        if Path(p).exists():
            return p
    return None


# ---------------------------------------------------------------- static rules
pages = sorted(p for p in ROOT.rglob("index.html") if "_src" not in p.parts)
css = (ROOT / "assets" / "site.css").read_text() if (ROOT / "assets" / "site.css").exists() else ""
js = "".join((ROOT / "assets" / n).read_text() for n in ("gp.js", "site.js") if (ROOT / "assets" / n).exists())

roots = "".join(re.findall(r":root[^{]*\{[^}]*\}", css))
outside = re.sub(r":root[^{]*\{[^}]*\}", "", css)
for m in re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)", outside):
    fail(f"site.css colour outside :root: {m}")
if "prefers-reduced-motion" not in css + (ROOT / "assets" / "gp.css").read_text():
    fail("no prefers-reduced-motion block")
if re.search(r"addEventListener\(\s*['\"]scroll", js):
    fail("scroll listener found, use IntersectionObserver")

for f in [*pages, ROOT / "assets" / "site.css", ROOT / "assets" / "site.js"]:
    if not f.exists():
        continue
    t = f.read_text()
    rel = f.relative_to(ROOT)
    if "—" in t or "–" in t:
        fail(f"{rel}: em or en dash")
    if EMOJI.search(t):
        fail(f"{rel}: emoji")

for p in pages:
    t = p.read_text()
    rel = p.relative_to(ROOT)
    if CREDIT not in t or 'href="https://www.itscold.com.au"' not in t:
        fail(f"{rel}: footer credit missing or wrong")
    tags = ["og:image", "og:image:secure_url", "og:image:type", "og:image:width", "og:image:height", "og:image:alt",
            "twitter:card", "twitter:title", "twitter:description", "twitter:image", "twitter:image:alt"]
    for tg in tags:
        if f'"{tg}"' not in t:
            fail(f"{rel}: missing meta {tg}")
    if 'href="tel:' not in t:
        fail(f"{rel}: no tap-to-call link")
    for a in re.findall(r'<form[^>]*action="([^"]+)"', t):
        if a != "https://api.web3forms.com/submit":
            fail(f"{rel}: form posts to {a}")
    keys = set(re.findall(r'name="access_key" value="([^"]+)"', t))
    if len(keys) > 1:
        fail(f"{rel}: more than one Web3Forms key")
    for subj in re.findall(r'name="subject" value="([^"]+)"', t):
        if " - " not in subj:
            fail(f"{rel}: form subject not in house pattern: {subj}")
    for ld in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try:
            json.loads(ld)
        except Exception as e:
            fail(f"{rel}: JSON-LD does not parse: {e}")
    m = re.search(r'<meta name="description" content="([^"]*)"', t)
    if not m or not (50 <= len(m.group(1)) <= 165):
        warn(f"{rel}: meta description length {len(m.group(1)) if m else 0}")
    for href in re.findall(r'href="(/[^"#?]*)"', t):
        target = ROOT / href.lstrip("/")
        if not (target.exists() or (target / "index.html").exists()):
            fail(f"{rel}: broken internal link {href}")

for f in ("favicon.svg", "favicon-32.png", "apple-touch-icon.png", "og-image.jpg"):
    if not (ROOT / "assets" / f).exists():
        fail(f"assets/{f} missing")
og = ROOT / "assets" / "og-image.jpg"
if og.exists():
    with Image.open(og) as im:
        if im.size != (1200, 630):
            fail(f"og-image is {im.size}, needs 1200x630")
for f in ("sitemap.xml", "robots.txt", "vercel.json", ".vercelignore"):
    if not (ROOT / f).exists():
        fail(f"{f} missing")

# ---------------------------------------------------------------- browser checks
Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
srv = socketserver.TCPServer(("127.0.0.1", 0), Handler)
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{port}"

PROBE = """() => {
  const vw = document.documentElement.clientWidth, out = {};
  out.overflow = document.documentElement.scrollWidth - vw;
  out.wide = [...document.querySelectorAll('body *')].filter(e => {
    const r = e.getBoundingClientRect(); if (r.width === 0 || r.right <= vw + 1) return false;
    for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) {
      const s = getComputedStyle(p); if (s.overflowX !== 'visible' || s.overflow === 'hidden' || s.overflow === 'clip') return false; }
    return getComputedStyle(e).position !== 'fixed';
  }).slice(0, 5).map(e => e.tagName + '.' + e.className);
  out.h1 = document.querySelectorAll('h1').length;
  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => +h.tagName[1]);
  out.jumps = hs.filter((h, i) => i && h > hs[i - 1] + 1).length;
  out.broken = [...document.images].filter(i => i.currentSrc && i.complete && i.naturalWidth === 0).map(i => i.currentSrc);
  out.unrevealed = document.querySelectorAll('.rv:not(.in)').length;
  out.small = [...document.querySelectorAll('a,button,summary,input,select,textarea')].filter(e => {
    const r = e.getBoundingClientRect(), s = getComputedStyle(e);
    return r.width > 0 && s.visibility !== 'hidden' && !e.closest('p,li,dd,figcaption,.gp-hp,.gp-skip,[aria-hidden=true]') && (r.height < 40 || r.width < 40);
  }).slice(0, 6).map(e => (e.textContent || e.name || e.tagName).trim().slice(0, 30));
  out.tinyText = [...document.querySelectorAll('body *')].filter(e => e.childNodes.length && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && parseFloat(getComputedStyle(e).fontSize) < 13 && e.getBoundingClientRect().width > 0).slice(0, 5).map(e => e.textContent.trim().slice(0, 30));
  const faqQ = [...document.querySelectorAll('[data-faq-q]')].map(e => e.textContent.trim());
  const faqA = [...document.querySelectorAll('[data-faq-a]')].map(e => e.textContent.trim());
  let schema = [];
  document.querySelectorAll('script[type="application/ld+json"]').forEach(s => {
    try { (JSON.parse(s.textContent)['@graph'] || []).forEach(n => { if (n['@type'] === 'FAQPage') schema = n.mainEntity.map(q => [q.name, q.acceptedAnswer.text]); }); } catch (e) {}
  });
  out.faqMismatch = (faqQ.length || schema.length) && JSON.stringify(faqQ.map((q, i) => [q, faqA[i]])) !== JSON.stringify(schema);
  const tel = [...document.querySelectorAll('a[href^="tel:"]')].find(a => { const r = a.getBoundingClientRect(); return r.width && r.top < innerHeight && r.bottom > 0 && getComputedStyle(a).visibility !== 'hidden'; });
  out.telFirstScreen = !!tel;
  return out;
}"""

if not chrome():
    fail("no Chrome found for browser checks")
else:
    from playwright.sync_api import sync_playwright
    if SHOTS.exists():
        shutil.rmtree(SHOTS)
    SHOTS.mkdir(parents=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=chrome())
        for w, h, tag in ((1440, 900, "desktop"), (390, 844, "phone")):
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1,
                                is_mobile=(tag == "phone"), has_touch=(tag == "phone"))
            for p in pages:
                path = "/" + str(p.parent.relative_to(ROOT)).replace(".", "").strip("/")
                path = (path + "/").replace("//", "/")
                name = path.strip("/").replace("/", "_") or "home"
                pg = ctx.new_page()
                errs = []
                pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("requestfailed", lambda r: errs.append("request failed " + r.url) if "web3forms" not in r.url else None)
                pg.on("response", lambda r: errs.append(f"{r.status} {r.url}") if r.status >= 400 and r.url.startswith(base) else None)
                pg.goto(base + path, wait_until="networkidle")
                first = pg.evaluate(PROBE)
                if not first["telFirstScreen"] and not path.startswith("/404"):
                    fail(f"{tag} {path}: no visible tap-to-call in the first screen")
                frames = []
                total = pg.evaluate("document.documentElement.scrollHeight")
                y = 0
                while True:
                    pg.evaluate(f"window.scrollTo(0,{y})")
                    pg.wait_for_timeout(350)
                    if not QUICK and (name == "home" or y == 0):
                        fn = SHOTS / f"{name}-{tag}-{len(frames):02d}.jpg"
                        pg.screenshot(path=str(fn), type="jpeg", quality=70)
                        frames.append(fn)
                    if y + h >= total or len(frames) > 40 or y > 60000:
                        break
                    y += int(h * 0.85)
                    total = pg.evaluate("document.documentElement.scrollHeight")
                pg.wait_for_timeout(400)
                r = pg.evaluate(PROBE)
                where = f"{tag} {path}"
                if r["overflow"] > 1:
                    fail(f"{where}: horizontal overflow {r['overflow']}px {r['wide']}")
                if r["h1"] != 1:
                    fail(f"{where}: {r['h1']} h1 elements")
                if r["jumps"]:
                    fail(f"{where}: heading level jump")
                if r["broken"]:
                    fail(f"{where}: broken images {r['broken'][:3]}")
                if r["unrevealed"]:
                    warn(f"{where}: {r['unrevealed']} reveals never fired")
                if r["faqMismatch"]:
                    fail(f"{where}: on-page FAQ does not match FAQPage schema")
                if r["small"] and tag == "phone":
                    warn(f"{where}: tap targets under 40px: {r['small']}")
                if r["tinyText"]:
                    warn(f"{where}: text under 13px: {r['tinyText']}")
                for e in errs:
                    fail(f"{where}: {e}")
                pg.close()
                if frames and name == "home":
                    ims = [Image.open(f) for f in frames]
                    scale = 0.5 if tag == "desktop" else 1.0
                    tw, th = int(w * scale), int(h * scale)
                    cols = 3 if tag == "desktop" else 5
                    rows = (len(ims) + cols - 1) // cols
                    sheet = Image.new("RGB", (cols * tw + (cols - 1) * 8, rows * th + (rows - 1) * 8), "white")
                    for i, im in enumerate(ims):
                        sheet.paste(im.resize((tw, th)), ((i % cols) * (tw + 8), (i // cols) * (th + 8)))
                    sheet.save(SHOTS / f"SHEET-home-{tag}.jpg", quality=72)
                    for f in frames:
                        if f.name.endswith("-00.jpg"):
                            continue
                        f.unlink()
            ctx.close()
        b.close()
srv.shutdown()

print(f"\n{len(pages)} pages checked in {ROOT.name}")
for m in fails:
    print("FAIL", m)
for m in warns:
    print("warn", m)
print("RESULT:", "FAIL" if fails else "PASS", f"({len(fails)} fails, {len(warns)} warnings)")
(SRC / "verify.json").write_text(json.dumps({"fails": fails, "warns": warns}, indent=2))
sys.exit(1 if fails else 0)
