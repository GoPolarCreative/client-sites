# Metrowide Plumbing: build notes

- Source: Trade Websites sheet row 47 (submitted 7/10/2026)
- Domain: https://www.metrowideplumbing.com.au (canonical and schema point here)
- Preview: https://metrowide-plumbing.vercel.app
- Built: 2026-11-18 by Claude with the go-polar-site-build skill
- Phone on site: 0423 017 489 / Form key: client key

## Design

- Direction: Go Polar house style (rebuilt 18 Nov 2026 after Chris rejected the first, experimental build)
- Idea: Dark photo hero with quote form, logo blue accent on near black and white, condensed uppercase headings
- Live thing: Hero quote form, suburb checker, count-up stat band, gallery lightbox, FAQ accordion
- Type: Barlow Condensed 600/700/800 (headings), DM Sans 400/500/700 (body), self-hosted
- Palette: Logo blue #46a0d2 accent (deep #1d6fa5 on light), near black #0d0f12 and #15181d, white and #f4f6f8
- Decision: Benchmarks: Bernard Electrics, Spray Pave, Turquoise, Moral Service, Quick Micks
- Decision: No reviews section and no star rating: none supplied

## Pages

- /
- /emergency-plumber-melbourne/
- /bathroom-renovation-plumbing-melbourne/
- /new-build-plumbing-melbourne/
- /commercial-plumbing-melbourne/
- /plumbing-maintenance-melbourne/
- /service-areas/
- /our-work/
- /about/
- /contact/

## Photos

- `green`: bath-green-tile.jpg (Bathroom with green finger tiles, terrazzo floor and a freestanding bath)
- `arch`: bath-terrazzo-arch.jpg (Terrazzo bathroom with black tapware, floating vanity and arch mirror)
- `double`: shower-double.jpg (Double shower with two black rail sets over white finger tile)
- `brassvan`: vanity-brass.jpg (Brushed brass wall mixer over an oval vessel basin)
- `brassshower`: shower-brass.jpg (Brushed brass rain head and hand shower on large grey tiles)
- `combo`: bath-laundry-combo.jpg (Bathroom and laundry in one room with black fixtures and a frameless screen)
- `under`: vanity-underside.jpg (Open vanity showing neat chrome waste and isolation valves beside a freestanding bath)

## Flags for the client (confirm before go-live)

- [ ] Service area was answered as 'All areas' with no city. Melbourne assumed (CONFIRM). Regions and suburbs on the areas page are a starting list for Dan to correct.
- [ ] No plumbing registration or licence number supplied. Research says trade sites convert better with it shown up front. CLIENT TO SUPPLY: VBA registration number.
- [ ] No insurance details supplied, so the site makes no insurance claim. CLIENT TO SUPPLY if covered.
- [ ] No reviews yet ('None as of yet'), so there is no testimonials section and no review schema. Add Google reviews when they come in.
- [ ] No business hours supplied. The site says emergency and same-day work (form answer Yes) but does not claim 24/7. CLIENT TO CONFIRM hours.
- [ ] No street address. Built as a service-area business with no address shown. Google Business Profile should match.
- [ ] Client chose to host elsewhere ('I'll set myself up and pay for hosting elsewhere'). Preview is on Vercel; confirm hosting before going live.
- [ ] All seven job photos are bathrooms. No photos of new build rough-ins, commercial work or maintenance callouts, so those pages reuse bathroom photos. CLIENT TO SUPPLY site photos.
- [ ] Logo arrived as a phone screenshot of the artwork. Cropped and made transparent; it holds up at header size but a vector original would be better.
- [ ] Photo bath-laundry-combo had a screen scrollbar on its right edge; trimmed 44px.
- [ ] Google reviews section is wired to the live Google Places API but stays hidden until Metrowide has a Google Business Profile with reviews. It finds the profile by name for now; CLIENT TO SUPPLY the Google Business Profile link so the exact place ID can be set (cheaper and cannot pick up the wrong business).

## Editing

Change `_src/site.json`, `_src/build.py`, `_src/site.css` or `_src/site.js`, then:

```
python3 sites/metrowide-plumbing/_src/build.py && python3 _kit/verify.py sites/metrowide-plumbing
```

Commit and push to main; the workflow redeploys only this folder.
