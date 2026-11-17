"""Go Polar site kit.

The mechanics every client site shares: image pipeline, self-hosted fonts, the page shell
(meta, Open Graph, JSON-LD @graph, favicons, GA4), Web3Forms forms, FAQ markup that matches
its schema, sitemap, robots, vercel.json, og-image and favicons.

Design does NOT live here. Each site's _src/build.py writes its own header, footer, page
bodies and site.css, so two sites never share a composition. Reuse mechanics, never layouts.

Usage from sites/<slug>/_src/build.py:

    import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / '_kit'))
    from gpkit import Site, esc
    s = Site(__file__)
    ...
    s.finish()
"""
from __future__ import annotations

import datetime
import hashlib
import html
import json
import re
import shutil
import subprocess
import tarfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

KIT = Path(__file__).resolve().parent
CREDIT_TEXT = "Website by Go Polar Creative"
CREDIT = f'<a href="https://www.itscold.com.au" target="_blank" rel="noopener">{CREDIT_TEXT}</a>'
PLACEHOLDER_KEY = "c898e546-5c35-4a3e-ba3a-fd5e7cae5100"
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
STATES = {"VIC": "Victoria", "NSW": "New South Wales", "QLD": "Queensland", "WA": "Western Australia",
          "SA": "South Australia", "TAS": "Tasmania", "ACT": "Australian Capital Territory", "NT": "Northern Territory"}


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


class Site:
    """One client site. `src` is the path of _src/build.py (pass __file__) or the _src folder."""

    def __init__(self, src):
        src = Path(src).resolve()
        self.src = src.parent if src.is_file() else src
        self.out = self.src.parent
        self.d = json.loads((self.src / "site.json").read_text())
        d = self.d
        self.name = d["name"]
        self.slug = self.out.name
        self.domain = d["domain"].replace("https://", "").replace("http://", "").replace("www.", "").strip("/")
        self.base = f"https://www.{self.domain}" if d.get("www", True) else f"https://{self.domain}"
        digits = re.sub(r"\D", "", d["phone"])
        self.tel = "+61" + digits[1:] if digits.startswith("0") else "+" + digits
        self.phone = d["phone"]
        key = (d.get("web3forms_key") or "").strip()
        self.form_key = key if UUID_RE.match(key) else PLACEHOLDER_KEY
        if self.form_key == PLACEHOLDER_KEY:
            self.flag("Web3Forms key missing or malformed, placeholder key used. Forms will not reach the client.")
        self.state = d.get("state", "VIC")
        self.assets = self.out / "assets"
        (self.assets / "img").mkdir(parents=True, exist_ok=True)
        (self.assets / "fonts").mkdir(parents=True, exist_ok=True)
        self.images: dict[str, dict] = {}
        self.pages: list[str] = []
        self.font_css = ""
        self.preloads: list[str] = []
        self.header = lambda path: ""
        self.footer = lambda path: ""
        self.callbar = None
        self.head_extra = ""
        self.flags: list[str] = list(d.get("flags", []))
        self.today = datetime.date.today().isoformat()

    # ------------------------------------------------------------------ monthly suburb pages
    def suburbs(self):
        """Published suburb pages: one JSON per suburb in _src/suburbs/, written by the monthly run.
        Returns (pages, links) where links maps suburb name to its URL path."""
        folder = self.src / "suburbs"
        pages = [json.loads(f.read_text()) for f in sorted(folder.glob("*.json"))] if folder.exists() else []
        plan = json.loads((self.src / "plan.json").read_text()) if (self.src / "plan.json").exists() else {}
        pattern = plan.get("pattern", "/{slug}/")
        for p in pages:
            p["path"] = pattern.format(slug=slugify(p["suburb"]))
        return pages, {p["suburb"]: p["path"] for p in pages}

    # ------------------------------------------------------------------ notes
    def flag(self, text: str):
        if text not in self.flags:
            self.flags.append(text)

    # ------------------------------------------------------------------ fonts
    def fonts(self, specs, preload=()):
        """specs: [(fontsource_pkg, 'Family Name', [weights], ['normal','italic'])]. Vendored as woff2."""
        cache = KIT / ".cache"
        cache.mkdir(exist_ok=True)
        css = []
        for pkg, family, weights, styles in specs:
            tgz = next(iter(sorted(cache.glob(f"fontsource-{pkg}-[0-9]*.tgz"))), None)
            if not tgz:
                subprocess.run(["npm", "pack", f"@fontsource/{pkg}", "--pack-destination", str(cache)],
                               check=True, capture_output=True)
                tgz = next(iter(sorted(cache.glob(f"fontsource-{pkg}-[0-9]*.tgz"))))
            with tarfile.open(tgz) as t:
                for w in weights:
                    for st in styles:
                        fn = f"{pkg}-latin-{w}-{st}.woff2"
                        (self.assets / "fonts" / fn).write_bytes(t.extractfile(f"package/files/{fn}").read())
                        css.append(f"@font-face{{font-family:'{family}';font-style:{st};font-weight:{w};"
                                   f"font-display:swap;src:url(/assets/fonts/{fn}) format('woff2')}}")
        self.font_css = "\n".join(css)
        self.preloads = list(preload)

    def ttf(self, woff2_name: str) -> str:
        """Convert a vendored woff2 to TTF so Pillow can draw with it (og-image)."""
        from fontTools.ttLib import TTFont
        out = KIT / ".cache" / woff2_name.replace(".woff2", ".ttf")
        if not out.exists():
            f = TTFont(self.assets / "fonts" / woff2_name)
            f.flavor = None
            f.save(out)
        return str(out)

    # ------------------------------------------------------------------ images
    def image(self, key, file, alt, focus=(50, 50), widths=(640, 1280, 1920)):
        """Process one client photo from _src/img into responsive WebP plus one JPG."""
        im = ImageOps.exif_transpose(Image.open(self.src / "img" / file)).convert("RGB")
        W, H = im.size
        srcset = []
        for w in widths:
            if w > W and srcset:
                continue
            ww = min(w, W)
            r = im.resize((ww, round(H * ww / W)), Image.LANCZOS) if ww != W else im
            fn = f"{key}-{ww}.webp"
            r.save(self.assets / "img" / fn, "WEBP", quality=78, method=6)
            srcset.append((ww, fn))
        big = srcset[-1][0]
        self.images[key] = dict(file=file, alt=alt, w=big, h=round(H * big / W), srcset=srcset, focus=focus)
        return self.images[key]

    def img(self, key, sizes="100vw", cls="", eager=False, alt=None, attrs=""):
        i = self.images[key]
        ss = ", ".join(f"/assets/img/{fn} {w}w" for w, fn in i["srcset"])
        mid = i["srcset"][min(1, len(i["srcset"]) - 1)][1]
        fx, fy = i["focus"]
        load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
        a = i["alt"] if alt is None else alt
        c = f' class="{cls}"' if cls else ""
        return (f'<img{c} src="/assets/img/{mid}" srcset="{ss}" sizes="{sizes}" width="{i["w"]}" '
                f'height="{i["h"]}" alt="{esc(a)}" {load} style="object-position:{fx}% {fy}%" {attrs}>')

    def largest(self, key):
        return "/assets/img/" + self.images[key]["srcset"][-1][1]

    # ------------------------------------------------------------------ forms
    def form(self, subject_suffix, fields_html, button="Send", cls="", note=""):
        """Web3Forms form. fields_html is the site's own markup for inputs. Kit adds the plumbing."""
        subject = f"{self.name} - {subject_suffix}"
        return f"""<form class="{cls}" action="https://api.web3forms.com/submit" method="POST" data-w3f>
<input type="hidden" name="access_key" value="{self.form_key}">
<input type="hidden" name="subject" value="{esc(subject)}">
<input type="hidden" name="from_name" value="{esc(self.name)} website">
<input type="checkbox" name="botcheck" class="gp-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
{fields_html}
<button type="submit">{button}</button>
<p class="gp-status" data-status role="status" aria-live="polite">{note}</p>
</form>"""

    # ------------------------------------------------------------------ FAQ (markup and schema from one list)
    @staticmethod
    def faq_html(items, group="faq", cls="", q_tag=""):
        out = []
        for i, (q, a) in enumerate(items):
            out.append(f'<details class="{cls}" name="{group}"{" open" if i == 0 and "open-first" in cls else ""}>'
                       f'<summary><span data-faq-q>{esc(q)}</span></summary>'
                       f'<div class="gp-faq-a"><p data-faq-a>{esc(a)}</p></div></details>')
        return "\n".join(out)

    # ------------------------------------------------------------------ schema
    def business_node(self):
        d = self.d
        areas = [{"@type": "City", "name": a} for a in d.get("areas", [])]
        areas.append({"@type": "State", "name": STATES.get(self.state, self.state)})
        node = {
            "@type": d.get("schema_type", "LocalBusiness"),
            "@id": f"{self.base}/#business",
            "name": self.name,
            "url": f"{self.base}/",
            "telephone": self.tel,
            "email": d.get("email"),
            "image": f"{self.base}/assets/og-image.jpg",
            "logo": f"{self.base}/assets/apple-touch-icon.png",
            "address": {"@type": "PostalAddress", "addressLocality": d.get("base_suburb", d.get("city")),
                        "addressRegion": self.state, "addressCountry": "AU"},
            "areaServed": areas,
            "hasOfferCatalog": {"@type": "OfferCatalog", "name": f"{self.name} services",
                                "itemListElement": [{"@type": "Offer", "itemOffered": {
                                    "@type": "Service", "name": s["name"],
                                    "url": f"{self.base}/{s['slug']}/" if s.get("page") else f"{self.base}/"}}
                                    for s in d.get("services", [])]},
        }
        if d.get("street"):
            node["address"]["streetAddress"] = d["street"]
        if d.get("postcode"):
            node["address"]["postalCode"] = d["postcode"]
        if d.get("additional_type"):
            node["additionalType"] = d["additional_type"]
        if d.get("hours"):
            node["openingHours"] = d["hours"]
        if d.get("licence"):
            node["hasCredential"] = {"@type": "EducationalOccupationalCredential",
                                     "credentialCategory": "licence", "name": d["licence"]}
        if d.get("same_as"):
            node["sameAs"] = d["same_as"]
        if d.get("reviews"):
            node["review"] = [{"@type": "Review", "author": {"@type": "Person", "name": r["name"]},
                               "reviewBody": r["text"],
                               "reviewRating": {"@type": "Rating", "ratingValue": r.get("stars", 5), "bestRating": 5}}
                              for r in d["reviews"]]
        return {k: v for k, v in node.items() if v}

    def graph(self, path, title, description, crumbs, faq, extra):
        url = f"{self.base}{path}"
        g = [self.business_node(),
             {"@type": "WebSite", "@id": f"{self.base}/#website", "url": f"{self.base}/", "name": self.name,
              "publisher": {"@id": f"{self.base}/#business"}, "inLanguage": "en-AU"},
             {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": title, "description": description,
              "isPartOf": {"@id": f"{self.base}/#website"}, "about": {"@id": f"{self.base}/#business"},
              "breadcrumb": {"@id": f"{url}#breadcrumb"}, "inLanguage": "en-AU"}]
        trail = [("Home", "/")] + list(crumbs or [])
        g.append({"@type": "BreadcrumbList", "@id": f"{url}#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{self.base}{p}"} for i, (n, p) in enumerate(trail)]})
        if faq:
            g.append({"@type": "FAQPage", "@id": f"{url}#faq", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
        g.extend(extra or [])
        return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False, indent=1)

    def service_node(self, path, name, description):
        return {"@type": "Service", "@id": f"{self.base}{path}#service", "name": name, "description": description,
                "provider": {"@id": f"{self.base}/#business"}, "url": f"{self.base}{path}",
                "areaServed": [{"@type": "City", "name": a} for a in self.d.get("areas", [])[:20]]}

    # ------------------------------------------------------------------ page shell
    def page(self, path, *, title, description, body, crumbs=None, faq=None, extra_graph=None,
             body_class="", og_alt=None):
        assert path.startswith("/") and path.endswith("/"), path
        assert len(description) <= 165, f"meta description too long on {path}"
        d = self.d
        url = f"{self.base}{path}"
        og = f"{self.base}/assets/og-image.jpg"
        og_alt = og_alt or f"{self.name}, {d.get('tagline', '')}".strip(", ")
        preload = "\n".join(f'<link rel="preload" href="/assets/fonts/{f}" as="font" type="font/woff2" crossorigin>'
                            for f in self.preloads)
        ga = d.get("ga4")
        ga_html = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={ga}"></script>\n'
                   f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}"
                   f"gtag('js',new Date());gtag('config','{ga}');</script>") if ga else \
            "<!-- CLIENT TO SUPPLY: GA4 measurement ID (site.json ga4) -->"
        callbar = self.callbar(path) if self.callbar else ""
        doc = f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="geo.region" content="AU-{self.state}">
<meta name="geo.placename" content="{esc(d.get('base_suburb', d.get('city', '')))}">
<meta name="theme-color" content="{d.get('theme_color', '#000000')}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(self.name)}">
<meta property="og:locale" content="en_AU">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{og}">
<meta property="og:image:secure_url" content="{og}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(og_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{og}">
<meta name="twitter:image:alt" content="{esc(og_alt)}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="alternate icon" href="/assets/favicon-32.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
{preload}
<style>{self.font_css}</style>
<link rel="stylesheet" href="/assets/gp.css?v={self.ver}">
<link rel="stylesheet" href="/assets/site.css?v={self.ver}">
<script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">
{self.graph(path, title, description, crumbs, faq, extra_graph)}
</script>
{ga_html}
{self.head_extra}
</head>
<body class="{body_class}">
<a class="gp-skip" href="#main">Skip to content</a>
<div class="gp-sentinel" aria-hidden="true"></div>
{self.header(path)}
<main id="main">
{body}
</main>
{self.footer(path)}
{callbar}
<script src="/assets/gp.js?v={self.ver}" defer></script>
<script src="/assets/site.js?v={self.ver}" defer></script>
</body>
</html>
"""
        target = self.out / path.strip("/") / "index.html" if path != "/" else self.out / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(doc)
        self.pages.append(path)

    @property
    def ver(self):
        css = self.src / "site.css"
        return hashlib.md5(css.read_bytes()).hexdigest()[:8] if css.exists() else "1"

    # ------------------------------------------------------------------ favicons and og-image
    def favicons(self, svg: str):
        import cairosvg
        (self.assets / "favicon.svg").write_text(svg)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(self.assets / "favicon-32.png"),
                         output_width=32, output_height=32)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(self.assets / "apple-touch-icon.png"),
                         output_width=180, output_height=180)

    def og_image(self, photo_key, *, focus=None, mark: Image.Image | None = None, headline: str, line2="",
                 small="", font_bold: str, font_text: str, ink="#ffffff", accent="#ffffff", scrim=(0, 0, 0)):
        """1200x630 JPG share card from a client photo. Separators use ' / ', never dashes."""
        i = self.images[photo_key]
        im = ImageOps.exif_transpose(Image.open(self.src / "img" / i["file"])).convert("RGB")
        fx, fy = focus or i["focus"]
        W, H = im.size
        scale = max(1200 / W, 630 / H)
        im = im.resize((round(W * scale), round(H * scale)), Image.LANCZOS)
        cx, cy = im.width * fx / 100, im.height * fy / 100
        x0 = int(min(max(cx - 600, 0), im.width - 1200))
        y0 = int(min(max(cy - 315, 0), im.height - 630))
        im = im.crop((x0, y0, x0 + 1200, y0 + 630)).convert("RGBA")
        grad = Image.new("L", (1200, 1))
        for x in range(1200):
            grad.putpixel((x, 0), int(235 * max(0.0, 1 - x / 980) ** 0.9))
        alpha = grad.resize((1200, 630))
        im.alpha_composite(Image.merge("RGBA", (*[Image.new("L", (1200, 630), c) for c in scrim], alpha)))
        dr = ImageDraw.Draw(im)
        y = 64
        if mark is not None:
            m = mark.copy()
            m.thumbnail((420, 120))
            im.alpha_composite(m, (64, y))
            y += m.height + 48
        fb = ImageFont.truetype(font_bold, 64)
        ft = ImageFont.truetype(font_text, 28)
        for line in headline.split("\n"):
            dr.text((64, y), line, font=fb, fill=ink)
            y += 72
        if line2:
            dr.text((64, y + 16), line2, font=ft, fill=ink)
        dr.rectangle((64, 630 - 92, 64 + 72, 630 - 86), fill=accent)
        if small:
            dr.text((64, 630 - 72), small, font=ft, fill=ink)
        im.convert("RGB").save(self.assets / "og-image.jpg", "JPEG", quality=84, optimize=True, progressive=True)

    # ------------------------------------------------------------------ monthly suburb pages
    def suburbs(self):
        """Published suburb pages: one JSON per suburb in _src/suburbs/, written by the monthly run.
        Returns (pages, links) where links maps suburb name to its URL path."""
        folder = self.src / "suburbs"
        pages = [json.loads(f.read_text()) for f in sorted(folder.glob("*.json"))] if folder.exists() else []
        plan = json.loads((self.src / "plan.json").read_text()) if (self.src / "plan.json").exists() else {}
        pattern = plan.get("pattern", "/{slug}/")
        for p in pages:
            p["path"] = pattern.format(slug=slugify(p["suburb"]))
        return pages, {p["suburb"]: p["path"] for p in pages}

    # ------------------------------------------------------------------ notes
    def notes(self, *, direction, idea, live, type_, palette, redraws=(), decisions=()):
        """Write BUILD-NOTES.md at the site root (not deployed). Call before finish()."""
        d = self.d
        lines = [f"# {self.name}: build notes", "",
                 f"- Source: {d.get('source_row', 'questionnaire')}",
                 f"- Domain: {self.base} (canonical and schema point here)",
                 f"- Preview: https://{self.slug}.vercel.app",
                 f"- Built: {self.today} by Claude with the go-polar-site-build skill",
                 f"- Phone on site: {self.phone} / Form key: {'client key' if self.form_key != PLACEHOLDER_KEY else 'PLACEHOLDER'}",
                 "", "## Design", "", f"- Direction: {direction}", f"- Idea: {idea}", f"- Live thing: {live}",
                 f"- Type: {type_}", f"- Palette: {palette}"]
        lines += [f"- Redraw: {r}" for r in redraws]
        lines += [f"- Decision: {x}" for x in decisions]
        lines += ["", "## Pages", ""] + [f"- {p}" for p in self.pages if p != "/404/"]
        lines += ["", "## Photos", ""] + [f"- `{k}`: {v['file']} ({v['alt']})" for k, v in self.images.items()]
        lines += ["", "## Flags for the client (confirm before go-live)", ""] + [f"- [ ] {f}" for f in self.flags]
        lines += ["", "## Editing", "", "Change `_src/site.json`, `_src/build.py`, `_src/site.css` or `_src/site.js`, then:", "",
                  "```", f"python3 sites/{self.slug}/_src/build.py && python3 _kit/verify.py sites/{self.slug}", "```", "",
                  "Commit and push to main; the workflow redeploys only this folder.", ""]
        (self.out / "BUILD-NOTES.md").write_text("\n".join(lines))

    # ------------------------------------------------------------------ finish
    def finish(self):
        shutil.copy(KIT / "gp.js", self.assets / "gp.js")
        shutil.copy(KIT / "gp.css", self.assets / "gp.css")
        for name in ("site.css", "site.js"):
            if (self.src / name).exists():
                shutil.copy(self.src / name, self.assets / name)
            else:
                (self.assets / name).write_text("")
        sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for p in self.pages:
            if p == "/404/":
                continue
            sm.append(f"<url><loc>{self.base}{p}</loc><lastmod>{self.today}</lastmod></url>")
        sm.append("</urlset>")
        (self.out / "sitemap.xml").write_text("\n".join(sm) + "\n")
        (self.out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {self.base}/sitemap.xml\n")
        (self.out / ".vercelignore").write_text("_src\nBUILD-NOTES.md\n")
        vercel = {
            "cleanUrls": True,
            "trailingSlash": True,
            "headers": [
                {"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=604800"}]},
                {"source": "/(.*)", "has": [{"type": "host", "value": "(?<sub>.*)\\.vercel\\.app"}],
                 "headers": [{"key": "X-Robots-Tag", "value": "noindex"}]},
            ],
        }
        (self.out / "vercel.json").write_text(json.dumps(vercel, indent=2) + "\n")
        nf = self.out / "404" / "index.html"
        if nf.exists():
            shutil.copy(nf, self.out / "404.html")
        (self.src / "flags.json").write_text(json.dumps(self.flags, indent=2) + "\n")
        print(f"built {self.slug}: {len(self.pages)} pages, {len(self.images)} images, {len(self.flags)} flags")


def ingest(raw_dir, img_dir, max_side=2400):
    """Copy client photos into _src/img: EXIF-rotated, capped at max_side, deduplicated by md5."""
    raw_dir, img_dir = Path(raw_dir), Path(img_dir)
    img_dir.mkdir(parents=True, exist_ok=True)
    seen = set()
    for f in sorted(raw_dir.iterdir()):
        if f.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp", ".heic"):
            continue
        h = hashlib.md5(f.read_bytes()).hexdigest()
        if h in seen:
            print("duplicate dropped:", f.name)
            continue
        seen.add(h)
        im = ImageOps.exif_transpose(Image.open(f))
        im.thumbnail((max_side, max_side), Image.LANCZOS)
        if im.mode in ("RGBA", "LA", "P"):
            im.save(img_dir / (f.stem + ".png"))
        else:
            im.convert("RGB").save(img_dir / (f.stem + ".jpg"), "JPEG", quality=88)
