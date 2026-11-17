"""Metrowide Plumbing. Direction: the well-kept board (taste-skill dense-tiles), cut on the logo's slant.

Idea: on this page, the slanted black band of the Metrowide logo, with its blue marker square, becomes
the board: every action tile is cut on the logo's slant, and the name runs wider than its band the way
'metro wide' covers more ground than one suburb.
Live thing: 'Tell Dan what's going on' composes the job as a text or a form message from three taps.

Run: python3 sites/metrowide-plumbing/_src/build.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_kit"))
from PIL import Image  # noqa: E402

from gpkit import CREDIT, Site, esc, slugify  # noqa: E402

s = Site(__file__)
d = s.d
TEL = s.tel
PH = s.phone
SMS = "sms:" + TEL

s.fonts([("libre-franklin", "Libre Franklin", [700, 800, 900], ["normal"]),
         ("libre-franklin", "Libre Franklin", [900], ["italic"]),
         ("source-serif-4", "Source Serif 4", [400, 600], ["normal"]),
         ("source-serif-4", "Source Serif 4", [400], ["italic"])],
        preload=["libre-franklin-latin-900-italic.woff2", "source-serif-4-latin-400-normal.woff2"])

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

# ---------------------------------------------------------------- shared chrome
NAV = [("Emergency", "/emergency-plumber-melbourne/"), ("Renovations", "/bathroom-renovation-plumbing-melbourne/"),
       ("New builds", "/new-build-plumbing-melbourne/"), ("Commercial", "/commercial-plumbing-melbourne/"),
       ("Maintenance", "/plumbing-maintenance-melbourne/"), ("Our work", "/our-work/"),
       ("Areas", "/service-areas/"), ("About", "/about/"), ("Contact", "/contact/")]


def header(path):
    links = "".join(f'<a href="{u}"{" aria-current=page" if u == path else ""}>{n}</a>' for n, u in NAV)
    return f"""<header class="hd">
<a class="hd-logo" href="/">{LOGO}></a>
<nav class="hd-nav" id="nav" aria-label="Main">{links}</nav>
<a class="hd-call slant" href="tel:{TEL}"><span>Call Dan</span> {PH}</a>
<button class="hd-menu" type="button" data-nav-toggle aria-controls="nav" aria-expanded="false">Menu</button>
</header>"""


def footer(path):
    nav = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in NAV)
    return f"""<footer class="ft board">
<div class="t ft-say"><p class="ft-line">Melbourne plumbing that turns up when it says it will.</p>
<p class="ft-legal">&copy; <span data-year>2026</span> Metrowide Plumbing. {CREDIT}</p></div>
<nav class="t ft-nav" aria-label="Footer"><h3>Pages</h3><ul>{nav}</ul></nav>
<div class="t ft-time"><h3>Melbourne</h3><p>It is <time data-mel-time>now</time> in Melbourne.</p><p>Emergency and same-day jobs taken.</p></div>
<div class="t ft-mail"><h3>Email</h3><a href="mailto:{d['email']}">{d['email']}</a></div>
<div class="t ft-mark">{LOGO} loading="lazy"></div>
<a class="t ft-go" href="tel:{TEL}"><span>Call Dan<br>{PH}</span><svg viewBox="0 0 48 48" aria-hidden="true"><path d="M8 40 40 8M16 8h24v24" fill="none" stroke="currentColor" stroke-width="4"/></svg></a>
</footer>"""


def callbar(path):
    return f"""<div class="cb" aria-label="Quick contact">
<a class="cb-call slant" href="tel:{TEL}">Call {PH}</a>
<a class="cb-text" href="{'/#job' if path == '/' else '/contact/#job'}">Text the job</a>
</div>"""


s.header, s.footer, s.callbar = header, footer, callbar

JOBS = ["Burst or leaking pipe", "Blocked drain or toilet", "Hot water", "Leaking tap or toilet",
        "Bathroom renovation", "New build or extension", "Commercial job", "Something else"]
WHEN = ["Today", "This week", "Just a quote"]


def composer(subject):
    chips = "".join(f'<label class="chip"><input type="radio" name="job" value="{esc(j)}"{" checked" if i == 0 else ""}><span>{esc(j)}</span></label>'
                    for i, j in enumerate(JOBS))
    when = "".join(f'<label class="chip"><input type="radio" name="when" value="{w}"{" checked" if i == 0 else ""}><span>{w}</span></label>'
                   for i, w in enumerate(WHEN))
    fields = f"""<fieldset class="pick"><legend>What is the job?</legend><div class="chips">{chips}</div></fieldset>
<fieldset class="pick"><legend>How soon?</legend><div class="chips">{when}</div></fieldset>
<div class="cells">
<label><span>Your name</span><input name="name" autocomplete="name" required></label>
<label><span>Phone</span><input name="phone" type="tel" autocomplete="tel" required></label>
<label><span>Suburb</span><input name="suburb" autocomplete="address-level2" required data-suburb></label>
</div>
<label class="msg"><span>What is going on</span><textarea name="message" rows="3" data-msg required></textarea></label>"""
    f = s.form(subject, fields, button="Send to Dan", cls="composer", note="")
    return f.replace("</form>", f'<a class="sms slant" data-sms href="{SMS}">Or send it as a text</a></form>')


def faq_block(items, heading="Questions people ask"):
    return f"""<section class="faq board" aria-labelledby="faq-h">
<div class="t faq-head"><h2 id="faq-h">{heading}</h2><p>Something else? Call Dan on <a href="tel:{TEL}">{PH}</a>.</p></div>
<div class="faq-list">{Site.faq_html(items, cls='t')}</div>
</section>"""


def quote_strip(subject="Contact Page Enquiry"):
    strip = "".join(s.img(k, sizes="200px", cls="strip-img") for k in ["green", "brassvan", "double", "arch", "brassshower", "combo", "under"] * 2)
    fields = """<label><span>Name</span><input name="name" autocomplete="name" required placeholder="Name"></label>
<label><span>Phone</span><input name="phone" type="tel" autocomplete="tel" required placeholder="Phone"></label>
<label><span>Suburb</span><input name="suburb" autocomplete="address-level2" required placeholder="Suburb"></label>
<label><span>What is going on</span><input name="message" required placeholder="What is going on"></label>"""
    return f"""<section class="quote" id="quote" aria-labelledby="quote-h">
<div class="strip" aria-hidden="true"><div class="strip-run">{strip}</div></div>
<h2 id="quote-h">Free quotes, straight from Dan</h2>
{s.form(subject, fields, button="Get my quote", cls="bar")}
<p class="quote-small">Quotes are free. Rather talk? Call <a href="tel:{TEL}">{PH}</a> or email <a href="mailto:{d['email']}">{d['email']}</a>.</p>
</section>"""


# ---------------------------------------------------------------- home
facts = ["5 years in business", "Emergency and same-day", "Free quotes", "Builders, developers, homeowners", "All of Melbourne"]
link_tiles = "".join(f'<a class="t lk" href="/{x["slug"]}/">{x["nav"]}<span aria-hidden="true">{x["name"]}</span></a>' for x in SERVICES[:4])
rail = ["We turn up when we say", "You get the price first", "You hear about changes first", "We clean up after"]
rail_html = "".join(f'<p class="t r{i}">{r}</p>' for i, r in enumerate(rail))

home_faq = [
    ("Do you do emergency plumbing?", "Yes. We take emergency and same-day jobs across Melbourne. Call 0423 017 489 and tell us what is happening. If water is running, turn it off at the mains first."),
    ("Do you charge for quotes?", "No. Quotes are free. For renovations and new builds we quote from plans or a site visit, and the price is clear before work starts."),
    ("Do you work with builders and developers?", "Yes. A lot of our work is alongside builders and developers on new builds and renovations, from drainage and rough-in through to fit-off."),
    ("Which areas do you cover?", "All of metropolitan Melbourne, from the inner suburbs out to the north, west, east and south east. If you are not sure, call and ask."),
    ("Do you do commercial plumbing?", "Yes. We do commercial work as well as residential, including repairs and maintenance for businesses and property managers."),
    ("What if the job changes once you start?", "We tell you before we do anything extra and agree the price first. No surprise lines on the invoice."),
]

wall = [("green", "Green finger tile, terrazzo and a freestanding bath"), ("arch", "Terrazzo, black tapware and an arch mirror"),
        ("brassvan", "Brushed brass wall mixer over a vessel basin"), ("double", "Double shower on white finger tile"),
        ("brassshower", "Brushed brass rain head and hand shower"), ("combo", "Bathroom and laundry in one room"),
        ("under", "Vanity wastes and stops, plumbed neat")]


def wall_html(items, big=False):
    return "".join(f'<a class="w" href="{s.largest(k)}" data-lb data-cap="{esc(c)}">{s.img(k, sizes="(min-width: 900px) 40vw, 62vw")}'
                   f'<span class="cap">{esc(c)}</span></a>' for k, c in items)


_rl = list(d["regions"].items())
regions_html = "".join(
    f'<div class="t rg{" rg-last" if i == len(_rl) - 1 else ""}"><h3>{esc(r)}</h3><ul>' + "".join(f'<li data-sub="{esc(x.lower())}">{esc(x)}</li>' for x in subs) + "</ul></div>"
    for i, (r, subs) in enumerate(_rl))
steps = [("Call or text", "Tell us the job and the suburb. Urgent, call. If it can wait, text or use the form and Dan comes back to you."),
         ("Free quote", "We look at the job and give you an accurate price up front. No obligation, no guesswork."),
         ("On the day", "We turn up when we said we would. If anything changes, you hear it from us first, not from the builder."),
         ("Done and tidy", "We test everything, clean up and tell you what we did before we leave.")]
steps_html = "".join(
    f'<div class="stp s{i}{" open" if i == 0 else ""}"><button type="button" aria-expanded="{"true" if i == 0 else "false"}" aria-controls="stp{i}">{n}</button><p id="stp{i}">{t}</p></div>' for i, (n, t) in enumerate(steps))

home = f"""
<section class="hero board" aria-labelledby="h1">
<div class="t band" aria-hidden="true"><span>Plumbing Metro<b>wide</b> Plumbing</span></div>
<nav class="links" aria-label="Main services">{link_tiles}</nav>
<div class="t h-port">{s.img('brassshower', sizes='(min-width: 900px) 16vw, 50vw', eager=True)}</div>
<ul class="t h-facts">{''.join(f'<li>{x}</li>' for x in facts)}</ul>
<div class="t h-main">{s.img('green', sizes='(min-width: 900px) 66vw, 100vw', eager=True)}
<div class="h-say"><h1 id="h1">Melbourne plumbing that turns up when it says it will.</h1>
<p>Bathrooms, new builds, commercial and emergency work for builders, developers and homeowners.</p></div></div>
<div class="h-rail">{rail_html}<a class="t r-go slant" href="tel:{TEL}">Call Dan<strong>{PH}</strong></a></div>
</section>

<section class="job board" id="job" aria-labelledby="job-h">
<div class="t job-head"><h2 id="job-h">Tell Dan what is going on</h2>
<p>Three taps and your suburb. Send it as a text from your phone or straight to Dan's inbox, and he comes back to you with a time.</p></div>
<div class="t job-form">{composer('Hero Form Enquiry')}</div>
</section>

<section class="mosaic board" aria-labelledby="what-h">
<div class="t m-head"><h2 id="what-h">What we plumb</h2></div>
<div class="t m-photo">{s.img('brassvan', sizes='(min-width: 900px) 50vw, 100vw')}</div>
<div class="t m-fig"><strong>5</strong><span>years in business</span></div>
<ul class="t m-list">{''.join(f'<li><a href="/{x["slug"]}/">{x["name"]}</a></li>' for x in SERVICES)}</ul>
<p class="t m-say m1">Builders: rough-in and fit-off booked to your program.</p>
<p class="t m-say m2">Homeowners: a clear quote before a single tile comes off.</p>
<p class="t m-say m3">Emergencies: same-day when water is where it should not be.</p>
</section>

<div class="marquee" aria-hidden="true"><div class="mq-run"><span>Metrowide Plumbing / All of Melbourne / Emergency and same-day / Free quotes / </span><span>Metrowide Plumbing / All of Melbourne / Emergency and same-day / Free quotes / </span></div></div>

<section class="work" aria-labelledby="work-h">
<div class="work-top"><h2 id="work-h">Recent work</h2><a href="/our-work/">See every job</a></div>
<div class="wall" data-gallery>{wall_html(wall)}</div>
</section>

<section class="about board" aria-labelledby="about-h">
<div class="t ab-intro"><h2 id="about-h">Trades who turn up</h2>
<p class="lead">Successful jobs rely on trades who arrive when they say they will, communicate before they are chased and finish to a consistent standard. That is the whole idea behind Metrowide.</p></div>
<figure class="t ab-photo">{s.img('arch', sizes='(min-width: 900px) 60vw, 100vw')}
<figcaption>Honest advice, quality work and plumbing that lasts, on custom homes, renovations and maintenance alike.</figcaption></figure>
<div class="t ab-who"><h3>Who calls us</h3><ul><li>Builders</li><li>Developers</li><li>Homeowners</li><li>Property managers</li></ul></div>
<dl class="t ab-facts"><div><dt>In business</dt><dd>5 years</dd></div><div><dt>Covers</dt><dd>Melbourne metro</dd></div>
<div><dt>Urgent jobs</dt><dd>Same-day</dd></div><div><dt>Quotes</dt><dd>Free</dd></div></dl>
</section>

<section class="how board" aria-labelledby="how-h">
<div class="t how-head"><h2 id="how-h">How a job runs</h2>
<p>Four steps, the same on a dripping tap or a new house. You always know what is next and who is coming.</p></div>
<div class="how-row">{steps_html}</div>
</section>

{faq_block(home_faq)}

<section class="areas board" aria-labelledby="areas-h">
<div class="t ar-head"><h2 id="areas-h">All of Melbourne</h2>
<label class="ar-find"><span>Check your suburb</span><input type="search" placeholder="Type your suburb" data-area-filter autocomplete="off"></label>
<p class="ar-note" data-area-note>Not listed? We probably still cover it. <a href="tel:{TEL}">Call and ask.</a></p></div>
{regions_html}
<a class="t ar-more slant" href="/service-areas/">Every area we cover</a>
</section>

{quote_strip()}
"""
hero_end = home.index("</section>") + 10
home = home[:hero_end] + re.sub(r'class="t ', 'class="t rv ', home[hero_end:])
s.page("/", title="Plumber Melbourne | Emergency, Renovations & New Builds | Metrowide Plumbing",
       description="Metrowide Plumbing: Melbourne plumbers for builders, developers and homeowners. Emergency and same-day jobs, renovations, new builds. Free quotes.",
       body=home, faq=home_faq, body_class="home")


# ---------------------------------------------------------------- inner page frame
def inner_hero(h1, lead, photo, crumbs):
    trail = '<a href="/">Home</a>' + "".join(f' / <a href="{u}">{esc(n)}</a>' for n, u in crumbs[:-1]) + f' / <span>{esc(crumbs[-1][0])}</span>'
    return f"""<section class="ih board" aria-labelledby="h1">
<div class="t ih-say"><p class="crumbs">{trail}</p><h1 id="h1">{esc(h1)}</h1><p class="lead">{esc(lead)}</p>
<div class="ih-acts"><a class="btn slant" href="tel:{TEL}">Call {PH}</a><a class="btn2" href="#quote">Free quote</a></div></div>
<div class="t ih-photo">{s.img(photo, sizes='(min-width: 900px) 45vw, 100vw', eager=True)}</div>
</section>"""


for x in SERVICES:
    path = f"/{x['slug']}/"
    others = "".join(f'<li><a href="/{o["slug"]}/">{o["name"]}</a></li>' for o in SERVICES if o is not x)
    body_tiles = "".join(f'<div class="t sv-txt"><h2>{esc(h)}</h2><p>{esc(t)}</p></div>' for h, t in x["body"])
    body = f"""{inner_hero(x['h1'], x['lead'], x['photo'], [(x['name'], path)])}
<section class="sv board" aria-label="{esc(x['name'])} details">
<div class="t sv-list"><h2>{esc(x['list_h'])}</h2><ul>{''.join(f'<li>{esc(i)}</li>' for i in x['items'])}</ul></div>
{body_tiles}
<div class="t sv-more"><h2>Other plumbing</h2><ul>{others}<li><a href="/service-areas/">Areas we cover</a></li></ul></div>
</section>
<section class="work" aria-labelledby="work-h"><div class="work-top"><h2 id="work-h">Jobs like this</h2><a href="/our-work/">All our work</a></div>
<div class="wall short" data-gallery>{wall_html([w for w in wall if w[0] != x['photo']][:4])}</div></section>
{faq_block(x['faq'], heading=x['name'] + ' questions')}
{quote_strip()}"""
    body = re.sub(r'class="t (sv|faq|rg|ar)', r'class="t rv \1', body)
    s.page(path, title=x["title"], description=x["desc"], body=body, faq=x["faq"], crumbs=[(x["name"], path)],
           extra_graph=[s.service_node(path, x["h1"], x["desc"])])

# areas page
areas_body = f"""{inner_hero('Plumber across Melbourne', 'Metrowide means what it says. We plumb homes, builds and businesses right across metropolitan Melbourne, from the inner suburbs to the growth corridors.', 'double', [('Service areas', '/service-areas/')])}
<!-- CONFIRM WITH CLIENT BEFORE LAUNCH: form said 'All areas'. Regions and suburbs below are a starting list for Dan to correct. -->
<section class="areas board" aria-labelledby="areas-h">
<div class="t ar-head"><h2 id="areas-h">Find your suburb</h2>
<label class="ar-find"><span>Check your suburb</span><input type="search" placeholder="Type your suburb" data-area-filter autocomplete="off"></label>
<p class="ar-note" data-area-note>These are the suburbs we work in most. If yours is not here, call. We probably still cover it.</p></div>
{regions_html}
<div class="t ar-svc"><h2>Plumbing in every area</h2><ul>{''.join(f'<li><a href="/{x["slug"]}/">{x["name"]}</a></li>' for x in SERVICES)}</ul></div>
</section>
{quote_strip()}"""
s.page("/service-areas/", title="Plumber Service Areas Melbourne | Metrowide Plumbing",
       description="Metrowide Plumbing covers metropolitan Melbourne: inner city, north, west, east, south east and bayside suburbs. Emergency, renovation and new build plumbing.",
       body=areas_body, crumbs=[("Service areas", "/service-areas/")])

# work page
work_body = f"""{inner_hero('Our plumbing work', 'Recent bathrooms and fit-offs from around Melbourne. Tap any photo to see it full size.', 'brassvan', [('Our work', '/our-work/')])}
<!-- CLIENT TO SUPPLY: suburb and year for each job, plus photos of new build, commercial and maintenance work. -->
<section class="work" aria-labelledby="work-h"><div class="work-top"><h2 id="work-h">Every job on file</h2><a href="#quote">Get a quote</a></div>
<div class="wall" data-gallery>{wall_html(wall)}</div></section>
{quote_strip()}"""
s.page("/our-work/", title="Our Work | Bathroom & Renovation Plumbing Melbourne | Metrowide",
       description="Photos of recent Metrowide Plumbing jobs in Melbourne: terrazzo and finger tile bathrooms, brushed brass and black tapware, showers and vanities.",
       body=work_body, crumbs=[("Our work", "/our-work/")])

# about page
about_body = f"""{inner_hero('About Metrowide Plumbing', 'Five years of plumbing across residential construction, renovations, maintenance and new builds, with the focus on workmanship, communication and turning up.', 'arch', [('About', '/about/')])}
<section class="sv board" aria-label="About us">
<div class="t sv-txt"><h2>How we work</h2><p>We work closely with builders, developers and homeowners so every job is delivered on time, on budget and with attention to detail. Rather than just completing the plumbing, we look after the whole experience, from an accurate quote to keeping you informed at every stage.</p></div>
<div class="t sv-txt"><h2>Why it matters</h2><p>Jobs rely on trades who turn up when they say they will, communicate before they are chased and finish to a consistently high standard. We know how much a late trade costs a build, so we plan not to be one.</p></div>
<div class="t sv-txt"><h2>Built to last</h2><p>Our reputation is built on honest advice, quality craftsmanship and dependable service. Whether it is a custom home, a renovation or ongoing maintenance, we take pride in plumbing that lasts.</p></div>
<div class="t sv-list"><h2>The short version</h2><ul><li>5 years in business</li><li>Residential and commercial</li><li>Emergency and same-day jobs</li><li>Free quotes</li><li>All of Melbourne</li></ul></div>
<!-- CLIENT TO SUPPLY: VBA registration number, insurance, a photo of Dan and the van. -->
</section>
{quote_strip()}"""
s.page("/about/", title="About Metrowide Plumbing | Melbourne Plumbers",
       description="Metrowide Plumbing has spent five years plumbing Melbourne homes, renovations and new builds, with a focus on workmanship, communication and turning up on time.",
       body=about_body, crumbs=[("About", "/about/")])

# contact page
contact_body = f"""<section class="ih board" aria-labelledby="h1">
<div class="t ih-say"><p class="crumbs"><a href="/">Home</a> / <span>Contact</span></p><h1 id="h1">Contact Metrowide Plumbing</h1>
<p class="lead">Call for anything urgent. For everything else, text, email or send the job below and Dan comes back to you.</p>
<div class="ih-acts"><a class="btn slant" href="tel:{TEL}">Call {PH}</a><a class="btn2" href="mailto:{d['email']}">{d['email']}</a></div></div>
<dl class="t ct-facts"><div><dt>Phone</dt><dd><a href="tel:{TEL}">{PH}</a></dd></div><div><dt>Email</dt><dd><a href="mailto:{d['email']}">{d['email']}</a></dd></div>
<div><dt>Area</dt><dd>All of Melbourne</dd></div><div><dt>Hours</dt><dd>Emergency and same-day jobs taken<!-- CLIENT TO CONFIRM: business hours --></dd></div></dl>
</section>
<section class="job board" id="job" aria-labelledby="job-h">
<div class="t job-head"><h2 id="job-h">Send Dan the job</h2><p>Pick the job and how soon, add your suburb, and send it as a text or a message.</p></div>
<div class="t job-form">{composer('Contact Page Enquiry')}</div>
</section>"""
s.page("/contact/", title="Contact Metrowide Plumbing | Call 0423 017 489",
       description="Call Metrowide Plumbing on 0423 017 489 for emergency and same-day plumbing in Melbourne, or send the job for a free quote.",
       body=contact_body, crumbs=[("Contact", "/contact/")])

s.page("/404/", title="Page not found | Metrowide Plumbing", description="That page is not here. Call Metrowide Plumbing on 0423 017 489 or head back to the home page.",
       body=f"""<section class="ih board"><div class="t ih-say"><h1>That page is not here</h1><p class="lead">The link may be old. Head home, or if water is going where it should not, call now.</p>
<div class="ih-acts"><a class="btn slant" href="tel:{TEL}">Call {PH}</a><a class="btn2" href="/">Home page</a></div></div>
<div class="t sv-more"><h2>Popular pages</h2><ul>{''.join(f'<li><a href="{u}">{n}</a></li>' for n, u in NAV)}</ul></div></section>""")

# ---------------------------------------------------------------- share card and favicons
s.og_image("green", focus=(50, 50), mark=logo, headline="Melbourne plumbing that\nturns up when it says it will",
           line2="Emergency / Renovations / New builds / Commercial", small=f"Call Dan  {PH}",
           font_bold=s.ttf("libre-franklin-latin-900-italic.woff2"), font_text=s.ttf("source-serif-4-latin-600-normal.woff2")
           if (s.assets / "fonts" / "source-serif-4-latin-600-normal.woff2").exists() else s.ttf("source-serif-4-latin-400-normal.woff2"),
           ink="#f4f4f2", accent="#46a0d2", scrim=(15, 15, 15))
s.favicons("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><path d="M14 6h46L50 58H4z" fill="#181818"/>
<path d="M22 16h30l-6 32H16z" fill="#46a0d2"/></svg>""")
s.notes(**{'direction': "The well-kept board (taste-skill dense-tiles), dark board, tiles on 8px gaps, action tiles cut on the logo's slant", 'idea': "The slanted black band of the Metrowide logo, with its blue marker square, becomes the board; the name runs wider than its band the way 'metro wide' covers more than one suburb", 'live': "'Tell Dan what is going on': three taps (job, how soon, suburb) write the message, sent as an SMS or a Web3Forms enquiry", 'type_': 'Libre Franklin 700/800/900 + 900 italic (display), Source Serif 4 400/600 (text), self-hosted', 'palette': 'Logo black #181818 and blue #46a0d2 on a #0f0f0f board, paper #f4f4f2, blue tints for the process accordion', 'redraws': ['work: book-spine index needs 20 to 40 project names, Metrowide has 7 photos, so giant title and uneven wall', 'about: team portraits do not exist, so wide photo, colour tile and facts'], 'decisions': ["No video: house rule is client photos only and no honest clip of Metrowide's work exists", 'Inspector covered-text at 390px is the fixed mobile call bar passing over one statement tile']})
s.finish()
