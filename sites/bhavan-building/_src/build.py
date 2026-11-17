"""Bhavan Building. Direction: photographs at uneven sizes (taste-skill uneven-photographs), green-black and bone.

Idea: on this page, Bhavan's 'select number of projects' becomes the gallery wall: each finished room is hung
like a print with space around it, few and far apart, and the registration number is signed under the work.
Live thing: the room filter on the project wall (All, Kitchens, Bathrooms, Laundries) re-hangs the wall.

Run: python3 sites/bhavan-building/_src/build.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_kit"))
from gpkit import CREDIT, Site, esc  # noqa: E402

s = Site(__file__)
d = s.d
TEL, PH, MAIL, LIC = s.tel, s.phone, d["email"], d["licence_no"]

s.fonts([("newsreader", "Newsreader", [300, 400, 500], ["normal"]),
         ("newsreader", "Newsreader", [300], ["italic"])],
        preload=["newsreader-latin-300-normal.woff2", "newsreader-latin-400-normal.woff2"])

P = {
    "arch": ("kitchen-fluted-arch.jpg", "Dark fluted timber kitchen with an arched rangehood alcove, granite splashback and curved island", (50, 55), "Kitchens", "Fluted timber kitchen, arched alcove"),
    "wf1": ("kitchen-waterfall-1.jpg", "Timber and white kitchen with a marble-look waterfall island and three pendant lights", (50, 55), "Kitchens", "Waterfall island, timber joinery"),
    "wf2": ("kitchen-waterfall-2.jpg", "Waterfall island bench with a black sink and pull-down mixer under white pendants", (55, 50), "Kitchens", "Island with integrated sink"),
    "vanity1": ("bath-double-vanity-1.jpg", "Double timber vanity with two vessel basins and brushed brass wall mixers", (45, 55), "Bathrooms", "Double vanity, brushed brass"),
    "vanity2": ("bath-double-vanity-2.jpg", "Bathroom with brass shower rail, vertical gloss tiles and a timber double vanity", (40, 50), "Bathrooms", "Walk-in shower and vanity"),
    "basin": ("bath-vessel-basin.jpg", "Round vessel basin on a white stone top with a brushed brass mixer", (50, 55), "Bathrooms", "Vessel basin, mirrored cabinet"),
    "powder": ("powder-terracotta.jpg", "Powder room with terracotta wall tiles, terrazzo floor and an organic mirror", (50, 50), "Bathrooms", "Terracotta powder room"),
    "laundry1": ("laundry-sage-1.jpg", "Sage green shaker laundry with stacked Miele washer and dryer", (50, 50), "Laundries", "Sage shaker laundry"),
    "laundry2": ("laundry-sage-2.jpg", "Sage green laundry cabinetry with a steel sink and white subway tiles", (40, 50), "Laundries", "Sink run and stacked machines"),
    "laundry3": ("laundry-black-timber.jpg", "Laundry with black and oak cabinetry, terracotta tiles and Bosch machines under the bench", (50, 50), "Laundries", "Oak and black laundry"),
}
for k, (f, alt, focus, _, _) in P.items():
    s.image(k, f, alt, focus)

SERVICES = [
    dict(slug="kitchen-renovations-melbourne", name="Kitchen renovations", short="Kitchens", photos=["arch", "wf1", "wf2"],
         title="Kitchen Renovations Bentleigh East & South-East Melbourne | Bhavan Building",
         desc="Kitchen renovations by a registered builder in Bentleigh East. Joinery, stone, lighting and layout changes across south-east Melbourne. Free quotes.",
         h1=("Kitchen renovations,", "south-east Melbourne"),
         lead="The kitchen carries more of the house than any other room. We rebuild it around how you cook and gather, then finish it so it still looks right in fifteen years.",
         included=["Layout changes and new islands", "Custom joinery and cabinetry", "Stone and porcelain benchtops and splashbacks",
                   "Plumbing and electrical, coordinated", "Lighting, from pendants to under-cabinet strips", "Flooring and making good"],
         blocks=[("Planned before anything comes out", "We work through the layout, the appliances and the finishes with you before demolition, so the program is clear and the decisions are made while they are cheap to change."),
                 ("One builder, every trade", "Cabinet makers, stone masons, plumbers and electricians are booked and managed by us. You deal with the builder, not a list of trades."),
                 ("Finished properly", "Shadow lines, scribes and the joins between stone and joinery are where a kitchen looks expensive or not. That is where we spend the time.")],
         faq=[("How long does a kitchen renovation take?", "It depends on the joinery lead time and whether walls or plumbing move. We give you a program with dates before work starts."),
              ("Can we keep living at home during the kitchen renovation?", "Usually, yes. We plan the works so you lose the kitchen for as short a time as possible and keep the rest of the house clean."),
              ("Do you help choose finishes?", "Yes. We guide you through layouts, benchtops, joinery and lighting, and work with your designer if you have one.")]),
    dict(slug="bathroom-renovations-melbourne", name="Bathroom renovations", short="Bathrooms", photos=["vanity2", "basin", "powder"],
         title="Bathroom Renovations Bentleigh East & South-East Melbourne | Bhavan Building",
         desc="Bathroom, ensuite and powder room renovations by a registered builder in Bentleigh East. Waterproofing, tiling and fit-off done properly. Free quotes.",
         h1=("Bathroom renovations,", "south-east Melbourne"),
         lead="Bathrooms, ensuites and powder rooms built from the waterproofing up. The part you never see is the part that decides whether it lasts.",
         included=["Full strip-out and removal", "Layout changes, walk-in showers and niches", "Waterproofing to the Australian Standard",
                   "Floor-to-ceiling tiling", "Vanities, tapware and fixtures", "Lighting, heat and ventilation"],
         blocks=[("Built from the waterproofing up", "Falls to the waste, membranes and screeds are done before a tile goes on. It is the least glamorous part of the job and the one we are most careful with."),
                 ("Details that hold up", "Mixer heights, niche positions and tile set-out are agreed before the wall is closed, so the finished room lines up the way the drawing does."),
                 ("Small rooms too", "Powder rooms and ensuites get the same care as a main bathroom. Often the smallest room is where a finish shows most.")],
         faq=[("How long does a bathroom renovation take?", "A typical bathroom runs a few weeks from strip-out to handover. We confirm your program once the design and fixtures are chosen."),
              ("Can you move the shower or toilet?", "Usually, yes. Moving fixtures depends on where the drainage runs, which we check before quoting."),
              ("Is waterproofing included?", "Yes. Waterproofing is part of every wet area we build, done to the Australian Standard before tiling.")]),
    dict(slug="laundry-renovations-melbourne", name="Laundry renovations", short="Laundries", photos=["laundry1", "laundry2", "laundry3"],
         title="Laundry Renovations Bentleigh East & South-East Melbourne | Bhavan Building",
         desc="Laundry renovations in Bentleigh East and south-east Melbourne. Stacked machines, full-height storage, new sinks and tiling by a registered builder.",
         h1=("Laundry renovations,", "south-east Melbourne"),
         lead="A good laundry is a room you do not have to think about. Machines at the right height, storage to the ceiling and a bench that works.",
         included=["Stacked or side-by-side machine housings", "Full-height storage and linen cupboards", "New sinks, tapware and plumbing",
                   "Benchtops and splashback tiling", "Hanging rails and pull-out baskets", "Moving the laundry to a better spot"],
         blocks=[("Designed around the machines", "We build the joinery around the exact washer and dryer you own or are buying, with the clearances and ventilation they need."),
                 ("Storage that earns its space", "Every cupboard is planned for what goes in it, from brooms and the ironing board to baskets under the bench."),
                 ("Finished like the rest of the house", "Shaker doors in sage, oak and black, terracotta tile. A laundry deserves the same finish as the kitchen next door.")],
         faq=[("Can you move my laundry?", "Often, yes. It depends on plumbing and drainage access, which we check on site before quoting."),
              ("Can the dryer be stacked on the washer?", "Yes, with the right stacking kit or a joinery shelf, and ventilation planned for the dryer."),
              ("Do you renovate the laundry with other rooms?", "Yes. Many clients do the laundry with the kitchen or bathroom to share the trades and the disruption.")]),
    dict(slug="home-extensions-rebuilds-melbourne", name="Extensions and rebuilds", short="Extensions", photos=["wf1", "arch", "wf2"],
         title="Home Extensions & Knock-Down Rebuilds Bentleigh East | Bhavan Building",
         desc="Home extensions, whole-house renovations and knock-down rebuilds in Bentleigh East and south-east Melbourne, by a registered domestic builder.",
         h1=("Extensions and rebuilds,", "south-east Melbourne"),
         lead="When the house no longer fits the family, we extend it, renovate it top to bottom or knock it down and build again, managed by one registered builder from permits to handover.",
         included=["Ground and first-floor extensions", "Whole-house renovations", "Knock-down rebuilds",
                   "Working with your architect, engineer and surveyor", "Permits and building approvals coordinated", "Open-plan living, kitchens and wet areas"],
         blocks=[("A builder who stays on the job", "We take on a select number of projects so you deal directly with the builder, not a call centre, from the first meeting to the keys."),
                 ("The right consultants", "We collaborate with trusted architects, engineers and suppliers, or work with the team you already have."),
                 ("Clear contracts, clear programs", "You know the price, the stages and the program before we start, and you hear from us at every stage.")],
         faq=[("Do you handle permits?", "We coordinate the building permit with your surveyor and work with your architect and engineer through approvals."),
              ("Can we live in the house during an extension?", "Often, yes, with the works sealed off. For major renovations and rebuilds you will need to move out, and we plan the program around that."),
              ("Do you build from someone else's plans?", "Yes. We can quote and build from your architect's drawings or bring in a designer we trust.")]),
]
d["services"] = [{"name": x["name"], "slug": x["slug"], "page": True} for x in SERVICES]
d["areas"] = [sub for subs in d["regions"].values() for sub in subs]

NAV = [("Home", "/")] + [(x["name"], f"/{x['slug']}/") for x in SERVICES] + [("Projects", "/projects/"), ("Areas", "/service-areas/"), ("About", "/about/"), ("Contact", "/contact/")]
WORDMARK = '<span class="wm">Bhavan<span>Building</span></span>'


def header(path):
    links = "".join(f'<li><a href="{u}"{" aria-current=page" if u == path else ""}>{n}</a></li>' for n, u in NAV)
    return f"""<header class="hd">
<button class="hd-menu" type="button" data-nav-toggle aria-controls="nav" aria-expanded="false">Menu</button>
<a class="hd-wm" href="/" aria-label="Bhavan Building home">{WORDMARK}</a>
<a class="hd-call" href="tel:{TEL}">{PH}</a>
<nav class="nav" id="nav" aria-label="Main"><ul>{links}</ul>
<p class="nav-foot"><a href="tel:{TEL}">{PH}</a><br><a href="mailto:{MAIL}">{MAIL}</a><br>Registration {LIC}</p></nav>
</header>"""


def footer(path):
    links = "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in NAV[1:])
    return f"""<footer class="ft">
<div class="ft-photo">{s.img('arch', sizes='(min-width: 900px) 50vw, 100vw', alt='')}</div>
<div class="ft-side"><a class="ft-wm" href="/">{WORDMARK}</a>
<nav aria-label="Footer"><ul class="ft-menu">{links}</ul></nav>
<div class="ft-blocks"><div><h3>Talk to Abi</h3><p><a href="tel:{TEL}">{PH}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p></div>
<div><h3>Registered builder</h3><p>{LIC}<br>Based in Bentleigh East, Victoria</p></div></div>
<p class="ft-legal">&copy; <span data-year>2026</span> Bhavan Building. {CREDIT}</p></div>
</footer>"""


def callbar(path):
    return f'<div class="cb"><a href="tel:{TEL}">Call {PH}</a><a href="{"#enquire" if path in ("/", "/contact/") else "/contact/#enquire"}">Enquire</a></div>'


s.header, s.footer, s.callbar = header, footer, callbar


def enquiry(subject, preset=""):
    opts = "".join(f'<option{" selected" if preset == o else ""}>{o}</option>' for o in
                   ["Kitchen renovation", "Bathroom renovation", "Laundry renovation", "Full house renovation", "Extension", "Knock-down rebuild", "Not sure yet"])
    fields = f"""<div class="f-grid">
<label><span>Name</span><input name="name" autocomplete="name" required></label>
<label><span>Phone</span><input name="phone" type="tel" autocomplete="tel" required></label>
<label><span>Email</span><input name="email" type="email" autocomplete="email" required></label>
<label><span>Suburb</span><input name="suburb" autocomplete="address-level2" required></label>
<label class="wide"><span>Project</span><select name="project">{opts}</select></label>
<label class="wide"><span>Tell us about your home and what you have in mind</span><textarea name="message" rows="4" required></textarea></label>
</div>"""
    return f"""<section class="enq" id="enquire" aria-labelledby="enq-h">
<div class="enq-say"><h2 id="enq-h">Tell us about your home</h2>
<p>We reply within one business day to arrange a time to talk or visit. Quotes are free.<!-- CLIENT TO CONFIRM: reply time --></p>
<p class="enq-alt">Or call Abi on <a href="tel:{TEL}">{PH}</a>, or text the same number.</p></div>
{s.form(subject, fields, button="Send enquiry", cls="enq-form")}
</section>"""


def faq_section(items, tall="laundry3", square="powder"):
    return f"""<section class="faq" aria-labelledby="faq-h">
<div class="faq-col"><h2 id="faq-h">Before you call</h2>
<ul class="faq-facts"><li>Based in Bentleigh East</li><li>Registered builder {LIC}</li><li>Free quotes</li><li><a href="tel:{TEL}">{PH}</a></li></ul>
<div class="faq-acc">{Site.faq_html(items)}</div>
<div class="faq-acts"><a class="btn" href="#enquire">Start a conversation</a><a class="tl" href="tel:{TEL}">Call {PH}</a></div></div>
<div class="faq-pics"><div class="fp-tall">{s.img(tall, sizes='(min-width: 900px) 40vw, 100vw')}</div><div class="fp-sq">{s.img(square, sizes='(min-width: 900px) 14vw, 38vw')}</div></div>
</section>"""


def contact_band():
    return f"""<section class="cband" aria-label="Contact">
<p class="cb-say">Renovations, extensions and rebuilds, a few at a time, in Bentleigh East and the suburbs around it.</p>
<div class="cb-pic">{s.img('basin', sizes='170px', alt='')}</div>
<div class="cb-links"><p class="cb-q">Planning something?</p><a href="mailto:{MAIL}">{MAIL}</a><a href="tel:{TEL}">{PH}</a>
<p class="cb-small">Bentleigh East, Melbourne. Free quotes.</p></div>
</section>"""


# ---------------------------------------------------------------- home
home_faq = [
    ("What does Bhavan Building do?", "We are a registered residential builder doing kitchen, bathroom and laundry renovations, full house renovations, extensions and knock-down rebuilds across Bentleigh East and south-east Melbourne."),
    ("Is Bhavan Building a registered builder?", f"Yes. We are a registered building practitioner in Victoria, registration {LIC}."),
    ("Do you charge for quotes?", "No. Quotes are free. We visit, talk through what you want and give you a clear price and program."),
    ("How many projects do you take on?", "A select number at a time, so every client deals directly with the builder and gets proper attention from start to finish."),
    ("Which suburbs do you work in?", "Bentleigh East and the suburbs around it, from Brighton and Sandringham to Glen Waverley, Malvern, Camberwell and Kew."),
    ("Do you work with architects and designers?", "Yes. We build from your architect's plans or bring in the designers, engineers and suppliers we trust."),
]
WALL = ["arch", "laundry1", "vanity1", "wf2", "powder", "basin", "wf1", "laundry2", "vanity2", "laundry3"]


def wall(keys, heading_html):
    tiles = "".join(f'<a class="pj p{i}" href="{s.largest(k)}" data-lb data-cap="{esc(P[k][4])}" data-room="{P[k][3]}">'
                    f'{s.img(k, sizes="(min-width: 900px) 44vw, 90vw")}<span class="pj-cap"><span>{esc(P[k][4])}</span><span>{P[k][3][:-1] if P[k][3] != "Laundries" else "Laundry"}</span></span></a>'
                    for i, k in enumerate(keys))
    chips = "".join(f'<button type="button" class="room{" on" if r == "All" else ""}" data-room-filter="{r}" aria-pressed="{"true" if r == "All" else "false"}">{"All rooms" if r == "All" else r}</button>'
                    for r in ["All", "Kitchens", "Bathrooms", "Laundries"])
    return f"""<section class="wall" aria-labelledby="wall-h">
<div class="wall-head">{heading_html}<div class="rooms" role="group" aria-label="Show rooms">{chips}</div><p class="rooms-n" data-room-count aria-live="polite">Ten rooms</p></div>
<div class="wall-grid" data-gallery>{tiles}</div>
</section>"""


statements = [("What we build", "/projects/", None)] + [(x["short"] if x["short"] != "Extensions" else "Extensions and rebuilds", f"/{x['slug']}/", x["photos"][:2]) for x in SERVICES] + [("Whole-home renovations", "/home-extensions-rebuilds-melbourne/", ["wf2", "laundry1"])]
pairs = "".join(f'<div class="sc-pair" data-k="{i}">' + "".join(s.img(k, sizes="240px", cls=f"sc-p{j}", alt="") for j, k in enumerate(ph)) + "</div>"
                for i, (_, _, ph) in enumerate(statements) if ph)
items = "".join((f'<li class="sc-i on" data-k="{i}"><h2 id="scene-h">{t}</h2></li>' if i == 0 else f'<li class="sc-i" data-k="{i}"><a href="{u}">{t}</a></li>')
                for i, (t, u, _) in enumerate(statements))
marks = "".join(f'<div class="sc-mark" data-k="{i}"></div>' for i in range(len(statements)))

steps = [("vanity2", "At the first meeting,", "we listen. What works about the house, what does not, how you live in it and what you want to spend. Then we tell you honestly what is possible."),
         ("basin", "Before anything is pulled out,", "you have a fixed price, a program with dates and every selection agreed. No surprises in week three."),
         ("wf1", "At handover,", "the house is clean, every trade's work is checked and you walk through it with the builder who built it.")]
how = "".join(f'<div class="hw hw{i}"><div class="hw-pic">{s.img(k, sizes="(min-width: 900px) 34vw, 90vw")}</div><p><strong>{a}</strong> {b}</p></div>' for i, (k, a, b) in enumerate(steps))

home = f"""
<section class="hero" aria-labelledby="h1">
<figure class="h-small">{s.img('wf1', sizes='(min-width: 900px) 24vw, 46vw', eager=True)}</figure>
<h1 id="h1" class="h-title"><span class="ln l1"><span>A few homes,</span></span> <span class="ln l2"><span>done well.</span></span></h1>
<figure class="h-tall">{s.img('arch', sizes='(min-width: 900px) 30vw, 72vw', eager=True)}</figure>
<div class="h-sub"><p>Kitchens, bathrooms, extensions and knock-down rebuilds in Bentleigh East and south-east Melbourne, by a registered builder who takes on a select number of homes at a time.</p>
<div class="h-acts"><a class="btn" href="#enquire">Start a conversation</a><a class="tl" href="tel:{TEL}">Call {PH}</a></div></div>
</section>

<section class="rooms-scene" aria-labelledby="scene-h">
<div class="sc-stage">{s.img('wf2', sizes='100vw', cls='sc-bg', alt='')}<div class="sc-scrim"></div>
<ol class="sc-list">{items}</ol>{pairs}</div>
<div class="sc-marks" aria-hidden="true">{marks}</div>
</section>

{wall(WALL, '<h2 id="wall-h">Recent<br>rooms</h2>')}

<section class="about" aria-label="About Bhavan Building">
<dl class="ab-facts"><div><dt>Based in</dt><dd>Bentleigh East</dd></div><div><dt>Registration</dt><dd>{LIC}</dd></div><div><dt>Building for</dt><dd>5 years</dd></div></dl>
<p class="ab-para">Bhavan Building is a registered residential builder. We do not take on more work than we can properly manage: a select number of homes at a time, so every client gets direct contact with the builder, honest advice and close attention to detail from the first consultation to handover.</p>
<p class="ab-word">Rooms</p>
<ul class="ab-list"><li>Kitchens</li><li>Bathrooms and ensuites</li><li>Powder rooms</li><li>Laundries</li><li>Extensions</li><li>Knock-down rebuilds</li></ul>
<p class="ab-word ab-w2">Alongside</p>
<ul class="ab-list ab-l2"><li>Architects</li><li>Engineers</li><li>Building surveyors</li><li>Trusted trades</li><li>Premium suppliers</li><li>Your designer</li></ul>
<a class="tl ab-more" href="/about/">More about Bhavan</a>
</section>

<section class="how" aria-labelledby="how-h"><h2 id="how-h">How a project runs</h2>{how}</section>

{faq_section(home_faq)}
{contact_band()}
{enquiry('Home Page Enquiry')}
"""
home = re.sub(r'class="(pj|hw|ab-|faq-col|cb-|enq-say)', r'class="rv \1', home)
s.page("/", title="Builder Bentleigh East | Renovations, Extensions & Rebuilds | Bhavan Building",
       description="Bhavan Building: registered builder in Bentleigh East for kitchen, bathroom and laundry renovations, extensions and knock-down rebuilds. Free quotes.",
       body=home, faq=home_faq, body_class="home")


# ---------------------------------------------------------------- inner pages
def inner_hero(h1a, h1b, lead, photos, crumbs, eager=True):
    trail = '<a href="/">Home</a>' + "".join(f' / <a href="{u}">{esc(n)}</a>' for n, u in crumbs[:-1]) + f" / <span>{esc(crumbs[-1][0])}</span>"
    a, b = photos[0], photos[1]
    return f"""<section class="ih" aria-labelledby="h1">
<p class="crumbs">{trail}</p>
<h1 id="h1" class="ih-title"><span class="ln l1"><span>{esc(h1a)}</span></span> <span class="ln l2"><span>{esc(h1b)}</span></span></h1>
<p class="ih-lead">{esc(lead)}</p>
<figure class="ih-a">{s.img(a, sizes='(min-width: 900px) 46vw, 100vw', eager=eager)}</figure>
<figure class="ih-b">{s.img(b, sizes='(min-width: 900px) 26vw, 72vw')}</figure>
</section>"""


for x in SERVICES:
    path = f"/{x['slug']}/"
    blocks = "".join(f'<div class="rv sv-b sv-b{i}"><h2>{esc(h)}</h2><p>{esc(t)}</p></div>' for i, (h, t) in enumerate(x["blocks"]))
    others = "".join(f'<li><a href="/{o["slug"]}/">{o["name"]}</a></li>' for o in SERVICES if o is not x)
    body = f"""{inner_hero(*x['h1'], x['lead'], x['photos'][:2], [(x['name'], path)])}
<section class="sv" aria-label="{esc(x['name'])}">
<div class="rv sv-inc"><h2>What is included</h2><ul>{''.join(f'<li>{esc(i)}</li>' for i in x['included'])}</ul></div>
<figure class="rv sv-pic">{s.img(x['photos'][2], sizes='(min-width: 900px) 30vw, 72vw')}</figure>
{blocks}
<div class="rv sv-more"><h2>Other work</h2><ul>{others}<li><a href="/projects/">All projects</a></li><li><a href="/service-areas/">Suburbs we build in</a></li></ul></div>
</section>
{faq_section(x['faq'], tall=x['photos'][0], square=x['photos'][1])}
{contact_band()}
{enquiry('Contact Page Enquiry', preset={'Kitchens': 'Kitchen renovation', 'Bathrooms': 'Bathroom renovation', 'Laundries': 'Laundry renovation'}.get(x['short'], 'Extension'))}"""
    s.page(path, title=x["title"], description=x["desc"], body=body, faq=x["faq"], crumbs=[(x["name"], path)],
           extra_graph=[s.service_node(path, " ".join(x["h1"]).replace(",", ""), x["desc"])])

SUBURB_PAGES, SUBURB_LINKS = s.suburbs()


def sub_li(name):
    return f'<li><a href="{SUBURB_LINKS[name]}">{esc(name)}</a></li>' if name in SUBURB_LINKS else f"<li>{esc(name)}</li>"


for sp in SUBURB_PAGES:
    path, sub = sp["path"], sp["suburb"]
    facts = [f"Postcode {sp['postcode']}", sp["council"], f"{sp['distance_km']} km from our Bentleigh East base, about {sp['drive_min']} minutes"]
    blocks = "".join(f'<div class="rv sv-b sv-b{i}"><h2>{esc(x["h"])}</h2><p>{esc(x["p"])}</p></div>' for i, x in enumerate(sp["sections"][:3]))
    near = "".join(f'<li><a href="{SUBURB_LINKS[n]}">Builder in {esc(n)}</a></li>' for n in sp["neighbours"] if n in SUBURB_LINKS)
    focus = [x for x in SERVICES if x["slug"] in sp.get("focus_services", [])] or SERVICES
    svc = "".join(f'<li><a href="/{x["slug"]}/">{x["name"]}</a></li>' for x in focus)
    body = f"""{inner_hero(*sp['h1'], sp['lead'], sp['photos'][:2], [('Service areas', '/service-areas/'), (sub, path)])}
<section class="sv" aria-label="Building in {esc(sub)}">
<div class="rv sv-inc"><h2>{esc(sub)} at a glance</h2><ul>{''.join(f'<li>{esc(f)}</li>' for f in facts)}<li>Next door: {esc(', '.join(sp['neighbours']))}</li></ul></div>
<figure class="rv sv-pic">{s.img(sp['photos'][2], sizes='(min-width: 900px) 30vw, 72vw')}</figure>
{blocks}
<div class="rv sv-more"><h2>What we build in {esc(sub)}</h2><ul>{svc}{near}<li><a href="/service-areas/">All suburbs</a></li></ul></div>
</section>
{faq_section(sp['faq'], tall=sp['photos'][0], square=sp['photos'][1])}
{contact_band()}
{enquiry('Contact Page Enquiry')}"""
    node = {"@type": "Service", "@id": f"{s.base}{path}#service", "name": f"Builder in {sub}", "description": sp["desc"],
            "provider": {"@id": f"{s.base}/#business"}, "url": f"{s.base}{path}",
            "areaServed": {"@type": "City", "name": sub, "address": {"@type": "PostalAddress", "postalCode": sp["postcode"], "addressRegion": "VIC", "addressCountry": "AU"}}}
    s.page(path, title=sp["title"], description=sp["desc"], body=body, faq=sp["faq"],
           crumbs=[("Service areas", "/service-areas/"), (sub, path)], extra_graph=[node])

rl = list(d["regions"].items())
regions = "".join(f'<div class="rv rg"><h2>{esc(r)}</h2><ul>' + "".join(sub_li(sub) for sub in subs) + "</ul></div>" for r, subs in rl)
areas_body = f"""{inner_hero('Building in Bentleigh East', 'and the suburbs around it', 'We are based in Bentleigh East and build across the south-east and inner-east suburbs, close enough that the builder is on site, not stuck in traffic.', ['vanity1', 'laundry2'], [('Service areas', '/service-areas/')])}
<!-- CONFIRM WITH CLIENT BEFORE LAUNCH: suburbs grouped into regions from the form list. -->
<section class="areas" aria-label="Suburbs">{regions}
<div class="rv rg rg-svc"><h2>What we build there</h2><ul>{''.join(f'<li><a href="/{x["slug"]}/">{x["name"]}</a></li>' for x in SERVICES)}</ul></div></section>
{contact_band()}
{enquiry('Contact Page Enquiry')}"""
s.page("/service-areas/", title="Builder Service Areas | Bentleigh East, Bayside & South-East Melbourne | Bhavan",
       description="Bhavan Building renovates and builds in Bentleigh East, Brighton, Hampton, Glen Waverley, Malvern, Camberwell, Kew and nearby south-east Melbourne suburbs.",
       body=areas_body, crumbs=[("Service areas", "/service-areas/")])

projects_body = f"""{inner_hero('Recent projects', 'kitchens, bathrooms, laundries', 'A selection of finished rooms. Filter by room, then tap any photograph to see it full size.', ['vanity2', 'laundry1'], [('Projects', '/projects/')])}
<!-- CLIENT TO SUPPLY: suburb and year for each project, and photos of extensions and rebuilds. -->
{wall(WALL, '<h2 id="wall-h">Every<br>room</h2>')}
{contact_band()}
{enquiry('Contact Page Enquiry')}"""
projects_body = re.sub(r'class="pj ', 'class="rv pj ', projects_body)
s.page("/projects/", title="Renovation Projects | Kitchens, Bathrooms & Laundries | Bhavan Building",
       description="Finished kitchens, bathrooms, powder rooms and laundries by Bhavan Building, a registered builder in Bentleigh East, south-east Melbourne.",
       body=projects_body, crumbs=[("Projects", "/projects/")])

about_body = f"""{inner_hero('About Bhavan Building', 'a select number of homes', 'A registered residential builder in Bentleigh East doing renovations, extensions and custom homes across Melbourne, with the builder on every job.', ['arch', 'basin'], [('About', '/about/')])}
<section class="sv" aria-label="About">
<div class="rv sv-b sv-b0"><h2>Why the name</h2><p>Bhavan is the Hindi and Sanskrit word for a house. It is a fair summary of the job: homes that are beautiful, practical and built to stand the test of time.<!-- CONFIRM WITH CLIENT BEFORE LAUNCH: meaning of the name --></p></div>
<div class="rv sv-b sv-b1"><h2>Fewer projects, done properly</h2><p>We do not cut corners or take on more work than we can manage. Focusing on a select number of projects means personal service, direct communication with the builder and real attention to detail throughout.</p></div>
<div class="rv sv-b sv-b2"><h2>The people around the build</h2><p>We work with trusted tradespeople, architects, engineers and suppliers to meet the highest standards of craftsmanship, compliance and finish, whether it is an extension, a full renovation or a custom home.</p></div>
<div class="rv sv-inc"><h2>In short</h2><ul><li>Registered builder, {LIC}</li><li>Based in Bentleigh East</li><li>5 years building in Melbourne</li><li>Free quotes</li><li>Renovations, extensions, rebuilds</li></ul></div>
<figure class="rv sv-pic">{s.img('laundry3', sizes='(min-width: 900px) 30vw, 72vw')}</figure>
</section>
{contact_band()}
{enquiry('Contact Page Enquiry')}"""
s.page("/about/", title="About Bhavan Building | Registered Builder, Bentleigh East",
       description="Bhavan Building is a registered residential builder in Bentleigh East taking a select number of renovations, extensions and rebuilds at a time.",
       body=about_body, crumbs=[("About", "/about/")])

contact_body = f"""<section class="ih ih-contact" aria-labelledby="h1">
<p class="crumbs"><a href="/">Home</a> / <span>Contact</span></p>
<h1 id="h1" class="ih-title"><span class="ln l1"><span>Talk to</span></span> <span class="ln l2"><span>the builder</span></span></h1>
<p class="ih-lead">Call or text Abi on <a href="tel:{TEL}">{PH}</a>, email <a href="mailto:{MAIL}">{MAIL}</a>, or send the form and we will arrange a time to visit.</p>
<dl class="ct-facts"><div><dt>Phone</dt><dd><a href="tel:{TEL}">{PH}</a></dd></div><div><dt>Email</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
<div><dt>Based in</dt><dd>Bentleigh East, VIC 3165</dd></div><div><dt>Registration</dt><dd>{LIC}</dd></div></dl>
</section>
{enquiry('Contact Page Enquiry')}"""
s.page("/contact/", title="Contact Bhavan Building | Builder Bentleigh East | 0426 045 004",
       description="Contact Bhavan Building in Bentleigh East on 0426 045 004 or by email to arrange a free quote for a renovation, extension or rebuild.",
       body=contact_body, crumbs=[("Contact", "/contact/")])

s.page("/404/", title="Page not found | Bhavan Building", description="That page is not here. Head back to Bhavan Building's home page or call 0426 045 004.",
       body=f"""<section class="ih" aria-labelledby="h1"><h1 id="h1" class="ih-title"><span class="ln l1"><span>Nothing</span></span> <span class="ln l2"><span>here</span></span></h1>
<p class="ih-lead">The link may be old. <a href="/">Go to the home page</a> or call <a href="tel:{TEL}">{PH}</a>.</p></section>
<section class="sv"><div class="sv-more"><h2>Pages</h2><ul>{''.join(f'<li><a href="{u}">{n}</a></li>' for n, u in NAV)}</ul></div></section>""")

# ---------------------------------------------------------------- share card, favicons
from PIL import Image, ImageDraw, ImageFont  # noqa: E402
mark = Image.new("RGBA", (420, 120), (0, 0, 0, 0))
ImageDraw.Draw(mark).text((0, 10), "Bhavan Building", font=ImageFont.truetype(s.ttf("newsreader-latin-400-normal.woff2"), 54), fill="#e3e2da")
s.og_image("arch", focus=(50, 55), mark=mark, headline="Renovations, extensions\nand rebuilds",
           line2="Bentleigh East / south-east Melbourne", small=f"{PH}  /  Registered builder {LIC}",
           font_bold=s.ttf("newsreader-latin-300-normal.woff2"), font_text=s.ttf("newsreader-latin-400-normal.woff2"),
           ink="#e3e2da", accent="#9fc7b8", scrim=(22, 28, 26))
s.favicons("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#161c1a"/>
<path d="M22 14h13c8 0 12 3.4 12 9 0 4-2.4 6.6-6 7.6 4.6.8 7.6 3.8 7.6 8.6 0 6.4-4.8 10.8-13.4 10.8H22zm7 6v10h5c4 0 6-1.8 6-5s-2-5-6-5zm0 15.6V44h6c4.4 0 6.6-2 6.6-5.4S39.4 35.6 35 35.6z" fill="#9fc7b8"/></svg>""")
s.notes(**{'direction': 'Photographs at uneven sizes (taste-skill uneven-photographs), green-black and bone, pale jade on the enquiry button only', 'idea': "Bhavan's 'select number of projects' becomes a gallery wall: each finished room hung like a print with space around it, and the registration number signed under the work", 'live': 'Room filter on the project wall re-hangs the wall by room (All, Kitchens, Bathrooms, Laundries)', 'type_': 'Newsreader 300/400/500 standing in for the dealt Sentient (Fontshare is unreachable from the build container), self-hosted', 'palette': "Dealt 'green-black and bone' kept, it matches the dark fluted kitchen; no logo to sample", 'redraws': ['about: portraits pass needs team photos, none exist, so side facts and wide paragraph'], 'decisions': ['Contact blueprint has no form; house rule needs one, so the band keeps its geometry and the enquiry form follows it', 'No video: client photos only']})
s.finish()
