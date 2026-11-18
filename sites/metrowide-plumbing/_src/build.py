"""Metrowide Plumbing. Go Polar house style: dark and light sections, logo blue accent,
condensed uppercase headings, hero quote form, service cards, stat band, CTA band.

Run: python3 sites/metrowide-plumbing/_src/build.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_kit"))
from PIL import Image  # noqa: E402

from gpkit import CREDIT, Site, esc  # noqa: E402

s = Site(__file__)
d = s.d
TEL = s.tel
PH = s.phone
EMAIL = d["email"]

s.fonts([("barlow-condensed", "Barlow Condensed", [600, 700, 800], ["normal"]),
         ("dm-sans", "DM Sans", [400, 500, 700], ["normal"])],
        preload=["barlow-condensed-latin-800-normal.woff2", "dm-sans-latin-400-normal.woff2"])

# ---------------------------------------------------------------- icons (Phosphor bold, inlined as a sprite)
_icons = []
for f in sorted((s.src / "icons").glob("*.svg")):
    inner = re.sub(r"^<svg[^>]*>|</svg>\s*$", "", f.read_text().strip())
    _icons.append(f'<symbol id="i-{f.stem}" viewBox="0 0 256 256">{inner}</symbol>')
SPRITE = '<svg class="sprite" aria-hidden="true" focusable="false">' + "".join(_icons) + "</svg>"


def I(name, cls="ic"):
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'


# ---------------------------------------------------------------- images
P = {
    "green": ("bath-green-tile.jpg", "Bathroom with green finger tiles, terrazzo floor and a freestanding bath", (50, 55)),
    "arch": ("bath-terrazzo-arch.jpg", "Terrazzo bathroom with black tapware, floating vanity and arch mirror", (50, 45)),
    "double": ("shower-double.jpg", "Double shower with two black rail sets over white finger tile", (45, 40)),
    "brassvan": ("vanity-brass.jpg", "Brushed brass wall mixer over an oval vessel basin", (55, 45)),
    "brassshower": ("shower-brass.jpg", "Brushed brass rain head and hand shower on large grey tiles", (50, 35)),
    "combo": ("bath-laundry-combo.jpg", "Bathroom and laundry in one room with black fixtures and a frameless screen", (50, 50)),
    "under": ("vanity-underside.jpg", "Open vanity showing neat chrome waste and isolation valves beside a freestanding bath", (40, 55)),
}
for k, (f, alt, focus) in P.items():
    s.image(k, f, alt, focus)

logo = Image.open(s.src / "img" / "logo.png").convert("RGBA")
lw = logo.resize((560, round(logo.height * 560 / logo.width)), Image.LANCZOS)
lw.save(s.assets / "img" / "logo.png", optimize=True)
lw.save(s.assets / "img" / "logo.webp", "WEBP", quality=90)
LOGO = f'<img src="/assets/img/logo.webp" width="{lw.width}" height="{lw.height}" alt="Metrowide Plumbing"'

# ---------------------------------------------------------------- services (money pages)
SERVICES = [
    dict(slug="emergency-plumber-melbourne", name="Emergency plumbing", nav="Emergency", page=True,
         title="Emergency Plumber Melbourne | Same-Day | Metrowide Plumbing",
         desc="Burst pipe, blocked drain or water through the ceiling? Metrowide Plumbing takes emergency and same-day jobs across Melbourne. Call Dan on 0423 017 489.",
         h1="Emergency plumber in Melbourne", photo="combo",
         lead="Water where it should not be is not a job for next week. We take emergency and same-day callouts across Melbourne, and we tell you straight when we can be there.",
         list_h="Call us now for", items=["Burst or split pipes", "Water coming through a ceiling or wall", "Blocked toilets and drains backing up",
                                          "A leaking or failed hot water unit", "Taps, cisterns or flexi hoses that will not stop running", "No water at all"],
         body=[("Before we get there", "Turn the water off at the mains. The tap is usually beside the meter near the front boundary. If the hot water unit is leaking, switch it off at the isolation valve and the power or gas. Move anything valuable out of the way and take a few photos if you think you will claim on insurance."),
               ("What happens on the call", "Tell us what you can see and which suburb you are in. We give you an honest time we can be there, and if it is something you can safely hold off until the morning, we say so."),
               ("Fixed properly, not patched", "Once the water is under control we find the cause. If it needs a bigger repair we explain the options and the price before we do it.")],
         faq=[("Do you do same-day plumbing in Melbourne?", "Yes. We take emergency and same-day jobs across Melbourne. Call 0423 017 489 and tell us what is happening and where."),
              ("What should I do while I wait?", "Turn the water off at the mains, switch off a leaking hot water unit, move valuables away from the water and take photos for insurance."),
              ("Will I know the price before you start?", "Yes. Once we have found the problem we explain the fix and the cost before any work beyond making it safe.")]),
    dict(slug="bathroom-renovation-plumbing-melbourne", name="Renovation plumbing", nav="Renovations", page=True,
         title="Bathroom Renovation Plumber Melbourne | Metrowide Plumbing",
         desc="Bathroom, laundry and kitchen renovation plumbing in Melbourne. Rough-in to fit-off, in-wall mixers, freestanding baths, on time for your trades.",
         h1="Bathroom renovation plumbing in Melbourne", photo="green",
         lead="Renovations are most of what is on this site: terrazzo, finger tile, brushed brass and black tapware. We plumb them from the strip-out to the last mixer, booked around your tiler and your builder.",
         list_h="On a renovation we handle", items=["Strip-out, capping and relocating services", "Rough-in for in-wall mixers and wall-hung vanities",
                                                     "Freestanding baths and floor wastes", "Laundry moves and bathroom-laundry combos",
                                                     "Kitchen sinks, dishwashers and fridge taps", "Fit-off of tapware, toilets and basins"],
         body=[("Planned with your other trades", "A renovation stalls when one trade is late. We work to the program, tell your builder or tiler where we are at, and come back for fit-off when the room is ready, not a week later."),
               ("Set out right the first time", "Mixer heights, waste positions and vanity set-outs are checked against the fixtures you have chosen before the wall is closed. That is what makes the finished room look as good as the photos."),
               ("Homeowners renovating direct", "If you are managing the job yourself, we quote from your plans or a site visit and walk you through what needs to happen and when.")],
         faq=[("Can you move my toilet, shower or laundry?", "Usually, yes. Moving fixtures depends on where the drainage runs, so we check on site and quote the move before anything is pulled up."),
              ("Do you supply the tapware?", "Most clients choose their own fixtures. We confirm the rough-in parts suit what you have picked so the fit-off goes smoothly."),
              ("How do you work with my tiler and waterproofer?", "We do rough-in before they start and fit-off after they finish, and we keep in touch so nobody is waiting on us.")]),
    dict(slug="new-build-plumbing-melbourne", name="New build plumbing", nav="New builds", page=True,
         title="New Build Plumber Melbourne | For Builders & Developers | Metrowide",
         desc="New build plumbing for Melbourne builders and developers. Drainage, under-slab, rough-in and fit-off, run to your program with clear communication.",
         h1="New build plumbing for Melbourne builders", photo="double",
         lead="Builders need a plumber who turns up when they say they will. We plumb new homes and developments from drainage to fit-off and keep you told at every stage.",
         list_h="Stages we plumb", items=["Sewer and stormwater drainage", "Under-slab plumbing", "Rough-in of water, waste and vent",
                                          "Hot water systems", "Fit-off of fixtures and tapware", "Final checks ready for handover"],
         body=[("Run to your program", "Give us the program and we book each stage around it. If something on site moves, we move with it and let your supervisor know."),
               ("Accurate quotes from plans", "We price from your plans with the stages laid out, so you know the cost of each visit and there are no surprise variations."),
               ("One plumber across the job", "The same crew rough-ins and fits off, so the person who set out the job is the one who finishes it.")],
         faq=[("Do you quote from plans?", "Yes. Send the plans and specifications and we quote each stage of the plumbing."),
              ("Do you work on multi-unit developments?", "Yes. We work with builders and developers on single homes and on developments. Tell us the scope and the program and we will quote it."),
              ("Which stages do you cover?", "Drainage, under-slab, rough-in, hot water and fit-off, through to final checks before handover.")]),
    dict(slug="commercial-plumbing-melbourne", name="Commercial plumbing", nav="Commercial", page=True,
         title="Commercial Plumber Melbourne | Metrowide Plumbing",
         desc="Commercial plumbing in Melbourne for offices, shops, fit-outs and property managers. Repairs, upgrades and maintenance done around your business hours.",
         h1="Commercial plumbing in Melbourne", photo="arch",
         lead="Offices, shops, fit-outs and the buildings property managers look after. We fix, upgrade and maintain commercial plumbing with the same clear communication we give homeowners.",
         list_h="Commercial work we take on", items=["Amenities and bathroom upgrades", "Fit-out plumbing for shops and offices",
                                                     "Leaks, blockages and breakdowns", "Hot water repairs and replacement",
                                                     "Planned maintenance for property managers", "Kitchenette and staff room plumbing"],
         body=[("Around your trading hours", "We plan the noisy and water-off parts of the job around when you are open, and tell you how long the water will be off before it goes off."),
               ("Clear paperwork", "Quotes and invoices that say what was done and where, so property managers can pass them on without chasing us for detail."),
               ("One number to call", "When something breaks, you call Dan. No call centre and no waiting for someone to pick up the job.")],
         faq=[("Do you work after hours on commercial jobs?", "We plan work around your business. Tell us when the site is quiet and we will schedule to suit where we can."),
              ("Do you look after rental and managed properties?", "Yes. We do repairs and maintenance for property managers and landlords across Melbourne."),
              ("Can you quote a fit-out from drawings?", "Yes. Send the drawings and the program and we quote the plumbing.")]),
    dict(slug="plumbing-maintenance-melbourne", name="Maintenance and repairs", nav="Maintenance", page=True,
         title="Plumbing Repairs & Maintenance Melbourne | Metrowide Plumbing",
         desc="Leaking taps, running toilets, hot water and blocked drains fixed properly. Residential plumbing repairs and maintenance across Melbourne. Free quotes.",
         h1="Plumbing repairs and maintenance in Melbourne", photo="under",
         lead="The everyday jobs matter as much as the big ones. Leaking taps, running toilets, hot water trouble and slow drains, fixed properly with the price agreed first.",
         list_h="Jobs we fix every week", items=["Leaking taps and mixers", "Running or leaking toilets", "Hot water repairs and replacement",
                                                 "Slow and blocked drains", "Tapware and toilet upgrades", "Water pressure problems"],
         body=[("The cause, not just the drip", "A dripping tap or a wet patch usually has a reason. We find it and fix that, so you are not calling us back for the same thing in a month."),
               ("Small jobs welcome", "No job is too small to ring about. If it is quick, we will often fit it in the same week."),
               ("Landlords and tenants", "We deal with tenants directly to get access and send the landlord or agent a clear invoice for the work.")],
         faq=[("Is it worth fixing a dripping tap?", "Yes. A steady drip wastes a surprising amount of water and usually gets worse. Most taps and mixers can be repaired rather than replaced."),
              ("Do you replace hot water systems?", "Yes. We repair hot water units where it makes sense and replace them when it does not, and explain which is which."),
              ("Do you charge a callout fee?", "Quotes are free. Ask when you call and we will tell you exactly how the job is priced before we come.")]),
]
SV = {x["slug"]: x for x in SERVICES}
d["services"] = [{"name": x["name"], "slug": x["slug"], "page": True} for x in SERVICES]
d["areas"] = [sub for subs in d["regions"].values() for sub in subs]

# ---------------------------------------------------------------- service extras for cards
EXTRA = {
    "emergency-plumber-melbourne": ("lightning", "combo", "Burst pipes, blocked drains and water where it should not be. Same-day callouts across Melbourne."),
    "bathroom-renovation-plumbing-melbourne": ("shower", "green", "Rough-in to fit-off for bathrooms, laundries and kitchens, booked around your tiler and builder."),
    "new-build-plumbing-melbourne": ("hard-hat", "double", "Drainage, under-slab, rough-in and fit-off for builders and developers, run to your program."),
    "commercial-plumbing-melbourne": ("buildings", "arch", "Repairs, upgrades and fit-outs for shops, offices and property managers, around your trading hours."),
    "plumbing-maintenance-melbourne": ("wrench", "under", "Leaking taps, running toilets, hot water and slow drains, fixed properly with the price agreed first."),
}
for x in SERVICES:
    x["icon"], x["card_photo"], x["blurb"] = EXTRA[x["slug"]]
    x["title"] = x["title"].replace("&amp;", "&")

JOBS = ["Burst or leaking pipe", "Blocked drain or toilet", "Hot water", "Leaking tap or toilet",
        "Bathroom renovation", "New build or extension", "Commercial job", "Something else"]
PAGES = [("Our work", "/our-work/"), ("Service areas", "/service-areas/"), ("About", "/about/"), ("Contact", "/contact/")]


def hl(text, n=None, phrase=None):
    """Wrap the accent phrase of a heading: an explicit phrase, or the last n words."""
    if phrase and phrase in text:
        a, b = text.split(phrase, 1)
        return f'{esc(a)}<span class="hl">{esc(phrase)}</span>{esc(b)}'
    w = text.split(" ")
    n = n or 2
    return esc(" ".join(w[:-n])) + f' <span class="hl">{esc(" ".join(w[-n:]))}</span>'


# ---------------------------------------------------------------- shared chrome
def header(path):
    svc = "".join(f'<a href="/{x["slug"]}/">{I(x["icon"])}<span>{x["name"]}</span></a>' for x in SERVICES)
    pages = "".join(f'<a class="nav-a" href="{u}"{" aria-current=page" if u == path else ""}>{n}</a>' for n, u in PAGES)
    return f"""{SPRITE}
<div class="topbar"><div class="wrap topbar-in">
<p>{I('lightning')} Emergency and same-day plumbing across Melbourne</p>
<a href="mailto:{EMAIL}">{I('envelope-simple')} {EMAIL}</a>
</div></div>
<header class="hd"><div class="wrap hd-in">
<a class="hd-logo" href="/" aria-label="Metrowide Plumbing home">{LOGO}></a>
<nav class="hd-nav" id="nav" aria-label="Main">
<div class="dd"><button class="dd-btn" type="button" aria-expanded="false" aria-controls="dd-svc">Services {I('plus', 'ic dd-ic')}</button>
<div class="dd-menu" id="dd-svc">{svc}</div></div>
{pages}
<a class="btn btn-accent nav-call" href="tel:{TEL}">{I('phone')} Call {PH}</a>
</nav>
<a class="hd-phone" href="tel:{TEL}">{I('phone', 'ic hd-phone-ic')}<span><small>Call Dan</small>{PH}</span></a>
<a class="btn btn-accent hd-cta" href="#contact">Free quote {I('arrow-right')}</a>
<button class="hd-menu" type="button" data-nav-toggle aria-controls="nav" aria-expanded="false" aria-label="Menu">{I('list', 'ic m-open')}{I('x', 'ic m-close')}</button>
</div></header>"""


def footer(path):
    svc = "".join(f'<li><a href="/{x["slug"]}/">{x["name"]}</a></li>' for x in SERVICES)
    pages = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in [("Home", "/")] + PAGES)
    return f"""<footer class="ft"><div class="wrap ft-grid">
<div class="ft-brand"><a href="/" class="ft-logo">{LOGO} loading="lazy"></a>
<p>Melbourne plumbers for builders, developers and homeowners. Bathrooms, new builds, commercial work and emergency callouts.</p>
<a class="btn btn-accent" href="tel:{TEL}">{I('phone')} {PH}</a></div>
<div><h3>Services</h3><ul>{svc}</ul></div>
<div><h3>Pages</h3><ul>{pages}</ul></div>
<div><h3>Contact</h3><ul class="ft-contact">
<li>{I('phone')}<a href="tel:{TEL}">{PH}</a></li>
<li>{I('envelope-simple')}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li>{I('map-pin')}<span>All of metropolitan Melbourne</span></li>
<li>{I('lightning')}<span>Emergency and same-day jobs taken</span></li></ul></div>
</div>
<div class="wrap ft-base"><p>&copy; <span data-year>2026</span> Metrowide Plumbing. All rights reserved.</p><p>{CREDIT}</p></div>
</footer>"""


def callbar(path):
    return f"""<div class="cb"><a class="cb-call" href="tel:{TEL}">{I('phone')} Call Dan</a><a class="cb-quote" href="#contact">Free quote</a></div>"""


s.header, s.footer, s.callbar = header, footer, callbar


def quote_form(subject, title, sub, dark=False, tag="h2"):
    opts = "".join(f"<option>{esc(j)}</option>" for j in JOBS)
    fields = f"""<div class="f-row"><label><span>Name</span><input name="name" autocomplete="name" required placeholder="Your name"></label>
<label><span>Phone</span><input name="phone" type="tel" autocomplete="tel" required placeholder="04xx xxx xxx"></label></div>
<div class="f-row"><label><span>Email</span><input name="email" type="email" autocomplete="email" placeholder="you@email.com"></label>
<label><span>Suburb</span><input name="suburb" autocomplete="address-level2" required placeholder="e.g. Brunswick"></label></div>
<label><span>What is the job?</span><select name="job">{opts}</select></label>
<label><span>Tell us a bit more</span><textarea name="message" rows="3" placeholder="What is happening and how soon you need us"></textarea></label>"""
    form = s.form(subject, fields, button=f"Send to Dan {I('arrow-right')}", cls="qf")
    return f"""<div class="qcard{' qcard-dark' if dark else ''}">
<{tag} class="qcard-h">{title}</{tag}><p class="qcard-p">{sub}</p>
{form}
<p class="qcard-note">{I('check-circle')} <span>Free quote, no obligation. Urgent? <a href="tel:{TEL}">Call {PH}</a></span></p>
</div>"""


def head(eyebrow, h2, p="", center=False, hid=None, dark=False):
    idattr = f' id="{hid}"' if hid else ""
    return f"""<div class="sh{' sh-c' if center else ''} rv"><p class="eyebrow">{eyebrow}</p><h2{idattr}>{h2}</h2>{f'<p class="sh-p">{p}</p>' if p else ''}</div>"""


def svc_cards(items):
    return "".join(f"""<a class="svc rv" style="--i:{i}" href="/{x['slug']}/">
<div class="svc-img">{s.img(x['card_photo'], sizes='(min-width: 1100px) 380px, (min-width: 700px) 45vw, 100vw')}</div>
<div class="svc-body"><span class="svc-ic">{I(x['icon'])}</span><h3>{x['name']}</h3><p>{x['blurb']}</p>
<span class="more">Learn more {I('arrow-right')}</span></div></a>""" for i, x in enumerate(items))


WALL = [("green", "Green finger tile, terrazzo and a freestanding bath"), ("arch", "Terrazzo, black tapware and an arch mirror"),
        ("brassvan", "Brushed brass wall mixer over a vessel basin"), ("double", "Double shower on white finger tile"),
        ("brassshower", "Brushed brass rain head and hand shower"), ("combo", "Bathroom and laundry in one room"),
        ("under", "Vanity wastes and stops, plumbed neat")]


def gallery(items, cls=""):
    return f'<div class="gal {cls}" data-gallery>' + "".join(
        f'<a class="gal-i rv" style="--i:{i % 3}" href="{s.largest(k)}" data-lb data-cap="{esc(c)}">'
        f'{s.img(k, sizes="(min-width: 1100px) 380px, (min-width: 700px) 45vw, 100vw")}<span class="gal-cap">{esc(c)}</span></a>'
        for i, (k, c) in enumerate(items)) + "</div>"


def cta_band():
    return f"""<section class="cta" aria-labelledby="cta-h"><div class="wrap cta-in rv">
<div><h2 id="cta-h">Need a plumber today?</h2><p>Emergency and same-day jobs across Melbourne. Free quotes on everything else.</p></div>
<div class="btns"><a class="btn btn-dark" href="tel:{TEL}">{I('phone')} Call {PH}</a><a class="btn btn-line-dark" href="#contact">Send an enquiry</a></div>
</div></section>"""


def contact_section():
    cards = [("phone", "Call Dan", f'<a href="tel:{TEL}">{PH}</a>'), ("envelope-simple", "Email", f'<a href="mailto:{EMAIL}">{EMAIL}</a>'),
             ("map-pin", "Service area", "All of metropolitan Melbourne"),
             ("clock", "Urgent jobs", "Emergency and same-day<!-- CLIENT TO CONFIRM: business hours -->")]
    cc = "".join(f'<div class="cc rv" style="--i:{i}"><span class="cc-ic">{I(ic)}</span><div><p class="cc-k">{k}</p><p class="cc-v">{v}</p></div></div>'
                 for i, (ic, k, v) in enumerate(cards))
    return f"""<section class="contact dark" id="contact" aria-labelledby="contact-h"><div class="wrap contact-in">
<div class="contact-copy">{head('Get in touch', 'Send Dan <span class="hl">the job</span>', 'Call for anything urgent. For everything else, send the details and Dan comes back to you with a time and a price.', hid='contact-h')}
<div class="cc-grid">{cc}</div></div>
<div class="rv">{quote_form('Contact Page Enquiry', 'Request a free quote', 'Name, number, suburb and the job. That is all we need.', dark=False, tag='h3')}</div>
</div></section>"""


def faq_section(items, title="Questions, <span class=\"hl\">answered</span>"):
    return f"""<section class="faq light-alt" aria-labelledby="faq-h"><div class="wrap faq-in">
<div class="faq-side">{head('Good to know', title, hid='faq-h')}
<div class="faq-call rv"><p>Cannot see your question? Dan is happy to talk it through.</p><a class="btn btn-accent" href="tel:{TEL}">{I('phone')} Call {PH}</a></div></div>
<div class="faq-list rv">{Site.faq_html(items, cls='fq')}</div>
</div></section>"""


_rl = list(d["regions"].items())
REGIONS = "".join(
    f'<div class="rg rv" style="--i:{i % 3}"><h3>{I("map-pin")} {esc(r)}</h3><ul>' + "".join(f'<li data-sub="{esc(x.lower())}">{esc(x)}</li>' for x in subs) + "</ul></div>"
    for i, (r, subs) in enumerate(_rl))


def areas_section(h2tag_id="areas-h", intro="We are Melbourne plumbers in the full sense. Builders, homeowners and businesses call us from the inner suburbs right out to the growth corridors."):
    return f"""<section class="areas light" aria-labelledby="{h2tag_id}"><div class="wrap areas-in">
<div class="areas-side">{head('Service areas', 'Plumbers across <span class="hl">all of Melbourne</span>', intro, hid=h2tag_id)}
<!-- CONFIRM WITH CLIENT BEFORE LAUNCH: form said 'All areas'. Regions and suburbs below are a starting list for Dan to correct. -->
<label class="find rv"><span>Check your suburb</span><span class="find-box">{I('magnifying-glass')}<input type="search" placeholder="Type your suburb" data-area-filter autocomplete="off"></span></label>
<p class="find-note rv" data-area-note>Not listed? We probably still cover it. <a href="tel:{TEL}">Call and ask.</a></p></div>
<div class="rg-grid">{REGIONS}</div>
</div></section>"""


STEPS = [("phone", "Call or send the job", "Tell us what is happening and where. Urgent, call. If it can wait, use the form and Dan comes back to you."),
         ("clipboard-text", "Free, upfront quote", "We look at the job and give you an accurate price before any work starts. No obligation."),
         ("calendar-check", "On site when we said", "We turn up on the day and time agreed. If anything changes, you hear it from us first."),
         ("broom", "Tested and tidy", "Everything is tested, the area is cleaned up and we tell you what we did before we leave.")]


def process_section():
    st = "".join(f'<div class="step rv" style="--i:{i}"><span class="step-n">{i + 1:02d}</span><span class="step-ic">{I(ic)}</span><h3>{t}</h3><p>{p}</p></div>'
                 for i, (ic, t, p) in enumerate(STEPS))
    return f"""<section class="process dark" aria-labelledby="proc-h"><div class="wrap">
{head('How it works', 'From first call to <span class="hl">job done</span>', 'Four steps, the same on a dripping tap or a new house. You always know what is next.', center=True, hid='proc-h')}
<div class="steps">{st}</div></div></section>"""


STATS = [("5", "", "Years plumbing Melbourne", True), ("Same", "-day", "Emergency callouts", False),
         ("Free", "", "Quotes, price agreed first", False), ("All", "", "Of metropolitan Melbourne", False)]


def stat_band():
    it = "".join(f'<div class="stat rv" style="--i:{i}"><p class="stat-n">{f"<span data-count={n}>0</span>" if c else n}{u}</p><p class="stat-l">{l}</p></div>'
                 for i, (n, u, l, c) in enumerate(STATS))
    return f'<section class="stats" aria-label="Metrowide at a glance"><div class="wrap stats-in">{it}</div></section>'


def inner_hero(h1_html, lead, photo, crumbs):
    trail = '<a href="/">Home</a>' + "".join(f'<span aria-hidden="true">/</span><a href="{u}">{esc(n)}</a>' for n, u in crumbs[:-1]) + f'<span aria-hidden="true">/</span><span>{esc(crumbs[-1][0])}</span>'
    return f"""<section class="ihero" aria-labelledby="h1">
<div class="hero-bg">{s.img(photo, sizes='100vw', eager=True, cls='hero-img')}</div>
<div class="wrap ihero-in"><p class="crumbs">{trail}</p>
<h1 id="h1">{h1_html}</h1><p class="hero-lead">{esc(lead)}</p>
<div class="btns"><a class="btn btn-accent" href="tel:{TEL}">{I('phone')} Call {PH}</a><a class="btn btn-ghost" href="#contact">Get a free quote</a></div></div>
</section>"""


def reviews_section():
    """Live Google reviews. Hidden until the kit loads reviews from /api/reviews (see _kit/reviews_api.js)."""
    if not s.has_google_reviews():
        return ""
    return f"""<section class="reviews light" data-gr-section aria-labelledby="rev-h"><div class="wrap">
<div class="sh sh-c"><p class="eyebrow">Google reviews</p><h2 id="rev-h">What customers <span class="hl">say about us</span></h2></div>
{s.reviews_mount(btn1='btn btn-line', btn2='btn btn-accent')}
</div></section>"""


# ---------------------------------------------------------------- home
home_faq = [
    ("Do you do emergency plumbing?", "Yes. We take emergency and same-day jobs across Melbourne. Call 0423 017 489 and tell us what is happening. If water is running, turn it off at the mains first."),
    ("Do you charge for quotes?", "No. Quotes are free. For renovations and new builds we quote from plans or a site visit, and the price is clear before work starts."),
    ("Do you work with builders and developers?", "Yes. A lot of our work is alongside builders and developers on new builds and renovations, from drainage and rough-in through to fit-off."),
    ("Which areas do you cover?", "All of metropolitan Melbourne, from the inner suburbs out to the north, west, east and south east. If you are not sure, call and ask."),
    ("Do you do commercial plumbing?", "Yes. We do commercial work as well as residential, including repairs and maintenance for businesses and property managers."),
    ("What if the job changes once you start?", "We tell you before we do anything extra and agree the price first. No surprise lines on the invoice."),
]

TRUST = [("clock", "5 years in business", "Residential and commercial"), ("lightning", "Emergency and same-day", "When water will not wait"),
         ("currency-circle-dollar", "Free, upfront quotes", "Price agreed before we start"), ("users-three", "Builders and homeowners", "Booked to your program")]
trust = "".join(f'<div class="tr rv" style="--i:{i}"><span class="tr-ic">{I(ic)}</span><div><p class="tr-k">{k}</p><p class="tr-v">{v}</p></div></div>'
                for i, (ic, k, v) in enumerate(TRUST))

WHY = [("Turn up when we say", "If we book 7am, we are there at 7am. If something changes, you hear it from us first."),
       ("Price before work", "A clear quote before a tile comes off or a pipe gets cut. Extras agreed first."),
       ("Work that lasts", "Set out right before the walls close, so the finished room looks as good as the photos."),
       ("Clean and tidy", "We protect your home, clean up after ourselves and walk you through what we did.")]
why = "".join(f'<li class="rv" style="--i:{i}">{I("check-circle", "ic why-ic")}<div><p class="why-k">{k}</p><p class="why-v">{v}</p></div></li>'
              for i, (k, v) in enumerate(WHY))

home = f"""
<section class="hero" aria-labelledby="h1">
<div class="hero-bg">{s.img('green', sizes='100vw', eager=True, cls='hero-img')}</div>
<div class="wrap hero-in">
<div class="hero-copy">
<ul class="pills"><li>{I('clock')} 5 years in business</li><li>{I('lightning')} Emergency and same-day</li><li>{I('currency-circle-dollar')} Free quotes</li></ul>
<h1 id="h1">Melbourne plumbers<br> who turn up<br> <span class="hl">when they say.</span></h1>
<p class="hero-lead">Bathroom renovations, new builds, commercial work and emergency callouts for builders, developers and homeowners right across Melbourne.</p>
<div class="btns"><a class="btn btn-accent btn-lg" href="tel:{TEL}">{I('phone')} Call {PH}</a><a class="btn btn-ghost btn-lg" href="#services">Our services</a></div>
<ul class="hero-ticks"><li>{I('check')} Residential and commercial</li><li>{I('check')} All of Melbourne</li><li>{I('check')} Price agreed first</li></ul>
</div>
<div class="hero-form" id="quote">{quote_form('Hero Form Enquiry', 'Get a <span class="hl">free quote</span>', 'Tell us about the job and Dan will get back to you with a time and a price.')}</div>
</div></section>

<section class="trust" aria-label="Why people call Metrowide"><div class="wrap trust-in">{trust}</div></section>

<section class="services light" id="services" aria-labelledby="svc-h"><div class="wrap">
<div class="sh-row">{head('What we do', 'Plumbing services <span class="hl">across Melbourne</span>', 'From a dripping tap to a full new build, one plumber who turns up, quotes first and finishes properly.', hid='svc-h')}</div>
<div class="svc-grid">{svc_cards(SERVICES)}
<div class="svc svc-cta rv" style="--i:5"><span class="svc-ic">{I('chat-circle-text')}</span><h3>Not sure what you need?</h3>
<p>Tell Dan what is going on and he will tell you straight what it needs and what it costs.</p>
<div class="btns"><a class="btn btn-dark" href="tel:{TEL}">{I('phone')} {PH}</a></div></div>
</div></div></section>

<section class="why dark" aria-labelledby="why-h"><div class="wrap why-in">
<div class="why-media rv">{s.img('arch', sizes='(min-width: 900px) 540px, 100vw')}
<div class="why-badge"><p class="why-badge-n">5</p><p class="why-badge-l">years plumbing<br>Melbourne</p></div></div>
<div class="why-copy">{head('Why Metrowide', 'Trades who <span class="hl">actually turn up</span>', 'Jobs run on trades who arrive when they say, talk to you before you have to chase them and finish to a consistent standard. That is the whole idea behind Metrowide.', hid='why-h')}
<ul class="why-list">{why}</ul>
<div class="btns rv"><a class="btn btn-accent" href="#contact">Get a free quote {I('arrow-right')}</a><a class="btn btn-ghost" href="/about/">About us</a></div></div>
</div></section>

{stat_band()}

<section class="work light-alt" aria-labelledby="work-h"><div class="wrap">
{head('Recent work', 'Bathrooms and fit-offs <span class="hl">we are proud of</span>', 'Terrazzo, finger tile, brushed brass and black tapware. Tap any photo to see it full size.', center=True, hid='work-h')}
<!-- CLIENT TO SUPPLY: suburb for each job, plus photos of new build, commercial and maintenance work. -->
{gallery(WALL[:6])}
<div class="center rv"><a class="btn btn-dark" href="/our-work/">See all our work {I('arrow-right')}</a></div>
</div></section>

{process_section()}

{reviews_section()}

{areas_section()}

{faq_section(home_faq)}

{cta_band()}

{contact_section()}
"""
s.page("/", title="Plumber Melbourne | Emergency, Renovations & New Builds | Metrowide Plumbing",
       description="Metrowide Plumbing: Melbourne plumbers for builders, developers and homeowners. Emergency and same-day jobs, renovations, new builds. Free quotes.",
       body=home, faq=home_faq, body_class="home")

# ---------------------------------------------------------------- service pages
for x in SERVICES:
    path = f"/{x['slug']}/"
    blocks = "".join(f'<div class="txt rv"><h2>{esc(h)}</h2><p>{esc(t)}</p></div>' for h, t in x["body"])
    items = "".join(f"<li>{I('check-circle')}<span>{esc(i)}</span></li>" for i in x["items"])
    others = [o for o in SERVICES if o is not x][:4]
    photos = [w for w in WALL if w[0] != x["photo"]][:3]
    body = f"""{inner_hero(hl(x['h1'], phrase='in Melbourne') if 'in Melbourne' in x['h1'] else hl(x['h1']), x['lead'], x['photo'], [(x['name'], path)])}
<section class="detail light" aria-label="{esc(x['name'])} details"><div class="wrap detail-in">
<div class="detail-main">{blocks}</div>
<aside class="detail-side rv"><div class="side-card"><h2>{esc(x['list_h'])}</h2><ul class="ticks">{items}</ul>
<a class="btn btn-accent btn-block" href="tel:{TEL}">{I('phone')} Call {PH}</a><a class="btn btn-line btn-block" href="#contact">Get a free quote</a></div></aside>
</div></section>
<section class="work light-alt" aria-labelledby="jobs-h"><div class="wrap">
{head('Our work', 'Jobs like <span class="hl">this one</span>', center=True, hid='jobs-h')}
{gallery(photos, 'gal-3')}
</div></section>
<section class="services light" aria-labelledby="more-h"><div class="wrap">
{head('More services', 'Other plumbing <span class="hl">we do</span>', hid='more-h')}
<div class="svc-grid svc-grid-4">{svc_cards(others)}</div></div></section>
{faq_section(x['faq'], title=esc(x['name']) + ' <span class="hl">questions</span>')}
{cta_band()}
{contact_section()}"""
    s.page(path, title=x["title"], description=x["desc"], body=body, faq=x["faq"], crumbs=[(x["name"], path)],
           extra_graph=[s.service_node(path, x["h1"], x["desc"])])

# ---------------------------------------------------------------- service areas
areas_body = f"""{inner_hero('Plumber <span class="hl">across Melbourne</span>', 'Metrowide means what it says. We plumb homes, builds and businesses right across metropolitan Melbourne, from the inner suburbs to the growth corridors.', 'double', [('Service areas', '/service-areas/')])}
{areas_section('areas-h', 'These are the suburbs we work in most. Type yours to check, and if it is not here, call. We probably still cover it.')}
<section class="services light-alt" aria-labelledby="every-h"><div class="wrap">
{head('Every area', 'Plumbing services <span class="hl">in every suburb</span>', hid='every-h')}
<div class="svc-grid">{svc_cards(SERVICES)}</div></div></section>
{cta_band()}
{contact_section()}"""
s.page("/service-areas/", title="Plumber Service Areas Melbourne | Metrowide Plumbing",
       description="Metrowide Plumbing covers metropolitan Melbourne: inner city, north, west, east, south east and bayside suburbs. Emergency, renovation and new build plumbing.",
       body=areas_body, crumbs=[("Service areas", "/service-areas/")])

# ---------------------------------------------------------------- our work
work_body = f"""{inner_hero('Our <span class="hl">plumbing work</span>', 'Recent bathrooms and fit-offs from around Melbourne. Tap any photo to see it full size.', 'brassvan', [('Our work', '/our-work/')])}
<section class="work light" aria-labelledby="all-h"><div class="wrap">
{head('Recent jobs', 'Every job <span class="hl">on file</span>', 'More photos are on the way as new jobs finish.', center=True, hid='all-h')}
<!-- CLIENT TO SUPPLY: suburb and year for each job, plus photos of new build, commercial and maintenance work. -->
{gallery(WALL)}</div></section>
{process_section()}
{cta_band()}
{contact_section()}"""
s.page("/our-work/", title="Our Work | Bathroom & Renovation Plumbing Melbourne | Metrowide",
       description="Photos of recent Metrowide Plumbing jobs in Melbourne: terrazzo and finger tile bathrooms, brushed brass and black tapware, showers and vanities.",
       body=work_body, crumbs=[("Our work", "/our-work/")])

# ---------------------------------------------------------------- about
about_body = f"""{inner_hero('About <span class="hl">Metrowide Plumbing</span>', 'Five years of plumbing across residential construction, renovations, maintenance and new builds, with the focus on workmanship, communication and turning up.', 'arch', [('About', '/about/')])}
<section class="why light" aria-labelledby="story-h"><div class="wrap why-in">
<div class="why-media rv">{s.img('green', sizes='(min-width: 900px) 540px, 100vw')}</div>
<div class="why-copy">{head('Our story', 'Plumbing built on <span class="hl">turning up</span>', hid='story-h')}
<div class="txt rv"><p>We work closely with builders, developers and homeowners so every job is delivered on time, on budget and with attention to detail. Rather than just completing the plumbing, we look after the whole experience, from an accurate quote to keeping you informed at every stage.</p></div>
<div class="txt rv"><p>Jobs rely on trades who turn up when they say they will, communicate before they are chased and finish to a consistently high standard. We know how much a late trade costs a build, so we plan not to be one.</p></div>
<div class="txt rv"><p>Our reputation is built on honest advice, quality craftsmanship and dependable service. Whether it is a custom home, a renovation or ongoing maintenance, we take pride in plumbing that lasts.</p></div>
<!-- CLIENT TO SUPPLY: VBA registration number, insurance, a photo of Dan and the van. -->
</div></div></section>
{stat_band()}
<section class="why dark" aria-labelledby="why-h"><div class="wrap why-in why-flip">
<div class="why-copy">{head('What you can expect', 'Four things <span class="hl">on every job</span>', hid='why-h')}<ul class="why-list">{why}</ul></div>
<div class="why-media rv">{s.img('double', sizes='(min-width: 900px) 540px, 100vw')}</div>
</div></section>
{cta_band()}
{contact_section()}"""
s.page("/about/", title="About Metrowide Plumbing | Melbourne Plumbers",
       description="Metrowide Plumbing has spent five years plumbing Melbourne homes, renovations and new builds, with a focus on workmanship, communication and turning up on time.",
       body=about_body, crumbs=[("About", "/about/")])

# ---------------------------------------------------------------- contact
contact_body = f"""{inner_hero('Contact <span class="hl">Metrowide Plumbing</span>', 'Call for anything urgent. For everything else, send the job below and Dan comes back to you with a time and a price.', 'brassshower', [('Contact', '/contact/')])}
{contact_section()}
{faq_section(home_faq)}"""
s.page("/contact/", title="Contact Metrowide Plumbing | Call 0423 017 489",
       description="Call Metrowide Plumbing on 0423 017 489 for emergency and same-day plumbing in Melbourne, or send the job for a free quote.",
       body=contact_body, faq=home_faq, crumbs=[("Contact", "/contact/")])

# ---------------------------------------------------------------- 404
s.page("/404/", title="Page not found | Metrowide Plumbing", description="That page is not here. Call Metrowide Plumbing on 0423 017 489 or head back to the home page.",
       body=f"""{inner_hero('That page <span class="hl">is not here</span>', 'The link may be old. Head home, or if water is going where it should not, call now.', 'under', [('Page not found', '/404/')])}
<section class="services light" aria-labelledby="pop-h"><div class="wrap">{head('Popular pages', 'Where to <span class="hl">next</span>', hid='pop-h')}
<div class="svc-grid">{svc_cards(SERVICES)}</div></div></section>
{contact_section()}""")

# ---------------------------------------------------------------- share card, favicons, notes
s.og_image("green", focus=(50, 50), mark=logo, headline="MELBOURNE PLUMBERS WHO\nTURN UP WHEN THEY SAY",
           line2="Emergency / Renovations / New builds / Commercial", small=f"Call Dan  {PH}",
           font_bold=s.ttf("barlow-condensed-latin-800-normal.woff2"), font_text=s.ttf("dm-sans-latin-500-normal.woff2"),
           ink="#ffffff", accent="#46a0d2", scrim=(12, 14, 17))
s.favicons("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#121417"/>
<path d="M18 14h36l-8 36H10z" fill="#46a0d2"/></svg>""")
s.notes(direction="Go Polar house style (rebuilt 18 Nov 2026 after Chris rejected the first, experimental build)",
        idea="Dark photo hero with quote form, logo blue accent on near black and white, condensed uppercase headings",
        live="Hero quote form, suburb checker, count-up stat band, gallery lightbox, FAQ accordion",
        type_="Barlow Condensed 600/700/800 (headings), DM Sans 400/500/700 (body), self-hosted",
        palette="Logo blue #46a0d2 accent (deep #1d6fa5 on light), near black #0d0f12 and #15181d, white and #f4f6f8",
        decisions=["Benchmarks: Bernard Electrics, Spray Pave, Turquoise, Moral Service, Quick Micks",
                   "No reviews section and no star rating: none supplied"])
s.finish()
